from Core import *
import ConfigParser
def GetConfig(dataname, section, option):
	cf = ConfigParser.ConfigParser()
	cf.read("./Data/" + dataname + ".conf")
	return cf.get(section, option)

def Init():
    pass
