# Usage:
# papir COMMAND SOURCE(s) CONTENT [DESTINATION(s)]
# Examples:
# papir --split some.pdf 1^10/2+5,6-7/69:42 new1.pdf new2.pdf new3.pdf
# papir --split D:\some_folder\some.pdf 1^10/2+5,6-7/69:42 new1.pdf new2.pdf new3.pdf
# papir --split some.pdf 1^10/2+5,6-7/69:42 E:\some_new_fodler\new1.pdf new2.pdf F:\one_more_new_folder\new3.pdf
# papir --split D:\some_folder\some.pdf 1^10/2+5,6-7/69:42
# papir --split some.pdf
# papir --merge new1.pdf new2.pdf new3.pdf 1^10/2+5,6-7/69:42 some.pdf
# papir --merge new1.pdf new2.pdf new3.pdf 1^10/2+5,6-7/69:42 D:\some_folder\some.pdf
# papir --merge E:\some_new_fodler\new1.pdf new2.pdf F:\one_more_new_folder\new3.pdf 1^10/2+5,6-7/69:42 some.pdf
# papir --merge E:\some_new_fodler\new1.pdf new2.pdf F:\one_more_new_folder\new3.pdf 1^10/2+5,6-7/69:42
# papir --merge new1.pdf new2.pdf new3.
from Pagero 	import Pagero
from PyPDF2 	import PdfFileReader
from PyPDF2 	import PdfFileWriter
from Excero 	import Excero
from re 		import compile as pmake
from os 		import path
from Excero 	import PapiroNoSourceException
from Excero 	import PapiroZeroSizeSourceException
from Excero 	import PapiroArgumentsLengthException
from Excero 	import PapiroOpsNoPagesArgumentsException
from logging 	import Logger
from logging 	import getLogger
from logging 	import Formatter
from logging 	import StreamHandler
from sys 		import stdout








class Papiro:
	"""
		This is the main class which implement pdf redacting.
		Usage implies instance creation with source files names.
		Two main methods split and merge do all the work in other
		ops methods.
	"""




	valid_name_pattern = pmake(".+\.[pP][dD][fF]$")




	def __init__(self, logger :Logger =None):
		"""
			Only logging for init
		"""
		self.loggy = logger

		if not self.loggy:
			self.loggy = getLogger("papir")
			
			loggy_formatter = Formatter("%(name)s: %(message)s")
			loggy_handler = StreamHandler(stdout)
			loggy_handler.setFormatter(loggy_formatter)

			self.loggy.addHandler(loggy_handler)
			self.loggy.setLevel(20)




	def verify_file_name(self, file_path :str, src :bool =False) -> str or Excero :
		"""
			Verifies source file is valid pdf file, which means it is existant
			non zero-size file with .pdf extension. Argument string may be either
			absolute path, or just file name, wheach implies using current directory
			for searching the file. Also only file name without extension is
			allowed, this method will try to concatinate .pdf to file name and search
			for that file.
		"""
		if not self.valid_name_pattern.match(file_path):
			return self.verify_file_name(file_path + ".pdf", src)


		if src:
			if not path.isfile(file_path):
				raise PapiroNoSourceException(file_path)

			if not path.getsize(file_path):
				raise PapiroZeroSizeSourceException(file_path)


		return file_path




	def ops_handler(op :callable):
		def ops_wrapper(self, *op_args):
			"""
				Wraps split or merge ops method for preparations.
			"""
			pages = op_args[0]

			if not pages:
				raise PapiroOpsNoPagesArgumentsException(arguments=pages)

			Pagero.check_pages(pages)


			pool1 = op_args[1]
			pool2 = op_args[2:]


			raw_pages = pages.split("/")
			raw_count = len(raw_pages)
			pool2_len = len(pool2)


			# Number of destination files must be either equal argument pages ranges or
			# it must be one range for every destination.
			if pool2_len != raw_count:
				if raw_count != 1:
					raise PapiroArgumentsLengthException(arguments=pages)

				# At this point there are multiple destination file names for split and only 1
				# pages argument for source file. That means argument range, if valid in case of
				# Pagero job verification in next steps, will be used to split source file the same
				# way for every destination. For correct implementation, already splitted to list
				# variable will be multiplied by number of destinations.
				raw_pages *= pool2_len


			return op(self, raw_pages, pool1, *pool2)
		return ops_wrapper




	@ops_handler
	def split(self, *split_args :( str and [ str, ], str, ( str, ))) -> None :
		"""
			method that splits lol
		"""
		raw_pages = split_args[0]
		source = self.verify_file_name(split_args[1], src=True)
		targets = [ self.verify_file_name(f) for f in split_args[2:] ]


		#try:
		with open(source, "rb") as tmpent:
			for r,raw_range in enumerate(raw_pages):
				
				pdfent = PdfFileReader(tmpent, strict=False)
				tmpout = PdfFileWriter()
				target = targets[r]
				
				for page in Pagero.make_content(raw_range, pdfent):
					tmpout.addPage(page)

				with open(target, "wb") as pdfout:
					
					tmpout.write(pdfout)
					self.loggy.info(f"splited {target}")
		
		#except Exception as e:
		#	print(e)




	@ops_handler
	def merge(self, *merge_args :( str and [ str, ], str, ( str, ))) -> None :
		"""
			method that merge lol
		"""
		raw_pages = merge_args[0]
		target = self.verify_file_name(merge_args[1])
		sources = [ self.verify_file_name(f, src=True) for f in merge_args[2:] ]


		#try:
		tmpout = PdfFileWriter()
		
		for f,file_name in enumerate(sources):
			with open(file_name, "rb") as tmpent:
				
				pdfent = PdfFileReader(tmpent, strict=False)
				raw_range = raw_pages[f]

				for page in Pagero.make_content(raw_range, pdfent):
					tmpout.addPage(page)
		
				with open(target, "ab") as pdfout:
					
					tmpout.write(pdfout)
		

		self.loggy.info(f"merged {target}")
		
		#except Excero as e:
		#	print(e)









if __name__ == "__main__":

	# def test_pagero_make_content(test_string :str, count :int) -> list:

	# 	with open("MNL-1785.pdf", "rb") as tmp_pdfent:
			
	# 		pdfent = PdfFileReader(tmp_pdfent)
	# 		pdfout = PdfFileWriter()
		
	# 		for i in Pagero.make_content(test_string, pdfent):
	# 			pdfout.addPage(i)
			
	# 		with open(f"test_output_{count}.pdf", "wb") as tmp_pdfout:
	# 			pdfout.write(tmp_pdfout)




	#test_pagero_make_content("1,2,3", 1)
	#test_pagero_make_content("4:7", 2)
	#test_pagero_make_content("18-15", 3)
	#test_pagero_make_content("4^4", 4)
	#test_pagero_make_content("10+11", 5)
	#test_pagero_make_content("1,2+,5^4", 6)
	
	# test_pagero_make_content("3-,3+,3^,5:5", 7)
	
	#test_pagero_make_content("4^,5:7", 8)



	
	# print("\n\nproc_pages broken args tests")
	# try:
	# 	test_pagero_make_content("1,,2", 1)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("4 : 7     ", 2)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("18,-15-16,", 3)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("4 5", 4)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("10++11", 5)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("1,2+ ,- ,5^4", 6)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("3_,3=,3$,%;%", 7)
	# except Excero as e:
	# 	print(e)
	
	# try:
	# 	test_pagero_make_content("4^5:7", 8)
	# except Excero as e:
	# 	print(e)




	#test1 = Papiro("MNL-1785", "MNL-1785 (copy)")
	test1 = Papiro()
	test1.split("1:2,3+/4-5/6^7", "MNL-1785", "MNL-1785+", "MNL-1785++", "MNL-1785+++")
	test1.merge("1:2,3-/1+2/1^2", "MNL-1785-", "MNL-1785+", "MNL-1785++", "MNL-1785+++")
	#test2 = Papiro("MNL-1785")
