import sys
_savedata=[{},{},{},{},{},{},{},{},{},{}]
_savestrs=[{},{},{},{},{},{},{},{},{},{}]
dontdoprint=False
"""Can query-replace Hash with nothing to enable printfs comments"""
class Mission:
    def Pickle(self):
        print 'pickling'
        return ''
    def __init__(self):
        print 'initinig'

    def UnPickle(self,s):
        print 'unpickling'
    def Execute(self):
        print 'execute'
def putSaveData (whichplayer, key, num, val):
    global _savedata
    _savedata[whichplayer][key][num]=val
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'putSaveData: %g --> Player%d["%s"][%d]'%(val,whichplayer,key,num)
    return len(_savedata[whichplayer][key])
def getSaveDataLength (whichplayer, key):
    global _savedata
    try:
        lent=len(_savedata[whichplayer][key])
        if (not dontdoprint):
            sys.stderr.write('DIRECTOR:');print 'getSaveDataLength len(Player%d["%s"])=%d'%(whichplayer,key,lent)
	return lent
    except:
        if (not dontdoprint):
            sys.stderr.write('DIRECTOR:');print 'getSaveDataLength len(Player%d["%s"])=EMPTY'%(whichplayer,key)
	return 0
def getSaveData (whichplayer, key,num):
    global _savedata
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'getSaveData Player%d["%s"][%d]=%g'%(whichplayer,key,num,_savedata[whichplayer][key][num])
    return _savedata[whichplayer][key][num]
def pushSaveData (whichplayer,key,val):
    global _savedata
    try:
	_savedata[whichplayer][key].append(val)
    except:
	_savedata[whichplayer][key]=[val]
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'pushSaveData: %g --> Player%d["%s"][%d]'%(val,whichplayer,key,len(_savedata[whichplayer][key]))
    return len(_savedata[whichplayer][key])-1
def eraseSaveData (whichplayer,key,num):
    global _savedata
    del _savedata[whichplayer][key][num]
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'eraseSaveData: del Player%d["%s"][%d]'%(whichplayer,key,num)
    return len(_savedata[whichplayer][key])
def putSaveString (whichplayer, key, num, val):
    global _savestrs
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'putSaveString: "%s" --> StrPlayer%d["%s"][%d]'%(val,whichplayer,key,num)
    _savestrs[whichplayer][key][num]=val
    return len(_savestrs[whichplayer][key])
def getSaveStringLength (whichplayer, key):
    global _savestrs
    try:
        lent=len(_savestrs[whichplayer][key])
        if (not dontdoprint):
            sys.stderr.write('DIRECTOR:');print 'getSaveStringLength len(StrPlayer%d["%s"])=%d'%(whichplayer,key,lent)
        return lent
    except:
        if (not dontdoprint):
            sys.stderr.write('DIRECTOR:');print 'getSaveStringLength len(StrPlayer%d["%s"])=EMPTY'%(whichplayer,key)
	return 0
def getSaveString (whichplayer, key,num):
    global _savestrs
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'getSaveString StrPlayer%d["%s"][%d]="%s"'%(whichplayer,key,num,_savestrs[whichplayer][key][num])
    return _savestrs[whichplayer][key][num]
def pushSaveString (whichplayer,key,val):
    global _savestrs
    try:
	_savestrs[whichplayer][key].append(val)
    except:
	_savestrs[whichplayer][key]=[val]
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'pushSaveString: "%s" --> StrPlayer%d["%s"][%d]'%(val,whichplayer,key,len(_savestrs[whichplayer][key]))
    return len(_savestrs[whichplayer][key])-1
def eraseSaveString (whichplayer,key,num):
    global _savestrs
    del _savestrs[whichplayer][key][num]
    if (not dontdoprint):
        sys.stderr.write('DIRECTOR:');print 'eraseSaveString: del StrPlayer%d["%s"][%d]'%(whichplayer,key,num)
    return len(_savestrs[whichplayer][key])

