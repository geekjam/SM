from Mod.Core import *
def HookCommandTest():
	print "I am test command, From test module."

def Test():
	test = Core.Config.GetConfig("system","soft", "welcome")
	test = test.replace("\\r","\r")
	test = test.replace("\\n","\n")
	#print test
	pass

def Init():
	Core.Command.CommandAdd("test", HookCommandTest, "test module")
	Test()
