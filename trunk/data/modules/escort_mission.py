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

class escort_mission (Director.Mission):
	you=VS.Unit()
	escortee=VS.Unit()
	adjsys=0
	arrived=0
        mplay="all"
	def __init__ (self,factionname, missiondifficulty, our_dist_from_jump, dist_from_jump, distance_from_base, creds, enemy_time, numsysaway):
		Director.Mission.__init__(self);
		self.you = VS.getPlayer();
		self.adjsys=go_to_adjacent_systems(self.you, numsysaway)
		print "e"
		self.adjsys.Print("You should start in the system named %s","Then jump to %s","Finally, jump to %s, your final destination","escort mission",1)
		print "f"
		self.distfrombase=distance_from_base
		print "g"
		self.faction=factionname
		self.escortee = launch.launch_wave_around_unit("Escort",
							       self.faction,
							       faction_ships.getRandomFighter("merchant"),
							       "default",
							       1,
							       self.you.rSize(),
							       2.0*self.you.rSize(),
							       self.you,
							       "")
		print "h"
		self.escortee.setFlightgroupLeader(self.you)
		print "dd"
		self.difficulty=missiondifficulty
		self.creds = creds
	def initbriefing(self):
		print "ending briefing"                
	def loopbriefing(self):
		print "loop briefing"
		Briefing.terminate();
	def endbriefing(self):
		print "ending briefing"        
	def Execute (self):
		self.escortee.setFgDirective('F')
		self.you.setFlightgroupLeader(self.you)
		if (self.escortee.isNull()):
			VS.IOmessage (0,"escort",self.mplay,"#ff0000You were to protect your escort. Mission failed.")
			universe.punish(self.you,self.faction,self.difficulty)
			VS.terminateMission(0)
			return   
		if (not self.adjsys.Execute()):
			return
		if (not self.arrived):
			self.arrived=1
			self.adjsys=go_somewhere_significant (self.escortee,1,self.distfrombase,self.difficulty<=1,self.faction)
			self.adjsys.Print ("You must escort your starship to the %s","defend","docked around the %s", 0)
		else:
			self.you.addCredits(self.creds)
			VS.IOmessage (0,"escort",self.mplay,"#00ff00Excellent work! You have completed this mission!")
			self.escortee.setFgDirective('b')
			VS.terminateMission(1)
def initrandom (factionname,difficulty,creds,entime,numsysaway):
	return escort_mission(factionname,difficulty,6000,vsrandom.randrange(5000,7000),vsrandom.randrange(10,300),creds,entime,numsysaway)
