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




main_commands = "-s", "--split", "-m", "--merge"
aux_commands = "-g", "--grind", "-c", "--concat"
pageros_flags = "-p", "--pages"
targets_flags = "-t", "--target"
valid_commands = *main_commands, *aux_commands
valid_flags = *pageros_flags, *targets_flags
sources = []
targets = []
pageros = "::"
argi = 1








try:
	command = argv[argi]
	argi += 1
	loggy.debug(f"COMMAND: {command}")
	aux = command in aux_commands

except IndexError:
	exit(print(usage))


if command not in valid_commands:

	loggy.critical(f"Command {command} not allowed")
	exit(print(usage))


try:
	currentsrc = argv[argi]

	while currentsrc:
		if currentsrc in valid_flags:

			sources[0] = sources[0]
			loggy.debug("End obtaining sources")
			break

		sources.append(currentsrc)
		argi += 1
		currentsrc = argv[argi]

	loggy.debug(f"SOURCES: {sources}")

except IndexError:
	if not sources:

		loggy.critical("No sources specified")
		exit(print(usage))




if not aux:
	try:
		nextarg = argv[argi]
		argi += 1

		if nextarg in pageros_flags:

			pageros = argv[argi]
			argi += 1
			loggy.debug(f"PAGEROS: {pageros}")
		else:
			raise IndexError

	except IndexError:
		
			loggy.critical("Pageros must be specified")
			exit(print(usage))


try:
	nextarg = argv[argi]
	argi += 1

	if nextarg in targets_flags:
		targets.extend(argv[argi:])

		if not targets:

			loggy.critical("Target flag must be ommited or target file names must be specified")
			exit(print(usage))
	else:
		loggy.critical("Target flag must be specified")
		exit(print(usage))

	loggy.debug(f"TARGETS: {targets}")

except IndexError:
	
	loggy.debug("No targets mode")
	targets = [ "" ]




papir = Papiro(loggy)
try:
	match command:

		case "-s" | "--split":
			if len(sources) != 1:

				loggy.critical("Must be single source for such operation")
				exit(print(usage))
			
			papir.split(pageros, *sources, *targets)

		case "-m" | "--merge":
			if len(targets) != 1:

				loggy.critical("Must be single target for such operation")
				exit(print(usage))
			
			papir.merge(pageros, *targets, *sources)

		case "-g" | "--grind":
			if len(sources) != 1:

				loggy.critical("Must be single source for such operation")
				exit(print(usage))
			
			papir.grind(pageros, *sources, *targets)

		case "-c" | "--concat":
			if len(targets) != 1:

				loggy.critical("Must be single target for such operation")
				exit(print(usage))
			
			papir.concat(pageros, *targets, *sources)

except Excero as inner:
	loggy.warning(inner)

except Exception as outer:
	loggy.critical(outer)
