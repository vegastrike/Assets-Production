import unit
import universe

class go_somewhere_significant:
  destination=""
  significantun=VS.Unit()
  jumps=()
  baseonly=0
  capship=0
  jumppoint=0
  arrivedsys=0
  arrivedarea=0
  distfrombase=500
  youcontainer=VS.Unit()
  
  def HaveArrived (self):
    return self.arrivedarea
  
  def InSystem(self):
    return self.arrivedsys
  
  #only run this function if we are InSystem()
  def SignificantUnit(self):
    return self.significantun
  
  def DestinationSystem (self):
    return self.destination
  
  def JumpPoints (self):
    return self.jumps
  
  def __init__ (self,you, numsystemsaway, capship_only, jumppoint_only,  distance_away_to_trigger,base_only=0):
    self.youcontainer = you
    self.capship = capship_only
    self.jumppoint = jumppoint_only
    self.distfrombase=distance_away_to_trigger
    (self.destination,self.jumps)=universe.getAdjacentSystem(VS.getSystemFile(),numsystemsaway)
  
  def Execute(self):
    if (self.arrivedsys):
      if (self.significantun.isNull() or self.youcontainer.isNull()):
        return
      if (unit.getSignificantDistance(self.youcontainer,self.significantun)<=self.distfrombase):
        self.arrivedarea=1
    else:
      if (VS.getSystemFile()==self.destination):
        self.arrivedsys=1
        significant=VS.Unit()
        if (capship):
          randint=random.randomint(0,128)
          significant = unit.getSignificant (randint,capship,baseonly)
        else:
          significant = universe.getRandomJumppoint ()
        if (significant.isNull()):
          significant =VS.getPlayer()
        if (significant.isNull()):
          arrivedsys=false
        else:
          _io.message (0,"game","all","You must visit the %s" % (significant.getName ()))
          self.significantun=significant

