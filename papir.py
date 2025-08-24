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
\t-s --split  - split one SOURCE pdf file to DESTINATIONS files
\t-m --merge  - merge all SOURCES files to one DESTINATION file
\t-g --grind  - grind SOURCE file pages in separate DESTINATIONS files
\t-c --concat - concatenate all SOURCES files to one DESTINATION file,
				or rotate all pages in single SOURCE file

SOURCE(s):
File names may be absolute or relative
\tsome[.pdf]                  - split/grind only one file at a time
\tsome[.pdf]                  - rotate all pages in one file by --concat command
\tsome1[.pdf] some2[.pdf] ... - merge/concat every files to one file

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
\t::     - delimeter for ranges of pages via --concat command
\t++     - delimeter for ranges of pages right rotation via --concat command
\t--     - delimeter for ranges of pages left rotation via --concat command
\t^^     - delimeter for ranges of pages upside down rotation via --concat command

DESTINATION(s):
File names may be absolute or relative
\t-t                          - start of target file names arguments
\t--target
\tsome[.pdf]                  - merge/concat every files to one file
\tsome1[.pdf] some2[.pdf] ... - split/grind only one file at a time

Examples:
\tpapir -s some.pdf --pages 1^10/2+5,6,7-7/69:42 -t new1.pdf new2.pdf new3.pdf
\t\toutcome: new1.pdf with 1 to 10 upside down pages from some.pdf,
\t\tnew2.pdf with pages 2 to 5 right rotated, page 6, page 7 left rotated,
\t\tnew3.pdf with pages 69 to 42.
\tpapir --merge /home/user/this1.pdf this2.pdf /mnt/server/this3.pdf -p 1^10
\t\toutcome: %d%m%Y-%H%M-%f.pdf with pages 1 to 10 upside down for every file,
\t\tthis1.pdf from user's home directory, this2.pdf from current directory,
\t\tthis3.pdf from mounted server directory.
\tpapir -g old1
\t\toutcome: as much %d%m%Y-%H%M-%f.pdf single page files as much pages does
\t\told1.pdf has.
\tpapir -grind old2.pdf --pages 42^69 -t itstime
\t\toutcome: itstime.pdf containing page 42 of old2.pdf upside down and 27 %d%m%Y-%H%M-%f.pdf
\t\tsingle page files all upside down
\tpapir --concat 1 2 3 4 -t 5
\t\toutcome: 5.pdf that contain all pages from 1.pdf 2.pdf 3.pdf 4.pdf concatenated as it is
\tpapir -c 1 2 3 4 -p ::/++/--/^^
\t\toutcome %d%m%Y-%H%M-%f.pdf with all pages from 1.pdf, all pages from 2.pdf right rotated,
\t\tall pages from 3.pdf left rotated, all pages from 4.pdf upside down
\tpapir -c /etc/passwd.pdf -p ^^ -target /root/nevermind
\t\toutcome: /root/nevermind.pdf file with all pages from file /etc/passwd.pdf upside down

version 1.7 10/11/2022
author: lngd
lngdeer@gmail.com
"""




loggy = getLogger("papir")

loggy_formatter = Formatter("%(levelname)s: %(message)s")
loggy_handler = StreamHandler(stdout)
loggy_handler.setFormatter(loggy_formatter)

loggy.addHandler(loggy_handler)
loggy.setLevel(20)




main_commands = "-s", "--split", "-m", "--merge"
aux_commands = "-g", "--grind", "-c", "--concat"
pageros_flags = "-p", "--pages"
targets_flags = "-t", "--target"
valid_commands = *main_commands, *aux_commands
valid_flags = *pageros_flags, *targets_flags
sources = []
targets = []
pageros = None
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




try:
	nextarg = argv[argi]
	argi += 1

	if nextarg in pageros_flags:

		pageros = argv[argi]
		argi += 1
		loggy.debug(f"PAGEROS: {pageros}")
	else:
		if aux:
			argi -= 1
		
		else:
			loggy.debug(f"current aux is {aux}")
			raise IndexError

except IndexError:
		if not aux:
			
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
