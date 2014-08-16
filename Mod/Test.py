from Mod.Core import *
def HookCommandTest():
	print "I am test command, From test module."

def Test():
	httpClient = Core.Http.HttpClient("http://cn.bing.com/az/hprichbg/rb/DaintreeNP_ZH-CN9005339324_1366x768.jpg")
	f = open("./Data/test.jpg", "w")
	f.write(httpClient.GetData())
	f.close()
	pass

def Init():
	Core.Command.CommandAdd("test", HookCommandTest, "test module")
	#Test()
