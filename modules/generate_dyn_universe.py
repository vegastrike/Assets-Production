import VS
import Director
import vsrandom
import fg_util
from universe import getAdjacentSystemList

cp=fg_util.ccp

fgnames=[] #list of lists of flightgroup names for each faction
fglists=[] #list of lists for each flightgroups to lists of ships for each faction
origfgnames=[]
origfglists=[]
import faction_ships
def XProductionRate(fac,type):
	if fac in type:
		return type[fac]
	return type["default"]

def GenerateFgShips (maxshipinfg,factionnr):
	lst=[]
	capship=()
	fac = faction_ships.intToFaction(factionnr)
	if vsrandom.random()<XProductionRate(fac,faction_ships.capitalProductionRate)/XProductionRate(fac,faction_ships.fighterProductionRate):
		capship=((faction_ships.getRandomCapitolInt(factionnr),1),)
	return ((faction_ships.getRandomFighterInt(factionnr),maxshipinfg),)+capship

def GenerateAllShips (numflightgroups,maxshipinfg):
	for fnr in range(faction_ships.getMaxFactions()-1):
		fglists.append([])
		fgnames.append(fg_util.GetRandomFGNames(numflightgroups,faction_ships.factions[fnr]))
		for i in range(numflightgroups):
			fglists[-1].append(GenerateFgShips(vsrandom.randrange(maxshipinfg)+1,fnr))


doNotAddBasesTo={"enigma_sector/heavens_gate":1,"sol_sector/celeste":1,"enigma_sector/enigma":1,"enigma_sector/niven":1}
def AddBasesToSystem (faction,sys):
	if (sys in doNotAddBasesTo):
		return
	if faction in faction_ships.factions:
		fsfac= list(faction_ships.factions).index(faction)
		numbases =vsrandom.randrange(fg_util.MinNumBasesInSystem(),
									 fg_util.MaxNumBasesInSystem())
		shiplist=[]
		nums=[]
		for i in range(numbases):
			whichbase = faction_ships.bases[fsfac][vsrandom.randrange(0,len(faction_ships.bases[fsfac]))]
			if whichbase in shiplist:
				nums[shiplist.index(whichbase)]+=1
			else:
				shiplist+=[whichbase]
				nums+=[1]
		tn =[]
		for i in range (len(shiplist)):
			tn+=[ (shiplist[i],nums[i])]
		fg_util.AddShipsToFG(fg_util.BaseFGInSystemName (sys),faction,tn,sys)
		


def AddSysDict (cursys):
	#pick random fighter from insysenemies with .3 probability OR pick one from the friendlies list.
#	print 'Addsysdict'
	sysfaction=VS.GetGalaxyProperty(cursys,"faction")
	global fgnames, fglists
	i=0
	AddBasesToSystem(sysfaction, cursys)
	for i in range (vsrandom.randrange(fg_util.MaxNumFlightgroupsInSystem())): #number of fgs in a system.
		faction=sysfaction
		if vsrandom.random()<.3 or sysfaction=='unknown' or sysfaction=='':
			faction=faction_ships.get_rabble_of(sysfaction)
		else:
			faction=faction_ships.get_friend_of(sysfaction)
		factionnr=faction_ships.factionToInt(faction)
		typenumbertuple=fglists[factionnr].pop(-1) #pop returns item inside array
		fgname=fgnames[factionnr].pop(-1) #pop returns item inside array
		if not len(fgnames):
			fgnames=fg_util.TweakFGNames(origfgnames)
			fglists=origfglists
		fg_util.AddShipsToFG (fgname,faction,typenumbertuple,cursys)
	return i


def ForEachSys (startingsys,functio):
	systemdict={}
	global origfgnames
	origfgnames=fgnames
	origfglists=fglists
	systemdict[startingsys]=functio(startingsys)
	todo=getAdjacentSystemList(startingsys)
	while len(todo):
		tmptodo=todo.pop(-1)
		if (not systemdict.has_key(tmptodo)):
			todo+=getAdjacentSystemList(tmptodo)
			systemdict[tmptodo]=functio(tmptodo)
	return len(systemdict)
def Makesys (startingsys):
	ForEachSys(startingsys,AddSysDict)

systemcount={}
def CountSystems(sys):
	systemcount[VS.GetGalaxyFaction(sys)]+=1
def TakeoverSystem(fac,sys):
	systemcount[VS.GetGalaxyFaction(sys)]-=1
	VS.SetGalaxyFaction(sys,fac)
	systemcount[fac]+=1
	AddBasesToSystem(fac,sys)

genUniverse=-1
if cp>=0:
	print 'Purging...'
	for i in fg_util.AllFactions():
		fg_util.PurgeZeroShips(i)
		systemcount[i]=0
	print 'StartSystemCount'
	ForEachSys(VS.getSystemFile(),CountSystems)
	print systemcount
	print 'EndSystemCount'	
	genUniverse=0
	curfaclist = fg_util.AllFactions()
	reflist = fg_util.ReadStringList(cp,"FactionRefList")
	if (reflist !=curfaclist):
		print 'reflist is '+str(reflist)
		print 'curfaclist is '+str(curfaclist) 
		
		fg_util.WriteStringList(cp,"FactionRefList",curfaclist)
		print 'generating ships... ... ...'
		GenerateAllShips (5000,5) ###Insert number of flight groups and max ships per fg
		print 'placing ships... ... ...'
		genUniverse=Makesys(VS.getSystemFile())
		#now every system has distributed ships in the save data!
	#TODO: add ships to current system (for both modes)  uru?
else:
	print 'fatal error: no cockpit'
