import VS
import Director
import fg_util
import vsrandom
import faction_ships
#hashed by system, then contains lists of pairs of (flightgroup,faction) pairs
persystemattacklis= {}

attacklist ={}#hashtable mapping (attackfg,attackfaction):(defendfg,defendfaction)
defendlist={}#hashtable mapping (defendfg,defendfaction):(attackfg,attackfaction)
def UpdateCombatTurn():
	numfac=VS.GetNumFactions()
	for i in range (numfac):
		fac = VS.GetFactionName(i)
		LookForTrouble (fac)
		Siege(fac)
	SimulateBattles();
def Siege(fac):
	turns_till_siege_effective=100
	numfg= fg_util.NumAllFlightgroups(fac)
	if (numfg):
		prob = float(numfg)/float(turns_till_siege_effective);
		numtimes = int (prob)
		if (numtimes==0):
			numtimes=1
		else:
			prob =1
		for i in range(numtimes):
			if (vsrandom.uniform(0,1)<prob):
				fg =fg_util.RandomFlightgroup(fac)
				sys = fg_util.FGSystem(fg,fac)
				enfac=VS.GetGalaxyFaction(sys)
				if (VS.GetRelation(fac,enfac)<0):#FIXME maybe even less than that
					if (fg_util.NumFactionFGsInSystem(enfac,sys)==0):
						VS.SetGalaxyFaction(sys,fac)
						print fac + ' took over '+ sys + ' originally owned by '+enfac
						#ok now we have him... while the siege is going on the allies had better initiate the battle--because we're now defending the place...  so that means if the owners are gone this place is ours at this point in time #FIXME write news story!!!
					
					
					
				
	
	
def SimulateBattles():
	deadbattles=[]
	global persystemattacklist
	global attacklist
	persystemattacklist = {}
	for ally in attacklist:
		enemy = attacklist[ally]		
		if (not attackFlightgroup (ally[0],ally[1],enemy[0],enemy[1])):
			deadbattles+=[ally]
		else:
			sys = fg_util.FGSystem(ally[0],ally[1])
			if not (sys in persystemattacklist):
				persystemattacklist[sys]=[]
			persystemattacklist[sys]+=[(ally,enemy)]#continue the battle
	for i in deadbattles:
		stopAttack(i[0],i[1])
def BattlesInSystem():
	if sys in persystemattacklist:
		return persystemattacklist[sys]
	#return {}  #used to be  a hash table
	return []
def LookForSystemWideTrouble(faction,sys):
	fg = fg_util.FGsInSystem(faction,sys)
	for i in fg:
		enemyfac = faction_ships.get_enemy_of (faction)
		efg = fg_util.AllFGsInSystem(enemy,sys)
		if (len(efg)):
			index=vsrandom.randrange(0,len(efg))#FIXME include some sort of measure "can I win"
			initiateAttack(fg,faction,sys,efg[index],enemyfac)

def randomMovement(fg,fac):
	import universe
	import fg_util
	sys=fg_util.FGSystem(fg,fac)
	if (sys!='no_sector/no_system' and fg!=fg_util.BaseFGInSystemName(sys)):
		l = universe.getAdjacentSystemList(sys)
		if (len(l)):
			newsys = l[vsrandom.randrange(0,len(l))]
#			print 'moving '+fg+' from '+sys+' to '+ newsys
			fg_util.TransferFG( fg,fac,newsys);

def LookForTrouble (faction):
	for i in fg_util.AllFlightgroups (faction):
		sys = fg_util.FGSystem (i,faction)
		enfac = faction_ships.get_enemy_of(faction)
		foundanyone=False
		for j in fg_util.AllFGsInSystem(enfac,sys):
			foundanyone=True
			#FIXME include some sort of measure "can I win"
			if (vsrandom.randrange(0,5)==0):
				initiateAttack(i,faction,sys,j,enfac)
		if (foundanyone==False and vsrandom.randrange(0,3)==0):
			randomMovement (i,faction)

def StopTargettingEachOther (fgname,faction,enfgname,enfaction):
	i=VS.getUnitList()
	un=i.current()
	while (un):
		if ((un.getFactionName()==enfaction and un.getFlightgroupName()==enfgname) or
			(un.getFactionName()==faction and un.getFlightgroupName()==fgname)):
			un.SetFgDirective ('b')
		#check to see that its' in this flightgroup or something :-)
		un=i.next()

def TargetEachOther (fgname,faction,enfgname,enfaction):
	i=VS.getUnitList()
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
	fg_util.RemoveShipFromFG(fg,enfac,tn[0],1)

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
	return i[1]
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
	if len(shiplaunchlist):
		pos=findLaunchedShipInFGInSystem (fgname,faction).GetPosition()
	for i in shiplaunchlist:
		while j in range (i[1]):
			pos=launch_recycle.LaunchNext(fgname,faction,"default",pos)

						 
def LaunchEqualShips (fgname, faction, enfgname, enfaction):
	land=fg_util.LandedShipsInFG(fgname,faction)
	launch=fg_util.ShipsInFG(fgname,faction)
	enland=fg_util.LandedShipsInFG(enfgname,enfaction)
	enlaunch=fg_util.ShipsInFG(enfgname,enfaction)
	numenland=countTn(enland)
	numenlaunch=countTn(enlaunch)
	numland=countTn(land)
	numlaunch=countTn(launch)
	if (numenland==0 or numland==0 or (numlaunch==0 and numenlaunch==0) ):
		return
	if (numlaunch/numland > numenlaunch/numenland):
		LaunchMoreShips (fgname,faction,land,int((numland*numenlaunch/numenland)-numlaunch))
	else:
		LaunchMoreShips (enfgname,enfaction,enland,int((numenland*numlaunch/numland)-numenlaunch))		
	
def stopAttack (fgname,faction):
	ally=(fgname,faction)
	if ally in attacklist:
		enemy = attacklist[ally]
		sys = fg_util.FGSystem (fgname,faction)
		if (VS.systemInMemory(sys)):
			VS.pushSystem(sys)
			StopTargettingEachOther(fgname,faction,enemy[0],enemy[1])
			VS.popSystem()
		del defendlist[enemy]
		del attacklist[ally]
		

def initiateAttack (fgname,faction,sys,enfgname,enfaction):
	if (fg_util.BaseFGInSystemName(sys)==fgname):
		fg=(enfgname,enfaction)#this is for a base... self defence
		efg=(fgname,faction)
	else:
		fg = (fgname,faction)
		efg = (enfgname,enfaction)
	#FIXME  can overwrite the attacking groups!!
	if (not efg in defendlist):
		if (fg in attacklist):
			del defendlist[attacklist[fg]]
		attacklist[fg]=efg
		defendlist[efg]=fg

#only works for FG's that are not the base FG...the base FG cannot initiate attacks as far as I know.
#though initiateAttack switches them around appropriately
def attackFlightgroup (fgname, faction, enfgname, enfaction):
	sys = fg_util.FGSystem (fgname,faction)
	ensys = fg_util.FGSystem (enfgname,enfaction)
	if (sys==ensys):
		if (VS.systemInMemory(sys)):
			VS.pushSystem(sys)
			LaunchEqualShips (fgname,faction,enfgname,enfaction)
			TargetEachOther (fgname,faction,enfgname,enfaction)
			VS.popSystem()
		SimulatedDukeItOut (fgname,faction,enfgname,enfaction)
	else:
		#pursue other flightgroup
		import universe
		adjSystemList=universe.getAdjacentSystemList(sys)
		if ensys in adjSystemList:
			fg_util.TransferFG (fgname,faction,ensys)
		else:
			return 0
	if (vsrandom.randrange(0,4)==0):
		#FIXME  if it is advantageous to stop attacking only!!
		return 0
	if (vsrandom.randrange(0,4)==0 and enfgname!=fg_util.BaseFGInSystemName(ensys)):
		#FIXME  if it is advantageous to run away only
		num=VS.GetNumAdjacentSystems(ensys)
		if (num>0):
			ensys=VS.GetAdjacentSystem(ensys,vsrandom.randrange(0,num))
			fg_util.TransferFG (fgname,faction,ensys)
	return 1
		

