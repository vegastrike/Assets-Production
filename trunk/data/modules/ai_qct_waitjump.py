import VS
import sys
import quest
import Vector
import unit
import vsrandom
import save_util
import faction_ships
import universe
import launch
import tuples_fg
import quest_contraband_truck


class waitjump(VS.PythonAI):



	def getJumppoint(self,target,ship):
		if (target.isJumppoint()):
			ship.SetTarget(target)
		else:
			target = VS.getUnit(self.count)
			self.count = self.count + 1
			self.getJumppoint(target,ship)





	def init(self,un):
		self.XMLScript ("++flystraight.xml")
		self.AddReplaceLastOrder(1)
		self.timer = 0
#		global ai_qct_waitjump.truck_exit
#		ai_qct_waitjump.truck_exit = 0


	def Execute(self):
		VS.PythonAI.Execute(self);
		if quest_contraband_truck.truck_exit == 1:
			self.trucktarget = ((self.GetParent()).GetTarget())
			self.count = 0
			self.getJumppoint(self.trucktarget,self.GetParent())
# starts him afterburning to target
			self.GetParent().MoveTo(self.trucktarget,1)
#			self.GetParent().AddReplaceLastOrder(1)
			if self.timer == 0:
				self.timer = VS.GetGameTime()
				print "Timer Set"
			elif self.timer + 20 < VS.GetGameTime():
# gets him to auto to the jump and jump out
				self.GetParent().ActivateJumpDrive(0)
				self.GetParent().AddReplaceLastOrder(1)
				print "should be go for good!................now!!!"
			print "should be go................now!!!"
			sys.stdout.write('Should be working...')
#			sys.stdout.write('h')
			return 1
		return 1
hi1 = waitjump()
print 'AI creation successful'
hi1 = 0
#: 1.7; previous revision: 1.6
