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

syscreds=500

def processSystem(sys):
	k= sys.split('/')
	if (len(k)>1):
		k=k[1]
	else:
		k=k[0]
	return k.capitalize()
def writemissionname(name,path):
	pass
def writedescription(name):
	pass
def writemissionsavegame (name):
	pass
def generatePatrolMission (path, numplanets):
	dist=1000
	creds = numplanets*500
	writemissionsavegame ("import patrol\ntemp=patrol.patrol(0, %d, %d, %d, %s)\ntemp=0\n"%(numplanets, dist, creds, str(path)))
	writedescription("Insystem authorities would like a detailed scan of the %s system. We require %d nav locations be visited on the scanning route.  The pay for this mission is %d."%(processSystem(path[-1]),numplanets,creds))
	writemissionname("Patrol_%d_Points_in_%s"%(numplanets,processSystem(path[-1])),path[-1])	


def generateEscortMission (path,fg,fac):
	###
	typ = fg_util.RandomShipIn(fg,fac)
	diff=vsrandom.randrange(0,6)	
	creds=500*diff+1.2*syscreds*len(path)
	writemissionsavegame ("import escort_mission\ntemp=escort_mission.escort_mission('%s', %d, %d, %g, 0, %s, '','%s','%s')\ntemp=0\n"%(fac, diff, creds, str(path),fg,typ))
	writedescription("The %s %s in the %s flightgroup requres an escort to %s. The reward for a successful escort is is %d."%(fac,typ,fg, processSystem(path[-1]),creds))
	writemissionname("Escort_%s_to_%s"%(fac,processSystem(path[-1])),path[-1])	

def generateCargoMission (path, category, fac):
	numcargos=vsrandom.randrange(1,15)
	if numcargos>10:
		numcargos=10
	diff=vsrandom.randrange(0,6)
	launchcap=(vsrandom.random()>=.75)
	creds=250*numcargos+500*diff+syscreds*len(path)+1000*(category.lower()=="contraband")
	writemissionsavegame ("import cargo_mission\ntemp=cargo_mission.cargo_mission('%s', 0, %d, %d, %g, %d, 0, '%s', %s, '')\ntemp=0\n"%(fac, numcargos, diff, creds, launchcap, category, str(path)))
	writedescription("We need to deliver some %s cargo to the %s system. The mission is worth %d to us.  You will deliver it to a base owned by the %s"%(category, processSystem(path[-1]),creds,fac))
	writemissionname("Deliver_%s_to_%s"%(category,processSystem(path[-1])),path[-1])

def generateBountyMission (path,fg,fac):
	typ = fg_util.RandomShipIn(fg,fac)
	cap = faction_ships.isCapital(typ)
	diff=vsrandom.randrange(0,6)
	runaway=(vsrandom.random()>=.75)
	creds=1000+2000*runaway+500*diff+syscreds*len(path)
	if (cap):
		creds*=40
	finalprice=creds+syscreds*len(path)
	writemissionsavegame("import bounty\ntemp=bounty.bounty(0, 0, %g, %d, %d, '%s', %s, '%s','%s')\ntemp=0\n"%(finalprice, runaway, diff, fac, str(path), fg,typ))
	writedescription("A %s starship in the %s flightgroup has been harassing operations in the %s system. Reward for the termination of said ship is %d credits."%(typ,fg, processSystem(path[-1]), finalprice))
	if (cap):
		writemissionname ("Bounty_on_%s_Capital_Vessel"%fac,path[-1])
	else:
		writemissionname ("Bounty_on_%s_starship"%fac,path[-1])

def generateDefendMission (path,defendfg,defendfac, attackfg,attackfac):
	defendtyp = fg_util.RandomShipIn(defendfg,defendfac)
	attacktyp = fg_util.RandomShipIn(attackfg,attackfac)			
	isbase=fg_util.BaseFGInSystemName(path[-1])==defendfg
	creds=1000
	minq = 1
	maxq = 8
	quantity = vsrandom.randrange(minq,maxq)
	reallydefend = "True"
	if (vsrandom.randrange(0,4)==0):
		reallydefend="False"
	writemissionsavegame("import defend\ntemp=defend.defend('%s', %d, %d, 8000.0, 100000.0, %g, %s, %d, '%s', %s, '%s', '%s', '%s', '%s')\ntemp=0\n"%
	                     (attackfac, 0, quantity, creds*quantity+syscreds*len(path), reallydefend, isbase, defendfac, str(path), attacktyp,attackfg, defendtyp, defendfg))
	iscapitol=""
	if isbase:
		iscapitol="capitol "
	writedescription("A %s assault wing named %s has jumped in and is moving for an attack on one of our %sstarships, a %s, in the %s system.\nYour task is to eradicate them before they eliminate our starship.\nIntelligence shows that they have starships of type %s. Your reward is %d credits per fighter."%(attackfac, attackfg, iscapitol, defendtyp, processSystem(path[-1]), attacktyp,creds))
	writemissionname("Defend_%s_from_%s"%(defendfac, attackfac),path[-1])

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
			if preferredfaction:
				for k in faction_ships.enemies[faction_ships.factiondict[thisfaction]]:
					for m in fg_util.FGsInSystem(k,j[-1]):
						if (vsrandom.randrange(0,4)==0):#fixme betterthan 4
							generateBountyMission(j,m,k)
				m = FGsInSystem ("merchant",j[-1])
				nummerchant=len(m)
				m+=FGsInSystem (thisfaction,j[-1])
				numthisfac=len(m)
				m+=FGsInSystem (fac,j[-1])
				
				numescort = vsrandom.randrange(0,10)
				if (numescort>len(m)):
					numescort=len(m)
				for k in range(numescort):
					f = "merchant"
					if f>=nummerchant:
						f= thisfaction
					if f>=numthisfac:
						f = fac
					generateEscortMission(j,k,f)
			for k in range(vsrandom.randrange(1,4)): ###FIXME: choose a better number than 4.
				if (rnd<.18):    # 18% - Patrol mission
					generatePatrolMission(maxsysaway, minsysaway,vsrandom.randrange(4,10))
				elif (rnd<.41):  # 23% - Cargo mission
					generateCargoMission(path,true)
				elif (fac=='pirates'): # 5% - Contraband mission (cargo contraband)
					generateCargoMission(path,false)
				else:            #  5% - Scout mission (patrol one planet)
					generatePatrolMission(path,1)

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
