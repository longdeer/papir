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
from Excero 	import PapiroRotationException
from logging 	import Logger
from logging 	import getLogger
from logging 	import Formatter
from logging 	import StreamHandler
from sys 		import stdout
from datetime 	import datetime








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
			and dflag
		"""
		self.dflag = datetime.today().strftime("%d%m%Y-%H%M-%f")
		

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

			if pages is None:
				
				self.loggy.debug("aux mode")
				raw_pages = [ None ]
			
			elif not pages:
				raise PapiroOpsNoPagesArgumentsException(arguments=pages)

			else:
				Pagero.check_pages(pages)
				raw_pages = pages.split("/")


			raw_count = len(raw_pages)

			self.loggy.debug(f"raw_pages: {raw_pages}")


			pool1 = op_args[1] or self.dflag
			pool2 = op_args[2:]

			if not pool2[0]:

				self.loggy.debug("rebuilding pool2")
				pool2 = [ f"{self.dflag}-{r+1}" for r in range(raw_count) ]

			pool2_len = len(pool2)


			self.loggy.debug(f"pool1 {pool1}")
			self.loggy.debug(f"pool2 {pool2}")


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




	@ops_handler
	def merge(self, *merge_args :( str and [ str, ], str, ( str, ))) -> None :
		"""
			method that merge lol
		"""
		raw_pages = merge_args[0]
		target = self.verify_file_name(merge_args[1])
		sources = [ self.verify_file_name(f, src=True) for f in merge_args[2:] ]


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




	@ops_handler
	def grind(self, *grind_args :( str and [ str, ], str, ( str, ))) -> None:
		"""
			method that grinds lol
		"""
		raw_pages = grind_args[0]
		self.loggy.debug(f"current raw_pages: {raw_pages}")
		source = self.verify_file_name(grind_args[1], src=True)
		targets = [ self.verify_file_name(f) for f in grind_args[2:] ]


		with open(source, "rb") as tmpent:
			pdfent = PdfFileReader(tmpent, strict=False)
			
			if raw_pages[0] is None:
				
				raw_count = pdfent.numPages
				raw_pages = Pagero.make_content(f"1:{raw_count}", pdfent)

			else:
				if raw_pages[0] in Pagero.auxdl:

					raw_count = pdfent.numPages
					raw_pages = Pagero.make_content(f"1{raw_pages[0][0]}{raw_count}", pdfent)
				
				else:
					raw_count = len(raw_pages)
					raw_pages = Pagero.make_content(raw_pages[0], pdfent)


			self.loggy.debug(f"current count: {raw_count}")
			self.loggy.debug(f"current pages: {raw_pages}")
			

			for r,pager in enumerate(raw_pages):
				
				tmpout = PdfFileWriter()
				tmpout.addPage(pager)
				
				try:
					target = targets[r]

				except IndexError:
					target = self.verify_file_name(f"{self.dflag}-{r+1}")

				with open(target, "wb") as pdfout:
					
					tmpout.write(pdfout)
					self.loggy.info(f"grinded {target}")




	@ops_handler
	def concat(self, *concat_args :( str and [ str, ], str, ( str, ))) -> None :
		"""
			method that concat lol
		"""
		raw_pages = concat_args[0]
		self.loggy.debug(f"current raw_pages: {raw_pages}")
		target = self.verify_file_name(concat_args[1])
		sources = [ self.verify_file_name(f, src=True) for f in concat_args[2:] ]


		tmpout = PdfFileWriter()
		
		for f,file_name in enumerate(sources):
			with open(file_name, "rb") as tmpent:
				
				pdfent = PdfFileReader(tmpent, strict=False)

				try:
					if raw_pages[f] in Pagero.auxdl:
						raw_range = f"1{raw_pages[f][0]}{pdfent.numPages}"

					else:
						raise PapiroRotationException(raw_pages)
				
				except IndexError:
					raw_range = f"1:{pdfent.numPages}"

				for page in Pagero.make_content(raw_range, pdfent):
					tmpout.addPage(page)
		
				with open(target, "ab") as pdfout:
					tmpout.write(pdfout)
		

		self.loggy.info(f"merged {target}")







