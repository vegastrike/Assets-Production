import Director
def findAndAddQuest(playernum,questname):
    mylen=Director.getSaveDataLength(playernum,questname)
    if (mylen>0):
        myfloat=Director.getSaveData(playernum,questname,0)
        print myfloat
        print "there she is"
        if (myfloat<1.01 and myfloat >.99):
            return 1
        Director.putSaveData(playernum,questname,0,1)
    else:
        Director.pushSaveData(playernum,questname,1)
    return 0

class quest:
    def Execute(self):
        print "default"
        return 1
class quest_factory:
    def __init__(self):
        self.name="quest"
    def create (self ):
        return quest()
    def factory (self,playernum):
        if (not findAndAddQuest (playernum,self.name)):
            return self.create()
        return


            
class drone_quest (quest):
    def __init__ (self):
        self.i=0
    def Execute (self):
        print self.i
        self.i+=1
        if (self.i>1000):
            return 0
        return 1

class drone_quest_factory (quest_factory):
    def __init__ (self):
        self.name="drone_quest";
    def create (self):
        return drone_quest()


quests = {"gemini_sector/delta_prime":drone_quest_factory(),
          "sol_sector/celeste":quest_factory()}


def newQuest(playernum,oldsys,newsys):
    newq=quests.get (newsys)
    if (newq):
        newq = newq.factory(playernum)
        if (newq):#only remove it if that player hasn't done it before
            del quests[newsys]
    return newq
