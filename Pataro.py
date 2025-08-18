import re, os


class Pataro:
	"""
		Paths Array Organizer.
		Represents the tool class with instantiation mechanism.
		Use with every path_string for source and destin separately.
		Checks if provided paths does exist in filesystem
		and does file names exist for sourcing
		or doesn't exist for destinationing.
		The only public field "files" will content list of all file paths,
		that was provided via the paths_string.
		The paths to files will be checked for existance and exeption will
		be raised if any path doesn't exist.
		Every file will be checked for existance and for consistency.
		That mean for source all files must exist, when for destin must not.
		If some file doesn't exist among existant or vice versa, exception raised.
		If no exception raised, files will content boolean as fisrt element,
		which will indicate that all files exist or not in the filesystem.
	"""

	def __init__(self, paths_string :str):

		if not len(paths_string):
			raise ValueError("%s is incorrect path"%paths_string)
		
		self.files = []
		exists = []

		# separate file paths from path string
		file_paths = re.split("(.*?),(?=\w:\\\\|/)", paths_string)

		# excluding redundant "" at the start of the splited list
		if not file_paths[0]:
			file_paths = file_paths[1:]

		# at this point file_paths is a list where
		# each element consist of path and file name(s)
		# separating path and file names(s) of each element
		# for checking existance of every path and file name(s)
		for file_path in file_paths:

			current_file_path = re.split("(.*[(\\\\)/])", file_path)

			# excluding redundant "" at the start of the splited list
			if not current_file_path[0]:
				current_file_path = current_file_path[1:]

			folder, target = current_file_path

			if not os.path.isdir(folder):
				raise ValueError("%s is incorrect path"%folder)

			# current implementation considering right file names
			# which does not include comas, besides it's allowed character
			# as in terms of flexibility paths_string doesn't have to
			# contain all file names with extensions, the following
			# procedure will account for it, and every coma will mean
			# separation of name string, so "fi,le.pdf" will became
			# "fi.pdf" and "le.pdf" which will break the stage,
			# where list of all file paths will try to match 
			# with list of pages & rotations
			# for that case Papiro must perfom lengths comparison of those lists
			fnames = target.split(",")
			
			for f in range(len(fnames)):

				if not re.match("\.[pP][dD][fF]", fnames[f][-4:]):
					fnames[f] += ".pdf"

				full_path = "%s%s"%(folder, fnames[f])

				# collect boolean of file existance
				# to consider source/destin possibility
				exists.append(os.path.isfile(full_path))

				# check the consistence of existence
				if all(exists) != any(exists):
					raise ValueError("{file}\n{indent}file doesn't exists or cannot be overwritten\n{indent}also check for file names doesn't include comas".format(file=fnames[f], indent=" "*12))

				# at this moment full_path is a valid and added to output
				self.files.append(full_path)

		# as all file paths passed without exceptions
		# every file path must exist for source or doesn't for destin
		# to address this adding special boolen in the start of output list
		# which will indicate the possibility of use for source/destin
		self.files = [ all(exists) ] + self.files


			


		
if __name__ == "__main__":
	import re, os
	a = "D:\\containers\\pdfr\\.PDF,D:\\Users\\user\\Documents\\Доверенность на Мажирина С.И. от 04.10.2018 № 77-509-н-77-2018-2-1961,договорМГТУ"
	test = Pataro(a)
	print(test.files)