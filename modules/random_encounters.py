import vsrandom
import faction_ships
import launch_recycle
import launch
import VS
import unit
import sys
import adventure
import news
import universe
class random_encounters:
  class playerdata:  
    def GeneratePhaseAndAmplitude(self):
      self.prob_phase=20*vsrandom.random()
      self.prob_amplitude = .5+.5*vsrandom.random()
      self.prob_period = 20*vsrandom.random()+1
    def UpdatePhaseAndAmplitude(self):
      self.prob_phase+=1;
      return self.prob_amplitude*(.6+.4*VS.cos ((self.prob_phase*3.1415926536*2)/self.prob_period))
    def __init__(self,sig_distance,det_distance):
      print "init playerdat"
      self.quests=[]
      self.curquest=0
      self.last_ship=0
      self.curmode=0
      self.lastmode=0
      self.lastsys=""
      self.sig_container=VS.Unit()
      self.significant_distance=sig_distance
      self.detection_distance=det_distance
      self.GeneratePhaseAndAmplitude()
      print "done playerdat"
  def __init__(self, sigdis, detectiondis, gendis,  minnships, gennships, unitprob, enemyprob, capprob, capdist):
    unitprob=1
    print "init random enc"
    self.capship_gen_distance=capdist
    #    player_num=player
    self.enprob = enemyprob
    self.fighterprob = unitprob

    self.det_distance = detectiondis
    self.sig_distance = sigdis
    self.players=[]
    self.generation_distance=gendis
    self.min_num_ships=minnships
    self.gen_num_ships=gennships
    self.capship_prob=capprob
    self.cur_player=0
    self.sig_distance_table = {"enigma_sector/heavens_gate":(2000,4000,.4)}
    print "end random enc"
  def AddPlayer (self):
#    print "begin add player"
    self.players+=[random_encounters.playerdata(self.sig_distance,self.det_distance)]
#    print "add player"
  def NewSystemHousekeeping(self,oldsystem,newsystem):
    news.newNews()
    newquest = adventure.newAdventure (self.cur_player,oldsystem,newsystem)
    if (newquest):
      self.cur.quests+=[newquest]
    else:
      self.RestoreDroneMission()
    self.CalculateSignificantDistance()
  def RestoreDroneMission(self):
    qdf=adventure.persistentAdventure (self.cur_player)
    if (qdf):
      self.cur.quests+=[qdf]
  def CalculateSignificantDistance(self):
    sysfile = VS.getSystemFile()
    self.cur.GeneratePhaseAndAmplitude()
    if sysfile in self.sig_distance_table:
      self.cur.significant_distance = self.sig_distance_table[sysfile][0]
      self.cur.detection_distance = self.sig_distance_table[sysfile][1]
      self.cur.prob_amplitude = self.sig_distance_table[sysfile][2]
      return
    minsig =  unit.minimumSigDistApart()
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
  def TrueEnProb(self,enprob):
    ret=1
    nam = VS.numActiveMissions()
    while (nam>0):
      ret*=(1-enprob)
      nam-=1
    print 1-ret
    return 1-ret;
    
  def launch_near_stage2 (self,un,near_faction,cap_prob):
    numfactions=vsrandom.randrange(0,4)
    if (numfactions<=0):
      numfactions=1
    sysfile = VS.getSystemFile()
    gen_num_ships=self.gen_num_ships
    for i in range(0,numfactions):
      localfaction = VS.GetGalaxyProperty(sysfile,"faction")
      if (vsrandom.random() < self.TrueEnProb(self.enprob)):
        localfaction = faction_ships.get_insys_enemy_of (localfaction)
      else:
        localfaction = faction_ships.get_friend_of(localfaction)
      if (len(near_faction)>0):
        if (i==0 and vsrandom.random()<(.3+(.4*VS.GetDifficulty()))):
          localfaction=near_faction
          gen_num_ships*=3
      else:
	cap_prob/=3;#1/3 chance of capships within a nation border
      numship= vsrandom.randrange(1,int(gen_num_ships)+1)
      self.det_distance = self.cur.detection_distance
      launch_recycle.launch_wave_around(localfaction,localfaction,"default",numship,0,self.generation_distance*vsrandom.random()*0.9,un, 2.0*self.det_distance,"")
      if (vsrandom.random()<cap_prob):
        if (self.AsteroidNear (un,self.cur.significant_distance)):
          print "ast near, no cap"
        else:
          print "no asty near"
          cap_prob=.7
          capship = faction_ships.getRandomCapitol (localfaction)
          launch_recycle.launch_wave_around("Capitol",localfaction,"default",1,1,self.capship_gen_distance*(0.5+(vsrandom.random()*0.4)),un, 8.0*self.det_distance,"")

  def launch_near(self,un):
    if (VS.GetGameTime()<10):
      print "hola!"
      return
    randomnum=vsrandom.random()
    system=cursys=VS.getSystemFile()
    faction=curfac=VS.GetGalaxyProperty(system,"faction")
    cap_prob=self.capship_prob
##    systemlist=universe.getAdjacentSystems(system,5)[1]
##    systemlist=(system,)+systemlist
##    i=0
##    cap_prob=self.capship_prob
##    for system in systemlist:
##      i+=1
##      faction=VS.GetGalaxyProperty(system,"faction")
##      if vsrandom.random()<.5:
##        cap_prob/=3
##        break
##      if faction!=curfac:
##        cap_prob/=i
##        break
##    if (faction==curfac):
##      faction=''
    otherfactions=[]
    i=0
    for i in range(VS.GetNumAdjacentSystems(cursys)):
      system=VS.GetAdjacentSystem(cursys,i)
      faction=VS.GetGalaxyProperty(system,"faction")
      if faction!=curfac:
        otherfactions.append(faction)
    if len(otherfactions)==0:
      faction=''
      cap_prob/=3
    else:
      if len(otherfactions)==1:
        cap_prob/=2
      faction=otherfactions[vsrandom.randrange(0,len(otherfactions))]
    self.launch_near_stage2 (un,faction,cap_prob)
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
    for q in self.cur.quests:
      q.NoSignificantsNear()

  def SetModeOne (self,significant):
    self.cur.last_ship=0
    self.cur.curmode=1
    self.cur.sig_container=significant
    cursys = VS.getSystemFile()
    oldsys = self.cur.lastsys==cursys
    if (not oldsys):
      self.NewSystemHousekeeping(self.cur.lastsys,cursys)
      self.cur.lastsys=cursys
    for q in self.cur.quests:
      q.SignificantsNear(self.cur.sig_container)
    

  def decideMode(self):
    myunit=VS.getPlayerX(self.cur_player)
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
        self.NewSystemHousekeeping(self.cur.lastsys,cursys)
        self.cur.lastsys=cursys
        self.SetModeZero()
        significant_unit.setNull ()
      return significant_unit

  def Execute(self):
    if (self.cur_player>=len(self.players)):
      self.AddPlayer()
    self.cur=self.players[self.cur_player]
    if (self.cur.curquest<len(self.cur.quests)):
      if (self.cur.quests[self.cur.curquest].Execute()):
        self.cur.curquest+=1
      else:
        del self.cur.quests[self.cur.curquest]
    else:
      self.cur.curquest=0
    un = self.decideMode ()
    if (self.cur.curmode!=self.cur.lastmode):
      #lastmode=curmode#processed this event don't process again if in critical zone
      self.cur.lastmode=self.cur.curmode
      print "curmodechange %d" % (self.cur.curmode)#?
      if ((vsrandom.random()<(self.fighterprob*self.cur.UpdatePhaseAndAmplitude())) and un):
        if (not self.atLeastNInsignificantUnitsNear (un,self.min_num_ships)):
          #determine whether to launch more ships next to significant thing based on ships in that range  
          print ("launch near")
          self.launch_near (VS.getPlayerX(self.cur_player))
    self.cur_player+=1
    if (self.cur_player>=VS.getNumPlayers()):
      self.cur_player=0
    VS.setMissionOwner(self.cur_player)
      
print "done loading rand enc"
