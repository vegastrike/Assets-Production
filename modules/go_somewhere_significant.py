import unit
import universe
import VS

class go_somewhere_significant:
  significantun=VS.Unit()
  arrivedarea=0
  distfrombase=500
  you=VS.Unit()
  frameoffset=0
  begsigdis=1.0
  sysfil=""
  
  def HaveArrived (self):
    return self.arrivedarea
  
  def SignificantUnit(self):
    return self.significantun
  
  def __init__ (self,you, capship_only, distance_away_to_trigger,base_only=0):
    self.you = you
    self.distfrombase=distance_away_to_trigger
    significant=VS.Unit()
    self.sysfil=VS.getSystemFile()
    if (capship_only):
      randint=random.randrange(0,128)
      significant = unit.getSignificant (randint,1,base_only)
    else:
      significant = universe.getRandomJumppoint ()
    if (significant.isNull()):
      print "ERROR: no significants found in starsystem %s" % (self.sysfil)
      VS.terminateMission(0)
    else:
      IOmessage (0,universe.getMessagePlayer(self.you),"You must visit the %s ship" % (significant.getName ()))
      self.significantun=significant
    self.obj=VS.addObjective("You must visit the %s ship" % (significant.getName ()))
    VS.setOwner(self.obj,self.you)
    self.begsigdis=self.you.getSignificantDistance(self.significantun)
  
  def Execute(self):
    if (self.significantun.isNull() or self.you.isNull() or VS.getSystemFile()!=sysfil):
      return
    frameoffset+=1
    sigdis=self.you.getSignificantDistance(self.significantun)
    if (sigdis<=self.distfrombase):
      self.arrivedarea=1
      VS.setCompleteness(self.obj,1.0)
    if ((not self.arrivedarea) and (frameoffset%25)):
      VS.setCompleteness(self.obj,float(sigdis)/float(begsigdis))
    return self.HaveArrived()
  
