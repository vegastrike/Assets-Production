import sys
import VS
import Director
def usingDifficulty ():
  return (VS.GetDifficulty()!=1.0)

def SetDiff(diff):
  if (diff>VS.GetDifficulty()):
    VS.SetDifficulty(diff)

_key="31337ness"
class difficulty:
  def SetDiff(self,diff):
    if (diff>VS.GetDifficulty()):
      VS.SetDifficulty(diff)

  def __init__(self,credsMax):
    print "init diff"
    self.diff=[]
    self.creds=[]
    self.credsToMax=credsMax
    print "unlogical start"
    un=VS.getPlayerX(0)
    print "unlogical end"
    self.i=0
    while (un):
      newdiff=0
      print "get save data length"
      if (Director.getSaveDataLength(self.i,_key)):
        print "get save dat"
        newdiff=Director.getSaveData(self.i,_key,0)
        print "get save end"
      else:
        print "get difficulty start"
        newdiff=VS.GetDifficulty()
        print "get diff done"
        Director.pushSaveData(self.i,_key,newdiff)
        print "done director"
      self.diff+=[newdiff]
      print "set diff start"        
      SetDiff(newdiff)
      print "set diff end"
      self.creds+=[un.getCredits()]
      self.i+=1
      print "save unit"
      un=VS.getPlayerX(self.i)
      print "done init diff"
  def usingDifficulty (self):
    return (VS.GetDifficulty()!=1.0)
  
  def getPlayerDifficulty (self,playa):
    return self.diff[playa]
  
  def Execute(self):
    if (self.i>=len(self.creds)):
      self.i=0
    else:
      un=VS.getPlayerX(self.i)
      if (un):
        newcreds=un.getCredits()
        if (self.creds[self.i]!=newcreds):
          if (self.creds[self.i]<newcreds):
            newdiff=self.getPlayerDifficulty(self.i)+((newcreds-self.creds[self.i])/self.credsToMax)
            if (newdiff>.999):
              #newdiff=.999
              newdiff=1
            Director.putSaveData(self.i,_key,0,newdiff)
            SetDiff(newdiff)
          self.creds[self.i]=newcreds
      self.i+=1
  
