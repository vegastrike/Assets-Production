import quest
import Vector
import VS
import unit
import random
class quest_drone (quest.quest):
    def __init__ (self):
        self.sysfile = VS.getSystemFile()
        self.stage=0
        self.lastdist=10000
        self.derelict=unit.getUnitByName("unknown_derelict")
        self.jumping=0
    def launchNewDrone (self):
        playa=VS.getPlayer()
        if (not playa.isNull()):
            self.makeQuestPersistant()
            vec = playa.Position()
            vec = Vector.Add(vec,(3000,0,0))
            self.drone=VS.launch("IO47","unknown_active","unknown","unit","default",1,1,vec,'')
            self.drone.SetTarget(playa)
            self.stage=1
        else:
            self.drone=VS.Unit()
    def setDroneNear (self,playa):
        vec = playa.Position()
        vec = Vector.Add (vec,(random.randrange(-1000,1000),
                               random.randrange(-1000,1000),
                               random.randrange(-1000,1000)))
        self.drone.SetCurPosition(vec)
        self.drone.SetTarget(playa)
    def Execute (self):
        playa=VS.getPlayer()
        if (playa.isNull()):
            return 1

        if (not self.stage):
            if (self.derelict):
                if (self.derelict.getSignificantDistance(playa)<200):
                    self.launchNewDrone()
            else:
                self.launchNewDrone()                
        else:
            if (self.drone.isNull()):
                self.removeQuest();
                return 0
            sf = VS.getSystemFile();
            if (self.sysfile!=sf and not self.jumping):
                self.drone.JumpTo(sf);
                self.sysfile=sf
#                self.setDroneNear(playa)
                self.lastdist=10000
                self.jumping=1
                print "jumping"
            else:
                if (self.jumping):
                    if (playa.getUnitSystemFile()==self.drone.getUnitSystemFile()):
                        self.drone.SetTarget (playa)                        
                        self.jumping=0
                        self.setDroneNear(playa)
                    
        return 1

class quest_drone_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_drone")
    def create (self):
        return quest_drone()



