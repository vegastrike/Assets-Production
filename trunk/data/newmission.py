import Director
import cPickle;
class mymission(Director.Mission):
	def __init__(self):
		Director.Mission.__init__(self)
		self.i=0
	def Execute(self):
		self.i=self.i+1
		print self.i
	def Pickle (self):
	  print 'prepare to fire the primary pickle'
	  return 'mission/exploration/explore_universe.mission\n'+cPickle.dumps(self.i)
	def UnPickle(self,s):
	  print 'prepare to load the primary pickle'
	  self.i = cPickle.loads(s)
myobj = mymission()
