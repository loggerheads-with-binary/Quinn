from sys import argv, exit as _exit, stdout
import Quinn.Client as qc
import sys

if ('-h' in argv) or ('--help' in argv):
	
	sys.stdout.write('Usage: Quinn.Client \n\t<opcode(vld default)>\n\t<key(None default)>\n\t<data(None default)>\n\t<permission-code(0 default)>\n\t<password(optional)>\n')
	_exit(0xff)

import colorama
colorama.init(autoreset = True)

def formatter(data):

	if data['status']:

	   sys.stdout.write(f"{colorama.Fore.GREEN}{data['data']}{colorama.Fore.RESET}")
	   sys.exit(0)

	else:

	  sys.stderr.write(f'{colorama.Fore.RED}UNSUCCESSFUL{colorama.Fore.RESET}\nERROR-MSG: {colorama.Fore.LIGHTRED_EX}{data["data"]}{colorama.Fore.RESET}')
	  sys.exit(1)


if len(sys.argv) < 2:

	formatter(qc.Call('vld'))

else:

	formatter(qc.Call(*sys.argv[1:6]))
