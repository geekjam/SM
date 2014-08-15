import os
import sys
import time
from Core import *
s = os.sep

def ModInit():
    global Core
    Core.Modules = []
    for f in os.listdir('Mod'):
        if os.path.isfile('Mod' + s + f):
            fname = os.path.splitext(f)
            if fname[1] == '.py' and fname[0] != '__init__' and fname[0] != 'Core':
                __import__('Mod.'+fname[0])
                #print '[-]Load Mod.' + fname[0]
                if fname[0] != "Controller":
                    Core.Modules.append(fname[0])
                exec 'Core.' + fname[0] + "=" + fname[0]

    Core.Modules.append("Controller")
    
    for m in Core.Modules:
        exec 'Core.' + m + '.Init()'
        
ModInit()

