import shlex 
from Quinn.Client.LowClient import PacketMaker
import Quinn.Client.ArgumentClient	as AC

if __name__ == '__main__' : 

	
	print('Quinn Shell\nUse shell-exit to quit\nCommand Syntax: <op code> <key> <data> <force=1/no-force=0>\n\n')
	
	while True:
	
		commands_ = shlex.split(input('\nQuinn Server>>> quinn '))
		
		if len(commands_) > 0 :
			
			if commands_[0] == 'shell-exit' :
			
				exit()
				
			elif commands_[0] == 'make-packet' : 
			
				packet = eval( input("Put dictionary {'op' : , 'key' : ,  'data' : , 'force' : }\n") )
				
			else: 
				packet = PacketMaker(*commands_)
			
			AC.socket.send(packet.__repr__().encode('utf8')) 
			print(eval(AC.socket.recv().decode('utf8')))
				
		
		continue 