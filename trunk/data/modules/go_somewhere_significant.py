import unit
import universe
import VS
import faction_ships
import random
import launch
import Briefing
class go_somewhere_significant:
#  frameoffset=0 #see note at bottom
#  begsigdis=1.0 #same note
  def HaveArrived (self):
    return self.arrivedarea
  
  def SignificantUnit(self):
    return self.significantun
  
  def __init__ (self,you, landable_only, distance_away_to_trigger,base_only=0,capshipfaction=""):
    self.obj=0
    self.orbitee=""
    self.capship=0
    self.you = you
    self.arrivedarea=0
    self.distfrombase=distance_away_to_trigger
    significant=VS.Unit()
    self.sysfil=VS.getSystemFile()
    if (landable_only or base_only):
      randint=random.randrange(0,128)
      significant = unit.getSignificant (randint,landable_only,base_only)
      if (capshipfaction!=""):
        newship=faction_ships.getRandomCapitol(capshipfaction)
        if (significant.isNull()):
          significant=you
        self.orbitee="%s" % (significant.getName())
        self.capship=1
        print "orbitee %s " % self.orbitee
        significant=launch.launch_wave_around_unit("Base",capshipfaction,newship,"sitting_duck",1,2000.0,5000.0,significant,"")
    else:
      significant = universe.getRandomJumppoint ()
    if (significant.isNull()):
      print "ERROR: no significants found in starsystem %s" % (self.sysfil)
      VS.terminateMission(0)
      return
    else:
      self.significantun=significant
      self.obj=VS.addObjective("You must visit the %s" % (significant.getName ()))
      VS.setOwner(self.obj,VS.getPlayer())
#      self.begsigdis=self.you.getSignificantDistance(self.significantun) #see note below
  
  def Print(self,visitstr,fro,dockstr="\0%s",time=0):
    if (self.capship):
      visitstr+=(dockstr % (self.orbitee))
    VS.IOmessage(time,fro,universe.getMessagePlayer(self.you),visitstr % (self.significantun.getName()))
  def DestinationSystem(self):
    return self.sysfil
  def JumpPoints (self):
    return (self.sysfile)
  def Execute(self):
    if (self.significantun.isNull() or self.you.isNull() or VS.getSystemFile()!=self.sysfil):
      return 0
#    self.frameoffset+=1 #see note below...
    sigdis=self.you.getSignificantDistance(self.significantun)
    if (sigdis<=self.distfrombase):
      self.arrivedarea=1
      VS.setCompleteness(self.obj,1.0)
#    if ((not self.arrivedarea) and (self.frameoffset%25)):
#      VS.setCompleteness(self.obj,(1-(float(sigdis)/float(self.begsigdis)))) #doesn't work too well... for now, it will be 0 until you dock
    return self.HaveArrived()
  def initbriefing (self):
    self.mytime = VS.GetGameTime();
    faction=self.you.getFactionName();
    name=self.you.getName()
    self.brief_you=Briefing.addShip(name,faction,(40.0,0.0,80.0))
    faction=self.significantun.getFactionName()
    name = self.significantun.getName()
    self.brief_sig=Briefing.addShip(name,faction,(-40,0.0,8000.0))
    Briefing.enqueueOrder (self.brief_you,(-30,0.0,7900.0),5.0)
  def loopbriefing (self):
    if (VS.GetGameTime()-self.mytime>5):
      return self.brief_you
    return -1
  def endbriefing(self):
    del self.mytime
    del self.brief_you
    del self.brief_sig
