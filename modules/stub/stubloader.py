import sys
sys.path += ['../modules/stub/','../modules','../bases']
def kfac (k):
	if (k==0):
		return 1
	return k*kfac(k-1)
import generate_dyn_universe
import dynamic_battle
dynamic_battle.UpdateCombatTurn()
import fg_util
conf = fg_util.SortedAllShips ('confed')
aera = fg_util.SortedAllShips ('aera')
def doit(n=1000):
	for i in range(n):
		dynamic_battle.UpdateCombatTurn()
	
