from Mod.Core import *
import sys
InputCallBack = None
ExitFuns = []
Prompt = "$"

def Init():
	print Core.Config.GetConfig("soft", "name") + " by " + Core.Config.GetConfig("soft", "god")
	print "Version:" + Core.Config.GetConfig("soft", "version")
	while True:
		inputStr = raw_input(Prompt)
		if InputCallBack != None:
			InputCallBack(inputStr)

def Exit():
	for func in ExitFuns:
		func()
	
	sys.exit(0)

