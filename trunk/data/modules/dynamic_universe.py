import VS
import Director
import vsrandom
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
		fgnames.append([])
		fglists.append([])
		for i in range(numflightgroups):
			fgnames[-1].append(???.GetRandomFlightgroupName(fglists[-1])) #TODO: make a function in module ??? that attempts to get a faction name that is not in the inputted list (only if possible; if it isn't possible then make a random name anyway.
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
			fgnames=origfgnames
			fglists=origfglists#reset fgnames and lists if run out (there will be two identical flightgroups then but most likely on the opposite side of the universe so the user hopefully won't notice.
		???.AddShipsToFG (fgname,faction,typenumbertuple,cursys) #TODO: generate a class of type dynamicuniverse OR make all of these functions members of that class.
	return i

def FilterAddList(todo):
	newtodo=getAdjacentSystemList()
	cur=0
	while cur<len(newtodo):
		if (newtodo[cur] in todo) or systemdict.has_key(newtodo[cur]):
			newtodo.pop(cur)
		else:
			cur+=1
	return newtodo

def Makesys ():
	global systemdict
	global origfgnames
	origfgnames=fgnames
	origfglists=fglists
	if True: #don't want to get mixed up with cursys; will go out of scope
		cursys=VS.getSystemFile()
		systemdict[cursys]=AddSysDict(cursys)
	todo=getAdjacentSystemList()
	while len(todo):
		tmptodo=todo.pop(-1)
		VS.pushSystem(tmptodo) #WARNING: DO NOT WANT TO LOAD ACTUAL SYSTEM (SIMPLE REASON: COULD TAKE HOURS OF TIME IF NOT DAYS)... IS THERE A FIX FOR THIS?
		todo+=FilterAddList(todo)
		systemdict[tmptodo]=AddSysDict(tmptodo)
		VS.popSystem()
	return len(systemdict)

genUniverse=-1
if cp>=0:
	genUniverse=Director.getSaveDataLength(cp,"FactionRefList")
	if (genuniverse>0):
		genUniverse=Director.getSaveData(cp,"FactionRefList",0)
	else:
		GenerateAllShips (5000,5) ###Insert number of flight groups and max ships per fg
		systemdict={}
		genUniverse=Makesys()
		del systemdict
		#now every system has distributed ships in the save data!
	#TODO: add ships to current system (for both modes
	


