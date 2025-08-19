from PyPDF2 import PdfFileReader as pdfr








class Pagero:
	"""
		PAGEs
	"""

	def __init__(self, file_path :str, raw_pages :str):

		self.file_path = file_path
		self.raw_pages = raw_pages

		
		# Dictionary to hold all PyPDF pages objects
		self.content = {}


		try:
			self.drypdf = open(self.file_path, "rb")

		except PermissionError:
			#
			pass




	def pagesproc(self, raw_pages :str) ->dict :
		"""
			do pagero magic
		"""
		pass




	def __enter__(self):

		wetpdf = pdfr(self.drypdf)
		pnums  = wetpdf.numPages

		#
		#

		# Check file contents pages
		if not pnums:
			raise ValueError(f"{self.file_path} is empty!")

		
		# Iterating via all page numbers of current pdf file and
		# populating self.content dictionary filed with key/value as
		# file name string page number/corresponding PyPDF2 page object.
		# Besides PyPDF use 0-indexed page, self.content keys will content
		# 1-indexed pages names.
		for p in range(pnums):

			ckey = str(p+1)
			cval = wetpdf.getPage(p)

			self.content[ckey] = cval

			#
			#

		else:
			#
			return self.content




	def __exit__(self, *exargs):
		
		# On exit the conditions of closed file and content expirence are enshured.
		self.drypdf.close()
		self.content.clear()
