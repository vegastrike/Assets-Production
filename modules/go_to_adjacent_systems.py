import VS
import universe
import unit

class go_to_adjacent_systems:
  you=VS.Unit()
  arrivedsys=0
  jumps=()
  destination=""
  obj=0
  com=0
  
  def InSystem(self):
    return self.arrivedsys
  
  def DestinationSystem (self):
    return self.destination
  
  def JumpPoints (self):
    return self.jumps
  
  def ChangeObjective(self,newind):
      VS.setObjective(self.obj,"Jump to the system named %s" % (self.jumps[newind]))
  
  def __init__ (self,you, numsystemsaway):
    self.you = you
    (self.destination,self.jumps)=universe.getAdjacentSystems(VS.getSystemFile(),numsystemsaway)
    if (len(self.jumps)>0):
      self.obj=VS.addObjective("")
      self.com=(1.0/float(len(self.jumps)))
      VS.setCompleteness(self.obj,0)
      VS.setOwner(self.obj,self.you)
      self.ChangeObjective(0)
    else:
      self.arrivedsys=1
  
  def Print(self,beginstr,midstr,endstr,fro,wait=0):
    msgply=universe.getMessagePlayer(self.you)
    if (len(self.jumps)>0):
      VS.IOmessage(wait,fro,msgply,beginstr % (VS.getSystemFile()))
      for i in range(len(self.jumps)-1):
        VS.IOmessage(wait,fro,msgply,midstr % (self.jumps[i]))
      VS.IOmessage(wait,fro,msgply,endstr % (self.jumps[len(self.jumps)-1]))
  
  def Execute (self):
    cursys=VS.getSystemFile()
    if (cursys in self.jumps):
      newjumps=list(self.jumps) #only lists can do 'index' but tuples strangely can do 'in'... at least it only happens when you jump...
      curind=newjumps.index(cursys)
      if ((curind+1)<len(self.jumps)):
        self.ChangeObjective(curind+1)
      newjumps.pop(curind)
      self.jumps=tuple(newjumps) #make it another tuple...
      if (cursys==self.destination):
        self.arrivedsys=1
        VS.setCompleteness(self.obj,1.0)
      else:
        VS.setCompleteness(self.obj,self.com*curind)
    return self.arrivedsys

