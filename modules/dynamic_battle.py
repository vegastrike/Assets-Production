import VS
import Director
import fg_util
import vsrandom
import faction_ships
import dynamic_news
#hashed by system, then contains lists of pairs of (flightgroup,faction) pairs
cpsal= {} #Current PerSystem AttackList
persystemattacklist= cpsal #assign this to a pointer to cpsal THE FIRST TIME ONLY

attacklist ={}#hashtable mapping (attackfg,attackfaction):(defendfg,defendfaction)
defendlist={}#hashtable mapping (defendfg,defendfaction):(attackfg,attackfaction)
lastfac=0
lookorsiege=1
def UpdateCombatTurn():
	global lastfac
	global lookorsiege
	if lastfac>=VS.GetNumFactions():
		if (not SimulateBattles()):
			lastfac=0
	else:
		fac = VS.GetFactionName(lastfac)
		if (lookorsiege):
			lookorsiege=LookForTrouble (fac)
		else:
			if (not Siege(fac)):
				#fg_util.CheckAllShips(fac)		
				lastfac+=1
				lookorsiege=1
		#first look for trouble, then go ahead and simulate all the battles

siegenumber=0
siegenumtimes=0
siegeprob=0
#fixme
def getImportanceOfSystem(sys):
	if (VS.GetGalaxyProperty(sys,"faction")==VS.GetGalaxyFaction(sys)):
		return .5
	else:
		return .1
def getImportanceOfType (typ):
	import faction_ships
	if (faction_ships.isCapital(typ)):
		return 1
	return .5

def moveSurroundingCapshipsToSiege(fac,sys):
	suc=0
	for i in range (VS.GetNumAdjacentSystems(sys)):
		asys=VS.GetAdjacentSystem(sys,i)
		for fg in fg_util.AllFGsInSystem(fac,asys):
			if fg_util.CapshipInFG(fg,fac):
				suc=1
				fg_util.TransferFG(fg,fac,sys)
	if (not suc):
		for fg in fg_util.AllFGsInSystem(fac,sys):
			if (fg_util.CapshipInFG(fg,fac)):
				suc=1
	return suc

#returns false if Siege is done going through all its vehicles
def Siege(fac):
	global siegenumber
	global siegenumtimes
	global siegeprob
	#	turns_till_siege_effective=100
	if (not fac in faction_ships.siegingfactions):
		return 
	numfg= fg_util.NumAllFlightgroups(fac)
	if (numfg):
		if (siegenumber==0):
			siegeprob = float(numfg)/float(faction_ships.siegingfactions[fac]);
			siegenumtimes = int (siegeprob)
			if (siegenumtimes==0):
				siegenumtimes=1
			else:
				siegeprob =1
		if siegenumber>=siegenumtimes:
			siegenumber=0
			return 0
		else:
			if (vsrandom.uniform(0,1)<siegeprob):
				fg =fg_util.RandomFlightgroup(fac)
				sys = fg_util.FGSystem(fg,fac)
				enfac=VS.GetGalaxyFaction(sys)
				#fg_util.CheckAllShips(fac)
				#fg_util.CheckAllShips(enfac)
				#if fac == "unknown" or enfac == "unknown":
				#	print "ERROR: siege had an unknown faction"
				#	return
				if (VS.GetRelation(fac,enfac)<0):#FIXME maybe even less than that
					numenemyfg = fg_util.NumFactionFGsInSystem(enfac,sys)
					numfriendfg = fg_util.NumFactionFGsInSystem(fac,sys)
					#print 'siegarol enemioes '+str(numenemyfg)+ ' friends '+str(numfriendfg)
					if (numenemyfg==0 and numfriendfg==0): #If both annihalate each other completely (unlikely but possible)
						facnum = VS.GetFactionIndex (fac)
						print 'cehcking started'
						print "DRAW error "+fg+" sys has "+sys+" has " +str(fg_util.NumFactionFGsInSystem(fac,sys))+" String is "+Director.getSaveString(0,fg_util.MakeStarSystemFGKey(sys),facnum)
						if sys != 'nil':
							Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["siege","end",fac,enfac,"0",str(getImportanceOfSystem(sys)),sys,"all",fg,"unknown","unknown","unknown"]))
												#FIXME use keyword (ignore
												#keyword for now Daniel)

					elif (numenemyfg==0 and (fg_util.CapshipInFG(fg,fac) or moveSurroundingCapshipsToSiege(fac,sys))):	#If aggressor succeeded
						print fac + ' took over '+ sys + ' originally owned by '+enfac
						#ok now we have him... while the siege is going on the allies had better initiate the battle--because we're now defending the place...  so that means if the owners are gone this place is ours at this point in time
						fgs = fg_util.FGsInSystem(fac,sys)
						if (len(fgs)>0):
							fgs=fgs[0]
						else:
							fgs = "unknown"
						if sys != 'nil':
							Director.pushSaveString(0,"dynamic_news"
						,dynamic_news.makeVarList(["siege","end",fac,enfac,"1",str(getImportanceOfSystem(sys)),sys,"all",fgs,"unknown","unknown","unknown"]))
												#FIXME use keyword (ignore
												#keyword for now Daniel)

						import generate_dyn_universe
						generate_dyn_universe.TakeoverSystem(fac,sys)
						#HACK, regenerate bases instnatly

					elif (numfriendfg==0):	#If aggressor lost
						print 'wtf!!'
						fgs = fg_util.FGsInSystem(enfac,sys)
						if (len(fgs)>0):
							fgs=fgs[0]
						else:
							fgs = "unknown"
						if sys != 'nil':
							Director.pushSaveString(0,"dynamic_news"
						,dynamic_news.makeVarList(["siege","end",fac,enfac,"-1",str(getImportanceOfSystem(sys)),sys,"all","unknown","unknown",fgs,"unknown"]))
												#FIXME use keyword (ignore
												#keyword for now Daniel)


					#FIXME add if statements if there is instead a (non appocalyptic) draw (if waring factions have relations "almost neutral" you could have a cease fire, or if the two factions are evenly matched and go nowhere a withdraw of the attackers might occur)!!!
			siegenumber+=1
		return 1
	else:
		return 0
	


#returns false if SimulateBattles gets through all its vehicles
simulateiter=None
deadbattles=[]
deadbattlesiter=-2
def SimulateBattles():
	global deadbattles
	global cpsal
	global attacklist
	global simulateiter
	global deadbattlesiter
	if not simulateiter:
		if (deadbattlesiter!=-2):
			if (deadbattlesiter<0):
				deadbattlesiter=-2
				return 0
			else:
				stopAttack(deadbattles[deadbattlesiter][0],deadbattles[deadbattlesiter][1])
				deadbattlesiter-=1
				return 1
		else:
			persystemattacklist=cpsal
			cpsal = {}
			simulateiter= attacklist.iteritems()
	
	try:
	#if (1):
		ally = simulateiter.next()
		godoit=1
	except:
		simulateiter = None
		deadbattlesiter = len(deadbattles)-1
		godoit=0
	if (godoit):
		enemy = ally[1]
		ally = ally[0]
		if (not attackFlightgroup (ally[0],ally[1],enemy[0],enemy[1])):
			deadbattles+=[ally]
		else:
			sys = fg_util.FGSystem(ally[0],ally[1])
			if not (sys in cpsal):
				cpsal[sys]=[]
			cpsal[sys]+=[(ally,enemy)]#continue the battle
	return 1
def BattlesInSystem(sys):
	if sys in cpsal:
		return cpsal[sys]
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
	if (sys!='nil' and fg!=fg_util.BaseFGInSystemName(sys)):
		l = universe.getAdjacentSystemList(sys)
		nthis = fg_util.NumFactionFGsInSystem(fac,sys)
		if (len(l)):
			suggestednewsys = l[vsrandom.randrange(0,len(l))]
			for i in l:
				ifac = VS.GetGalaxyFaction(i)
				if (ifac==fac and nthis > fg_util.NumFactionFGsInSystem(fac,i)):
					suggestednewsys = i
				elif (VS.GetRelation(fac,ifac)<0):
					fg_util.TransferFG(fg,fac,i)
					return
			#			print 'moving '+fg+' from '+sys+' to '+ newsys
			fg_util.TransferFG( fg,fac,suggestednewsys);
		else:
			pass #print "flightgroup "+fg+" in system "+sys + " is stuck"
def XProductionRate(fac,type):
	if fac in type:
		return type[fac]
	return type["default"]

def AddFighterTo(fgname,fac):
	sys = VS.getSystemFile()
	#print 'add fighter'
	import generate_dyn_universe
	numsystems = generate_dyn_universe.systemcount[fac]	
	numfighters = int(XProductionRate(fac,faction_ships.fighterProductionRate)*numsystems)
	if (numfighters<1):
		numfighters=1
	fg_util.AddShipsToFG (fgname,fac,((faction_ships.getRandomFighter(fac),numfighters),),sys)
	numcapships = XProductionRate(fac,faction_ships.capitalProductionRate)*numsystems
	if (numcapships<1):
		if (vsrandom.uniform(0,1)>numcapships):
			return
		numcapships=1
	sys = fg_util.FGSystem(fgname,fac)
	if (VS.GetGalaxyFaction(sys)!=fac):
		if fac in faction_ships.homeworlds:
			sys=faction_ships.homeworlds[fac]
	cap =faction_ships.getRandomCapitol(fac)
	fg_util.AddShipsToFG(fgname,fac,((cap,int(numcapships)),),sys)

#returns false if done with vehicles
lftiter=0
import Director
def LookForTrouble (faction):
	global lftiter
	key = fg_util.MakeFactionKey(faction)
	numfg=Director.getSaveStringLength(fg_util.ccp,key)
	if (lftiter>=numfg):
		lftiter=0
		if (numfg):
			AddFighterTo(Director.getSaveString(fg_util.ccp,key,vsrandom.randrange(0,numfg)),faction)
		return 0
	i = Director.getSaveString(fg_util.ccp,key,lftiter)
	lftiter+=1	
	sys = fg_util.FGSystem (i,faction)
	if (sys!='nil'):
		enfac = faction_ships.get_enemy_of(faction)
		foundanyone=0
		l=fg_util.AllFGsInSystem(enfac,sys)
		j=vsrandom.randrange(0,len(l)+3)
		if (j<len(l)):
			foundanyone=1 #FIXME include some sort of measure "can I win"
			if (vsrandom.randrange(0,5)==0):
				initiateAttack(i,faction,sys,l[j],enfac)
		elif (vsrandom.randrange(0,3)==0):
			randomMovement (i,faction)
	return 1

def StopTargettingEachOther (fgname,faction,enfgname,enfaction):
	i=VS.getUnitList()
	un=i.current()
	while (un):
		if ((un.getFactionName()==enfaction and un.getFlightgroupName()==enfgname) or
			(un.getFactionName()==faction and un.getFlightgroupName()==fgname)):
			un.setFgDirective ('b')
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
def KillOne (fg,enfac,tn,num):
	return fg_util.RemoveShipFromFG(fg,enfac,tn[0],num,1)

stattable={
	"nova":(.7,.4,2,1),
	"tian":(.7,.5,1,1),
	"avenger":(.8,.3,5,2),
	"wayfarer":(.3,.2,1,1),
	"longhaul":(.5,.3,1,2),
	"khanjarli":(.4,.3,3,2),
	"epeellcat":(.6,.4,3,1),
	"firefly":(.6,.3,1,2),
	"butterfly":(.6,.3,4,1),
	"dryad":(.4,.4,1,2),
	"destroyer":(.8,.6,6,10),
	"fleetcarrier":(.4,.8,3,15),
	"carrier":(.4,.8,3,15),
	"cruiser":(.9,.7,10,14),
	"dagger":(.5,.8,2,1),
	"cargoship":(.5,.3,1,5),
	"commerce_center":(.2,.4,1,25),
	"corvette":(.7,.4,4,6),
	"destiny":(.6,.8,1,2),
	"drydock":(0,.2,0,2),
	"hispidus":(.5,.2,5,2),
	"katar":(.4,.4,2,1),
	"kira":(.8,.3,4,2),
	"kyta":(.7,.4,2,1),
	"lekra":(.6,.5,2,1),
	"leokat":(.8,.5,1,2),
	"metron":(.6,.5,1,2),
	"mongoose":(.8,.4,2,1),
	"osprey":(.6,.35,2,1),
	"relay":(.4,.3,1,10),
	"research":(.4,.2,1,12),
	"refinery":(.5,.1,1,20),
	"revoker":(.4,.5,1,20),
	"skart":(.8,.5,1,1),
	"starfish":(.9,.2,3,1),
	"starfortress":(.9,.6,15,30),
	"starrunner":(.7,.8,12,12),
	"truck":(.2,.1,1,4),
	"vark":(.5,.6,8,4),
	"vitik":(.6,.8,6,18),
	"yavok":(.9,.8,14,20),
	"yrilan":(.8,.5,2,12),
	"rlaan_cruiser":(.9,.5,2,50),
	"eagle":(.6,.4,3,2),	
	"fighter_barracks":(.4,.4,2,16),
	"escortcarrier":(.8,.5,2,12),   
	"factory":(.6,.1,2,20),
	"f109vampire":(.7,.3,2,2),
	"aeon":(.5,.5,3,1),	
	"aevant":(.5,.4,4,2),
	"beholder":(.8,.5,5,10)
   }

def GetStats ( name):
	try:
		return stattable[name]
	except:
		return (.5,.5,1,1)
def HowMuchDamage (shiptypes):
	dam=0
	for i in shiptypes:
		stats=GetStats(i[0])
		if (vsrandom.uniform(0,1)<stats[0]):
			dam+=stats[2]*i[1]
	return dam
def ApplyDamage (fg,fac,shiptypes,damage):
	rnum = vsrandom.randrange(0,len(shiptypes))
	stats = GetStats (shiptypes[rnum])
	if (vsrandom.uniform(0,1)>=stats[1]):
		dampool=fg_util.GetDamageInFGPool(fg,fac)
		tmpdam=damage+int(dampool/len(shiptypes))
		numshipstokill=int(tmpdam/stats[3])
		damage -= KillOne(fg,fac,shiptypes[rnum],numshipstokill)*stats[3]#returns how many ships killed
		dampool+=damage
		

def SimulatedDukeItOut (fgname,faction,enfgname,enfaction):
	ally=fg_util.LandedShipsInFG(fgname,faction)
	enemy=fg_util.LandedShipsInFG(enfgname,enfaction)
	#roll z'dice
	#FIXME!!!
	if (len(enemy) and len(ally)):
		endam = HowMuchDamage(enemy)
		ApplyDamage(enfgname,enfaction,enemy,HowMuchDamage(ally))
		ApplyDamage(fgname,faction,ally,endam)		
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
		index=vsrandom.randrange(0,len(landedtn))
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
			VS.StopTargettingEachOther(fgname,faction,enemy[0],enemy[1])
			VS.popSystem()
		del defendlist[enemy]
		del attacklist[ally]
		

def initiateAttack (fgname,faction,sys,enfgname,enfaction):
# FIXME This should only occur for fleet battles, so is commented out for now
#	Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","start",faction,enfaction,"0",str(getImportanceOfSystem(sys)),sys,"all",fgname,"unknown",enfgname,"unknown"]))
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
	leader = fg_util.getFgLeaderType(fgname,faction)
	enleader = fg_util.getFgLeaderType(enfgname,enfaction)
	sys = fg_util.FGSystem (fgname,faction)
	ensys = fg_util.FGSystem (enfgname,enfaction)
	if (sys==ensys):
		if (VS.systemInMemory(sys)):
			VS.pushSystem(sys)
			LaunchEqualShips (fgname,faction,enfgname,enfaction)
			VS.TargetEachOther (fgname,faction,enfgname,enfaction)
			VS.popSystem()
		SimulatedDukeItOut (fgname,faction,enfgname,enfaction)
	elif (sys!='nil' and ensys!='nil'):
		#pursue other flightgroup
		import universe
		adjSystemList=universe.getAdjacentSystemList(sys)
		if ensys in adjSystemList:
			fg_util.TransferFG (fgname,faction,ensys)
		else:
			return 0
	else:
		return 0 #print 'nil DRAW error'
	if (fg_util.NumShipsInFG(fgname,faction)==0):
		if (fg_util.NumShipsInFG(enfgname,enfaction)==0):
			Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","end",faction,enfaction,"0",str(getImportanceOfSystem(sys)),sys,"all",fgname,leader,enfgname,enleader]))
		else:
			Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","end",faction,enfaction,"-1",str(getImportanceOfSystem(sys)),sys,"all",fgname,leader,enfgname,enleader]))
		return 0
	elif (fg_util.NumShipsInFG(enfgname,enfaction)==0):
		Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","end",faction,enfaction,"1",str(getImportanceOfSystem(sys)),sys,"all",fgname,leader,enfgname,enleader]))	
		return 0
	if (vsrandom.randrange(0,4)==0):
		#FIXME  if it is advantageous to stop attacking only!!
		#FIXME add a stop attacking news report?  -- this should now be fixed, as a draw is reported (not heavilly tested)
		Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","end",faction,enfaction,"0",str(getImportanceOfSystem(sys)),sys,"all",fgname,leader,enfgname,enleader]))
		return 0
	if (vsrandom.randrange(0,4)==0 and enfgname!=fg_util.BaseFGInSystemName(ensys)):
		#FIXME  if it is advantageous to run away only
		#FIXME add a retreat news report?  -- this should now be fixed, as a draw is reported (not heavilly tested)
		Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(["battle","end",faction,enfaction,"-1",str(getImportanceOfSystem(sys)),sys,"all",fgname,leader,enfgname,enleader]))
		num=VS.GetNumAdjacentSystems(ensys)
		if (num>0):
			ensys=VS.GetAdjacentSystem(ensys,vsrandom.randrange(0,num))
			fg_util.TransferFG (fgname,faction,ensys)
	return 1
		
##for i in range(10000):
##	UpdateCombatTurn()
