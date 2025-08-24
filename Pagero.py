from PyPDF2 import PdfFileReader
from re import compile as pmake
from Excero import Excero
from Excero import PageroRangeException
from Excero import PageroCheckPagesException
from Excero import PageroPagesCountException
from Excero import PageroIndexingException
from Excero import PageroMapperException








class Pagero:
	"""
		PAGEs
	"""
	



	numbp = pmake("\d+")
	delip = pmake("(\D)")
	argsp = pmake("[\d\+\-:^/,]")
	pagep = pmake("^\d+[\+\-\^]?$")
	fullp = pmake("^[\d\+\-:^/,]+$")
	auxdl = "::", "++", "--", "^^"




	@staticmethod
	def make_content(raw_pages :str, raw_pdf :PdfFileReader =None) -> [[ str, ]] :
		"""
			Prepare arguments raw string and do Pagero magic
		"""
		# print(raw_pages)
		# print(raw_pdf.numPages)
		Pagero.count_pages(raw_pages, raw_pdf.numPages)


		for pager in Pagero.proc_pages(raw_pages):
			yield Pagero.mapper(pager, raw_pdf)




	@staticmethod
	def mapper(pager :str, pdfr : PdfFileReader) -> PdfFileReader :
		"""
			Mapps pagero output to something.
		"""
		p,d = *pager,


		match d:

			case "":
				return pdfr.getPage(p)

			case "+":
				return pdfr.getPage(p).rotateClockwise(90)

			case "-":
				return pdfr.getPage(p).rotateCounterClockwise(90)

			case "^":
				return pdfr.getPage(p).rotateClockwise(180)

			case _:
				raise PageroMapperException(f"{p+1}{d}")




	@staticmethod
	def count_pages(raw_pages :str, fpages :int) -> None or Excero :
		"""
			Satisfy source file pages count and provided argument.
		"""
		for page in set(Pagero.numbp.findall(raw_pages)):
			actual = int(page)
			
			if actual == 0:
				raise PageroIndexingException(raw_pages)

			if actual > fpages:
				raise PageroPagesCountException(fpages, raw_pages)




	@staticmethod
	def check_pages(raw_pages :str) -> None or Excero :
		"""
			Checks weather raw_pages string content valid characters
		"""
		for char in set(raw_pages):

			if not Pagero.argsp.match(char):
				raise PageroCheckPagesException(raw_pages)




	@staticmethod
	def proc_pages(raw_pages :str) -> dict :
		"""
			Does pagero magic
		"""
		# Process file-associated chunks to obtaine range-associated chunks.
		raw_chunks = raw_pages.split(",")


		# Process every chunk as a range.
		for ci in range(len(raw_chunks)):

			current_chunk = raw_chunks[ci]
			yield from Pagero.proc_ranges(current_chunk)




	@staticmethod
	def proc_ranges(raw_range :str) -> [ str, ] or False :
		"""
			Processes the chunk of pages argument to return usable range of pages
			with orientations
		"""
		try:
			# s - start of range
			# d - delimiter of current range
			# e - end of range
			# Regex split by (\D+) insures we will have s,d,e in all cases
			# when argument chunk provided as range or as single page with rotation,
			# as split by group allways return the delimeter too, with empty string
			# if nothing goes after delimeter in chunk.
			s,d,e = Pagero.delip.split(raw_range)


			# Guard for absent start of range. Redirect to Excero.
			if not s:
				raise ValueError

			# Process single page with rotation.
			if not e:
				print([( int(s)-1,d )])
				return [( int(s)-1,d )]


			# At this point range is provided. As it may be either ascending or descending,
			# r - range calculation.
			s,e = int(s),int(e)
			r = range(s,e+1) if s<e else range(s,e-1,-1)

			# Pages from range without rotation marked with ":" symbol, which is redundant.
			return (( p-1,d.replace(":", "") ) for p in r )

		# At this point ValueError was raised in 2 possible ways:
		# 1. There is no delimeter in chunk, which means we have just a single page;
		# 2. The chunk is corrupted by some extra delimeters.
		except ValueError:

			if not raw_range:
				raise PageroRangeException(raw_range, "extra comas")


			if not Pagero.pagep.match(raw_range):
				raise PageroRangeException(raw_range, "symbols")

			return [( int(raw_range)-1,"" )]







