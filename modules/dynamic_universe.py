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
	def Check():
		if (not un):
			if (VS.systemInMemory (self.starsystem)):
				RemoveShipFromFG(self.fgname,self.faction,self.type)
			else:
				LandShip(self.fgname,self.faction,self.type)
			return 0
		else:
			sys=un.getUnitSystemFile()
			if (len(sys)):
				self.starsystem=sys
		return 1
def TrackLaunchedShip(fgname,fac,typ,un):
	import fg_util
	fg_util.LaunchShip(fgname,fac,typ)
	_ships+= [ShipTracker(fgname,fac,typ,un)]
curiter=0
def Execute():
	global curiter
	if (len(_ships)>curiter):
		if (not _ships[curiter].Check()):
			del (_ships[curiter])
		else:
			curiter+=1
	else:
		curiter=0


	
