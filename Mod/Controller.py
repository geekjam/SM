from Mod.Core import *
import sys
InputCallBack = None
InitFuns = []
ExitFuns = []
Prompt = ">"

def Welcome():
	logoinfo = Core.Config.GetConfig("system","soft", "welcome")
	logoinfo += " Ver " + Core.Config.GetConfig("system", "soft", "version")
	print logoinfo.replace("\\r\\n","\r\n") + "\r\n"
	print Core.Config.GetConfig("system","soft", "name") + " by " + Core.Config.GetConfig("system", "soft", "god")
	#print "Version:" + Core.Config.GetConfig("system", "soft", "version")

def Init():
	Welcome()

	for func in InitFuns:
		func()

	while True:
		try:
			inputStr = raw_input(Prompt)
		except KeyboardInterrupt:
			Exit()

		if InputCallBack != None:
			InputCallBack(inputStr)

def Exit():
	for func in ExitFuns:
		func()
	
	sys.exit(0)

