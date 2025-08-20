from Papiro 	import Papiro
from Pagero 	import Pagero
from logging 	import getLogger
from logging 	import Formatter
from logging 	import StreamHandler
from sys 		import stdout
from sys 		import argv








usage = """
Usage:

papir COMMAND SOURCE(s) PAGEROS [DESTINATION(s)]

COMMAND:
-s --split - split one SOURCE pdf file to DESTINATIONS files
-m --merge - merge all DESTINATIONS files to one SOURCE file
"""




loggy = getLogger("papir")

loggy_formatter = Formatter("%(levelname)s: %(message)s")
loggy_handler = StreamHandler(stdout)
loggy_handler.setFormatter(loggy_formatter)

loggy.addHandler(loggy_handler)
loggy.setLevel(10)




try:
	command = argv[1]
	
	topageros = 2
	sources = []

	while True:
		currentsrc = argv[topageros]
		
		if Pagero.fullp.match(currentsrc):
			break

		sources.append(currentsrc)
		topageros += 1


	pageros = argv[topageros]
	targets = argv[topageros+1:]

	loggy.debug(f"COMMAND: {command}")
	loggy.debug(f"SOURCES: {sources}")
	loggy.debug(f"PAGEROS: {pageros}")
	loggy.debug(f"TARGETS: {targets}")

except IndexError:
	print(usage)




papir = Papiro(loggy)


match command:

	case "-s" | "--split":
		papir.split(pageros, *sources, *targets)

	case "-m" | "--merge":
		papir.merge(pageros, *targets, *sources)

	case _:
		loggy.critical(f"Command {command} not allowed")
