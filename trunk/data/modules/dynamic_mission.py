import VS
import Director
import fg_util
import vsrandom
import faction_ships
import universe

plr=0
basefac='neutral'

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
	if len(path)<=1:
		name="In_System_"+name
	Director.pushSaveString(plr, "mission_names", name)
	
def writedescription(name):
	Director.pushSaveString(plr, "mission_descriptions", name)
	
def writemissionsavegame (name):
	Director.pushSaveString(plr, "mission_scripts", name)

def eraseExtras():
	import sys
	len=Director.getSaveStringLength(plr, "mission_scripts")
	if (len!=Director.getSaveStringLength(plr, "mission_names") or len!=Director.getSaveStringLength(plr, "mission_descriptions")):
		sys.stdout.write("Warning: Number of mission descs., names and scripts are unequal.\n")
	if len>0:
		for i in range(len-1,0,-1):
			Director.eraseSaveString(plr, "mission_scripts", i)
			Director.eraseSaveString(plr, "mission_names", i)
			Director.eraseSaveString(plr, "mission_descriptions", i)

fixerpct=0.1

def generatePatrolMission (path, numplanets):
	dist=1000
	creds = numplanets*500
	addstr=""
	isFixer=vsrandom.random()<fixerpct
	if isFixer:
		creds*=2
		addstr+="#F#bases/fixers/confed.spr#Talk to the Confed Officer#Thank you.  Your help makes space a safer place.#\n"
	writemissionsavegame (addstr+"import patrol\ntemp=patrol.patrol(0, %d, %d, %d, %s)\ntemp=0\n"%(numplanets, dist, creds, str(path)))
	writedescription("Insystem authorities would like a detailed scan of the %s system. We require %d nav locations be visited on the scanning route.  The pay for this mission is %d."%(processSystem(path[-1]),numplanets,creds))
	ispoint="s"
	if numplanets==1:
		ispoint=""
	writemissionname("Patrol/Patrol_%d_Point%s_in_%s"%(numplanets,ispoint, processSystem(path[-1])),path)	

def isNotWorthy(fac):
	return VS.GetRelation(fac,VS.getPlayer().getFactionName())<0
def generateEscortMission (path,fg,fac):
	###
	if (isNotWorthy(fac)):
		return
	typ = fg_util.RandomShipIn(fg,fac)
	diff=vsrandom.randrange(0,6)	
	creds=500*diff+1.2*syscreds*len(path)
	addstr=""
	isFixer=vsrandom.random()<fixerpct
	if isFixer:
		creds*=2
		addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust that you will safely guide my collegue until you reach the destination.#\n"
	writemissionsavegame (addstr+"import escort_mission\ntemp=escort_mission.initrandom('%s', %d, %g, 0, 0, %s, '','%s','%s')\ntemp=0\n"%(fac, diff, float(creds), str(path),fg,typ))
	writedescription("The %s %s in the %s flightgroup requres an escort to %s. The reward for a successful escort is is %d."%(fac,typ,fg, processSystem(path[-1]),creds))
	writemissionname("Escort/Escort_%s_to_%s"%(fac,processSystem(path[-1])),path)	

def changecat(category):
	l=category.split('/')
	if len(l)>1:
		return l[-1]+'_'+l[0]
	else:
		return category

def generateCargoMission (path, numcargos,category, fac):
	if (isNotWorthy(fac)):
		return	
	diff=vsrandom.randrange(0,6)
	launchcap=(vsrandom.random()>=.75)
	creds=250*numcargos+500*diff+syscreds*len(path)+5000*(category=="Contraband")+20000*(category=="starships")
	addstr=""
	isFixer=vsrandom.random()<fixerpct
	if isFixer:
		creds*=2
		addstr+="#F#bases/fixers/merchant.spr#Talk to the Merchant#Thank you. I entrust you will make the delivery successfully.#\n"
	writemissionsavegame (addstr+"import cargo_mission\ntemp=cargo_mission.cargo_mission('%s', 0, %d, %d, %g, %d, 0, '%s', %s, '')\ntemp=0\n"%(fac, numcargos, diff, creds, launchcap, category, str(path)))
	if (category==''):
		category='generic'
	writedescription("We need to deliver some %s cargo to the %s system. The mission is worth %d to us.  You will deliver it to a base owned by the %s"%(category, processSystem(path[-1]),creds,fac))
	writemissionname("Cargo/Deliver_%s_to_%s"%(changecat(category),processSystem(path[-1])),path)
def generateRescueMission(path,rescuelist):
	numships = vsrandom.randrange(0,6)
	creds = (numships+len(path))*vsrandom.randrange(2041,3140)
	writemissionsavegame("import rescue\nntemp=rescue.rescue(%d,0,'%s',%d,'%s','%s',%s)\nntemp=0"%(creds,rescuelist[0],numships,rescuelist[2],rescuelist[1],str(path)))
	writedescription("SOS! This is an ejected %s pilot under attack by %s forces. I request immediate assistance to the %s system and will offer %d credits for a safe return to the local planet where I may recover."%(rescuelist[0],rescuelist[2],processSystem(path[-1]),creds))
	writemissionname("Rescue/Rescue_%s_from_%s_ships"%(rescuelist[0],rescuelist[2]),path)

def generateBountyMission (path,fg,fac):
	typ = fg_util.RandomShipIn(fg,fac)
	cap = faction_ships.isCapital(typ)
	diff=vsrandom.randrange(0,6)
	runaway=(vsrandom.random()>=.75)
	creds=1000+2000*runaway+500*diff+syscreds*len(path)
	if (cap):
		creds*=40
	finalprice=creds+syscreds*len(path)
	addstr=""
	isFixer=vsrandom.random()<fixerpct
	if isFixer:
		creds*=2
		addstr+="#F#bases/fixers/hunter.spr#Talk with the Bounty Hunter#We will pay you on mission completion.  And as far as anyone knows-- we never met."
		if (runaway):
			addstr += '#Also-- we have information that the target may be informed about your attack and may be ready to run. Be quick!'
		addstr+="#\n"
	writemissionsavegame(addstr+"import bounty\ntemp=bounty.bounty(0, 0, %g, %d, %d, '%s', %s, '', '%s','%s')\ntemp=0\n"%(finalprice, runaway, diff, fac, str(path), fg,typ))
	diffstr = ""
	if (diff>0):
		diffstr="  The ship in question is thought to have %d starships for protection."%diff
	writedescription("A %s starship in the %s flightgroup has been harassing operations in the %s system. Reward for the termination of said ship is %d credits.%s"%(typ,fg, processSystem(path[-1]), finalprice,diffstr))
	if (cap):
		writemissionname ("Bounty/Bounty_on_%s_Capital_Vessel_in_%s"%(fac,processSystem(path[-1])),path)
	else:
		writemissionname ("Bounty/Bounty_on_%s_starship_%s"%(fac,processSystem(path[-1])),path)

def generateDefendMission (path,defendfg,defendfac, attackfg,attackfac):
	if (isNotWorthy(defendfac)):
		return
	defendtyp = fg_util.RandomShipIn(defendfg,defendfac)
	attacktyp = fg_util.RandomShipIn(attackfg,attackfac)			
	isbase=fg_util.BaseFGInSystemName(path[-1])==defendfg
	creds=1000
	minq = 1
	maxq = 8
	quantity = vsrandom.randrange(minq,maxq)
	reallydefend = "1"
	if (vsrandom.randrange(0,4)==0):
		reallydefend="0"
	addstr=""
	isFixer=vsrandom.random()<fixerpct
	if isFixer:
		creds*=2
		addstr+="#F#bases/fixers/confed.spr#Talk to the Confed Officer#Thank you. Your defense will help confed in the long run.  We appreciate the support of the bounty hunting community.#\n"
	writemissionsavegame(addstr+"import defend\ntemp=defend.defend('%s', %d, %d, 8000.0, 100000.0, %g, %s, %d, '%s', %s, '%s', '%s', '%s', '%s')\ntemp=0\n"%
	                     (attackfac, 0, quantity, creds*quantity+syscreds*len(path), reallydefend, isbase, defendfac, str(path), attacktyp,attackfg, defendtyp, defendfg))
	iscapitol=""
	if isbase:
		iscapitol="capitol "
	writedescription("A %s assault wing named %s has jumped in and is moving for an attack on one of our %sstarships, a %s, in the %s system.\nYour task is to eradicate them before they eliminate our starship.\nIntelligence shows that they have %d starships of type %s. Your reward is %d credits per fighter."%(attackfac, attackfg, iscapitol, defendtyp, processSystem(path[-1]),quantity, attacktyp,creds))
	writemissionname("Defend/Defend_%s_from_%s"%(defendfac, attackfac),path)

def GetFactionToDefend(thisfaction, fac, cursys):
	m = fg_util.FGsInSystem ("merchant",cursys)
	nummerchant=len(m)
	m+=fg_util.FGsInSystem (thisfaction,cursys)
	numthisfac=len(m)
	m+=fg_util.FGsInSystem (fac,cursys)
	return (m,nummerchant,numthisfac)

def contractMissionsFor(fac,minsysaway,maxsysaway):
	facnum=faction_ships.factionToInt(fac)
	enemies = list(faction_ships.enemies[facnum])
	script=''
	cursystem = VS.getSystemFile()
	thisfaction = VS.GetGalaxyFaction (cursystem)
	preferredfaction=None
	if (VS.GetRelation (fac,thisfaction)>=0):
		preferredfaction=thisfaction#try to stay in this territory
	l=[]
	for i in range (minsysaway,maxsysaway+1):
		for j in getSystemsNAway(cursystem,i,preferredfaction):
			import dynamic_battle
			if (i<2):
				if j[-1] in dynamic_battle.rescuelist:
					generateRescueMission(j,dynamic_battle.rescuelist[j[-1]])
			l = dynamic_battle.BattlesInSystem(j[-1])
			nodefend=1
			for k in l:
				if (VS.GetRelation(fac,k[1][1])>=0):
					nodefend=0
					generateDefendMission(j,k[1][0],k[1][1],k[0][0],k[0][1])
			if preferredfaction:
				(m,nummerchant,numthisfac)=GetFactionToDefend(thisfaction, fac, j[-1])
				for kk in faction_ships.enemies[faction_ships.factiondict[thisfaction]]:
					k=faction_ships.intToFaction(kk)
					for mm in fg_util.FGsInSystem(k,j[-1]):
						if (vsrandom.randrange(0,4)==0):#fixme betterthan 4
							if nodefend and len(m) and vsrandom.random()<.4:
								if 1:#for i in range(vsrandom.randrange(1,3)):
									rnd=vsrandom.randrange(0,len(m))
									def_fg=m[rnd]
									def_fac = "merchant"
									if rnd>=nummerchant:
										def_fac= thisfaction
									if rnd>=numthisfac:
										def_fac = fac
									generateDefendMission(j,def_fg,def_fac,mm,k)
								nodefend=0
							elif (i==0 or vsrandom.random()<.5):
								generateBountyMission(j,mm,k)
				numescort = vsrandom.randrange(0,2)
				if (numescort>len(m)):
					numescort=len(m)
				count=0
				for k in m:
					if (i==0):
						if vsrandom.random()<.92:
							count+=1
							continue
					elif vsrandom.random()<.97:
						count+=1
						continue
					f = "merchant"
					if count>=nummerchant:
						f= thisfaction
					if count>=numthisfac:
						f = fac
					generateEscortMission(j,k,f)
					count+=1
			for k in range(vsrandom.randrange(-3,3)): ###FIXME: choose a better number than 4.
				if k<0:
					k=0
				rnd=vsrandom.random()
				if (rnd<.3):    # 30% - nothing
					continue
				if (rnd<.6):    # 30% - Patrol Mission
					generatePatrolMission(j,vsrandom.randrange(4,10))
				else:   # 40% - Cargo mission
					numcargos=vsrandom.randrange(1,25)
					if numcargos>20:
						numcargos=20
					category=''
					if (rnd>.87 and fac!='confed' and fac != "ISO"):
						category='Contraband'
					carg=VS.getRandCargo(numcargos,category)
					generateCargoMission(j,numcargos,carg.GetCategory(),fac)

def CreateMissions(minsys=0,maxsys=4):
	eraseExtras()
	i=0
	global plr,basefac
	plrun=VS.getPlayer()
	plr=plrun.isPlayerStarship()
	un=VS.getUnit(i)
	while(un):
		i+=1
		if (un.isDocked(plrun)):
			break
		un=VS.getUnit(i)
	if (un):
		basefac=un.getFactionName()
	if (basefac=='neutral'):
		basefac=VS.GetGalaxyFaction(VS.getSystemFile())
	contractMissionsFor(basefac,minsys,maxsys)
	import news
	news.processNews(plr)