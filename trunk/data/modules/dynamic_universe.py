import VS
import Director
import vsrandom
import fg_util
from universe import getAdjacentSystemList

#SEE LINES 27, 46, 70, 87 FOR CURRENT BUGS!!!!!!!

cp=VS.getCurrentPlayer()
fgnames=[] #list of lists of flightgroup names for each faction
fglists=[] #list of lists for each flightgroups to lists of ships for each faction
origfgnames=[]
origfglists=[]
import faction_ships

def GenerateFgShips (maxshipinfg,factionnr):
	lst=[]
	capship=()
	if vsrandom.random()<.1:
		capship=(faction_ships.getRandomCapitolInt(factionnr),1)
	return (faction_ships.getRandomFighterInt(factionnr),maxshipinfg)+capship

def GenerateAllShips (numflightgroups,maxshipinfg):
	for fnr in range(faction_ships.getMaxFactions()-1):
		fglists.append([])
		fgnames.append(fg_util.GetRandomFGNames(numflightgroups))
		for i in range(numflightgroups):
			fglists[-1].append(GenerateFgShips(vsrandom.randrange(maxshipinfg)+1,fnr))

def AddSysDict (cursys):
	#pick random fighter from insysenemies with .3 probability OR pick one from the friendlies list.
	sysfaction=VS.GetGalaxyProperty(cursys,"faction")
	global fgnames, fglists
	for i in range (vsrandom.randrange(10)): #number of fgs in a system.
		facion=sysfaction
		if vsrandom.random()<.3:
			faction=faction_ships.get_insys_enemy_of(sysfaction)
		else:
			faction=faction_ships.get_friend_of(sysfaction)
		factionnr=faction_ships.FactionToInt(factionnr)
		typenumbertuple=fglists[factionnr].pop(-1) #pop returns item inside array
		fgname=fgnames[factionnr].pop(-1) #pop returns item inside array
		if not len(fgnames):
			fgnames=fg_util.TweakFGNames(origfgnames)
			fglists=origfglists
		fg_util.AddShipsToFG (fgname,faction,typenumbertuple,cursys)
	return i

def Makesys (startingsys):
	global systemdict
	global origfgnames
	origfgnames=fgnames
	origfglists=fglists
	systemdict[startingsys]=AddSysDict(cursys)
	todo=getAdjacentSystemList(startingsys)
	while len(todo):
		tmptodo=todo.pop(-1)
		if (not systemdict.has_key(tmptodo)):
			todo+=universe.getAdjacentSystemList(tmptodo)
			systemdict[tmptodo]=AddSysDict(tmptodo)
	return len(systemdict)

genUniverse=-1
if cp>=0:
	genUniverse=Director.getSaveDataLength(cp,"FactionRefList")
	if (genuniverse==0):
		Director.pushSaveData (cp,"FactionRefList",1)
		GenerateAllShips (5000,5) ###Insert number of flight groups and max ships per fg
		systemdict={}
		genUniverse=Makesys(VS.getSystemFile())
		del systemdict
		#now every system has distributed ships in the save data!
	#TODO: add ships to current system (for both modes)  uru?
	for i in range(VS.GetNumFactions):
		PurgeZeroShips(VS.getFactionName(i))

	













#not needed!
#def FilterAddList(todo,oursys):
#	newtodo=universe.getAdjacentSystemList(oursys)
#	cur=0
#	while cur<len(newtodo):
#		if (newtodo[cur] in todo) or systemdict.has_key(newtodo[cur]):
#			newtodo.pop(cur)
#		else:
#			cur+=1
#	return newtodo
