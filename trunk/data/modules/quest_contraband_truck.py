import quest
import Vector
import VS
import unit
import vsrandom
import save_util
import faction_ships
import universe
import launch
import tuples_fg


class quest_contraband_truck_factory (quest.quest_factory):
	def __init__ (self):
		quest.quest_factory.__init__ (self,"quest_contraband_truck")
	def create (self):
		return quest_contraband_truck()
	def precondition(self,playernum):
		return 1

class quest_contraband_truck (quest.quest):


	def do_aera_count(self):
		self.aera_count=0
		for i in self.aera_specopp:
			if (i):
				self.aera_count = self.aera_count + 1
		return self.aera_count

# This stuff should now be done in the ai
#	def getJumppoint(self,target,ship):
#		if (target.isJumppoint()):
#			ship.SetTarget(target)
#
#		else:
#			target = VS.getUnit(self.count)
#			self.count = self.count + 1
#			self.getJumppoint(target,ship)
		

	def aera_attack(self):
		self.aera_specopp[self.count].SetTarget(self.playa)
		self.aera_specopp[self.count].setFgDirective('A')

	def mission_fail(self):
		print "mission failed"
		VS.IOmessage (0,"game","news","AERAN WARP CORE EXPLODES: \n GNN reports the explosion of a warp core in Klondike system today.  The unstable core was apparently being smuggled through the system by cloaked Aeran ships.  When merchants entered the system, they took the apparently unguarded cargo pod as scrap and approached.  It exploded soon after.  Aeran and merchant ships presumed destroyed.  Our informant wishes to remain anonymous.")
		print "mission terminating"

#		VS.terminateMission(False)
		print "mission terminated"
		return 0

	def mission_success(self):
		self.confed_cruiser=launch.launch_wave_around_unit("Sonorous","confed","corvette","default",1,4000,8000,self.cargo_container)
		self.confed_epeels=launch.launch_wave_around_unit("Sonorous E1","confed","epeellcat","default",5,1000,1000,self.confed_cruiser)
		VS.IOmessage (3,"game","all","Attention Merchant Vessel!")
		VS.IOmessage (4,"game","all","Under Code 1530 of the Trade Practices Charter, we take posessoin of this cargo pod.")
		VS.IOmessage (6,"game","all","Please move away or we will remove you.")
		self.jumpout = 0
#		VS.terminateMission(True)
		return 0





	def setup_all(self):
			print
			print "Truck Launched"
			print
			self.truck_pirate=launch.launch_wave_around_unit("Smuggler","pirate","truck","modules/ai_qct_waitjump.py",1,3000,5000,self.playa)


			print
			print "Scrap Released"
			print

			self.cargo_container=launch.launch_wave_around_unit("Scrap","aera","cargo","default",1,7000,5000,self.playa)


			print
			print "Aera Released"
			print

			self.numaera = 4
			self.aera_specopp = ()
			for i in range(self.numaera):
#				self.aera_specopp = self.aera_specopp + (VS.launch("Aera/SpecOpp","dagger","aera","unit",
#                "default",1,1,self.cargo_container.Position() + (0,3000,5000),""),)
				self.aera_specopp = self.aera_specopp + (launch.launch_wave_around_unit("Aera/SpecOpp","aera","dagger","default",1,2000,4000,self.playa),)

			print
			print "Aera Cloaked"
			print
			tuples_fg.fgCloak(1,self.aera_specopp)

			self.repeat_more = 1
			self.repeat_less = 1
			self.repeat_end1 = 1
			self.repeat_end2 = 1
			self.timer1 = 0
			self.jumpout = 0
			global truck_exit
			truck_exit = 0

	def start_destruction(self):
		if self.repeat_end2 == 2:
			if self.timer1 == 0:
				self.timer1 = VS.GetGameTime()
			self.cargo_container.Split(75)
			VS.playAnimation("explosion_wave.ani",self.cargo_container.Position(),300)
			VS.playAnimation("explosion_wave.ani",self.cargo_container.Position(),100)
			VS.playAnimation("explosion_wave.ani",self.cargo_container.Position(),700)
			VS.playAnimation("explosion_wave.ani",self.cargo_container.Position(),1000)
			VS.playSound("sfx43.wav",self.cargo_container.Position(),self.cargo_container.GetVelocity())
			VS.playSound("Flux.wav",self.cargo_container.Position(),self.cargo_container.GetVelocity())
			VS.playSound("electricity.wav",self.cargo_container.Position(),self.cargo_container.GetVelocity())

			print "adding particle"
			VS.addParticle(self.cargo_container.Position(),self.cargo_container.GetVelocity(),(1,.2,.2))
			print "added particle"
			tuples_fg.fgAttackTgt(self.aera_specopp,self.playa)

#			self.count = 0
#			for i in range(self.numaera):
#				self.aera_attack()
#				self.count = self.count + 1
			print "begin msgs"
			VS.IOmessage (0,"game","all","[Translate: Aernoss -> Englysh] Turn your attention <surprise> Entity/self triggered item warp core!")
			VS.IOmessage (5,"game","all","[Translate: Aernoss -> Englysh] <fear, anxiety, anger> Filthy human procreate entity/self!")
			VS.IOmessage (12,"game","all","[Translate: Aernoss -> Englysh] Group leave fast danger avo...")
			print "ended msgs"
			self.jumpout = 1
			self.repeat_end2 = 0
			print "ended start_destruction"

	def end_destruction(self):
		print "testing timer"
		if (self.timer1 + 12) <= VS.GetGameTime():

				print "playing sounds"
				VS.playSound("sfx43.wav",self.playa.Position(),self.playa.GetVelocity())
				VS.playSound("Flux.wav",self.playa.Position(),self.playa.GetVelocity())
				VS.playSound("electricity.wav",self.playa.Position(),self.playa.GetVelocity())

				print "attempting the jump"

				tuples_fg.fgJumpTo(self.aera_specopp,"gemini_sector/pestilence")

				print "attempted the jump"

#				self.count = 0
#				for i in range(self.numaera):
#					self.aera_specopp[self.count].JumpTo("gemini_sector/pestilence")
#					self.aera_attack()
#					self.count = self.count + 1




				self.playa.JumpTo("gemini_sector/pestilence")
				print "jumped playa"
				VS.IOmessage (0,"game","all","[Translate: Aernoss -> Englysh] ...id")
				VS.IOmessage (5,"game","all","[Translate: Aernoss -> Englysh] <untranslatable> section of excretement <untranslatable> human <untranslatable> genitalia <untranslatable> fire <untranslatable> nice day.")

				VS.IOmessage (0,"game","all","[Translate: Aernoss -> Englysh] Flee smart to go entity/self <conditional> life value.")

#				VS.IOmessage (1,"game","all","Oh no, what that idiot has done!")
				print "done all but fail"
				self.mission_fail()













	def __init__ (self):
		self.playa = VS.getPlayer()
		if (self.playa):
			self.setup_all()
			VS.IOmessage (3,"game","all","[Computer] Scans show several peices of scrap in this system.  May contain valuable cargo.")



	def Execute (self):
		if (self.playa):


			if self.cargo_container.getMinDis(self.playa.Position()) < 2500:
				if self.repeat_end2 == 1:
					VS.IOmessage (3,"game","all","[Computer] Warning! Annomalous warp echos detected.")
					print
					print "Aera Un-loaked"
					print
					tuples_fg.fgCloak(0,self.aera_specopp)
#					self.count = 0
#					for i in range(self.numaera):
#						self.aera_specopp[self.count].Cloak(0)
#						self.count = self.count + 1
					self.repeat_end2 = 2

			if self.cargo_container.getMinDis(self.playa.Position()) < 1000:
				self.start_destruction()

			if self.jumpout == 1:
				self.end_destruction()


			if tuples_fg.fgisNull(self.aera_specopp):
				VS.IOmessage (0,"game","all","[Computer] Warning! Annomalous fucking python detected.")



			if self.truck_pirate.getMinDis(self.playa.Position()) < 200:
				if self.repeat_end1 == 2:
					VS.IOmessage (0,"game","all","I am with Confed Special Service.")
					VS.IOmessage (0,"game","all","You are hampering a priority 0 operation.")
					self.confed_epeels2=launch.launch_wave_around_unit("Sonorous A3","confed","epeellcat","default",5,1000,5000,self.playa)				
					VS.IOmessage (5,"game","all","You are Terminated.")
					self.confed_epeels2.SetTarget(self.playa)
					self.confed_epeels2.setFgDirective('A')
					self.repeat_end1 = 3

			if self.truck_pirate.getMinDis(self.playa.Position()) < 1000:
				if self.repeat_end1 == 1:
					VS.IOmessage (0,"game","all","Back off mate, if you know what's good for you.")
					print "My target is..."

#					print ai_qct_waitjump.truck_exit
#					print ai_qct_waitjump().truck_exit
#					print waitjump.truck_exit
#					print waitjump().truck_exit
					truck_exit = 1
					print truck_exit

# This stuff should now be done in the ai
#					self.trucktarget = self.truck_pirate.GetTarget()
#					self.count = 0
#					self.getJumppoint(self.trucktarget,self.truck_pirate)
#					self.truck_pirate.MoveTo(self.trucktarget,1)
#					self.truck_pirate.ActivateJumpDrive(0)


					self.repeat_more = 0
					self.repeat_less = 0
					self.repeat_end1 = 2

			elif self.truck_pirate.getMinDis(self.playa.Position()) < 3000:
				if self.repeat_less == 1:
					VS.IOmessage (0,"game","all","Please stay away, we are carrying valuable cargo.")
					self.repeat_more = 1
					self.repeat_less = 0

			else:
				if self.repeat_more == 1:
					VS.IOmessage (0,"game","all","Keep your distance.")
					self.repeat_more = 0
					self.repeat_less = 1
			








#			self.makeQuestPersistent()
			return 1

