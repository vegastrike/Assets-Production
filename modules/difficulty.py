import sys
import VS
import pickle
import Director
_key="31337ness"
class difficulty:
  diff=()
  creds=()
  credsToMax=1
  i=0 #comment this if you want to check all in 1 frame
  def SetDiff(diff):
    if (diff>VS.GetDifficulty()):
      VS.SetDifficulty(diff)
  
  def __init__(self,credsMax):
    self.credsToMax=credsMax
    un=VS.getPlayerX(0)
    i=0
    while (un):
      newdiff=0
      if (Director.getSaveDataLength(i,_key)):
        newdiff=Director.getSaveData(i,_key,0)
        self.diff+=(newdiff,)
      else:
        newdiff=VS.GetDifficulty()
        self.diff+=(newdiff,)
        Director.pushSaveData(i,_key,newdiff)
      SetDiff(newdiff)
      self.creds+=(un.getCredits(),)
      i+=1
      un=VS.getPlayerX(i)
      
  def usingDifficulty (self):
    return (VS.GetDifficulty()!=1.0)
  
  def getPlayerDifficulty (self,playa):
    return self.diff[playa]
  
  def Execute(self):
#    for i in range(len(self.creds)): #uncomment this if you want to check all in 1 frame
      if (len(self.creds)<=0):
        if (self.i!=-1):
          self.i=-1
          raise IndexError("Empty creds and diff arrays in difficulty module\nUnable to find any players...")
        return
      i=self.i #comment this if you want to check all in 1 frame
      un=VS.getPlayerX(i)
      newcreds=un.getCredits()
      if (self.creds[i]!=newcreds):
        if (self.creds[i]>newcreds):
          newdiff=((newcreds-self.creds)/self.credsToMax)
          Director.putSaveData(i,_key,0,newdiff)
          SetDiff(newdiff)
        self.creds[i]=newcreds
      self.i+=1 #comment this also if you want to check all in 1 frame
  
