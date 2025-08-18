import re
import os
from Pagero import Pagero
from Pataro import Pataro
from PyPDF2 import PdfFileReader as pdfr, PdfFileWriter as pdfw



class Papiro:
	""" 
		Pypdf2 API Redact Organizer.
	"""

	def __init__(	
					self,
					source_names	:Pataro,
					destin_names	:Pataro,
					pages_string	:Pagero,
				):

		self.source = Pataro(source_names)
		self.destin = Pataro(destin_names)
		self.result = Pagero(pages_string)

		# check if source file(s) exist
		if not self.source.files[0]:
			raise ValueError("Source file(s) doesn't exist")

		# check if destin file(s) does not exist
		if self.destin.files[0]:
			raise ValueError("Destination files exists and cannot be overwritten")

		self.src = self.source.files[1:]
		self.dst = self.destin.files[1:]
		self.pages = self.result.pages

		# tool for obtaining max number from pages string to verify
		# string doesn't exceed number of pages in source file
		self.pfit = lambda pstr: max([ int(peak.strip("+-^")) -1 for part in pstr for peak in part ])


	def pdf_split(self) -> None :
		"""
			Method
		"""
		# validate operation as destin and result all have same lengths
		if len(self.dst) != len(self.pages):
			raise ValueError("There is missmatch in number of operations and source/destin files")
		
		#open pdf for every file path in destinations string
		#to add pages from single source 
		for i in range(len(self.dst)):

			with open(*self.src, "rb") as tmpent:

				# create PyPDFReader object with file path input 
				# and PyDPFWriter for output
				# and obtain corresponding pages numbers
				pdfent = pdfr(tmpent)
				
				# verify source file have enough pages for operation
				pnums = [ int(peak.strip("+-^")) -1 for part in self.pages for peak in part ]
				if not max(pnums) < pdfent.numPages:
					raise ValueError("Pages string exceed %s pages in %s source file"%(pdfent.numPages, *self.src))
				
				pdfout = pdfw()
				current_pages = self.pages[i]

				# loop through pages to add to new file
				for page in current_pages:

					current_page = self.prepare_peak(page)
					self.process_peak(current_page, pdfent, pdfout)

				self.safe_pdf_file(self.dst[i], pdfout)




	def pdf_merge(self) -> None :
		"""
			Method
		"""
		# validate operation as source and result all have same lengths
		if len(self.src) != len(self.pages):
			raise ValueError("There is missmatch in number of operations and source/destin files")

		pdfout = pdfw()

		for i in range(len(self.src)):

			# open current source file that must be closed after all
			# create PyPDFReader object with opened stream 
			# obtain corresponding pages numbers
			exec(f"tmpent_{i} = open(self.src[{i}], 'rb')")
			exec(f"getent = pdfr(tmpent_{i})")
			pdfent = locals().get("getent")

			# verify source file have enough pages for operation
			pnums = [ int(peak.strip("+-^")) -1 for peak in self.pages[i] ]
			if not max(pnums) < pdfent.numPages:
				raise ValueError("Pages string exceed %s pages in %s source file"%(pdfent.numPages, self.src[i]))
			
			current_pages = self.pages[i]

			for page in current_pages:

				current_page = self.prepare_peak(page)
				self.process_peak(current_page, pdfent, pdfout)

		self.safe_pdf_file(*self.dst, pdfout)

		for i in range(len(self.src)):

			# close every source file
			exec(f"tmpent_{i}.close()")


	def prepare_peak(self, page_string :str) -> str :
		"""
			Method
		"""
		# separate page number and rotation sign (if provided)
		# if no rotation provided, goto else clause
		current_page = [ n for n in re.split("(\d+)", page_string) ]

		# get rid of redundant "" at the start of split
		if not current_page[0]:
			current_page = current_page[1:]

		return current_page


	def process_peak(
						self,
						page_string :str,
						pdf_input :pdfr,
						pdf_output :pdfw,
					) -> None :
		"""
			Method
		"""
		# unpack page number and rotation sign and reorder to 1-ordered numbers
		p, r = page_string
		p = int(p) -1

		# in case input was 0-ordered
		if p < 0:
			raise ValueError("Negative page number occurred! Use 1-orderd pages!")

		# PyPDF API in action
		if r == "+":
			pdf_output.addPage(pdf_input.getPage(p).rotateClockwise(90))

		elif r =="-":
			pdf_output.addPage(pdf_input.getPage(p).rotateCounterClockwise(90))

		elif r =="^":
			pdf_output.addPage(pdf_input.getPage(p).rotateClockwise(180))

		else:
			pdf_output.addPage(pdf_input.getPage(p))


	def safe_pdf_file(self, file_path :str, pdf_output :pdfw) -> None :
		"""
			Method
		"""
		# safe in corresponding destination file
		with open(file_path, "wb") as tmpout:
			pdf_output.write(tmpout)





if __name__ == "__main__":
	
	#test_fpath_0 = "D:\\ArrestedDevelopment\\papiro\\papiro.py,papir_mesp.py"
	#test_fpath_1 = "D:\\ArresteddDevelopment\\papiro\\papiro.py,papir_mesp.py"
	#test_fpath_2 = "D:\\Users\\user\\Documents\\A2\\Бухгалтерия и финансы\\Перемещение\\СканГМССБА2 пермещение нетбук-ИТ.pdf"

	#test_split = Papiro("C:\\Users\\lngd\\Desktop\\0048 Инструкция по делопроизводству 2021", "E:\\ArrestedDevelopment\\continers\\one,two,three", "1+23/24-33,34/35^47")
	#test_split.pdf_split()

	test_merge = Papiro("E:\\ArrestedDevelopment\\continers\\one,two,three", "E:\\ArrestedDevelopment\\continers\\mergedFile", "1-23/1+10,11/1^12,13")
	test_merge.pdf_merge()
	

	#print(test_split.source.files)
	#print(test_split.destin.files)
	#print(test_split.result.pages)
	#print(test_filo.destin.files)

