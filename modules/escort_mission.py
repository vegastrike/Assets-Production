from go_to_adjacent_systems import *
from go_somewhere_significant import *
import random
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
	def __init__ (self,factionname, missiondifficulty, our_dist_from_jump, dist_from_jump, distance_from_base, creds, enemy_time, AllInThisSystem):
		Director.Mission.__init__(self);
		self.you = VS.getPlayer();
		if (AllInThisSystem==0):
			AllInThisSystem=1
		elif (AllInThisSystem==1):
			AllInThisSystem=0
		self.adjsys=go_to_adjacent_systems(self.you, AllInThisSystem)
		self.distfrombase=distance_from_base
		self.faction=factionname
		self.escortee = launch.launch_wave_around_unit(self.you.getFlightgroupName(),
							       self.you.getFactionName(),
							       faction_ships.getRandomFighter("merchant"),
							       "default",
							       1,
							       self.you.rSize(),
							       2.0*self.you.rSize(),
							       self.you,
							       "")
		self.escortee.setFactionName(factionname)
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
		self.you.setFgDirective('F')
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
			self.adjsys=go_somewhere_significant (self.you,1,self.distfrombase,self.difficulty<=1,self.faction)
			self.adjsys.Print ("You must escort your starship to the %s","defend","docked around the %s", 0)
		else:
			self.you.addCredits(self.creds)
			VS.IOmessage (0,"escort",self.mplay,"#00ff00Excellent work! You have completed this mission!")
			VS.terminateMission(1)
