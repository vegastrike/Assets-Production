import VS
import sys
import random
from Vector import *
import car_lib
maxspeed=43

class TrafficAI(VS.PythonAI):
    def restoreCruisingSpeed(self,speed):
	self.MatchLinearVelocity(0,(0,0,speed),0,1)
        self.AddReplaceLastOrder(1)
	self.GetParent().setSpeed(speed)
    def init(self,un):
	self.shipiter=0;
	self.speed = random.uniform (0,maxspeed);
	print 'self.speed'
	print self.speed
	self.stopping=0
	self.restoreCruisingSpeed(self.speed)
    def Execute(self):
        VS.PythonAI.Execute(self)
	un = VS.getUnit (self.shipiter);
	parent = self.GetParent()
	if (parent and un):
		if (parent!=un):
			if (car_lib.isCar (un)):
				posdiff=SafeNorm(Sub (un.Position(),parent.Position())) 			#look 1 second ahead
#				distInOneSec = Dot (Sub(parent.GetVelocity(),un.GetVelocity()),posdiff)
				distInOneSec = Dot (Sub(parent.GetVelocity(),un.GetVelocity()),posdiff)
				if (distInOneSec>un.getDistance(parent) and Dot (posdiff,un.GetOrientation()[2])>0):
#					print "%s too close to %s \n" % (parent.getName(),un.getName())
#					print distInOneSec
#					print un.getDistance (parent)
					self.restoreCruisingSpeed(0)
					self.stopping=1
					self.shipiter=-1 #-1 + 1 =0
				
		self.shipiter +=1
	else:
		if (self.stopping):
			if (parent):
				self.stopping=0
				self.restoreCruisingSpeed(self.speed)
		self.shipiter=0
        return
hi1 = TrafficAI()
print 'AI creation successful'
hi1 = 0
#: 1.7; previous revision: 1.6
