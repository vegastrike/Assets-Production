#import wc1_mis0
import Briefing
import Director
import VS
import launch
import save_util
import wc1_mis0
class wc1 (Director.Mission):
  
  def __init__ (self):
    Director.Mission.__init__(self)
    self.campaign={("vega_sector/enyo",0):wc1_mis0.wc1_mis0()}
    self.sector=save_util.loadStringList (0,"wc1sector")
    if (self.sector==[]):
      self.sector = "vega_sector/enyo";
    else:
      [self.sector]=self.sector
    self.curmission=0
    if (self.sector==""):
      self.sector="vega_sector/enyo"
    self.mission=Director.getSaveData(0,"wc1mission",0)
    self.carrier = launch.launch ("BengalClass","confed","fleetcarrier","default",1,1,(0,0,0))
    self.wfm=""
    self.StartMission(VS.getSystemFile(),self.sector,self.mission)

  def StartMission (self,lastsector, cursector,mission):
    print (cursector,)
    print cursector
    save_util.saveStringList(0,"wc1sector",(cursector,))
    if (Director.getSaveDataLength (0,"wc1mission")>0):
      Director.putSaveData(0,"wc1mission",0,mission)
    else:
      Director.pushSaveData(0,"wc1mission",mission)
    if (lastsector!=cursector):
      self.wfm=cursector
      self.JumpTo(cursector)
    else:
      self.LoadMission(cursector,mission)
  def LoadMission (self,sec,mis):
    self.curmission = self.campaign.get((sec,mis))
    if (self.curmission):
      self.curmission.Start(self.carrier)
  def JumpTo(self,loc):
    self.carrier.JumpTo(loc)
    if (not (VS.getPlayer().isDocked (self.carrier) or self.carrier.isDocked(VS.getPlayer()))):
      VS.getPlayer().JumpTo(loc)
  def Execute(self): #this execute function should not need to be changed...
    if (self.wfm==VS.getSystemFile()):
      self.wfm=""
      self.LoadMission (self.sector,self.mission)
    if (self.wfm =="" and self.curmission):
      newmis=self.curmission.Execute()
      if (newmis):
        cursector= self.sector
        curmission=self.mission
        (self.sector,self.mission)=newmis
        if (curmission!=self.mission or cursector!= self.sector):
          self.StartMission (cursector,self.sector,self.mission)
  def initbriefing(self):
    print "ending briefing"                
  def loopbriefing(self):
    print "loop briefing"
    Briefing.terminate();
  def endbriefing(self):
    print "ending briefing"        

#def initstarsystem():
#  random_encounters.initstarsystem() #??? that isn't there
