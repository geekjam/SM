import sys
from Mod.Core import *
HookCommand = None
CommandList = []
def CommandShow():
        print "[+]Command  Description"
	for cmds in CommandList:
		print "[-]" + cmds[0] + " - "  + cmds[2]

def CommandAdd(cmd, func, des):
	CommandList.append([cmd,func, des])

def CommandEvil(inputStr):
	for cmds in CommandList:
		if inputStr[0:len(cmds[0])] == cmds[0]:
			argv = inputStr[len(cmds[0])+1:len(inputStr)].split(' ')
			try:
				if len(argv) == 1 and argv[0] == '':
					cmds[1]()

				if len(argv) == 1 and argv[0] != '':
					cmds[1](argv[0])
				if len(argv) == 2:
					cmds[1](argv[0], argv[1])
				if len(argv) == 3:
					cmds[1](argv[0], argv[1], argv[2])
				if len(argv) == 4:
					cmds[1](argv[0], argv[1], argv[2], argv[3])

			except Exception, e:
				print e
			return
	if len(CommandList) > 0:
		cmds = CommandList[len(CommandList)-1]
		if cmds[0] == "other":
			cmds[1](inputStr)
			return

	if inputStr != '':
		print "Error! Command not found."
			

def Init():
    Core.Controller.InputCallBack = CommandEvil
    CommandAdd("quit", Core.Controller.Exit, "Exit the program")
    CommandAdd("exit", Core.Controller.Exit, "Exit the program")
    CommandAdd("help", CommandShow, "Will be Show the command list")
