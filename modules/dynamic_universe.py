import VS
import Director
import vsrandom
import generate_dyn_universe
_ships=[]
class ShipTracker:
	def __init__ (self,fgname,faction,typ,un):
		self.un=un
		self.fgname=fgname
		self.faction= faction
		self.starsystem = VS.getSystemFile()
		self.type=typ
	def Check(self):
		import fg_util
		if (not self.un):
			if (VS.systemInMemory (self.starsystem)):
				fg_util.RemoveShipFromFG(self.fgname,self.faction,self.type)
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


	
