import universe
from go_to_adjacent_systems import go_to_adjacent_systems
from go_somewhere_significant import go_somewhere_significant
import vsrandom
import launch
import faction_ships
import Director
import Briefing
import unit
import VS
import quest
class bounty (Director.Mission):
	def SetVar (self,val):
	  if (self.var_to_set!=''):
	    quest.removeQuest (self.you.isPlayerStarship(),self.var_to_set,val)
	def __init__ (self,minnumsystemsaway, maxnumsystemsaway, creds, run_away, shipdifficulty, tempfaction,jumps=(),var_to_set=''):
	  Director.Mission.__init__ (self)
	  run_away=0
	  self.newship=""
	  self.mplay="all"
	  self.var_to_set = var_to_set
	  self.istarget=0
	  self.obj=0
	  self.curiter=0
	  self.arrived=0
	  self.faction = tempfaction	  
	  self.difficulty = shipdifficulty
	  self.runaway=run_away
	  self.cred=creds
	  mysys=VS.getSystemFile()
	  sysfile = VS.getSystemFile()
	  self.you=VS.getPlayer()
	  self.enemy=VS.Unit()
	  self.adjsys=go_to_adjacent_systems (self.you,vsrandom.randrange(minnumsystemsaway,maxnumsystemsaway+1),jumps)
	  self.mplay=universe.getMessagePlayer(self.you)
	  if (self.you):
	    VS.IOmessage (0,"bounty mission",self.mplay,"Good Day, %s. Your mission is as follows:" % (self.you.getName()))
	    self.adjsys.Print("You should start in the system named %s","Then jump to %s","Finally, jump to %s, your final destination","bounty mission",1)
	    VS.IOmessage (1,"bounty mission",self.mplay,"Once there, you must destroy a %s unit." % (self.faction))
	    VS.IOmessage (2,"bounty mission",self.mplay,"You will then %.2f credits as your reward (if you survive)." % (self.cred))
	    VS.IOmessage (3,"bounty mission",self.mplay,"#00ff00Good luck!")
	  else:
	    print "aboritng bounty constructor..."
	    VS.terminateMission (0)
	
	def Win (self,un,terminate):
	  self.SetVar(1)
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00Excellent work pilot.")
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00You have been rewarded for your effort as agreed.")
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00Your contribution to the war effort will be remembered.")
	  un.addCredits(self.cred)
	  if (terminate):
	    print "you win bounty mission!"
	    VS.terminateMission(1)
	  
	def Lose (self,terminate):
	  VS.IOmessage(0,"bounty mission",self.mplay,"#ff0000You have failed this mission and will not be rewarded.")
	  self.SetVar(-1)
	  if (terminate):
	    print "lose bounty mission"
	    VS.terminateMission(0)
	  
	def Execute (self):
	  isSig=0
	  if (self.you.isNull()):
	    self.Lose (1)
	    return
	  if (self.arrived==2):
	    if (not self.runaway):
	      if (not self.istarget):
		if (self.enemy):
		  curun=VS.getUnit(self.curiter)
		  self.curiter+=1
		  if (curun==self.enemy):
		    self.enemy.SetTarget(self.you)
		  elif (curun.isNull()):
		    self.curiter=0
	    if (self.enemy.isNull()):
	      self.Win(self.you,1)
	      return
	  elif (self.arrived==1):
	    significant=self.adjsys.SignificantUnit()
	    if (significant.isNull ()):
	      print "sig null"
	      VS.terminateMission(0)
	      return
	    else:
	      if (self.you.getSignificantDistance(significant)<10000.0):
		if (self.newship==""):
		  self.newship=faction_ships.getRandomFighter(self.faction)
		self.enemy=launch.launch_wave_around_unit("Shadow",self.faction,self.newship,"default",1+self.difficulty,3000.0,4000.0,significant)
		self.obj=VS.addObjective("Destroy the Shadow %s ship." % (self.enemy.getName ()))
		if (self.enemy):
		  if (self.runaway):
		    self.enemy.SetTarget(significant) #CHANGE TO SetTarget ==>NOT setTarget<==
		    self.enemy.ActivateJumpDrive(0)
		  self.arrived=2
		else:
		  print "enemy null"
		  VS.terminateMission(0)
		  return
	  else:
	    if (self.adjsys.Execute()):
	      self.arrived=1
	      self.newship=faction_ships.getRandomFighter(self.faction)
	      self.adjsys=go_somewhere_significant(self.you,0,500)
	      localdestination=self.adjsys.SignificantUnit().getName()
	      VS.IOmessage (3,"bounty mission",self.mplay,"You must destroy the %s unit in this system." % (self.newship))
	      if (self.runaway):	#ADD OTHER JUMPING IF STATEMENT CODE HERE
	        VS.IOmessage (4,"bounty mission",self.mplay,"He is running towards the jump point.  Catch him!")
	        VS.IOmessage (5,"bounty mission",self.mplay,"he is going to %s" % (localdestination))
	      else:
	        VS.IOmessage (4,"bounty mission",self.mplay,"Scanners are picking up a metallic object!")
	        VS.IOmessage (5,"bounty mission",self.mplay,"Coordinates appear near %s" % (localdestination))
	
	def initbriefing(self):
		print "ending briefing"                
	
	def loopbriefing(self):
		print "loop briefing"
		Briefing.terminate();
	
	def endbriefing(self):
		print "ending briefing"        	  
	

def initrandom (minns, maxns, credsmin, credsmax, run_away, minshipdifficulty, maxshipdifficulty,jumps=(),var_to_set=''):
  you=VS.getPlayer()
  tempfaction='aera'
  if (you):
    name = you.getFactionName ()
    factionname=vsrandom.randrange(0,faction_ships.getMaxFactions())
    tempfaction=faction_ships.intToFaction(factionname)
    i=0
    while ((name==tempfaction or name=="unknown") and i<10):
      factionname=vsrandom.randrange(0,faction_ships.getMaxFactions())
      tempfaction=faction_ships.intToFaction(factionname)
      i+=1
    sd = vsrandom.random()*(maxshipdifficulty-minshipdifficulty)+minshipdifficulty
    return bounty (minns,maxns,(1.0+(sd*0.5))*(vsrandom.random ()*(credsmax-credsmin)+credsmin),run_away,sd,tempfaction,jumps,var_to_set)
  else:
    print "aborting bounty initrandom"
    VS.terminateMission(0)
  
