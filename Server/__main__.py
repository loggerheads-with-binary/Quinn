import Quinn.Server as qs
import Quinn.config as qc
import threading

parser = qs.InstructionToolkit(	prog = 'quinn-server' ,
								description = 'The server script for the infamous Quinn Server Variable Storage',
								epilog = f'The Quinn Program is currently stored at "{qc.ProgramPath}", \
																Default Server Logs at "{qc.ServerLogs}", \
																Default Instruction Logs at "{qc.LogFile}"')
parser.make_args()

qs.SetPrefs(parser.parse_args())
qs.Initialize()
qs.SocketBinder()

#qs.DriverMain()


main_thread = threading.Thread(target = qs.DriverMain)
instructions_thread = threading.Thread(target = qs.InstructionsExecute)

main_thread.start()
instructions_thread.start()
