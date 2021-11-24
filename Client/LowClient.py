import subprocess
import sys
import json


def Call(	op_code : str = 'vld' ,
			key : str = None ,
			data  = None ,
			force : int = 0,
			password = None,
			**kwargs):

	if password == None:
		packet = {'op' : op_code  , 'key' : key , 'data' : data , 'force' : force, }# 'password' : password  }

	else:
		packet = {'op' : op_code  , 'key' : key , 'data' : data , 'force' : force, 'password' : password  }

	packet.update(kwargs)

	proc = subprocess.Popen(					[sys.executable , '-m' , 'Quinn.Client.ArgumentClient' ,
												json.dumps(packet)]  ,

												stdout = subprocess.PIPE , stderr = subprocess.PIPE)

	out , err = proc.communicate()

	if proc.returncode != 0:

		return {'data' : 'Client Decode Error' , 'status' : False}

	return json.loads(out.decode('utf8'))

if __name__ == '__main__':

	import colorama
	colorama.init(autoreset = True)

	def formatter(data):

		if data['status']:

		   sys.stdout.write(f"{colorama.Fore.GREEN}{data['data']}{colorama.Fore.RESET}")
		   sys.exit(0)
		else:

		  sys.stderr.write(f'{colorama.Fore.RED}UNSUCCESSFUL{colorama.Fore.RESET}\nERROR-MSG: {colorama.Fore.LIGHTRED_EX}{data["data"]}{colorama.Fore.RESET}')
		  sys.exit(1)

	if ('-h' in sys.argv) or ('--help' in sys.argv):

		sys.stdout.write('Usage: LowClient \n\t<opcode(vld default)>\n\t<key(None default)>\n\t<data(None default)>\n\t<permission-code(0 default)>\n\t<password(optional)>\n')

	else:

		if len(sys.argv) < 2:

			formatter(Call('vld'))

		else:

			formatter(Call(*sys.argv[1:6]))

	colorama.deinit()
