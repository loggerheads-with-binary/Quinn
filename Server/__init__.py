import zmq
from argparse import ArgumentParser, Namespace
import Quinn.config as cfg
import os, sys, subprocess
import json
from hashlib import sha512
#import nint  		##Isabella Protocol
import time
from datetime import datetime
import gc

class BLANKNONE(int):

	def __new__(cls, *args, **kwargs):
		return  super(BLANKNONE, cls).__new__(cls, 1-(10**9))

	def __repr__(self):

		return 'NULL'

	def __str__(self):

		return 'NULL'

	def encode(self, encoding):

		return b'NULL'

BlankNone = BLANKNONE()

class SafeQuinnDict(dict):

	def __getitem__(self , key):

		return super().get(key.lower() , BlankNone)

DataMain ,  CountersMain , InstructionsQueue, ALLOW_QUEUE,  ServerPacket , ClientPacket , FileHandle, ServerLogs = \
dict() , 		dict() , 		list(),			True,			dict() , 	SafeQuinnDict(), 	None,	None

class FlushWriter():

	def __init__(self , filename , flush_count = cfg.FlushCacheCount):

		self.file = filename
		self.queue = list()
		self.limit = flush_count

	def write(self  , text):

		self.queue.append(text)

		if len(self.queue) > self.limit:

			self.WritetoFile()

	def WritetoFile(self):

		with open(self.file, 'a') as handle:

			handle.write(''.join(self.queue))
			self.queue = list()

class LogWriter(FlushWriter):

	def LoggerWriteMain(self, text, level):

		from datetime import datetime

		self.write(f'{datetime.now().strftime("%d-%m-%Y")},{datetime.now().strftime("%H:%M:%S")},{level},{text}\n')

	def info(self , text):

		self.LoggerWriteMain(text , 'info')


	def warning(self, text):

		self.LoggerWriteMain(text , 'WARNING')

	def debug(self, text):

		self.LoggerWriteMain(text , 'debug')

	def critical(self, text):

		self.LoggerWriteMain(text , '*****CRITICAL*****')

	def error(self, text):

		self.LoggerWriteMain(text , '*ERROR*')

def Initialize():

	global DataMain , ServerPacket , ClientPacket, FileHandle, ServerLogs

	DataMain = dict()																						##Will store all of the variables
	ServerPacket = {'data' : None , 'status' : False}															##Sample Server Packet[to be sent]
	ClientPacket = {'op' : 'vld' , 'key' : None , 'data' : None , 'force' : 0 , 'password' : '0xff'}		##Sample Client Packet[to be received]
	FileHandle	= FlushWriter(cfg.LogFile)																	##Logging File
	ServerLogs = LogWriter(cfg.ServerLogs)																	##Server Logging File

	ServerLogs.info(f'Quinn Server Established on PID {os.getpid()}')

def SetPrefs(options):

	cfg.LogFile = options.logfile
	cfg.port = options.port
	cfg.PersistentStorage = options.storage
	cfg.QuinnPassword = options.password
	cfg.ServerLogs = options.serverlogs

	return True

context = zmq.Context()
socket = context.socket(zmq.REP)

def SocketBinder(port_number : int = None):

	global ServerLogs

	if port_number == None:
		port_number = cfg.port

	global socket

	try:
		socket.bind(f"tcp://*:{port_number}")

	except zmq.error.ZMQError:
		ServerLogs.critical(f'Port {port_number} already in use. Cannot use the port.')
		LoggerMain('occ' , port_number , False)
		_Self_Destruct()

	except:

		raise

	ServerLogs.info(f'Established connection at port {port_number}')

put_socket = lambda x = dict() : socket.send(json.dumps(x).encode('utf8'))
one_and_zero = lambda x : 1 if x else 0
hasher_main = lambda x  = '' : (sha512(x).digest()) if type(x) == bytes else (sha512(str(x).encode('utf8')).digest())

def InstructionsExecute():

	global ALLOW_QUEUE , InstructionsQueue

	while True :

		if ALLOW_QUEUE:

			if len(InstructionsQueue)==0:

				time.sleep(2)
				continue


			if time.time() > InstructionsQueue[0][0]:

				subprocess.Popen(InstructionsQueue[0][-1])
				InstructionsQueue.pop(0)

				continue

		time.sleep(1)

def LoggerMain(op_code, key_s_packet , status_code):

	global FileHandle

	FileHandle.write(f'{datetime.now().strftime("%d-%m-%Y")},{datetime.now().strftime("%H:%M:%S")},{op_code},{key_s_packet},{one_and_zero(status_code)}\n')

	return None

def _Self_Destruct(accidental: bool = True ):

	global FileHandle , ServerLogs

	LoggerMain('end' , None , True)
	FileHandle.WritetoFile()

	ServerLogs.critical(f'Shutting Down Quinn Server on PID {os.getpid()}')

	ServerLogs.WritetoFile()

	if accidental:

		try:

			put_socket({'data' : 'Shutting Down Server' , 'status' : True})

		except :

			pass

	subprocess.call(['notif' , '-t' , 'Quinn Server' , '-m' , 'Quinn Server is Shutting Down' , '-d' , '10'])
	os._exit(200)

class InstructionToolkit(ArgumentParser):

	def make_args(self):

		import hashlib

		self.add_argument(	'-p' , '--port' ,
							dest = 'port' , action = 'store' , default = cfg.port , type = int,
							help = "Port to operate Quinn Server on")

		self.add_argument(	'--log-file' ,
							dest = 'logfile' , action = 'store' , default = cfg.LogFile , type = os.path.abspath ,
							help = 'Log File to Write Logs into' )

		self.add_argument(	'--storage' , '--db' , '--freeze-file' , '--persistent' ,
							dest = 'storage' , action = 'store' , default = cfg.PersistentStorage , type = os.path.abspath ,
							help = 'Persistent Storage file to write content into')

		self.add_argument(	'--server-logs' , '--server-logger' ,
							dest = 'serverlogs' , action = 'store' , default = cfg.ServerLogs , type = os.path.abspath ,
							help = 'Server Logs File')

		self.add_argument(	'-P' , '--pass' , '--password' ,
							dest = 'password' , action = 'store' , type = lambda x : hashlib.sha512(x.encode('utf8')).digest() ,
							default = cfg.QuinnPassword ,
							help = 'Quinn Server Password' )

def PermissionCode(code):

	try:
		if isinstance(code , int):
			return abs(code)

		elif isinstance(code, str):

			return abs(int(eval(code)))

		elif isinstance(code , bytes):

			return abs(int(eval(code.decode('utf8'))))

		return 0

	except:
		ServerLogs.warning(f'Incorrect permission code entered {code}')
		return 0

"""ALL INSTRUCTIONS COME HERE"""
##Just for indentation and blocking
if len("All Instructions") > 0:

	def _instruction_get_():

		global ServerPacket , ClientPacket, DataMain

		perm = PermissionCode(ClientPacket['force'])

		data = DataMain.get(ClientPacket['key'] , BlankNone)

		if data == BlankNone:
			ServerPacket = {'data' : 'Key does not exist on server' , 'status' : False}
			return

		else:

			trustlevel = data[0]

			if (trustlevel&8):
				if not (perm&8):
					ServerPacket = {'data' : 'Key does not exist on server' , 'status' : False}
					return

			if trustlevel&2:

					if ClientPacket['password'] == data[1]:		##&3 structure
						ServerPacket = {'data' : data[-1] , 'status' : True}
						return

					ServerPacket = {'data' : "Incorrect Password" , 'status' : False}
					return

			ServerPacket = {'data' : data[-1] , 'status' : True}
			return

	def _instruction_set_():
		global ServerPacket , ClientPacket, DataMain

		perm = PermissionCode(ClientPacket['force'])

		if ClientPacket['key'] in DataMain:

			data = DataMain[ClientPacket['key']]
			trustlevel = data[0]

			if (trustlevel&4):
				ServerPacket = {'status' : False , 'data' : 'Cannot overwrite permanent entries and constants'}
				return

			if (trustlevel&2):

				if data[1] == ClientPacket['password']:

					DataMain.update({ClientPacket['key'] : (perm|2 , ClientPacket['password'] , ClientPacket['data'])})
					ServerPacket = {'status' : True , 'data' : None}
					return

				else :
					ServerPacket = {'status' : False, 'data' : "Cannot overwrite due to incorrect password"}
					return

			if not (perm&1):
				ServerPacket = {'status' : False  , 'data' : 'Inadequate Permissions to overwrite'}
				return

			DataMain.update({ClientPacket['key'] : (perm , ClientPacket['password'] , ClientPacket['data'])})
			ServerPacket = {'status' : True, 'data' : None}
			return

		else:

			if (perm&2):
				if 'password' not in ClientPacket:
					ServerPacket = {'data' : "Password not provided for Set Instruction with a permission key 2" , 'status' : False}
					return

				DataMain.update({ClientPacket['key'] : ( perm|2 , ClientPacket['password'] , ClientPacket['data'] )})
				ServerPacket = {'data' : None , 'status' : True}
				return

			DataMain.update({ClientPacket['key'] : (perm ,  ClientPacket['data'])})
			ServerPacket = {'data' : None , 'status' : True}
			return

	def _instruction_chk_():
		global ServerPacket , ClientPacket, DataMain

		data = DataMain.get(ClientPacket['key'] , BlankNone)

		if data == BlankNone:
			ServerPacket = {'data' : 'Key does not exist' , 'status' : False}
			return

		if (data[0]&8):

			if PermissionCode(ClientPacket['force'])&8:
				ServerPacket = {'data' : 'Key exists on server' , 'status' : True}
				return

			else:
				ServerPacket = {'data' : 'Key does not exist' , 'status' : False}
				return

		ServerPacket = {'data' : 'Key exists on server' , 'status' : True}
		return

	def _instruction_pop_():

		global ServerPacket , ClientPacket, DataMain

		data = DataMain.get(ClientPacket['key'] , BlankNone)

		if data == BlankNone:
			ServerPacket = {'data': 'Key does not exist' , 'status' : False}
			return

		trustlevel , perm = data[0] , PermissionCode(ClientPacket['force'])

		if (trustlevel&8):
			if not(perm&8):
				ServerPacket = {'data': 'Key does not exist' , 'status' : False}
				return

		if (trustlevel&4):
			ServerPacket = {'data': 'Cannot pop perm/const variables' , 'status' : False}
			return

		if (trustlevel&2):
			if not ClientPacket['password'] == data[1]:
				ServerPacket = {'data' : 'Incorrect Password' , 'status' : False }
				return

		if (trustlevel&1):
			if not (perm&1):
				ServerPacket = {'data' : 'Inadequate Permission' , 'status' : False }
				return

		ServerPacket = {'data' : data[-1] , 'status' : True}
		DataMain.pop(ClientPacket['key'])
		return

	def _instruction_del_():
		global ServerPacket , ClientPacket, DataMain

		data = DataMain.get(ClientPacket['key'] , BlankNone)

		if data == BlankNone:
			ServerPacket = {'data' : "Key does not exist" , 'status' : False}
			return

		perm = PermissionCode(ClientPacket['force'])

		if (data[0]&8):
			if not (perm&8):
				ServerPacket = {'data' : "Key does not exist" , 'status' : False}
				return

		if (data[0]&4):
			ServerPacket = {'data' : "Perm/Const variables cannot be deleted" , 'status' : False}
			return


		if (data[0]&2):
			if ClientPacket['password'] != data[1]:
				ServerPacket = {'data' : 'Incorrect Password' , 'status' : False }
				return

		if (data[0]&1):
			if not (perm&1):
				ServerPacket = {'data' : 'Inadequate Permissions' , 'status' : False}
				return

		ServerPacket = {'data' : "Successfully Deleted Key" , 'status' : True}
		DataMain.pop(ClientPacket['key'])
		return

	##Large Scale Server Instructions
	def _instruction_end_():
		global ServerPacket , ClientPacket

		perm  = PermissionCode(ClientPacket['force'])

		if not perm&(8|1|64) :
			ServerPacket = {'data' : 'Inadequate Permissions' , 'status' : False}
			return

		if hasher_main(ClientPacket['password']) != cfg.QuinnPassword :
			ServerPacket = {'data' : 'Incorrect Password' , 'status' : False}
			return

		_Self_Destruct(True)

	def _instruction_vld_():
		global ServerPacket , ClientPacket

		ServerPacket = {'data' : 'Server is up and running' , 'status' : True}

		return

	def _instruction_wrt_():
		global ServerPacket , ClientPacket, DataMain , CountersMain, ServerLogs

		if hasher_main(ClientPacket['password']) != cfg.QuinnPassword:
			ServerPacket = {'data' : 'Incorrect Password' , 'status' : False}
			return

		if not PermissionCode(ClientPacket['force'])&(8|1|64):
			ServerPacket = {'data' : 'Inadequate Permissions' , 'status' : False}
			return


		import _pickle as pickle

		data_1 = {key : value for key , value in DataMain.items() if not (data[0]&64)}

		with open(cfg.PersistentStorage , 'wb') as filehandle:
			pickle.dump((data_1 , CountersMain) , filehandle)

		ServerLogs.critical('Persistent Storage has been written and all variables are frozen')
		return

	def _instruction_rld_():
		global ServerPacket , ClientPacket, CountersMain , DataMain , ServerLogs

		if hasher_main(ClientPacket['password']) != cfg.QuinnPassword:
			ServerPacket = {'data' : 'Incorrect Password' , 'status' : False}
			return

		if not PermissionCode(ClientPacket['force'])&(8|1|64):
			ServerPacket = {'data' : 'Inadequate Permissions' , 'status' : False}
			return

		import _pickle as pickle

		try:
			with open(cfg.PersistentStorage , 'rb') as filehandle:
				DataMain , CountersMain = pickle.load(filehandle)

		except:
			DataMain, CountersMain = dict() , dict()
			ServerLogs.critical(f'Error in re-reading frozen variables. Will instantiate new class')
			ServerPacket = {'data'  :"Frozen Decode Error" , 'status' : False}
			return

		ServerPacket = {'data' : 'Variables Successfully Reloaded' , 'status' : True}
		ServerLogs.critical(f'Frozen variables from `{os.stat(cfg.PersistentStorage).st_mtime}`[epoch timestamp] have been loaded')

	def _instruction_lst_():
		global ServerPacket , ClientPacket, CountersMain , DataMain

		if not hasher_main(ClientPacket['password']) == cfg.QuinnPassword :
			ServerPacket = {'data' : "Listing all Variables needs Quinn Password|| Incorrect Password Entered" , 'status' : False}
			return

		data_1 = [key for key , value in DataMain.items() if not (value[0]&8)]
		ServerPacket = {'data' : {'Variables' : data_1 , 'Counters' : list(CountersMain.keys())} , 'status' : True}
		return

	def _instruction_rfr_():
		global ServerPacket , ClientPacket, CountersMain , DataMain

		if not PermissionCode(ClientPacket['force'])&(8|64|1):
			ServerPacket = {'data' : "Inadequate Permissions" , 'status' : False}
			return

		if hasher_main(ClientPacket['password']) != cfg.QuinnPassword:
			ServerPacket = {'data' : 'Incorrect Password' , 'status' : False}
			return

		ServerPacket = {'data' : "Resetting All Variables" , 'status' : True}
		CountersMain , DataMain = dict() , dict()
		return

	##Counter Instructions
	def _instruction_udt_():
		global ServerPacket , ClientPacket, CountersMain

		if ClientPacket['key'] not in CountersMain:
			CountersMain.update({ClientPacket['key']  : 1})

		else :
			CountersMain[ClientPacket['key'] ] += 1

		ServerPacket = {'data' : 'Successful' , 'status' : True}

	def _instruction_rtr_():
		global ServerPacket , ClientPacket, CountersMain

		ServerPacket = {'data' : CountersMain.get(ClientPacket['key'] , 0) , 'status' : True}
		return

	def _instruction_crm_():
		global ServerPacket , ClientPacket, CountersMain

		status = CountersMain.pop(ClientPacket['key'] , BlankNone)

		if status == BlankNone:
			ServerPacket = {'data' : 'Counter did not exist on Server' , 'status' : False}
			return

		ServerPacket = {'data' : f"Counter {ClientPacket['key'] } removed at {status}", 'status' : True}
		return

	##Queue Feature
	def _instruction_feed_():

		global ClientPacket, ServerPacket, InstructionsQueue, ALLOW_QUEUE

		if not isinstance(ClientPacket['data'] , list):

			if not isinstance(ClientPacket['data'] , str):
				ServerPacket = {'data' : "Data type for instruction not valid. Should be list/string" , 'status' : True}
				return

			ClientPacket['data'] = list([ClientPacket['data']])

		time_ = ClientPacket.get('time' , ClientPacket.get('wait' , 0) + time.time())

		ALLOW_QUEUE = False

		i = [index for index , (timing , _) in enumerate(InstructionsQueue ) if timing < time_ ][-1:]

		InstructionsQueue.insert((0 if len(i)==0 else (i[0])) , (time_ , ClientPacket['data']) )

		ALLOW_QUEUE = True
		ServerPacket = {'status' : True ,
						'data' : f"Instruction fed. Will be executed at {datetime.fromtimestamp(time_).strftime('%H:%M:%S on %d-%m-%Y')}"}
		return

	##Isabella Protocol Instructions
	def _instruction_iss_():
		global ServerPacket , ClientPacket

		##Key, Password
		try:

			options = nint.filtration(nint.arguments(['--sudo' , ClientPacket['password'] , '-q' , ClientPacket['key']]))

		except nint.NintErrors.LoginError:

			ServerPacket = {'status' : False , 'data' : "Incorrect Sudo Password"}
			return

		except:
			ServerPacket = {'status' : False , 'data' : "Isabella Protocol Error"}
			return

		try :

			password = nint.golden_retriever(options, True , False)

		except KeyError:
			ServerPacket = {'data' : "Key does not exist on Nint" , 'status' : False}
			return

		except:
			ServerPacket = {'status' : False , 'data' : "Isabella Protocol Error"}
			return

		ServerPacket = {'data' : nint.convert_password_to_string(password) , 'status' : True}

	def _instruction_isr_():
		global ServerPacket , ClientPacket

		nint.OpenedDatabase.make_data(nint.NINT_STANDARD_DATABASE)

		try:
			password = nint.golden_retriever(nint.Namespace(**{	'sudomode' : False ,
																'upass' : ClientPacket['password'] ,
																'query' : ClientPacket['key'] ,
																}) )

		except nint.NintErrors.PasswordError:
			ServerPacket = {'status' : False , 'data' : "Incorrect Password Provided"}
			return

		except KeyError:
			ServerPacket = {'status' : False , 'data' : "Key does not exist on NINT"}
			return

		except:
			ServerPacket = {'status' : False , 'data' : "Isabella Protocol Error"}
			return

		ServerPacket = {'data' : nint.convert_password_to_string(password), 'status' : True}
		return

	def _instruction_isx_():
		global ServerPacket , ClientPacket

		if not PermissionCode(ClientPacket['force'])&1:
			ServerPacket = {'data': "Incorrect Permissions" , 'status' : False}
			return

		nint.data , nint.sudodata = None , None
		nint.OpenedDatabase.make_data(nint.NINT_STANDARD_DATABASE)

		ServerPacket = {'data' : 'Refreshed Nint' , 'status' : True}
		return

	##Multiple Instructions

	def _instruction_mset_():

		global ClientPacket, ServerPacket, DataMain

		if not isinstance(ClientPacket['data'] , dict):
			ServerPacket = {'data' : 'Incorrect Datatype for instruction' , 'status' : False}
			return

		cl_tmp = ClientPacket.copy()
		s_tmp = list()

		for key , value in cl_tmp['data'].items():
			ClientPacket = {'key' : key , 'value' : value , 'force' : cl_tmp['force'] , 'password' : cl_tmp['password']}
			_instruction_set_()
			s_tmp.update({key : ServerPacket.copy()})

		ServerPacket = { 'data' : s_tmp.copy() , 'status' : True}
		del s_tmp , cl_tmp
		return

	def _instruction_mget_():
		pass

		global ClientPacket, ServerPacket, DataMain

		if not isinstance(ClientPacket['data'] , dict):
			ServerPacket = {'data' : 'Incorrect Datatype for instruction' , 'status' : False}
			return

		cl_tmp = ClientPacket.copy()
		s_tmp = list()

		for key , value in cl_tmp['data'].items():
			ClientPacket = {'key' : key , 'value' : value , 'force' : cl_tmp['force'] , 'password' : cl_tmp['password']}
			_instruction_get_()
			s_tmp.update({key : ServerPacket.copy()})

		ServerPacket = { 'data' : s_tmp.copy() , 'status' : True}
		del s_tmp , cl_tmp
		return

	def _instruction_mux_():

		global ServerPacket, ClientPacket
		pass

		if not isinstance(ClientPacket['data'] , list):
			ServerPacket =  {'data' : 'Incorrect Datatype for instruction' , 'status' : False}
			return

		cl_tmp , s_tmp = ClientPacket.copy() , list()

		for index , instr in enumerate(cl_tmp):

			if not isinstance(instr , dict):
				s_tmp.append({'data' : f'Incorrect instruction at index `{index}`' , 'status' : False})
				continue

			ClientPacket = SafeQuinnDict(ClientPacket)
			ClientPacket['op'] = ClientPacket['op'].lower()

			if not ClientPacket['op'] in cfg.OP_CODES:
				s_tmp.append({'data' : f"Incorrect Operation Code at index {index}" ,'status' : False})
				continue

			exec(f'_instruction_{ClientPacket["op"]}_')
			s_tmp.append(ServerPacket.copy())

		ServerPacket = {'data' : s_tmp.copy() , 'status' : True}
		return

def DriverMain():

	global DataMain, ClientPacket, ServerPacket, socket, AgentHandler, FileHandle, ServerLogs, driver

	try:
		while True:

			##Somehow receive data
			ClientPacket = socket.recv()
			SWITCH_VALID = True

			##JSON Decode
			try :
				ClientPacket = ClientPacket.decode('utf8')
				ClientPacket = json.loads(ClientPacket)
				ClientPacket = SafeQuinnDict(ClientPacket)

			except:
				SWITCH_VALID = False
				ServerPacket = {'data' : "Server Cannot Decode" , 'status' : False}
				LoggerMain('nav' , None , False)

			##Validity Check
			if not all(s.lower() in cfg.ALLOWED_PARAMS for s in ClientPacket.keys()):

				ServerPacket = {'data' : "Illegal Parameters Fed to the Server" , 'status' : False}
				LoggerMain('ivp' , ClientPacket['key'] , False)
				#ServerLogs.error("Illegal Parameters given to the server")
				SWITCH_VALID = False

			if not (ClientPacket['op'].lower() in cfg.OP_CODES ):
				SWITCH_VALID = False
				ServerPacket = {'data' : 'Operational Code unrecognized' , 'status' : False}
				LoggerMain('urop' , None , False)
				#ServerLogs.error(f'Illegal Request made to server `{ClientPacket.get('op' , None)}`')

			if SWITCH_VALID :

				op_code = ClientPacket.get('op' , 'vld').lower()
				##Instructions Execut
				exec(f'_instruction_{op_code}_()')
				LoggerMain(ClientPacket['op'] , ClientPacket['key'] , ServerPacket.get('status' , 0))

			put_socket(ServerPacket)

			ServerPacket, ClientPacket = dict(), SafeQuinnDict()
			#time.sleep(cfg.SLEEP_TIME)
			gc.collect()

	except KeyboardInterrupt:

		ServerLogs.warning(f'Someone Externally Shut down the server')
		_Self_Destruct()

	except SystemExit:
		pass
		os._exit(200)

	except:

		FileHandle.WritetoFile()
		ServerLogs.WritetoFile()
		subprocess.call(['notif' , '-t' , 'Quinn Server' , '-m' , 'Quinn Server is Shutting Down' , '-d' , '15'])

		raise

	subprocess.call(['notif' , '-t' , 'Quinn Server' , '-m' , 'Quinn Server is Shutting Down' , '-d' , '15'])

if __name__ == '__main__':

	import sys
	sys.stdout.write('Kindly Use The module __main__ instead of __init__')
	sys.stderr.write('Kindly Use The module __main__ instead of __init__')
