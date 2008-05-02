# 299 "unit_wrapper.cpp"
import sys
import math
import time
import xml
import xml.dom
import xml.dom.minidom
import math
#########For dynamic universe simulation
def getParentVal(node,val):
	i = node.parentNode
	while(i):
		j = i.firstChild
		while (j):
			try:
				if (j.tagName!='var'):
					return None
				if (j.getAttribute('name')==val):
					return j.getAttribute('value')
			except:
				pass
			j = j.nextSibling		
		i = node.parentNode
	return getParentVal(node,val)
def toPair (s):
	if (not s):
		return None
	k=s.split(' ')
	return (float(k[0]),float(k[1]),float(k[2]))
def getVal(node,val):
	for i in node.getElementsByTagName('var'):
		if (i.getAttribute('name')==val):
			return i.getAttribute('value')
	return getParentVal(node,val)
def getValND(node,val):
	for i in node.getElementsByTagName('var'):
		if (i.getAttribute('name')==val):
			return i.getAttribute('value')
	return None
def removeVal(node,val):
	for i in node.getElementsByTagName('var'):
		if (i.getAttribute('name')==val):
			node.removeChild(i)

try:
	import cached_universe
	universe=cached_universe.universe
except:
	#end dynamic universe sim
	try:
		fil = open("../universe/wcuniverse.xml","r")
	except:
		fil = open("../universe/milky_way.xml","r")
	g = xml.dom.minidom.parseString(fil.read());
	fil.close()
	systems = g.getElementsByTagName('system')
	universe={}
	for s in systems:
		name=s.parentNode.getAttribute('name')+"/"+s.getAttribute('name')
		properties={}
		for i in s.getElementsByTagName('var'):
			properties[i.getAttribute('name')]=i.getAttribute('value')
		properties["faction"]=getVal(s,"faction")
		jumps=[]
		if "jumps" in properties:
			jumps=properties["jumps"].split(" ")
		properties["jumps"]=jumps
		universe[name]=properties
	try:
		fil = open("cached_universe.py","w")
		fil.write("universe=")
		fil.write(str(universe))
		fil.close()
	except:
		pass
_sysfile = ['Gemini/Troy']
_unitlist=[]
def timeofday():
   return time.time()
def sqrt (s):
   return math.sqrt(s)
def log (s):
   return math.log(s)
def exp (s):
   return math.exp(s)
def cos (s):
   return math.cos(s)
def sin (s):
   return math.sin(s)
def asin (s):
   return math.asin(s)
def acos (s):
   return math.acos(s)
def atan (s):
   return math.atan(s)
def tan (s):
   return math.tan(s)
def micro_sleep (n):
   pass
def vsConfig(section, var, value):
   print 'returned save variable '+section+' \"'+var+'\" as \"'+value+'\"'
def addParticle (loc,vel,col):
   print 'added particle ' + loc + ' vel '+vel+' col '+col
def pushSystem(sysname):
   #print "pushSystem"
   global _sysfile
   _sysfile+=[sysname]
def StopTargettingEachOther (fg,fac,enfg,enfac):
	#print "detarget"
	pass
def TargetEachOther (fg,fac,enfg,enfac):
	#print "target"
	pass
def systemInMemory(sys):
    if (sys=='no_sector/no_system'):
      return 0
    import vsrandom
    ret = vsrandom.randrange(0,2)	
    if (sys in _sysfile):
        #print sys+' in memory'
		pass
    if (ret):
        #print sys+' maybe in memory'
		pass
    else:
        #print sys + ' maybe not in memory'
		pass
    return ret

def popSystem():
   del _sysfile[-1]
def getSystemFile():
   return _sysfile[-1]
def getPlanetRadiusPercent ():
	return .75

def getSystemName():
   print "getSystemName" 
   return _sysfile[-1]+' system'
def getUnitList():
   print "getUnitList" 
   return un_iter()
def getUnit(which):
   print "getUnit"
   if (len(_unitlist)>which):
      return _unitlist[which]
   else:
      return 0
def getNumUnits():
   return len(_unitlist)
def cacheAnimation(ani):
   print 'cache '+str(ani)

def launchJumppoint(name,faction,type,unittype,ai,nr,nrwaves,pos,squadlogo,destinations):
   print "launchJumppoint" 
   for i in range (nr):
      _unitlist+=[Unit(type,name)]
   return _unitlist[len(_unitlist)-nr]

def launch(name,type,faction,unittype,ai,nr,nrwaves,pos,squadlogo):
   print "launch"
   global _unitlist
   for i in range (nr):
      _unitlist+=[Unit(type,name)]
   return _unitlist[len(_unitlist)-nr]
_cargotypes = ['boxes','plastic','metal','junk','food']
def getRandCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getRandCargo"
   import vsrandom
   which = vsrandom.randrange(0,len(_cargotypes))
   return Cargo(_cargotypes[which],_cargotypes[which],1,1,1,1)
_factions=['neutral','confed','kilrathi','retro','steltek','militia','landreich','border_worlds','firekkan','aera','merchant','rlaan','powerups','upgrades','unknown','pirates','hunter','privateer','ISO','planets','shaper','klkk','luddites','andolian','rlaan_briin','LIHW','uln','shmrn','purist','highborn','unadorned','dgn','forsaken','mechanist','homeland-security','AWACS']
def fgsInSector(sector,factions=_factions,printout=False):
   import fg_util
   ret={}
   for sys in universe:
      if sys.find(sector)==0:
         ret[sys[len(sector)+1:]]=[]
         if printout:
             print sys[len(sector)+1:]+": "
         for f in factions:
            if (not (type(f)==type(()) or type(f)==type([]))):
               f=(f,)
            numcaps=0
            numfighters=0

            for fac in f:
               fgs=fg_util.AllFGsInSystem(fac,sys)
               if (len(fgs)):
                  for fg in fgs:
                      for ship in fg_util.ShipsInFG(fg,fac):
                          import faction_ships
                          if faction_ships.isCapital(ship[0]):
                              numcaps+=ship[1]
                          else:
                              numfighters+=ship[1]
            if (numcaps or numfighters):
                ret[sys[len(sector)+1:]]+=[(f[0][0].upper(),numcaps,numfighters)]
            if (numcaps and printout):
               print str(f[0][0].upper())+": cap:"+str(numcaps)+" f: "+str(numfighters)
            elif (numfighters and printout):
               print str(f[0][0].upper())+":       f: "+str(numfighters)
   return ret
def InvertSector(inp):
    ret={}
    for sec in inp:
        for k in inp[sec]:
           if k[0] in ret:
              ret[k[0]][0]+=k[1]
              ret[k[0]][1]+=k[2]
           else:
              ret[k[0]]=[k[1],k[2]]
    return ret
def InvertSystem(inp):
    ret={}
    for sec in inp:
        for k in inp[sec]:
           if k[0] in ret:
              ret[k[0]].append(sec)
           else:
              ret[k[0]]=[sec]
    return ret
def Simulate(turns, increment):
    fac=[["confed","militia","hunter"],["merchant"],["kilrathi"],["pirates"],["retro"]]
    ret=[fgsInSector("Gemini",fac)]
    for i in range (turns):
        import dynamic_battle
        for j in range(int(increment*72000)):#20 simulation atoms per second
            dynamic_battle.UpdateCombatTurn()
        ret.append(fgsInSector("Gemini",fac))
    return ret

def GetFactionName(index):
   return _factions[index]
def GetFactionIndex(name):
   if (name in _factions):
      return _factions.index(name)
   return 0
def GetRelation(myfac,theirfac):
	import faction_ships
	try:
		myn=faction_ships.factionToInt(myfac)
		enn=faction_ships.factionToInt(theirfac)
		if enn in faction_ships.enemies[myn]:
			return -1
		if enn in faction_ships.friendlies[myn]:
			return 1
		return 0
	except:
		print 'bad faction'+myfac + theirfac 
		import vsrandom
		return vsrandom.uniform(-1,1)
def AdjustRelation(myfac,theirfac,val):
   print "AdjustRelation"
def GetNumFactions():
   return len(_factions) 
   return 0
_gametime=0
def GetGameTime():
   global _gametime
   _gametime+=.1
   return _gametime
def SetTimeCompression(val):
   print "SetTimeCompression"
def GetAdjacentSystem(mystr,which):
   return universe[mystr]["jumps"][which]

def GetGalaxyFaction(sysname):
   import faction_ships
   import vsrandom
   if sysname in universe:
       return universe[sysname]["faction"]
   return "confed"
def GetGalaxyProperty(sysname,prop):
	if (prop=='faction'):
		return GetGalaxyFaction(sysname)
	if sysname in universe:
		if prop in universe[sysname]:
			return universe[sysname][prop]
	print "error property "+prop+" not in universe "+sysname
	return ""
def SetGalaxyFaction(sysname,faction):
	print faction+' took over '+sysname
	if sysname in universe:
		universe[sysname]["faction"]=faction
	else:
		print "error "+sysname+" does not exist"
def GetNumAdjacentSystems(mystr):
	if mystr in universe:
		return len(universe[mystr]["jumps"])
	return 0
def musicAddList(mystr):
   print "musicAddList" 
   return 0
def musicSkip ():
   pass
def getCurrentPlayer ():
   import vsrandom
   return vsrandom.randrange(0,2)
def musicLoopList (numloops):
   pass
def musicPlaySong(mysong):
   print "musicPlaySong"
def musicPlayList(mylist):
   bleh = int (mylist)
   print "musicPlayList"
_difficulty=.88
def LoadMission (whichmission):
   temp = str(whichmission)
def LoadMissionScript (whichmission):
   temp = str(whichmission)
def GetDifficulty():
   return _difficulty
def SetDifficulty(diff):
   print "SetDifficulty"
   global _difficulty
   _difficulty=diff
def playSound(soundName,loc,speed):
   print "playSound"
def playAnimation(aniName,loc,size):
   print "playAnimation"
def playAnimationGrow(aniName,loc,size,growth):
   print "playAnimationGrow"
def terminateMission(success):
   print "terminateMission"
def getPlayer():
   print "getPlayer" 
   return _unitlist[0]
def getPlayerX(which):
   print "getPlayerX" 
   return _unitlist[which]
def getNumPlayers():
   print "getNumPlayers" 
   return 2
_objectives=[]
def addObjective(name):
   print "addObjective" 
   _objectives+=[name]
   return len(_objectives)-1
def setObjective(which,name):
   print "setObjective"
   _objectives[which]=name
def SafeEntrancePoint(vec,dist):
   return vec
def setCompleteness(which, compl):
   bleh = float(compl)
   print "setCompleteness"
   setObjective (which,_objectives[which])
def getCompleteness(which):
   setObjective (which,_objectives[which])
   print "getCompleteness" 
   import vsrandom
   return vsrandom.randrange(0,3)*.5
def setOwner(which,un):
   print "setOwner"
def getOwner(which):
   print "getOwner" 
   return _unitlist[0]
def IOmessage(time,fr,to,message):
   sys.stderr.write("IOmessage [printed in %f seconds; from %s to %s: '%s']\n" % (time,fr,to,message))
def numActiveMissions():
   import vsrandom
   return vsrandom.randrange(1,3)
def GetMasterPartList():
   print "GetMasterPartList" 
   return Unit("master_part_list")
def GetContrabandList(faction):
   print "GetContrabandList" 
   return Unit("master_part_list","updates")
def SetAutoStatus(glob,playa):
   print "SetAutoStatus"
def string ():
  return ''
def unorNone():
  import vsrandom
  if (vsrandom.randrange(0,6)):
    return _unitlist[vsrandom.randrange(0,len(_unitlist))]
  else:
    return None
class Unit:
  def __init__(self,nam='noname',fg='fgname'):
    self.name=nam
    self.fg=fg
    print 'Unit constructor called with '+nam
  def getUnitSystemFile(self):
    print "getUnitSystemFile"
    return getSystemFile()
  def AutoPilotTo(self,un,ignore_friendlies): 
   print "AutoPilotTo" 
   return 0
  def SetTurretAI(self): 
   print "SetTurretAI"
  def DisableTurretAI(self): 
   print "DisableTurretAI"
  def leach(self,XshieldPercent,YrechargePercent,ZenergyPercent): 
   print "leach"
  def getFgSubnumber(self):
   print "getFgSubnumber" 
   return -1
  def getFgID(self):
   print "getFgID" 
   return self.name
  def setFullname(self,name): 
   print "setFullname"
  def getFullname(self):
   print "getFullname" 
   return self.name+'_hi'
  def getFullAIDescription(self):
   print "getFullAIDescription" 
   return 'default'
  def setTargetFg(self,primary,secondary,tertiary): 
   print "setTargetFg"
  def ReTargetFg(self,which_target): 
   print "ReTargetFg"
  def isStarShip(self):
   print "isStarShip" 
   return 0
  def isPlanet(self):
   print "isPlanet" 
   return 0
  def isJumppoint(self):
   print "isJumppoint" 
   return 0
  def isEnemy(self,other): 
   print "isEnemy" 
   return 0
  def isFriend(self,other): 
   print "isFriend" 
   return 0
  def isNeutral(self,other): 
   print "isNeutral" 
   return 0
  def getRelation(self,other): 
   print "getRelation" 
   return 0
  def ToggleWeapon(self,Missile): 
   print "ToggleWeapon"
  def SelectAllWeapon(self,Missile): 
   print "SelectAllWeapon"
  def Split(self,level): 
   print "Split"

  def Init(self): 
   print "Init"
  def ActivateJumpDrive(self,destination): 
   print "ActivateJumpDrive"
  def DeactivateJumpDrive(self): 
   print "DeactivateJumpDrive"
  def Destroy(self): 
   print "Destroy"
  def LocalCoordinates(self,un): 
   print "LocalCoordinates" 
   return (0,0,0)
  def InRange(self,target,cone,cap): 
   print "InRange" 
   return 0
  def CloakVisible(self):
   print "CloakVisible" 
   return 0
  def Cloak(self,cloak): 
   print "Cloak"
  def RemoveFromSystem(self): 
   print "RemoveFromSystem"
  def PositionITTS(self,local_posit,vel,speed): 
   print "PositionITTS" 
   return (0,0,0)
  def Position(self):
   print "Position" 
   return (0,0,0)
  def LocalPosition(self):
   print "LocalPosition" 
   return (0,0,0)

  def Threat(self):
   print "Threat" 
   import vsrandom
   return _unitlist[vsrandom.randrange(0,len(_unitlist))]
  def TargetTurret(self,targ): 
   print "TargetTurret"
  def getSubUnits(self):
   print "getSubUnits" 
   return 0
  def Threaten(self,targ,danger): 
   print "Threaten"
  def ResetThreatLevel(self): 
   print "ResetThreatLevel"
  def Fire(self,Missile): 
   print "Fire"
  def UnFire(self): 
   print "UnFire"
  def computeLockingPercent(self):
   print "computeLockingPercent" 
   return 0
  def FShieldData(self):
   print "FShieldData" 
   return 0
  def RShieldData(self):
   print "RShieldData" 
   return 0
  def LShieldData(self):
   print "LShieldData" 
   return 0
  def BShieldData(self):
   print "BShieldData" 
   return 0
  def FuelData(self):
   print "FuelData" 
   return 0
  def EnergyData(self):
   print "EnergyData" 
   return 0
  def GetHull(self):
   print "GetHull" 
   return 0
  def rSize(self):
   print "rSize" 
   return 0
  def getMinDis(self,pnt): 
   print "getMinDis" 
   return 0
  def querySphere(self,start,end,my_unit_radius): 
   print "querySphere" 
   return 0
  def queryBoundingBox(self,origin,direction,err): 
   print "queryBoundingBox" 
   return 0
  def PrimeOrders(self): 
   print "PrimeOrders"
  def LoadAIScript(self,aiscript): 
   print "LoadAIScript"
  def LoadLastPythonAIScript(self):
   print "LoadLastPythonAIScript" 
   return 0
  def EnqueueLastPythonAIScript(self):
   print "EnqueueLastPythonAIScript" 
   return 0
  def SetPosition(self,pos): 
   print "SetPosition"
  def SetCurPosition(self,pos): 
   print "SetCurPosition"
  def SetPosAndCumPos(self,pos): 
   print "SetPosAndCumPos"
  def Rotate(self,axis): 
   print "Rotate"
  def ApplyForce(self,Vforce): 
   print "ApplyForce"
  def ApplyLocalForce(self,Vforce): 
   print "ApplyLocalForce"
  def Accelerate(self,Vforce): 
   print "Accelerate"
  def ApplyTorque(self,Vforce,Location): 
   print "ApplyTorque"
  def ApplyBalancedLocalTorque(self,Vforce,Location): 
   print "ApplyBalancedLocalTorque"
  def ApplyLocalTorque(self,torque): 
   print "ApplyLocalTorque"
  def DealDamageToHull(self,pnt,Damage): 
   print "DealDamageToHull" 
   return 0
  def ClampThrust(self,thrust,afterburn): 
   print "ClampThrust" 
   return (0,0,0)
  def Thrust(self,amt,afterburn): 
   print "Thrust"
  def LateralThrust(self,amt): 
   print "LateralThrust"
  def VerticalThrust(self,amt): 
   print "VerticalThrust"
  def LongitudinalThrust(self,amt): 
   print "LongitudinalThrust"
  def ClampVelocity(self,velocity,afterburn): 
   print "ClampVelocity" 
   return (0,0,0)
  def ClampAngVel(self,vel): 
   print "ClampAngVel" 
   return (0,0,0)
  def ClampTorque(self,torque): 
   print "ClampTorque" 
   return (0,0,0)
  def SetOrientation(self,q,r): 
   print "SetOrientation"
  def UpCoordinateLevel(self,v): 
   print "UpCoordinateLevel" 
   return (0,0,0)
  def DownCoordinateLevel(self,v): 
   print "DownCoordinateLevel" 
   return (0,0,0)
  def ToLocalCoordinates(self,v): 
   print "ToLocalCoordinates" 
   return (0,0,0)
  def ToWorldCoordinates(self,v): 
   print "ToWorldCoordinates" 
   return (0,0,0)
  def GetAngularVelocity(self):
   print "GetAngularVelocity" 
   return (0,0,0)
  def GetVelocity(self):
   print "GetVelocity" 
   return (0,0,0)
  def SetVelocity(self,v): 
   print "SetVelocity"
  def SetAngularVelocity(self,v): 
   print "SetAngularVelocity"
  def GetMoment(self):
   print "GetMoment" 
   return 0
  def GetMass(self):
   print "GetMass" 
   return 0
  def LockMissile(self):
   print "LockMissile" 
   return 0
  def EjectCargo(self,index): 
   print "EjectCargo"
  def PriceCargo(self,s): 
   print "PriceCargo" 
   return 0
  def numCargo(self):
   print "numCargo" 
   return 0
  def IsCleared(self,dockingunit): 
   print "IsCleared" 
   return 0
  def ImportPartList(self,category,price,pricedev,quantity,quantdev): 
   print "ImportPartList"
  def RequestClearance(self,dockingunit): 
   print "RequestClearance" 
   return 0
  def isDocked(self,dockingUnit): 
   print "isDocked" 
   return 0
  def Dock(self,unitToDockWith): 
   print "Dock" 
   return 0
  def UnDock(self,unitToDockWith): 
   print "UnDock" 
   return 0
  def GetNumMounts(self):
   print "GetNumMounts" 
   return 0

  def JumpTo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "JumpTo" 
   return 0
  def getFactionName(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   import faction_ships
   import vsrandom
   return faction_ships.factions[vsrandom.randrange(0,len(faction_ships.factions)-1)]
  def getFactionIndex(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   return 0
  def setFactionName(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "setFactionName"
  def setFactionIndex(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "setFactionIndex"
  def getName(self):
   return self.name
  def getFlightgroupName(self):
   print "getFlightgroupName" 
   return self.fg
  def getFgDirective(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getFgDirective" 
   return ''
  def getFlightgroupLeader(self):
   print "getFlightgroupLeader"
   names=[]
   for i in _unitlist:
      if i.fg==self.fg:
          names+=[i]
   import vsrandom
   leng=len(names)
   if (leng):
     return names[vsrandom.randrange(0,leng)]
   return self
  def addCredits(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "addCredits"
  def switchFg(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "switchFg"
  def getCredits(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getCredits" 
   return 0
  def setFlightgroupLeader(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "setFlightgroupLeader" 
   return 0
  def setFgDirective(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "setFgDirective" 
   return 0
  def getFgSubnumber(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getFgSubnumber" 
   return -1
  def isSignificant(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "isSignificant" 
   return 0
  def isSun(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "isSun" 
   return 0
  def communicateTo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "communicateTo" 
   return 0
  def commAnimation(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "commAnimation" 
   return 0
  def removeCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "removeCargo" 
   return 0
  def upgrade(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "upgrade" 
   return 0
  def addCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "addCargo" 
   return 0
  def getDistance(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getDistance" 
   return 0
  def incrementCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "incrementCargo" 
   return 0
  def decrementCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "decrementCargo" 
   return 0
  def getSignificantDistance(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "getSignificantDistance" 
   return 0
  def isPlayerStarship(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "isPlayerStarship" 
   return -1
  def hasCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "hasCargo" 
   return 0
  def GetCargo(a=None,b=None,c=None,d=None,e=None,f=None,g=None,h=None,i=None,j=None): 
   print "GetCargo" 
   return Cargo("","",1,1,1,1)
# 351 "unit_wrapper.cpp" 2

  def __eq__(self,oth): 
   print "__eq__" 
   return 0;
  def __ne__(self,oth): 
   print "__ne__" 
   return 1;
  def Kill(self): 
   print "Kill";
  def setNull(self): 
   print "setNull";
  def __nonzero__(self):
   import vsrandom
   return vsrandom.randrange(0,2);
  def isNull(self):
   import vsrandom
   return vsrandom.randrange(0,2);
  def SetTarget(self,un): 
   print "SetTarget";
  def GetTarget(self):
   print "GetTarget"
   return unorNone()
  def GetVelocityReference(self):
   print "GetVelocityReference" 
   return unorNone()
  def SetVelocityReference(self,un): 
   print "SetVelocityReference";
  def GetOrientation(self):
   print "GetOrientation" 
   return ((1,0,0),(0,1,0),(0,0,1))
  def queryBSP(self,start,end): 
   print "queryBSP" 
   return (un,(0,0,1),0)
  def cosAngleToITTS(self,un,speed,range): 
   print "cosAngleToITTS" 
   return (.95,10000)
  def cosAngleTo(self,un): 
   print "cosAngleTo" 
   return (.93,10000)
  def cosAngleFromMountTo(self,un): 
   print "cosAngleFromMountTo" 
   return (.93,10000)
  def getAverageGunSpeed(self):
   print "getAverageGunSpeed" 
   return (200,10000)
  def InsideCollideTree(self,un): 
   print "InsideCollideTree" 
   return ((0,0,0),(0,0,1),(0,0,0),(0,1,0))
  def getSubUnit(self,which): 
   print "getSubUnit" 
   return unorNone()

class un_iter:
  def __init__(self):
     pass
  def current(self):
    return unorNone()
  def advance(self): 
    pass
  def next(self):
    self.advance()
    return self.current()
  def remove(self): 
   print "remove"
  def preinsert(self,un): 
   print "preinsert"

class Cargo:
  def __init__ (self,a,b,c,d,e,f):
    print 'Cargo constructor called with (self,%s,%s,%f,%d,%f,%f)' % (a,b,c,d,e,f)
  def SetPrice(self,price): 
   print "SetPrice"
  def GetPrice(self):
   print "GetPrice" 
   return 1
  def SetMass(self,mass): 
   print "SetMass"
  def GetMass(self):
   print "GetMass" 
   return 1
  def SetVolume(self,volume): 
   print "SetVolume"
  def GetVolume(self):
   print "GetVolume" 
   return 1
  def SetQuantity(self,quantity): 
   print "SetQuantity"
  def GetQuantity(self):
   print "GetQuantity" 
   return 1
  def SetContent(self,content): 
   print "SetContent"
  def GetContent(self):
   print "GetContent" 
   return "weapons"
  def SetCategory(self,category): 
   print "SetCategory"
  def GetCategory(self):
   print "GetCategory" 
   import vsrandom
   if vsrandom.randrange(0,2)==0:
    return "Contraband"
   return "Medical"
  def SetMissionFlag(self,flag): 
   print "SetMissionFlag"
  def GetMissionFlag(self):
   print "GetMissionFlag" 
   return 0

  def GetCategory(self):
   print "GetCategory" 
   return "contraband"
  def GetDescription(self):
   print "GetDescription" 
   return ""

class PythonAI:
  def init(self,un):
   print "init"
  def Execute(self): 
   print "Execute"
  def GetParent(self):
   print "GetParent" 
   import vsrandom
   return _unitlist[vsrandom.randrange(0,len(_unitlist))]
  def __init__(self):
    print 'PythonAI constructor called with (self)'
    self.init(Unit('noname'))
  def AddReplaceLastOrder(self,replace): 
   print "AddReplaceLastOrder"
  def ExecuteLastScriptFor(self,time): 
   print "ExecuteLastScriptFor"
  def FaceTarget(self,end): 
   print "FaceTarget"
  def FaceTargetITTS(self,end): 
   print "FaceTargetITTS"
  def MatchLinearVelocity(self,terminate,vec,afterburn,local): 
   print "MatchLinearVelocity"
  def MatchAngularVelocity(self,terminate,vec,local): 
   print "MatchAngularVelocity"
  def ChangeHeading(self,vec): 
   print "ChangeHeading"
  def ChangeLocalDirection(self,vec): 
   print "ChangeLocalDirection"
  def MoveTo(self,Targ,afterburn): 
   print "MoveTo"
  def MatchVelocity(self,terminate,vec,angvel,afterburn,local): 
   print "MatchVelocity"
  def Cloak(self,enable,seconds): 
   print "Cloak"
  def FormUp(self,pos): 
   print "FormUp"
  def FaceDirection(self,distToMatchFacing,finish): 
   print "FaceDirection"
  def XMLScript(self,script): 
   print "XMLScript"
  def LastPythonScript(self): 
   print "LastPythonScript"

_unitlist = [Unit("me","blue"),Unit("him","gold")]
