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
  
  def __init__ (self,you, numsystemsaway):
    self.you = you
    (self.destination,self.jumps)=universe.getAdjacentSystem(VS.getSystemFile(),numsystemsaway)
    self.obj=VS.addObjective("")
    self.com=(1.0/float(len(self.jumps)))
    VS.setCompleteness(self.obj,-self.com)
    VS.setOwner(self.obj,self.you)
  
  def Execute (self):
    cursys=VS.getSystemFile()
    if (cursys in self.jumps):
      curind=index(cursys)
      VS.setObjective(self.obj,"Jump to the system named "+self.jumps[curind+1])
      self.jumps.pop(curind)
      if (cursys==self.destination):
        self.arrivedsys=1
        VS.setCompleteness(self.com,1.0)
        return 1
      else:
        VS.setCompleteness(self.com,VS.getCompleteness(self.obj)+com)
        return 0

