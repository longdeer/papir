from PyPDF2 import PdfFileReader as pdfr








class Pagero:
	"""
		PAGEs
	"""

	def __init__(self, file_path :str):

		self.file_path = file_path

		# Dictionary to hold all PyPDF pages objects
		self.pages = {}
		self.dry = None




	def __enter__(self):

		try:
			self.dry = open(self.file_path, "rb")
			wet = pdfr(self.dry)

			pnums = wet.numPages

			#
			#


			# Check file contents pages
			if not pnums:
				raise ValueError(f"{self.file_path} is empty")


			# Iterating via all page numbers of current pdf file and
			# populating self.pages dictionary filed with key/value as
			# file name string page number/corresponding PyPDF2 page object.
			# Besides PyPDF use 0-indexed page, self.pages keys will content
			# 1-indexed pages names.
			for p in range(pnums):

				ckey = f"{self.file_path}-page{p+1}"
				cval = wet.getPage(p)

				#


				self.pages[ckey] = cval

				#

			else:
				#
				return self.pages


			#
			raise ValueError("Not all pages are added!")

		except PermissionError:
			#
			pass




	def __exit__(self, *exit_arguments):
		self.dry.close()

		# for page in self.pages.values():

			# try:
			# 	page.close()
			# 	#

			# except AttributeError:
			# 	#
			# 	continue
