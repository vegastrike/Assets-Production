import VS
import random
BATTLELIST=0
PEACELIST=1
PANICLIST=2
VICTORYLIST=3
LOSSLIST=4
HOSTILE_AUTODIST=10000
un = VS.getPlayer()
if (not un):
    VS.musicPlayList (PEACELIST)
    print "peace"
else:
    perfect=1
    iter = VS.getUnitList()
    target = iter.current()
    while (target):
        ftmp = 2*un.getRelation(target)
        if (ftmp<0 and un.getDistance(target)<HOSTILE_AUTODIST):
            perfect=0
        iter.advance()
        target=iter.current()
    if (perfect):
        VS.musicPlayList(PEACELIST)
        print "peace"
    else:
        ftmp = (un.FShieldData()+2*un.GetHullPercent()+un.RShieldData()-2.8)*10
        if (ftmp<-.5):
            VS.musicPlayList(PANICLIST)
            print "panic"
        else:
            VS.musicPlayList(BATTLELIST)
            print "battle"
