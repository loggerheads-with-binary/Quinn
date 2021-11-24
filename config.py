# decompyle3 version 3.7.7
# Python bytecode 3.8.0 (3413)
# Decompiled from: Python 3.8.6 (default, Nov 10 2021, 08:58:45) 
# [GCC 10.2.1 20210110]
# Embedded file name: A:\Anaconda\lib\site-packages\Quinn\config.py
# Compiled at: 2021-09-24 16:59:00
# Size of source mod 2**32: 2207 bytes
import os
ProgramPath = os.path.dirname(os.path.abspath(__file__))
port = 15252
QuinnPassword = b'\xafJ\xca\xdeN\x937\xa7\xd3w\x14\xdc\xe3\xca@\x9fn\x92\x15?\t=\x16=>"\x15\xd8\xb7\xda\x00\x9e\x9cn\xd8g\xb0e)V\xecT\xd3\xb6\x8b\x8cv\x82\xb3\x91\x00\xee$x\xcd?j=g\xa5Q3\xb08'
PersistentStorage = os.path.abspath(f"{ProgramPath}/Server/frozen.pickle")
LogFile = os.path.abspath(f"{ProgramPath}/Server/Instruction-Logs.csv")
FlushCacheCount = 5
ServerLogs = os.path.abspath(f"{ProgramPath}/Server/Server-Logs.csv")
ClientTimeout = 5000
SLEEP_TIME = 0.1
ALLOWED_PARAMS = {
 'op', 'key', 'data', 'force', 'password', 'time', 'wait'}
OP_CODES = {
 'get', 'set', 'pop', 'del', 'chk', 'end', 'vld', 'wrt', 'rld',
 'lst', 'rfr',
 'udt', 'rtr', 'crm',
 'isr', 'iss', 'isx',
 'mset', 'mget', 'mux',
 'feed'}
CommandAliases = {'vld':'vld', 
 'valid':'vld', 
 'running':'vld', 
 'get':'get', 
 'obtain':'get', 
 'set':'set', 
 'put':'set', 
 'push':'set', 
 'chk':'chk', 
 'check':'chk', 
 'verify':'chk', 
 'pop':'pop', 
 'sobtain':'pop', 
 'single-obtain':'pop', 
 'del':'del', 
 'rm':'del', 
 'remove':'del', 
 'end':'end', 
 'exit':'end', 
 'shut':'end', 
 'quit':'end', 
 'close':'end', 
 'wrt':'wrt', 
 'write':'wrt', 
 'log':'wrt', 
 'note':'wrt', 
 'freeze':'wrt', 
 'store':'wrt', 
 'rld':'rld', 
 'reload':'rld', 
 'reinstall':'rld', 
 'restart':'rld'}