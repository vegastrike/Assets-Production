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
import quest_contraband_truck


class waitjump(VS.PythonAI):

	def init(self,un):
		self.XMLScript ("++flystraight.xml")
		self.AddReplaceLastOrder(1)
		self.timer = 0
		self.got_target = 0


	def Execute(self):
		VS.PythonAI.Execute(self);
		if quest_contraband_truck.truck_exit == 1:
			if self.got_target == 0:
				self.trucktarget = ((self.GetParent()).GetTarget())
				self.GetParent().SetTarget(universe.getRandomJumppoint())
				self.trucktarget = (self.GetParent()).GetTarget()
				self.got_target = 1
			self.trucktarget_locat = self.trucktarget.Position()
# starts him afterburning to target
			self.FaceTarget(1)
			self.AddReplaceLastOrder(1)

			if self.timer == 0:
				self.timer = VS.GetGameTime()
				print "Timer Set"
			elif self.timer + 5 < VS.GetGameTime():
				self.MoveTo(self.trucktarget_locat,1)
				self.AddReplaceLastOrder(1)
				self.GetParent().ActivateJumpDrive(1)
#			elif self.timer + 60 < VS.GetGameTime():
# gets him to auto to the jump and jump out
#				self.GetParent().ActivateJumpDrive(1)
			return 1

		return 1
hi1 = waitjump()
print 'AI creation successful'
hi1 = 0

