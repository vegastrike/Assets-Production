import VS
import Director
import fg_util
import vsrandom

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
