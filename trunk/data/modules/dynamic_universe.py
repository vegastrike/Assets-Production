import VS
import Director
import vsrandom
import generate_dyn_universe
_ships=[]
player_kill_list=[]
def updatePlayerKillList(playernum,faction):
	fac = VS.GetFactionIndex(faction)
	ret=0
	for i in range (VS.getNumPlayers()-len(player_kill_list)):
		player_kill_list.append([]);
	for i in range(VS.getNumPlayers()):
		numfac=Director.getSaveDataLength(i,"kills")
		for j in range (numfac-len(player_kill_list[i])):
			player_kill_list[i].append(0)
		for j in range (numfac):
			if (i==playernum and j==fac):
				ret = Director.getSaveData(i,"kills",j)-player_kill_list[i][j];
			player_kill_list[i][j]=Director.getSaveData(i,"kills",j)
	return ret

class ShipTracker:
	def __init__ (self,fgname,faction,typ,un):
		self.un=un
		self.fgname=fgname
		self.faction= faction
		self.starsystem = VS.getSystemFile()
		self.type=typ
	def Check(self):
		import fg_util
		dead=not self.un
		if (not dead):
			dead = self.un.GetHull()<=0
		if (dead):
			if (VS.systemInMemory (self.starsystem)):
				fg_util.RemoveShipFromFG(self.fgname,self.faction,self.type)
				if (fg_util.NumShipsInFG(self.fgname,self.faction)==0): #generate news here fg killed IRL
					import dynamic_news
					import dynamic_battle
					numships = updatePlayerKillList(0,self.faction)
					varList=["destroyed","end","unknown",self.faction,"1",str(dynamic_battle.getImportanceOfType(self.type)),self.starsystem,"all","unknown","unknown",self.fgname,self.type]
					if (numships>0 and VS.getPlayer()):
						varList=["destroyed","end",VS.getPlayer().getFactionName(),self.faction,"1",str(dynamic_battle.getImportanceOfType(self.type)),self.starsystem,"all",VS.getPlayer().getFlightgroupName(),VS.getPlayer().getName(),self.fgname,self.type]
					Director.pushSaveString(0,"dynamic_news",dynamic_news.makeVarList(varList))
			else:
				fg_util.LandShip(self.fgname,self.faction,self.type)
			return 0
		else:
			sys=self.un.getUnitSystemFile()
			if (len(sys)):
				self.starsystem=sys
		return 1
def TrackLaunchedShip(fgname,fac,typ,un):
	import fg_util
	fg_util.LaunchShip(fgname,fac,typ)
	global _ships
	_ships+= [ShipTracker(fgname,fac,typ,un)]
curiter=0
def Execute():
	global curiter, _ships
	if (len(_ships)>curiter):
		if (not _ships[curiter].Check()):
			del (_ships[curiter])
		else:
			curiter+=1
	else:
		curiter=0
	

	
