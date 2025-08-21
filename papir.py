from Papiro 	import Papiro
from Pagero 	import Pagero
from Excero 	import Excero
from logging 	import getLogger
from logging 	import Formatter
from logging 	import StreamHandler
from sys 		import stdout
from sys 		import argv
from sys 		import exit








usage = """
Usage:

papir COMMAND SOURCE(s) -p|--pages PAGEROS [-t|--target DESTINATION(s)]

COMMAND:
\t-s --split - split one SOURCE pdf file to DESTINATIONS files
\t-m --merge - merge all SOURCES files to one DESTINATION file

SOURCE(s):
File names may be absolute or relative
\tsome[.pdf]                  - split only one file at a time
\tsome1[.pdf] some2[.pdf] ... - merge every files to one file

PAGEROS:
Synopsis N[+-^:]N[,/M[+-^:]]
\t-p     - start of operation's pages argument
\t--pages
\tN      - take page N from source file
\tN+     - rotate page right (90 degrees clockwise)
\tN-     - rotate page left (90 degrees counter clockwise)
\tN^     - rotate page upside down (180 degrees clockwise)
\tN:+-^M - take range from page N to M with rotation (: without rotation)
\t,      - pages delimeter in chunks (targets for split, sources for merge)
\t/      - delimeter for chunks (targets for split, sources for merge)

DESTINATION(s):
File names may be absolute or relative
\t-t                          - start of target file names arguments
\t--target
\tsome[.pdf]                  - merge every files to one file
\tsome1[.pdf] some2[.pdf] ... - split only one file at a time

Examples:
\tpapir -s some.pdf --pages 1^10/2+5,6,7-7/69:42 -t new1.pdf new2.pdf new3.pdf
\t\toutcome: new1.pdf with 1 to 10 upside down pages from some.pdf,
\t\tnew2.pdf with pages 2 to 5 right rotated and 7 left rotated,
\t\tnew3.pdf with pages 69 to 42.
\tpapir --merge /home/user/this1.pdf this2.pdf /mnt/server/this3.pdf -p 1^10
\t\toutcome: %d%m%Y-%H%M-%f.pdf with pages 1 to 10 upside down for every file,
\t\tthis1.pdf from user's home directory, this2.pdf from current directory,
\t\tthis3.pdf from mounted server directory.
"""




loggy = getLogger("papir")

loggy_formatter = Formatter("%(levelname)s: %(message)s")
loggy_handler = StreamHandler(stdout)
loggy_handler.setFormatter(loggy_formatter)

loggy.addHandler(loggy_handler)
loggy.setLevel(10)








try:
	command = argv[1]

	if command not in ( "-s", "--split", "-m", "--merge", "-g", "--grind", "-c", "--concat"):

		loggy.critical(f"Command {command} not allowed")
		raise ValueError


	nextarg = 2
	sources = []
	targets = []

	while True:
		try:
			currentsrc = argv[nextarg]
		
			if currentsrc in ( "-p", "--pages", "-t", "--target" ):
				if nextarg > 2:
					
					loggy.debug("All sources obtained")
					break
				else:
					
					loggy.critical("No sources obtained")
					raise ValueError

			sources.append(currentsrc)
			nextarg += 1

		except IndexError:

			loggy.debug("Arguments end reached while obtaining sources")
			break


	topageros = argv[nextarg]
	loggy.debug(topageros)

	match topageros:
		case "-p" | "--pages":

			nextarg += 1
			pageros = argv[nextarg]
			nextarg += 1
			loggy.debug("Pageros flag found and pageros obtained")

		case _:
			
			loggy.critical("No pageros flag provided")
			raise ValueError


	try:
		totargets = argv[nextarg]
		nextarg += 1

		match totargets:
			
			case "-t" | "--target":
				targets.extend(argv[nextarg:])

				if not targets:

					loggy.critical("No targets found after flag")
					raise ValueError

				loggy.debug("Targets successfully specified")

			case _:

				loggy.critical("Targets must be specified with \"-t\" or \"--target\"")
				raise ValueError

	except IndexError:

		loggy.debug(f"No targets specified, None passed")
		targets.append(None)


	loggy.debug(f"COMMAND: {command}")
	loggy.debug(f"SOURCES: {sources}")
	loggy.debug(f"PAGEROS: {pageros}")
	loggy.debug(f"TARGETS: {targets}")

except (IndexError, ValueError):
	exit(print(usage))




papir = Papiro(loggy)
try:
	match command:

		case "-s" | "--split":
			papir.split(pageros, *sources, *targets)

		case "-m" | "--merge":
			papir.merge(pageros, *targets, *sources)

		case _:
			
			loggy.critical(f"Command {command} not allowed")
			raise ValueError

except Excero as inner:
	loggy.warning(inner)

# except Exception as outer:
# 	loggy.critical(outer)
