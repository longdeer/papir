# Usage:
# papirus COMMAND SOURCE(s) CONTENT [DESTINATION(s)]
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
# papir --merge new1.pdf new2.pdf new3.pdf








class Papiro:

	def __init__(self):
		pass




	def split(self, source :Pagero) ->None :
		"""
			method that splits lol
		"""
		pass




	def merge(self, *source :Pagero) ->None :
		"""
			method that merge lol
		"""
		pass
