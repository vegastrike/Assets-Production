from trading import trading
from random_encounters import random_encounters
from difficulty import difficulty
#from garbage_collect import garbage_collect
import Director

class privateer (Director.Mission):
  loops=()
  def __init__ (self,sigdis, detectiondis, gendis, minships, genships, fighterprob, enemyprob, capprob, credits_to_maximize_difficulty, capdist):#negative garbage collect dist disables that feature
    self.loops=(#difficulty (credits_to_maximize_difficulty),
          random_encounters (sigdis, detectiondis, gendis, minships,genships,fighterprob,enemyprob,capprob,capdist),
          trading (),
#          garbage_collect (),
          )

  def Execute(self): #this execute function should not need to be changed...
    for i in self.loops:
      print i
      i.Execute()

#def initstarsystem():
#  random_encounters.initstarsystem() #??? that isn't there

#test
priv=privateer(3.5,6.2,85.1,1,2,.7,.6,.2,59.0,9.1)
for i in range(10):
  priv.Execute()

