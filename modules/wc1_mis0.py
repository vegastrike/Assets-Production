import random
import VS
import unit
import launch
from Vector import Add
class wc1_mis0:
    def __init__(self):
        pass
    def Start(self,carrier):
        self.origin =unit.getJumpPoint(random.randrange(0,99)).Position()
        print self.origin
        self.carrier=carrier
        self.origin=Add(self.origin,(1000+carrier.rSize(),100,100))
        carrier.SetPosAndCumPos (self.origin)
        self.spirit= launch.launch (VS.getPlayer().getFlightgroupName(),"confed","nova","default",1,1,Add((1000,200,0),self.origin))
        self.nav=[]
        self.visited=[0,0,0]
        self.launched=[0,0,0]
        self.nav+=[launch.launch("nav1","neutral","navpoint","sitting_duck",1,1,Add(self.origin,(50000,40000,10000)))]
        self.nav+=[launch.launch("nav2","neutral","navpoint","sitting_duck",1,1,Add(self.origin,(10000,100000,10000)))]
        VS.launch("Asteroids","neutral","asteroid","AFieldSparse","default",1,1,Add(self.origin,(10000,100000,10000)),"")
        VS.launch("Asteroids","neutral","asteroid","AFieldThin","default",1,1,Add(self.origin,(50000,40000,10000)),"")
        self.nav+=[launch.launch("nav3","neutral","navpoint","sitting_duck",1,1,Add(self.origin,(-40000,40000,10000)))]
    def LaunchNav (self,i,playa):
        if (i==0):
            launch.launch_wave_around_unit("BadGuys","aera","lekra","default",3,100,1000,playa)
        elif (i==2):
            launch.launch_wave_around_unit("BadGuys","aera","kyta","default",2,100,1000,playa)
    def EndMission (self):
        if (self.visited[0] and self.visited[1] and self.visited[2]):
            #success (change debrief maybe?)
            return ("vega_sector/enyo",1)
        else:
            #failed
            return ("vega_sector/enyo",1) 
    def Execute(self):
        playa= VS.getPlayer()
        for i in range (len(self.nav)):
            if (not self.launched[i]):
                if (playa.getDistance (self.nav[i])<1000):
                    self.LaunchNav(i,playa)
                    self.launched[i]=1
            else:
                if (playa.getDistance (self.nav[i])<100):
                    self.visited[i]=1
            
        if (playa.isDocked(self.carrier) or self.carrier.isDocked(playa)):
            return self.EndMission()
        return
