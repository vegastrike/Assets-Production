import VS
import sys
import random
from Vector import *
maxspeed=43
def isCar(c):
	return c.getName()=='car'

class TrafficAI(VS.PythonAI):
    def restoreCruisingSpeed(self,speed):
	self.MatchLinearVelocity(0,(0,0,speed),0,1)
        self.AddReplaceLastOrder(1)
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
		if (isCar (un)):
			posdiff=SafeNorm(Sub (un.Position(),parent.Position())) 			#look 1 second ahead
			distInOneSec = Dot (Sub(parent.GetVelocity(),un.GetVelocity()),posdiff)
			if (distInOneSec<un.getDistance(parent)):
				self.restoreCruisingSpeed(0)
				self.stopping=1
				
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
