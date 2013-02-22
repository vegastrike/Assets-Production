import Director

def loadStringList (playernum,mykey):
    lengt = Director.getSaveDataLength (playernum,mykey)
    if (lengt<1):
        return []
    rez = []
    curstr = []
    curstr_append = curstr.append
    lengt = Director.getSaveData(playernum,mykey,0)
    for i in range (1,lengt+1):
        myint=Director.getSaveData (playernum,mykey,i)
        if myint:
            curstr_append(myint)
        else:
            rez.append("".join(map(chr,curstr)))
            del curstr[:]
    return rez
def saveStringList (playernum,mykey,names):
    ord_ = ord
    length = Director.getSaveDataLength (playernum,mykey)
    k=1
    tot=0
    for i in range (len (names)):
        tot += len (names[i])+1
    if (length==0):
        Director.pushSaveData(playernum,mykey,tot)
    else:
        Director.putSaveData(playernum,mykey,0,tot)
    for i in range (len (names)):
        for j,c in enumerate (names[i]):
            if (k < length):
                Director.putSaveData(playernum,mykey,k,ord_(c))
            else:
                Director.pushSaveData(playernum,mykey,ord_(c))
            k+=1
        if (k < length):
            Director.putSaveData(playernum,mykey,k,0)
        else:
            Director.pushSaveData(playernum,mykey,0)
        k+=1
