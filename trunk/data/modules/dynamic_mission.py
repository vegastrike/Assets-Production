import VS
import Director
import fg_util
import vsrandom


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

def SimulatedDukeItOut (fgname,faction,enfgname,enfaction):
	ally=fg_util.LandedShipsInFG(fgname,faction)
	enemy=fg_util.LandedShipsInFG(enfgname,enfaction)
	#roll z'dice
def countTn (l):
	count=0
	for i in l:
		count+=i[1]
	return count

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
		pass
	else:
		pass
	
	
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
		pass

	

def contractMissionsFor(fac,minsysaway,maxsysaway):
	fac=faction_ships.intToFaction()
	enemies = list(faction_ships.enemies[fac])
	script=''
	while len(enemies):
		index=vsrandom.randrange(0,len(enemies))
		script=contractMissionForTo(fac,enemies[index],minsysaway,maxsysaway)
		if (script):
			return script
		del enemies[index]
	return script

#Credit to Peter Trethewey, master of python and all things nefarious
def getSystemsKAwayNoFaction( start, k ):
	set = [start]#set of systems that have been visited
	pathset = [[start]]#parallel data structure to set, but with paths
	pathtor = [[start]]#parallel data structure to raw return systems with path
	r = [start] #raw data structure containing systems n away where n<=k
	for n in range(0,k):
		set.extend(r)
		pathset.extend(pathtor)
		r=[]
		pathtor=[]
		for iind in range(len(set)):
			i = set[iind]
			l = universe.getAdjacentSystemList(i)
			for jind in range(len(l)):
				j=l[jind]
				if not (j in set or j in r):
					r.append(j)
					pathtor.append(pathset[iind]+[j])
	return pathtor

def getSystemsNAway (start,preferredfaction):
	l = getSystemsKAwayNoFaction(start,k)
	if (preferredfaction==None):
		return l
	lbak=l
	if (preferredfaction==''):
		preferredfaction=VS.GetGalaxyFaction(start)
	i=0
	while i <len(l):
		if (VS.GetRelation(preferredfaction,VS.GetGalaxyFaction(l[i][-1]))<0):
			del l[i]
			i-=1
		i+=1
	if (len(l)):
		return l
	return lbak

def contractMissionForTo (fac,enemy,minsysaway,maxsysaway):
	script=''
	cursystem = VS.getSystemFile()
	thisfaction = VS.GetGalaxyFaction (cursystem)
	preferredfaction=None
	if (VS.GetRelation (fac,thisfaction)>0):
		preferredfaction=fac#try to stay in this territory
	for i in range (minsysaway,maxsysaway+1):
		for j in getSystemsNAway(cursystem,i,preferredfaction):
			pass
	return script
