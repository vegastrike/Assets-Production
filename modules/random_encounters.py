import random
import faction_ships
import launch_recycle
import launch
import VS
import unit
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
  player_num=0
  players=()
  class playerdata:  
    #struct playerdata {
    last_ship=0 #cur[0]
    curmode=0 #cur[1] #are we in battle mode (true) or cruise mode (false)
    lastmode=0 #cur[2] #were we in battle mode (true) or cruise mode(false)
    lastsys="" #cur[3]
    sig_container=VS.Unit() #cur[4]
    significant_distance=sig_distance #cur[5]
    detection_distance=det_distance #cur[6]
    this_unit=VS.Unit() #cur[7]
    playernum=0 #cur[8]
    def __init__(self,playernum=None):
      if (playernum==None):
        return
      px = VS.getPlayerX(playernum)
      self.player_num=playernum
      this_unit=px
  cur=playerdata()
  def __init__(self, sigdis, detectiondis, gendis,  minnships, gennships, unitprob, enemyprob, capprob, capdist):
    capship_gen_distance=capdist
    #    player_num=player
    enprob = enemyprob
    fighterprob = unitprob

    faction_ships.init()
    det_distance = detectiondis
    sig_distance = sigdis

    generation_distance=gendis
    min_num_ships=minnships
    gen_num_ships=gennships
    capship_prob=capprob
    px = _unit.getPlayerX(player_num)
    while (px):
        print ("init")
        self.player=self.player+(playerdata(player_num))
        player_num=player_num+1
        px = _unit.getPlayerX(player_num)
  
  def getMinDistFrom(sig1):
    sig2=unit.getPlanet (0,false)
    mindist=100000000000000000000000000000000000000000000.0
    i=0
    while (sig2):
      tempdist = sig1.getSignificantDistance(sig2)
      if (tempdist<mindist and tempdist>0.0):
          mindist=tempdist
      i+=1
      sig2 = unit.getPlanet (i,false)
    return mindist

  def minimumSigDistApart():
    sig1=unit.getPlanet (0,false)
    i=0
    mindist=100000000000000000000000000000000000000000000.0
    ave=0.0
    while (sig1):
      tempdist = getMinDistFrom (sig1)
      if (ave<0.9):
        mindist = tempdist
      else:
        mindist += tempdist
      ave+=1.0
      i+=1
      sig1 = unit.getPlanet (i,false)
    if (ave!=0.0):
      mindist = mindist/ave
    return mindist

  def CalculateSignificantDistance():
    minsig =  minimumSigDistApart()
    significant_distance = 0
    if (sig_distance>minsig*0.15):
      significant_distance = minsig*0.15
      cur.significant_distance=minsig*0.15
    else:
      cur.significant_distance=sig_distance
      significant_distance = sig_distance
    if (det_distance>minsig*0.2):
      cur.detection_distance=minsig*0.2
      detection_distance = minsig*0.2
    else:
      cur.detection_distance=det_distance
      detection_distance = det_distance
    
    print "resetting sigdist=%f detdist=%f" % (significant_distance,detection_distance)

  def SetEnemyProb (enp):
    enprob = enp


  def AsteroidNear (unit, how):
    num_ships=0
    count=0
    un = VS.getUnit (count)
    while (un):
      dd = cur.detection_distance
      if (unit.getSignificantDistance(un,unit)<how):
        if (unit.isAsteroid (un)):
          _io.printf ("asty near")
          return 1
      count=count+1
      if (un):
        un = _unit.getUnit(count)
    return 0

  def launch_near (un):
    numfactions=VS.GetNumFactions()
    if (numfactions==0):
      sys.stderr.write('warning: no factions\n')
      numfactions=1
    sysfile = _std.getSystemFile()
    for i in range(0,numfactions):
      localfaction = _std.getGalaxyProperty(sysfile,"faction")
      if (random.random() < enprob):
        localfaction = faction_ships.get_enemy_of (localfaction)
      else:
        localfaction = faction_ships.get_friend_of(localfaction)
      #      fighter = faction_ships.getRandomFighter (localfaction)
      numship= random.randrange(1,gen_num_ships)
      det_distance = cur.detection_distance
      launch_recycle.launch_wave_around(localfaction,localfaction,"default",numship,false,generation_distance*_std.Rnd()*0.9,un, 2.0*det_distance)
      rnd_num = random.random()
      if (rnd_num<capship_prob):
        if (AsteroidNear (un,cur.significant_distance)):
          print "ast near, no cap"
        else:
          print "no asty near"
          capship = faction_ships.getRandomCapitol (localfaction)
          launch_recycle.launch_wave_around("Capitol",localfaction,"default",1,true,capship_gen_distance*(0.5+(_std.Rnd()*0.4)),un, 8.0*det_distance)

  def test_atLeastNInsignificantUnitsNear (unit, n):
    num_ships=0
    count=0
    un = VS.getUnit (count)
    while (un):
      dd = cur.detection_distance
      if (unit.getSignificantDistance(un,unit)<dd):
        if ((not un.isSignificant()) and (not un.isSun())):
          print "unit not sig %d %s %s" % (num_ships,un.getFgName(),un.getName())
          num_ships+=1
          if (num_ships>=n):
            break
      count=count+1
      un = _unit.getUnit(count)
    return (num_ships>=n)

  def atLeastNInsignificantUnitsNear (uni, n):
    num_ships=0
    count=0
    leadah = uni.getFgLeader ()
    un = VS.getUnit (count)
    dd = cur.detection_distance
    while (un):
      if (uni.getSignificantDistance(un)<dd*1.6):
        if ((not un.isSignificant()) and (not un.isSun())):
          unleadah = un.getFgLeader ()
          if (leadah!=unleadah):
            num_ships+=1
      count+=1
      un = VS.getUnit(count)
    return num_ships>=n

  def SetModeZero():
    #    last_ship=0
    cur.last_ship=0
    cur.curmode=0
    #    curmode=0
    cur.sig_container.setNull()

  def SetModeOne (significant):
    cur[0]=0
    #curmode=1
    cur[1]=1
    cur[4]=significant
    cursys = VS.getSystemFile()
    lastsys = cur[3]
    oldsys = lastsys==cursys
    cur[3]=cursys
    if (not oldsys):
      CalculateSignificantDistance()

  def HaveWeSignificant ():
    significant_unit=cur.sig_container
    return significant_unit

  def decideMode():
    if (cur.this_unit.isNull()):
      SetModeZero()
      return cur.this_unit
    significant_unit = HaveWeSignificant()
    if (significant_unit.isNull()):
      un=VS.getUnit(cur.last_ship)
      if (un.isNull ()):
        SetModeZero()
      else:
        sd = cur.significant_distance
        if ((un.getSignificantDistance(cur.this_unit)<sd) and (un.isSignificant())):
          SetModeOne (un)
          return un
        cur.last_ship+=1
      return Unit()
    else:
      #significant_unit is something.... lets see what it is
      cursys = VS.getSystemFile()
      if (cursys== cur.lastsys):
        dd = cur.detection_distance
        if (cur.this_unit.getSignificantDistance (significant_unit)>dd):
          SetModeZero ()
          return VS.Unit()
        else:
          return significant_unit
      else:
        print "different"
        cur.lastsys=cursys
        SetModeZero()
        significant_unit.setNull ()
      return significant_unit

  def loop():
    for cur in players:
        un = decideMode ()
        if (cur.curmode!=cur.lastmode):
          #lastmode=curmode#processed this event don't process again if in critical zone
          cur.lastmode=cur.curmode
          print "curmodechange %d" % (curmode)#?
          if (random.random()<fighterprob and un):
              if (not atLeastNInsignificantUnitsNear (un,min_num_ships)):
                #determine whether to launch more ships next to significant thing based on ships in that range  
                print ("launch near")
                launch_near (player_unit)

