import VS
import Director
import vsrandom
import fg_util
import campaigns
from universe import getAdjacentSystemList

cp=fg_util.ccp
maxshipsinfg=20
fgnames=[] #list of lists of flightgroup names for each faction
origfgnames=[]
import faction_ships
def XProductionRate(fac,type):
    if fac in type:
        return type[fac]
    return type["default"]

def GenerateFgShips (shipinfg,factionnr,friendly):
    lst=[]
    capship=()
    fac = faction_ships.intToFaction(factionnr)
    if (friendly==2 or (friendly==1 and vsrandom.random()<XProductionRate(fac,faction_ships.capitalProductionRate)/XProductionRate(fac,faction_ships.fighterProductionRate))):
        capship=((faction_ships.getRandomCapitolInt(factionnr),1),)
    return ((faction_ships.getRandomFighterInt(factionnr),shipinfg),)+capship

def GenerateAllShips ():
    global fgnames,origfgnames
    for fnr in range(faction_ships.getMaxFactions()):
        fgnames.append(fg_util.GetRandomFGNames(1,faction_ships.factions[fnr]))
        origfgnames.append(list(fgnames[-1]))


doNotAddBasesTo={"enigma_sector/heavens_gate":1,"sol_sector/celeste":1,"enigma_sector/enigma":1,"enigma_sector/niven":1,"Gemini":1,"Crucible/Cephid_17":1}
def AddBasesToSystem (faction,sys):
    if (sys in doNotAddBasesTo):
        return
    slash = sys.find("/")
    if (slash!= -1):
        if (sys[0:slash] in doNotAddBasesTo):
            return
    if faction in faction_ships.factions:
        fsfac= list(faction_ships.factions).index(faction)
        numbases=0
#               numplanets=VS.GetGalaxyProperty(sys,"num_planets");
        numjumppoints=VS.GetNumAdjacentSystems(sys);
        if (numjumppoints<4):
            if (vsrandom.random()>=.25):
                numbases=1
        elif (vsrandom.random()>=.005):
            if (numjumppoints<7):
                numbases=vsrandom.randrange(1,int(numjumppoints/2)+1)
            elif numjumppoints==7:
                numbases=vsrandom.randrange(1,6)
            else:
                numbases=vsrandom.randrange(1,numjumppoints+1)
        if numbases==0:
            return
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

numericalfaction=0

def GetNewFGName(faction):
    factionnr=faction_ships.factionToInt(faction)
    global numericalfaction
    if(factionnr>=len(fgnames)):
        print "Faction "+faction+" unable to create fgname"

        numericalfaction+=1
        return "Alpha_"+str(numericalfaction)
    if (not len(fgnames[factionnr])):
        fgnames[factionnr]=fg_util.TweakFGNames(origfgnames[factionnr])
        fg_util.origfgoffset+=1
    k=vsrandom.randrange(0,len(fgnames[factionnr])); #pop returns item inside array
    fgname=fgnames[factionnr][k]
    del fgnames[factionnr][k]
    return fgname
def AddSysDict (cursys):
    #pick random fighter from insysenemies with .3 probability OR pick one from the friendlies list.
#       print 'Addsysdict'
    sysfaction=VS.GetGalaxyProperty(cursys,"faction")
    global fgnames, fglists
    i=0
    AddBasesToSystem(sysfaction, cursys)
    for i in range (1+vsrandom.randrange(fg_util.MinNumFlightgroupsInSystem()-1,fg_util.MaxNumFlightgroupsInSystem())): #number of fgs in a system.
        faction=sysfaction
        friendly=0
        if vsrandom.random()<.3 or sysfaction=='unknown' or sysfaction=='':
            faction=faction_ships.get_rabble_of(sysfaction)
        else:
            if (faction==sysfaction):
                friendly=1
            if (sysfaction in faction_ships.homeworlds):
                if (cursys==faction_ships.homeworlds[sysfaction]):
                    friendly=2
            faction=faction_ships.get_friend_of(sysfaction)
        factionnr=faction_ships.factionToInt(faction)
        global maxshipsinfg
        typenumbertuple=GenerateFgShips(vsrandom.randrange(maxshipsinfg)+1,factionnr,friendly)
        fgname=GetNewFGName(faction)
        fg_util.AddShipsToFG (fgname,faction,typenumbertuple,cursys)
    return i


def ForEachSys (startingsys,functio):
    systemdict={}
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
    fac =VS.GetGalaxyFaction(sys)
    if fac in systemcount:
        systemcount[fac]+=1
    else:
        systemcount[fac]=1
        print "FATAL ERROR "+fac+" not in list;"
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
    sys=VS.getSystemFile()
    if (VS.GetGalaxyProperty("Sol/Sol","jumps")!="" and VS.GetGalaxyProperty("Sol/Sol","faction")!=""):
        sys="Sol/Sol"
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
        GenerateAllShips () ###Insert number of flight groups and max ships per fg
        print 'placing ships... ... ...'
        genUniverse=Makesys(VS.getSystemFile())
        #now every system has distributed ships in the save data!
    else:
        GenerateAllShips()
        print "Second Load"
        for i in range(len(fgnames)):
            fgnames[i]=fg_util.TweakFGNames(origfgnames[i])
        fg_util.origfgoffset+=1
    campaigns.loadAll(cp)
    #TODO: add ships to current system (for both modes)  uru?
else:
    print 'fatal error: no cockpit'
