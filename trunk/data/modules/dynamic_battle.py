import VS
import Director
import fg_util
import vsrandom
class FG:
	def __init__(self,fgname,faction):
		self.fg=fgname
		self.fac=fact		

#hashed by system, then by 
persystemattacklist {}

attacklist ={}
defendlist={}
def SimulateBattles():
	deadbattles=[]
	global persystemattacklist
	global attacklist
	persystemattacklist = {}
	for ally in attacklist:
		enemy = attacklist[ally]		
		if (not attackFlightgroup (ally.fg,ally.fac,enemy.fg,enemy.fac)):
			deadbattles+=[ally]
		else:
			sys = fg_util.FGSystem(ally.fg,ally.fac)
			#if not (sys in persystemattacklist):
			#	persystemattacklist[sys]={}#used to be a haash table in BattlesInSystem
			#(persystemattacklist[sys])[ally]=enemy
			persystemattacklist[sys]+=[(ally,enemy)]
	for i in deadbattles:
		stopAttack(i)
def BattlesInSystem():
	if sys in persystemattacklist:
		return persystemattacklist[sys]
	#return {}  #used to be  a hash table
	return []

def StopTargettingEachOther (fgname,faction,enfgname,enfaction):
	i=getUnitList()
	un=i.current()
	while (un):
		if ((un.getFactionName()==enfaction and un.getFlightgroupName()==enfgname) or
			(un.getFactionName()==faction and un.getFlightgroupName()==fgname)):
			un.SetFgDirective ('b')
		#check to see that its' in this flightgroup or something :-)
		un=i.next()

def TargetEachOther (fgname,faction,enfgname,enfaction):
	i=getUnitList()
	un=i.current()
	en=None
	al=None
	while (un and ((not en) or (not al))):
		if (un.getFactionName()==enfaction and un.getFlightgroupName()==enfgname):
			if ((not en) or (vsrandom.randrange(0,3)==0)):
				en=un
		if (un.getFactionName()==faction and un.getFlightgroupName()==fgname):
			al=un
		un=i.next()
	if (en and al):
		al.setFlightgroupLeader(al)
		al.SetTarget(en)
		al.setFgDirective ('A.')#attack target, darent change target!
		en.setFlightgroupLeader(en)
		en.SetTarget(al)
		en.setFgDirective ('h')#help me out here!
def KillOne (fg,enfac,tn):
	fg_util.RemoveShipFromFG(fg,enfac,tn[0])

def SimulatedDukeItOut (fgname,faction,enfgname,enfaction):
	ally=fg_util.LandedShipsInFG(fgname,faction)
	enemy=fg_util.LandedShipsInFG(enfgname,enfaction)
	#roll z'dice
	#FIXME!!!
	if (len(enemy) or len(ally)):
		rnum=vsrandom.randrange (0,len(ally)+len(enemy))
		if rnum<len(ally):
			KillOne(fgname,faction,ally[rnum])
		else:
			KillOne(enfgname,enfaction,enemy[rnum-len(ally)])
def numShips(i):
	if (faction_ships.isCapital(i[0])):
		return i[1]*10
def countTn (l):
	count=0
	for i in l:
		count+=numShips(i)
	return count
def findLaunchedShipInFGInSystem (fgname,faction):
	uni = VS.getUnitList()
	un=uni.current()
	while (un):
		if (un.getFlightgroupName()==fgname and un.getFactionName()==faction):
			return un
		un= uni.next()
def LaunchMoreShips(fgname,faction,landedtn,nums):
	shiplaunchlist=[]
	while nums>0 and len(landedtn)>0:
		index=vsrandom.randrange(0,len(nt))
		nums-=numShips(landedtn[index])/landedtn[index][1]
		shiplaunchlist += [(landedtn[index][0],1)]
		if (landedtn[index][1]>1):
			landedtn[index]=(landedtn[index][0],landedtn[index][1]-1)
		else:
			del landedtn[index]
	if len(shiplaunchlis):
		pos=findLaunchedShipInFGInSystem (fgname,faction).GetPosition()
	for i in shiplaunchlist:
		while j in range (i[1]):
			pos=launch_recycle.LaunchNext(fgname,faction,"default",pos)

						 
def LaunchEqualShips (fgname, faction, enfgname, enfaction):
	land=LandedShipsInFG(fgname,faction)
	launch=ShipsInFG(fgname,faction)
	enland=LandedShipsInFG(enfgname,enfaction)
	enlaunch=ShipsInFG(enfgname,enfaction)
	numenland=countTn(enland)
	numenlaunch=countTn(enlaunch)
	numland=countTn(land)
	numlaunch=countTn(launch)
	if (enland==0 or land==0 or (launch==0 and enlaunch==0) ):
		return
	if (numlaunch/numland > numenlaunch/numenland):
		LaunchMoreShips (fgname,faction,land,int((numland*numenlaunch/numenland)-numlaunch))
	else:
		LaunchMoreShips (enfgname,enfaction,enland,int((numenland*numlaunch/numland)-numenlaunch))		
	
def stopAttack (fgname,faction):
	ally=FG (fgname,faction)
	if ally in attacklist:
		enemy = attacklist[ally]
		sys = fg_util.FGSystem (fgname,faction)
		if (VS.systemInMemory(sys)):
			VS.pushSystem(sys)
			StopTargettingEachOther(fgname,faction,enemy.fg,enemy.fac)
			VS.popSystem(sys)
		del defendlist[enemy]
		del attacklist[ally]
		

def initiateAttack (fgname,faction,enfgname,enfaction):
	fg = FG(fgname,faction)
	efg = FG(enfgname,enfaction)
	attacklist[fg]=efg
	defendlist[efg]=fg

#only works for FG's that are not the base FG...the base FG cannot initiate attacks as far as I know.
#though eventually we may want to change that
def attackFlightgroup (fgname, faction, enfgname, enfaction):
	sys = fg_util.FGSystem (fgname,faction)
	ensys = fg_util.FGSystem (enfgname,enfaction)
	if (sys==ensys):
		if (VS.systemInMemory(sys)):
			VS.pushStarSystem(sys)
			LaunchEqualShips (fgname,faction,enfgname,enfaction)
			TargetEachOther (fgname,faction,enfgname,enfaction)
			VS.popStarSystem()
		SimulatedDukeItOut (fgname,faction,enfgname,enfaction)
	else:
		#pursue other flightgroup
		adjSystemList=VS.getAdjacentSystemList(sys)
		if ensys in adjSystemList:
			TransferFG (fgname,faction,ensys)
		else:
			return 0
	return 1
		

