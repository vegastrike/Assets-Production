import VS
import Director
def isCar(c):
	return c.getName()=='car'

class Environment(Director.Mission):
	def __init__ (self):
		Director.Mission.__init__(self)
		print 'initing'
		self.iter=0
	def OldeExecute(self):
		un = VS.getUnit (self.iter)
		if (un):
			if (isCar(un)):
				self.ApplyEnvironment (un)
			self.iter+=1
		else:
			self.iter=0
	def Execute(self):
		iter = VS.getUnitList ()
		un = iter.current()
		while (un):
			if (isCar(un)):
				self.ApplyEnvironment (un)
			iter.advance()
			un = iter.current()
	def ApplyEnvironment (self,un):
		pos = un.Position()
		vel = un.GetVelocity()
		if (pos[1]!=0):
			pos=(pos[0],0,pos[2])
			un.SetCurPosition(pos)
		if (vel[1]!=0):
			vel = (vel[0],0,vel[2])
			un.SetVelocity(vel)
