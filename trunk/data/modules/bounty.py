import universe
from go_to_adjacent_systems import go_to_adjacent_systems
from go_somewhere_significant import go_somewhere_significant
import random
import launch
import faction_ships
import Director
import Briefing
import unit
import VS

class bounty (Director.Mission):

	def __init__ (self,minnumsystemsaway, maxnumsystemsaway, creds, run_away, shipdifficulty, tempfaction):
	  Director.Mission.__init__ ()
	  self.newship=""
	  self.mplay="all"
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
	  self.significant=VS.Unit()
	  self.adjsys=go_to_adjacent_systems (self.you,random.randrange(minnumsystemsaway,maxnumsystemsaway+1))
	  self.mplay=universe.getMessagePlayer(self.you)
	  if (you):
	    VS.IOmessage (0,"bounty mission",self.mplay,"Good Day, %s. Your mission is as follows:" % (you.getName()))
	    self.adjsys.Print("You should start in the system named %s","Then jump to %s","Finally, jump to %s, your final destination","bounty mission",1)
	    VS.IOmessage (2,"bounty mission",self.mplay,"Once there, you must destroy a %s unit." % (faction))
	    VS.IOmessage (3,"bounty mission",self.mplay,"You will then %.2f credits as your reward (if you survive)." % (self.cred))
	    VS.IOmessage (4,"bounty mission",self.mplay,"#00ff00Good luck!")
	  else:
	    print "aboritng bounty constructor..."
	    VS.terminateMission (0)
	
	def Win (self,un,terminate):
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00Excellent work pilot.")
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00You have been rewarded for your effort as agreed.")
	  VS.IOmessage (0,"bounty mission",self.mplay,"#00ff00Your contribution to the war effort will be remembered.")
	  un.addCredits(self.cred)
	  if (terminate):
	    print "you win bounty mission!"
	    VS.terminateMission(1)
	  
	def Lose (self,terminate):
	  VS.IOmessage(0,"bounty mission",self.mplay,"#ff0000You have failed this mission and will not be rewarded.")
	  if (terminate):
	    print "lose bounty mission"
	    VS.terminateMission(0)
	  
	def loop (self):
	  isSig=0
	  if (self.you.isNull()):
	    self.Lose (1)
	    return
	  if (self.arrived==3):
	    if (not self.istarget):
	      curun=VS.getUnit(self.curiter)
	      if (self.enemy):
		if (curun==self.enemy):
		  self.enemy.setTarget(self.you)
	      self.curiter+=1
	    if (you.isNull()):
	      self.Lose(1)
	      return
	    if (self.enemy.isNull()):
	      self.Win(you,1)
	      return
	  elif (self.arrived==2):
	    if (VS.getSystemFile()==self.adjsys.DestinationSystem()):
	      self.arrived=3
	    else:
	      VS.ResetTimeCompression()
	    if (self.you.isNull()):
	      Lose(1)
	      return
	    if (self.enemy.isNull()):
	      Win(you,1)
	      return
	  elif (self.arrived==1):
	    significant=self.significant
	    if (significant.isNull ()):
	      print "sig null"
	      VS.terminateMission(0)
	    else:
	      if (you.getSignificantDistance(significant)<10000.0):
		if (self.newship==""):
		  self.newship=faction_ships.getRandomFighter(faction)
		self.enemy=launch.launch_wave_around_unit("Base",self.faction,self.newship,"default",1+self.difficulty,3000.0,4000.0,self.significant)
		if (self.enemy):
		  if (runaway):
		    self.enemy.setTarget(significant)
		    self.enemy.Jump()
		    self.arrived=2
		  else:
		    self.arrived=3
	  else:
	    if (self.adjsys.Execute()):
	      self.arrived=1
	      self.newship=faction_ships.getRandomFighter(faction)
	      localdestination=self.significant.getName()
	      self.adjsys=go_somewhere_significant(self.you,0,500)
	      VS.IOmessage (0,"bounty mission",self.mplay,"You must destroy the %s unit in this system." % (self.newship))
	      self.obj=VS.addObjective("Destroy the %s unit" % (self.newship))
	      if (runaway):	#ADD OTHER JUMPING IF STATEMENT CODE HERE
	        VS.IOmessage (3,"bounty mission",self.mplay,"He is running towards the jump point.  Catch him!")
	        VS.IOmessage (4,"bounty mission",self.mplay,"he is going to %s" % (localdestination))
	      else:
	        VS.IOmessage (3,"bounty mission",self.mplay,"Scanners are picking up a metallic object!")
	        VS.IOmessage (4,"bounty mission",self.mplay,"Coordinates appear near %s" % (localdestination))
	
	def initbriefing():
		print "ending briefing"                
	
	def loopbriefing():
		print "loop briefing"
		Briefing.terminate();
	
	def endbriefing():
		print "ending briefing"        	  
	

def initrandom (minns, maxns, credsmin, credsmax, run_away, minshipdifficulty, maxshipdifficulty):
  you=VS.getPlayer()
  tempfaction
  if (you):
    name = you.getFaction ()
    factionname=random.randrange(0,faction_ships.getMaxFactions())
    tempfaction=faction_ships.intToFaction(factionname)
    i=0
    while (name==tempfaction and i<10):
      factionname=random.randrange(0,faction_ships.getMaxFactions())
      tempfaction=faction_ships.intToFaction(factionname)
      i+=1
    sd = random.random()*(maxshipdifficulty-minshipdifficulty)+minshipdifficulty
    return bounty (minns,maxns,(1.0+(sd*0.5))*(random.random ()*(credsmax-credsmin)+credsmin),run_away,sd,tempfaction)
  else:
    print "aborting bounty initrandom"
    VS.terminateMission(0)
  
