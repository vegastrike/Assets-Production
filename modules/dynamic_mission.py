import VS
import Director
import fg_util
import vsrandom


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

def getSystemsNAway (start,k,preferredfaction):
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

def generatePatrolMission (path, numplanets):
	###

def generateEscortMission (path,fg,fac):
	###

def generateCargoMission (path, contraband):
	###

def generateBountyMission (path,fg,fac):
	###

def generateDefendMission (path,defendfg,defendfac, attackfg,attackfac):
	###

def contractMissionsFor(fac,minsysaway,maxsysaway):
	fac=faction_ships.intToFaction(fac)
	enemies = list(faction_ships.enemies[fac])
	script=''
	cursystem = VS.getSystemFile()
	thisfaction = VS.GetGalaxyFaction (cursystem)
	preferredfaction=None
	if (VS.GetRelation (fac,thisfaction)>0):
		preferredfaction=thisfaction#try to stay in this territory
	l=[]
	for i in range (minsysaway,maxsysaway+1):
		for j in getSystemsNAway(cursystem,i,preferredfaction):
			import dynamic_battle
			try:
				l = dynamic_battle.persystemattacklist
			except:
				l= []
			for k in l:
				if (VS.GetRelation(fac,l[1][1])>0):
					generateDefendMission(j,l[1][0],l[1][1],l[0][0],l[0][1])
			for k in range(vsrandom.randrange(1,4)): ###FIXME: choose a better number than 4.
				pass
		if (rnd<.18):    # 18% - Patrol mission
			generatePatrolMission(maxsysaway, minsysaway,vsrandom.randrange(4,10)):
		elif (rnd<.41):  # 23% - Cargo mission
			generateCargoMission(path,true)
		elif (rnd<.59):  # 18% - Bounty mission
			generateBountyMission(path)
		elif (rnd<.77):  # 18% - Defend mission
			generateDefendMission(path)
		if (rnd<.95):    # 18% - Escort mission
			generateEscortMission(path):
		elif (fac=='pirates'): # 5% - Contraband mission (cargo contraband)
			generateCargoMission(path,false)
		else:            #  5% - Scout mission (patrol one planet)
			generatePatrolMission(path,1)
	return script

def CreateMissions(minsys=1,maxsys=4):
	i=0
	plr=VS.GetPlayer()
	un=VS.GetUnit(i)
	while(un):
		i+=1
		if (un.isDocked(plr)):
			break
		un=VS.GetUnit(i)
	contractMissionsFor(plr.GetFactionNum(),minsys,maxsys)
