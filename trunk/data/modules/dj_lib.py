import VS
import vsrandom
BATTLELIST=0
PEACELIST=1
PANICLIST=2
VICTORYLIST=3
LOSSLIST=4
HOSTILE_AUTODIST=10000
HOSTILE_NEWLAUNCH_DISTANCE=20000
peacelist={"aera":VS.musicAddList('aera.m3u'),
            "confed":VS.musicAddList('terran.m3u'),
            "iso":VS.musicAddList('iso.m3u'),
            None:PEACELIST
            }
battlelist={"aera":VS.musicAddList('aerabattle.m3u'),
            "confed":VS.musicAddList('terranbattle.m3u'),
            "iso":VS.musicAddList('isobattle.m3u'),
	    None:BATTLELIST
            }
paniclist={None:PANICLIST}
asteroidmisic=VS.musicAddList('asteroids.m3u')

def LookupTable(list,faction):
	if faction in list:
		if (list[faction]!=-1):
			return list[faction]
		else:
			return list[None]
	else:
		return list[None]
situation=PEACELIST

def mpl (list,newsituation,forcechange):
	global situation
	print "SITUATION IS "+str( situation)+"force change "+str(forcechange) + " bool "+ str(forcechange or newsituation!=situation)
	if (forcechange or newsituation!=situation):
		print "SITUATION IS RESET TO "+str( newsituation)
		situation=newsituation
		VS.musicPlayList(list) 
def PlayMusik(forcechange=1,hostile_dist=0):
	un = VS.getPlayer()
	if (not un):		
		mpl (PEACELIST,PEACELIST,forcechange)
		print "peace"
	else:
		perfect=1
		iter = VS.getUnitList()
		target = iter.current()
		unlist=[]
		asteroid=False
		while (target):
			ftmp = 2*target.getRelation(un)
			nam=target.getName().lower()
			if un.getSignificantDistance(target)<=2*target.rSize() and ('afield'==nam[:6] or 'asteroid'==nam[:8]):
				asteroid=True
			hdis = HOSTILE_AUTODIST
			if (hostile_dist!=0):
				hdis = hostile_dist
			if (target.GetTarget()==un or (ftmp<0 and un.getDistance(target)<hdis)):
				unlist.append(un.getFactionName())
				perfect=0
			iter.advance()
			target=iter.current()
		if (perfect):
			if asteroid and asteroidmisic!=-1 and vsrandom.random()<.7:
				mpl(asteroidmisic,PEACELIST,forcechange)
				return
			sys=VS.getSystemFile()
			fact=VS.GetGalaxyProperty(sys,"faction")
			if vsrandom.random()<.5:
				fact=None
			mpl(LookupTable(peacelist,fact),PEACELIST,forcechange)
			print "peace"
		else:
			ftmp = (un.FShieldData()+2*un.GetHullPercent()+un.RShieldData()-2.8)*10
			fact=None
			if len(unlist) and vsrandom.random()<.5:
				fact=unlist[vsrandom.randrange(0,len(unlist))]
			if (ftmp<-.5):
				mpl(LookupTable(paniclist,fact),BATTLELIST,forcechange)
				print "panic"
			else:
				mpl(LookupTable(battlelist,fact),BATTLELIST,forcechange)
				print "battle"

