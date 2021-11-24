import Quinn.config as cfg
import zmq
import json

socket = None

def Setup(port : int = cfg.port , timeout = cfg.ClientTimeout):

	global socket

	if socket != None :
		return

	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.RCVTIMEO  = timeout
	socket.connect(f"tcp://localhost:{port}")

	return

def Call(op:str = 'vld' , key : str = None, data = None, force:int = 0 , password:str = None , **kwargs ):

	global socket

	Setup()

	if password == None :
		packet = {'op' : op , 'key' : key , 'data' : data , 'force' : force , }

	else :
		packet = {'op' : op , 'key' : key , 'data' : data , 'force' : force , 'password' : password , }

	packet.update(kwargs)

	socket.send(json.dumps(packet).encode('utf8'))

	try :
		rec_packet = socket.recv()

	except zmq.error.Again:

		return {'data' : "SERVER UNAVAILABLE" ,'status' : False }

	except:

		raise

	return json.loads(rec_packet.decode('utf8'))
