import time
import string

def log(message):
    print string.strip(repr(str(message)),'\'\"')
    #print str(time.strftime("[%d.%m.%Y-%H:%M:%S]", time.localtime()))+': '+str(message)
