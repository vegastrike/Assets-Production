from go_to_adjacent_systems import *
from go_somewhere_significant import *
import vsrandom
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import Director
import quest
class defend (Director.Mission):
    def __init__ (self,factionname,numsystemsaway, enemyquantity, distance_from_base, escape_distance, creds, defendthis, defend_base,protectivefactionname='',jumps=(),var_to_set=''):
          Director.Mission.__init__(self)
          self.dedicatedattack=vsrandom.randrange(0,2)
          self.arrived=0
          self.protectivefaction = protectivefactionname
          self.var_to_set=var_to_set
          self.quantity=0
          self.mplay="all"
	  self.defendbase = defend_base	  
	  self.attackers = []
          self.objective= 0
	  self.targetiter = 0
	  self.ship_check_count=0
	  self.defend = defendthis
          self.defend_base = defend_base
          self.faction = factionname
	  self.escdist = escape_distance
          minsigdist=unit.minimumSigDistApart()
          if (minsigdist*.5<self.escdist):
              self.escdist = minsigdist
	  self.cred=creds
	  self.quantity=enemyquantity
	  self.distance_from_base=distance_from_base
          self.defendee=VS.Unit()
          self.difficulty=1
	  self.you=VS.getPlayer()
          name = self.you.getName ()
          self.mplay=universe.getMessagePlayer(self.you)
          self.adjsys = go_to_adjacent_systems(self.you,numsystemsaway,jumps)  
	  VS.IOmessage (0,"defend",self.mplay,"Good Day, %s. Your mission is as follows:" % name)
          self.adjsys.Print("You are in the %s system,","Proceed swiftly to %s.","Your arrival point is %s.","defend",1)
	  VS.IOmessage (2,"defend",self.mplay,"And there eliminate any %s starships at a point."  % self.faction)
    def SetVarValue (self,value):
        if (self.var_to_set!=''):
            quest.removeQuest (self.you.isPlayerStarship(),self.var_to_set,value)
    def SuccessMission (self):
        self.you.addCredits (self.cred)
        self.SetVarValue(1)
        VS.IOmessage(0,"defend",self.mplay,"Excellent work pilot! Your effort has thwarted the foe!")
        VS.IOmessage(0,"defend",self.mplay,"You have been rewarded for your effort as agreed.")
        VS.terminateMission(1)
    def FailMission (self):
        self.you.addCredits (-self.cred)
        self.SetVarValue(-1)
        VS.IOmessage (0,"defend",self.mplay,"You Allowed the base you were to protect to be destroyed.")
        VS.IOmessage (0,"defend",self.mplay,"You are a failure to your race!")
        VS.IOmessage (1,"defend",self.mplay,"We have contacted your bank and informed them of your failure to deliver on credit. They have removed a number of your credits for this inconvenience. Let this serve as a lesson.")
        _std.terminateMission(0)
    def NoEnemiesInArea (self,jp):
        if (self.adjsys.DestinationSystem()!=VS.getSystemFile()):
	    return 0
        un= VS.getUnit (self.ship_check_count)
        self.ship_check_count+=1
        if (un.isNull ()):
            VS.setCompleteness(self.objective,1.0)
	    return 1
        
        if (un!=self.you):
            if (un.getFactionName()==self.faction): 
                if (un.getSignificantDistance (jp)<self.escdist):
                    if (un.getFlightgroupName()!="Base"):
                        VS.setObjective(self.objective,"Destroy the %s"%un.getName())
                        self.ship_check_count=0
        return 0
	
    def GenerateEnemies (self,jp,you):
        VS.IOmessage (0,"defend",self.mplay,"Eliminate all %s ships here" % self.faction)
        if (self.defend):
            VS.IOmessage (0,"defend",self.mplay,"You must protect %s." % jp.getName ())
        count=0
        VS.addObjective ("Protect %s from %s" % (jp.getName(),self.faction))
        self.objective = VS.addObjective ("Destroy All %s Hostiles" % self.faction)
        VS.setCompleteness(self.objective,-1.0)

        while (count<self.quantity):
	    launched = launch.launch_wave_around_unit ("Shadow",self.faction,faction_ships.getRandomFighter(self.faction),"default",1,2000.0,4500.0,you,'')
            if (self.defend):
                launched.SetTarget (jp)
	    else:
                launched.SetTarget (you)
	    launched.setFgDirective('B')
            self.attackers += [ launched ]
	    count+=1
        self.quantity=0
    def Execute (self):
        if (self.you.isNull() or (self.arrived and self.defendee.isNull())):
            VS.IOmessage (0,"defend",self.mplay,"#ff0000You were unable to arrive in time to help. Mission failed.")
            self.SetVarValue(-1)
            VS.terminateMission(0)
            return   
        if (not self.adjsys.Execute()):
            return
        if (not self.arrived):
            self.arrived=1
            tempfaction=''
            if (self.defend_base):
                tempfaction=self.protectivefaction
                if (tempfaction==''):
                    tempfaction = faction_ships.get_enemy_of(self.faction)
            self.adjsys=go_somewhere_significant (self.you,self.defend,self.distance_from_base,self.defend or self.defend_base,tempfaction)
            self.adjsys.Print ("You must visit the %s","defend","docked around the %s", 0)
            self.defendee=self.adjsys.SignificantUnit()
        else:
            if (self.defendee.isNull ()):
		if (self.defend):
                    self.FailMission(you)
		else:
                    self.SuccessMission()
                    return
            else:
		if (self.quantity>0):
                    self.GenerateEnemies (self.defendee,self.you)
                if (self.ship_check_count==0 and self.dedicatedattack):
                    if (self.targetiter>=len(self.attackers)):
                        self.targetiter=0
                    else:
                        un =  self.attackers[self.targetiter]
                        if (not un.isNull()):
                            if (self.defend):#		  if (not un.isNull())
                                un.SetTarget (self.defendee)
                            else:
                                un.SetTarget (self.you)
                        self.targetiter=self.targetiter+1
                if (self.NoEnemiesInArea (self.defendee)):
                    self.SuccessMission()
    def initbriefing(self):
        print "ending briefing"                
    def loopbriefing(self):
        print "loop briefing"
        Briefing.terminate();
    def endbriefing(self):
        print "ending briefing"        
		
def initrandom(factionname,numsysaway,minenquant,maxenquant,credperen,defendit,defend_base,p_faction='',jumps=(),var_to_set=''):
    enq=vsrandom.randrange(minenquant,maxenquant)
    return defend(factionname,numsysaway,enq,8000.0,100000.0,enq*credperen,defendit,defend_base,p_faction,jumps,var_to_set)
