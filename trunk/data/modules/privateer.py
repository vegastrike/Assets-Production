from trading import trading
from random_encounters import random_encounters
from difficulty import difficulty
#from garbage_collect import garbage_collect
import Director
import Briefing
class privateer (Director.Mission):
  loops=()
  def __init__ (self,sigdis, detectiondis, gendis, minships, genships, fighterprob, enemyprob, capprob, credits_to_maximize_difficulty, capdist):#negative garbage collect dist disables that feature
    Director.Mission.__init__(self)
    self.loops=(difficulty (credits_to_maximize_difficulty),
          random_encounters (sigdis, detectiondis, gendis, minships,genships,fighterprob,enemyprob,capprob,capdist),
          trading (),
#          garbage_collect (),
          )

  def Execute(self): #this execute function should not need to be changed...
    for i in self.loops:
       i.Execute()
  def initbriefing(self):
    print "ending briefing"                
  def loopbriefing(self):
    print "loop briefing"
    Briefing.terminate();
  def endbriefing(self):
    print "ending briefing"        

#def initstarsystem():
#  random_encounters.initstarsystem() #??? that isn't there
