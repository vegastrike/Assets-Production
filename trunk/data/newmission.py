import pickle
import Director
class picklable:
    def __init__(self,a):
        self.a=0
    def Execute(self):
        self.a = self.a+1;
        print self.a
class MyMission(Director.Mission):
    def begin (self):
        self.pick = picklable(100)
    def Execute(self):
        self.pick.Execute()
    def Pickle (self):
        print 'prepare to fire the primary pickle'
        return 'newmission.py\n'+pickle.dumps(self.pick)
    def UnPickle(self,s):
        print 'prepare to load the primary pickle'
        self.pick = pickle.loads(s)
        print self.pick.a
tmpmission = MyMission()
tmpmission.begin()
tmpmission.Execute()
tmpmission.Execute()
tmpmission.Execute()
tmpmission=0

