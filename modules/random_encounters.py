import random
import faction_ships
import launch_recycle
import launch
import VS
import unit
import sys
class random_encounters:
  sig_distance=0#backup var
  det_distance=0#backup var
  generation_distance=0
  capship_gen_distance=0
  min_num_ships=1#the number of ships that have to be there or else more will be made
  gen_num_ships=0#the num ships to be made
  capship_prob=0#probability a capship will be there
  fighterprob=0
  enprob=0
  players=()
  class playerdata:  
    #struct playerdata {
    last_ship=0 #cur[0]
    curmode=0 #cur[1] #are we in battle mode (1) or cruise mode (0)
    lastmode=0 #cur[2] #were we in battle mode (1) or cruise mode(0)
    lastsys="" #cur[3]
    sig_container=VS.Unit() #cur[4]
    significant_distance=5000 #cur[5]
    detection_distance=2500 #cur[6]
    playernum=0 #cur[8]
    def __init__(self,sig_distance,det_distance,pnum=None):
      if (pnum==None):
        return
      self.significant_distance=sig_distance
      self.detection_distance=det_distance
      self.playernum=pnum
  cur=playerdata(0,0)
  def __init__(self, sigdis, detectiondis, gendis,  minnships, gennships, unitprob, enemyprob, capprob, capdist):
    self.capship_gen_distance=capdist
    #    player_num=player
    self.enprob = enemyprob
    self.fighterprob = unitprob

    self.det_distance = detectiondis
    self.sig_distance = sigdis

    self.generation_distance=gendis
    self.min_num_ships=minnships
    self.gen_num_ships=gennships
    self.capship_prob=capprob
    player_num=0
    px = VS.getPlayerX(player_num)
    while (px):
        print ("init")
        self.players=self.players+(random_encounters.playerdata(self.sig_distance,self.det_distance,player_num),)
        player_num+=1
        px = VS.getPlayerX(player_num)
  
  def getMinDistFrom(self,sig1):
    sig2=unit.getPlanet (0,0)
    mindist=100000000000000000000000000000000000000000000.0
    i=0
    while (sig2):
      tempdist = sig1.getSignificantDistance(sig2)
      if (tempdist<mindist and tempdist>0.0):
          mindist=tempdist
      i+=1
      sig2 = unit.getPlanet (i,0)
    return mindist

  def minimumSigDistApart(self):
    sig1=unit.getPlanet (0,0)
    i=0
    mindist=100000000000000000000000000000000000000000000.0
    ave=0.0
    while (sig1):
      tempdist = self.getMinDistFrom (sig1)
      if (ave<0.9):
        mindist = tempdist
      else:
        mindist += tempdist
      ave+=1.0
      i+=1
      sig1 = unit.getPlanet (i,0)
    if (ave!=0.0):
      mindist = mindist/ave
    return mindist

  def CalculateSignificantDistance(self):
    minsig =  self.minimumSigDistApart()
    if (self.sig_distance>minsig*0.15):
      self.cur.significant_distance=minsig*0.15
    else:
      self.cur.significant_distance=self.sig_distance
    if (self.det_distance>minsig*0.2):
      self.cur.detection_distance=minsig*0.2
    else:
      self.cur.detection_distance=self.det_distance
    
    print "resetting sigdist=%f detdist=%f" % (self.cur.significant_distance,self.cur.detection_distance)

  def SetEnemyProb (self,enp):
    self.enprob = enp


  def AsteroidNear (self,uni, how):
    num_ships=0
    count=0
    un = VS.getUnit (count)
    while (un):
      dd = self.cur.detection_distance
      if (uni.getSignificantDistance(un)<how):
        if (unit.isAsteroid (un)):
          print "asty near"
          return 1
      count=count+1
      if (un):
        un = VS.getUnit(count)
    return 0

  def launch_near (self,un):
    numfactions=random.randrange(0,4)
    if (numfactions<=0):
      numfactions=1
    sysfile = VS.getSystemFile()
    for i in range(0,numfactions):
      localfaction = VS.GetGalaxyProperty(sysfile,"faction")
      if (random.random() < self.enprob):
        localfaction = faction_ships.get_enemy_of (localfaction)
      else:
        localfaction = faction_ships.get_friend_of(localfaction)
      numship= random.randrange(1,self.gen_num_ships+1)
      self.det_distance = self.cur.detection_distance
      launch_recycle.launch_wave_around(localfaction,localfaction,"default",numship,0,self.generation_distance*random.random()*0.9,un, 2.0*self.det_distance,"")
      if (random.random()<self.capship_prob):
        if (self.AsteroidNear (un,self.cur.significant_distance)):
          print "ast near, no cap"
        else:
          print "no asty near"
          capship = faction_ships.getRandomCapitol (localfaction)
          launch_recycle.launch_wave_around("Capitol",localfaction,"default",1,1,self.capship_gen_distance*(0.5+(random.random()*0.4)),un, 8.0*self.det_distance,"")

  def atLeastNInsignificantUnitsNear (self,uni, n):
    num_ships=0
    count=0
    leadah = uni.getFlightgroupLeader ()
    un = VS.getUnit (count)
    dd = self.cur.detection_distance
    while (un):
      if (uni.getSignificantDistance(un)<dd*1.6):
        if ((not un.isSignificant()) and (not un.isSun())):
          unleadah = un.getFlightgroupLeader ()
          if (leadah!=unleadah):
            num_ships+=1
      count+=1
      un = VS.getUnit(count)
    return num_ships>=n

  def SetModeZero(self):
    self.cur.last_ship=0
    self.cur.curmode=0
    self.cur.sig_container.setNull()

  def SetModeOne (self,significant):
    self.cur.last_ship=0
    self.cur.curmode=1
    self.cur.sig_container=significant
    self.cursys = VS.getSystemFile()
    oldsys = self.cur.lastsys==self.cursys
    self.cur.lastsys=self.cursys
    if (not oldsys):
      self.CalculateSignificantDistance()

  def decideMode(self):
    myunit=VS.getPlayerX(self.cur.playernum)
    if (myunit.isNull()):
      self.SetModeZero()
      return myunit
    significant_unit = self.cur.sig_container
    if (significant_unit.isNull()):
      un=VS.getUnit(self.cur.last_ship)
      if (un.isNull ()):
        self.SetModeZero()
      else:
        sd = self.cur.significant_distance
        if ((un.getSignificantDistance(myunit)<sd) and (un.isSignificant())):
          self.SetModeOne (un)
          return un
        self.cur.last_ship+=1
      return VS.Unit()
    else:
      #significant_unit is something.... lets see what it is
      cursys = VS.getSystemFile()
      if (cursys== self.cur.lastsys):
        dd = self.cur.detection_distance
        if (myunit.getSignificantDistance (significant_unit)>dd):
          self.SetModeZero ()
          return VS.Unit()
        else:
          return significant_unit
      else:
        print "different"
        self.cur.lastsys=cursys
        self.SetModeZero()
        significant_unit.setNull ()
      return significant_unit

  def Execute(self):
    for self.cur in self.players:
        un = self.decideMode ()
        if (self.cur.curmode!=self.cur.lastmode):
          #lastmode=curmode#processed this event don't process again if in critical zone
          self.cur.lastmode=self.cur.curmode
          print "curmodechange %d" % (self.cur.curmode)#?
          if (random.random()<self.fighterprob and un):
              if (not self.atLeastNInsignificantUnitsNear (un,self.min_num_ships)):
                #determine whether to launch more ships next to significant thing based on ships in that range  
                print ("launch near")
                self.launch_near (VS.getPlayerX(self.cur.playernum))

