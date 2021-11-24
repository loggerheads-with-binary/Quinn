import zmq
import sys
import subprocess
import Quinn.config as cfg

socket = None

def Setup():

	global socket

	if socket != None :
		return

	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.RCVTIMEO  = cfg.ClientTimeout
	socket.connect(f"tcp://localhost:{cfg.port}")

	return


if __name__ == "__main__":

	Setup()

	if len(sys.argv)<1:
		packet = b'{"op": "vld", "key": null, "data": null, "force": 0}'

	else :
		packet = sys.argv[1].encode('utf8')

	socket.send(packet)
	sys.stdout.write(socket.recv().decode('utf8'))
