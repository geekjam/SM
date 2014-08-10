from Core import *
import ConfigParser
def GetConfig(section, option):
    cf = ConfigParser.ConfigParser()
    cf.read("./Data/system.conf")
    return cf.get(section, option)

def Init():
    pass
