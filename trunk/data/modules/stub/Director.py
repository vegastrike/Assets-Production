_savedata=[{},{},{},{},{},{},{},{},{},{}]
_savestrs=[{},{},{},{},{},{},{},{},{},{}]

class Mission:
    def Pickle(self):
        print 'pickling'
        return ''
    def UnPickle(self,s):
        print 'unpickling'
    def Execute(self):
        print 'execute'
def putSaveData (whichplayer, key, num, val):
    global _savedata
    _savedata[whichplayer][key][num]=val
    return len(_savedata[whichplayer][key])
def getSaveDataLength (whichplayer, key):
    global _savedata
    try:
	return len(_savedata[whichplayer][key])
    except:
	return 0
def getSaveData (whichplayer, key,num):
    global _savedata
    return _savedata[whichplayer][key][num]
def pushSaveData (whichplayer,key,val):
    global _savedata
    try:
	_savedata[whichplayer][key].append(val)
    except:
	_savedata[whichplayer][key]=[val]
    return len(_savedata[whichplayer][key])
def eraseSaveData (whichplayer,key,num):
    global _savedata
    del _savedata[whichplayer][key][num]
    return len(_savedata[whichplayer][key])
def putSaveString (whichplayer, key, num, val):
    global _savestrs
    _savestrs[whichplayer][key][num]=val
    return len(_savestrs[whichplayer][key])
def getSaveStringLength (whichplayer, key):
    global _savestrs
    try:
	return len(_savestrs[whichplayer][key])
    except:
	return 0
def getSaveString (whichplayer, key,num):
    global _savestrs
    return _savestrs[whichplayer][key][num]
def pushSaveString (whichplayer,key,val):
    global _savestrs
    try:
	_savestrs[whichplayer][key].append(val)
    except:
	_savestrs[whichplayer][key]=[val]
    return len(_savestrs[whichplayer][key])
def eraseSaveString (whichplayer,key,num):
    global _savestrs
    del _savestrs[whichplayer][key][num]
    return len(_savestrs[whichplayer][key])

