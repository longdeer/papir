import re


class Pagero:
	"""
		Pages & Rotations Organizer
		Represents the tool class with instantiation mechanism.
		Use with the only pages string for validate and prepare pages numbers
		and their corresponding rotations for resulting pdf file(s).
		The only public field pages will content list of lists of pages numbers
		with corresponding rotations (if there is one) which all will be
		used to construct result file(s).
	"""

	def __init__(self, pages_string :str):

		if not len(pages_string):
			raise ValueError("%s is incorrect result pages"%pages_string)

		# validate input as it have only numbers and allowed operational characters
		in_chars = set(pages_string)
		
		for char in in_chars:

			if not re.match("[\d\+\-\^:/, ]", char):
				raise ValueError("%s is incorrect character"%char)

		# at this point pages_string is validated
		# means that it consist of digits representing pages numbers
		# pages rotation characters such as + - ^ :
		# and delimeters / , for parts and peaks
		self.pages = self.get_pages(pages_string)


	def get_pages(self, astr :str) -> list :
		"""
			Method
		"""
		# 
		pages = astr.split("/")
		pages = [ part.split(",") for part in pages ]

		for ipart in range(len(pages)):

			cpart = pages[ipart]
			npart = []

			for ipeak in range(len(cpart)):

				cpeak = cpart[ipeak].replace(" ", "")
				npeak = self.process_peak(cpeak)

				npart.extend(npeak)

			pages[ipart] = npart

		return pages


	def process_peak(self, rstr :str) -> list :
		"""
			Method
		"""
		# s - start of range, e - end of range, d - delimeter of current range
		try:
			s, d, e = re.split("(\D+)", rstr)

			# account for single page with orientation
			if not e:
				return [ f"{s}{d}".replace(":", "") ]

			# r - range, accounts for backward ranges
			s, e = int(s), int(e)
			r = range(s, e +1) if s < e else range(s, e -1, -1)

			pages_range = [ f"{p}{d}".replace(":", "") for p in r ]

			return pages_range

		# during unpacking s, d, e there might be 2 ways of ValueError:
		# 1. there is no e (end of range), that means the peak consist of
		# single page with rotation
		# 2. there are more than 3 values to unpack, that means a peak 
		# with a mistake, such as more than one delimeter
		except ValueError:

			if not re.match("^\d+[\+\-\^]?$", rstr):
				raise ValueError("( %s ) peak's operations incorrect"%rstr)
			
			return [ rstr ]






if __name__ == "__main__":
	import re
	test = Pagero("1 + ,2-,3  ^,4,5 :6/7-1/11+15/2222")
	print(test.pages)