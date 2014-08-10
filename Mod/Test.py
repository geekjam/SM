from Mod.Core import *
def HookCommandTest():
	print "I am test command, From test module."

def Init():
        Core.Command.CommandAdd("test", HookCommandTest, "test module")
