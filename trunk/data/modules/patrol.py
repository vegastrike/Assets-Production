from go_to_adjacent_systems import *
import vsrandom
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import quest
import Director
class patrol (Director.Mission):
    def __init__ (self,numsystemsaway, num_significants_to_patrol, distance_from_base, creds, jumps=(), donevar=''):
          Director.Mission.__init__(self)
          self.donevar=donevar
          self.jnum=0
          self.cred=creds
	  self.patrolpoints = []
          self.objectives = []
	  self.distance = distance_from_base
	  self.you = VS.getPlayer()
          self.quantity=num_significants_to_patrol
          name = self.you.getName ()
          self.mplay=universe.getMessagePlayer(self.you)
	  VS.IOmessage (0,"patrol",self.mplay,"Greetings, %s. You must patrol a system for us :" % name)
          self.adjsys = go_to_adjacent_systems(self.you,numsystemsaway,jumps)
          self.adjsys.Print("From the %s system,","Carefully go to %s.","You should shortly arrive in the %s: patrol it.","patrol",1)
          
    def SuccessMission (self):
        self.you.addCredits (self.cred)
        if self.donevar!='':
            quest.removeQuest(self.you.isPlayerStarship(),self.donevar,1)
        VS.IOmessage (0,"computer",self.mplay,"[Computer] Transmitting Data..")
        VS.IOmessage (0,"patrol",self.mplay,"Thank you! Patrol Complete.")
        VS.IOmessage (0,"patrol",self.mplay,"We have credited your account.")
        VS.terminateMission(1)
        
    def GeneratePatrolList (self):
        VS.IOmessage (0,"patrol",self.mplay,"You must get within %f klicks of" % self.distance)
        count=self.quantity*2
        str=""
        while (self.quantity>0 and count > 0):
            count -= 1
	    sig = unit.getSignificant (vsrandom.randrange (0,128),0,0)
            if (not sig.isNull()):
                if (not (sig in self.patrolpoints)):
                    self.patrolpoints += [sig]
                    self.quantity=self.quantity-1
                    fac =sig.getFactionName()
                    nam =sig.getName ()
                    if (fac!="neutral"):
                        obj=VS.addObjective ("Scan %s's %s"% (fac,nam))
                        VS.IOmessage (0,"patrol",self.mplay,"%s owned %s " % (fac,nam))
                    else:
                        if (sig.isPlanet()):
                            if (sig.isJumppoint()):
                                obj=VS.addObjective ("Scan Jumppoint %s" % nam)
                            else:
                                obj=VS.addObjective ("Scan Planet %s" % nam)
                        else:
                            obj=VS.addObjective ("Scan Natural Phenomenon: %s" % nam)
                        VS.IOmessage (0,"patrol",self.mplay,"The object %s " % nam) 
                    VS.setOwner(int(obj),self.you)
                    VS.setCompleteness(int(obj),-1.0)
                    self.objectives+=[int(obj)]
                    
        self.quantity=0

    def DeletePatrolPoint (self,num,nam):
        VS.IOmessage (0,"patrol",self.mplay,"[Computer] %s scanned, data saved..."%nam)
        VS.setCompleteness(self.objectives[self.jnum],1.0)
        del self.objectives[self.jnum]        
        del self.patrolpoints[self.jnum]
    def FinishedPatrol (self):
        if (self.jnum<len(self.patrolpoints)):
	    jpoint =self.patrolpoints[self.jnum]
            if (jpoint.isNull()):
                self.DeletePatrolPoint(self.jnum,"Debris")
            else:
	      if (self.you.getSignificantDistance (jpoint)<self.distance):
                  self.DeletePatrolPoint(self.jnum,jpoint.getName())
              else:
                  self.jnum+=1                  
        else:
	    self.jnum=0
        return (len(self.patrolpoints)==0)
    def Execute (self):
        if (self.you.isNull()):
            VS.terminateMission(0)
            return            
        if (self.adjsys.Execute()):
            if (self.quantity>0):
		self.GeneratePatrolList ()
            else:
		if (self.FinishedPatrol()):
                    self.SuccessMission()

    def initbriefing(self):
        print "ending briefing"                
    def loopbriefing(self):
        print "loop briefing"
        Briefing.terminate();
    def endbriefing(self):
        print "ending briefing"   
def initrandom (minsysaway,maxsysaway,minsigtopatrol,maxsigtopatrol,mincred,maxcred):
    nsys = vsrandom.randrange (minsysaway, maxsysaway)
    nsig = vsrandom.randrange (minsigtopatrol, maxsigtopatrol)
    return patrol (nsys, nsig,vsrandom.randrange(100.0,300.0),(1+nsys*0.5)*nsig*vsrandom.randrange (mincred,maxcred))