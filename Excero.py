class Excero(Exception):
	"""
		Papir Exceptions base class.
	"""
	pass




class PageroRangeException(Excero):
	"""
		Pagero proc_range Exception.
	"""
	def __init__(self, chunk, check):

		self.chunk = chunk
		self.check = check


	def __str__(self):
		return f"Incorrect chunk \"{self.chunk}\", check {self.check}!"




class PageroCheckPagesException(Excero):
	"""
		Pagero check_pages Exception.
	"""
	def __init__(self, raw_pages):
		self.raw_pages = raw_pages


	def __str__(self):
		return f"Pages argument \"{self.raw_pages}\" is incorrect!"




class PageroPagesCountException(Excero):
	"""
		Pagero source file pages count satisfaction Exception.
	"""
	def __init__(self, src_num, arg_num):
		self.src_num = src_num
		self.arg_num = arg_num


	def __str__(self):
		return f"Source file has {self.src_num} pages and doesn't fit to \"{self.arg_num}\" argument"




class PageroIndexingException(Excero):
	"""
		Pagero check 0-indexing usage Exception.
	"""
	def __init__(self, raw_pages):
		self.raw_pages = raw_pages


	def __str__(self):
		return f"Argument \"{self.raw_pages}\" using 0-indexing, must be 1-indexing!"




class PageroDublicateException(Excero):
	"""
		Pagero check for dublicate page numbers with different rotations.
	"""
	pass # TO DO: Add check for different rotation of the same page within same chunk
		 # as it leads to adding to writer the very last version of pages.








class PapiroSourceVerificationBase(Excero):
	"""
		Papiro verify_file_name Exception Base class
	"""
	def __init__(self, file_name :str):
		self._output = f"Source file \"{file_name}\""




class PapiroNoSourceException(PapiroSourceVerificationBase):
	"""
		Papiro source file existance verification Exception.
	"""
	def __str__(self):
		return f"{self._output} doesn't exist!"


class PapiroZeroSizeSourceException(PapiroSourceVerificationBase):
	"""
		Papiro source file size verifiaction Exception.
	"""
	def __str__(self):
		return f"{self._output} has invalid size!"








class PapiroOpsBase(Excero):
	"""
		Papiro operations Exception Base class.
	"""
	def __init__(
					self,
					arguments :str =None,
					sources :str or ( str, ) =None,
					targets :str or ( str, ) =None
				) :
		self._current_arguments = arguments

		if sources:
			self._current_sources = ", ".join(sources)
		
		if targets:
			self._current_targets = ", ".join(targets)




class PapiroOpsNoPagesArgumentsException(PapiroOpsBase):
	"""
		Papiro no pages arguments Exception
	"""
	def __str__(self):
		return f"Operation arguments \"{self._current_arguments}\" not valid"


class PapiroArgumentsLengthException(PapiroOpsBase):
	"""
		Papiro split arguments length satisfy condition of 1 for all targets or
		1 for every target verification Exception.
	"""
	def __str__(self):
		return f"Pages argument \"{self._current_arguments}\" must be 1 for all or every target for split"
