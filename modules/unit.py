import VS
def isLandable (un):
    if (un):
        return un.isDockableUnit()

def isBase (un):
    unit_fgid = un.getFlightgroupName()
    retval = unit_fgid=="Base"
    return retval and not un.isSun()

def findPlayerNum (un):
    for i in range (VS.getNumPlayers()):
        if (VS.getPlayerX(i)==VS.getPlayer()):
            return i
    return 0

def isAsteroid (un):
    unit_fgid = un.getFlightgroupName()
    retval = unit_fgid=="Asteroid"
    return retval


def getUnitFullName(un):
    thename=(un.getName())
    fg=un.getFlightgroupName()
    if fg=='Base':
        thename=un.getFullname()+' '+thename.replace('_',' ')
    elif fg!='Shadow' and fg!='':
        thename=thename+' in the '+fg+' flightgroup'            
    return thename

def getSignificant (whichsignificant, landable_only, capship_only):
    import vsrandom
    which=0
    signum=0
    rez = []
    un=VS.getUnit(0)
    #print "is this null "+str(un.isNull())
    while (not un.isNull()):
        #print "is this null "+str(un.isNull())
        un=VS.getUnit(which)
        if (un.isNull()):
            which=0
            if (signum==0):
                signum=whichsignificant+1
        else:
            #print "checking "+un.getName()
            if ((landable_only) or (capship_only)):
                if(capship_only):
                    if (isBase (un)):
                        signum=signum+1
                        rez.append(un)
                else:
                    if (isLandable (un)):
                        signum=signum+1
                        rez.append(un)
                    else:
                        print "not landable "+un.getName()+" fg "+un.getFlightgroupName()
            else:
                if (un.isSignificant()):
                    signum=signum+1
                    rez.append(un)
            which=which+1
    if (len(rez)==0):
        if (capship_only):
            return getSignificant(whichsignificant,landable_only,0)
        elif(landable_only):
            return getSignificant (whichsignificant,0,0)
        else:
            print "fatal error, no significants in system "+VS.getSystemFile()
            return VS.getPlayer()
    return rez[vsrandom.randrange(0,len(rez))]

  #this one terminates if fewer than so many planets exist with null

def inSystem (unit):
    i=VS.getUnitList ()
    while (i.notDone()):
        if (i.current()==unit):
            return 1
        i.advance()
    return 0
def getPlanet (whichsignificant, sig):
    un=VS.Unit()
    signum=0
    i = VS.getUnitList()
    while (signum<=whichsignificant):
        un=i.current()
        if (un):
            if(sig):
                if (un.isSignificant ()):
                    signum=signum+1
            else:
                if (un.isPlanet ()):
                    signum=signum+1
            i.advance()
        elif (i.isDone()):
            break
        else:
            i.advance()
    return un

def getJumpPoint(whichsignificant):
    un=VS.Unit()
    which=0
    signum=0
    while (signum<whichsignificant):
        un=VS.getUnit(which)
        if (un):
            if (un.isJumppoint()):
                signum=signum+1
            which=which+1
        else:
            which=0
            if (signum==0):
                un.setNull()
                signum=whichsignificant
    return un

def obsolete_getNearestEnemy(my_unit,range):
    ship_nr=0
    min_dist=9999999.0
    min_enemy=VS.Unit()
    un=VS.getUnit(ship_nr)
    while(unit):
        unit_pos=un.getPosition()
        dist=my_unit.getMinDis(unit_pos)
        relation=my_unit.getRelation(unit)
        if(relation<0.0):
            if((my_unit==unit) and (dist<range) and (dist<min_dist)):
                min_dist=dist
                min_enemy=unit
        ship_nr=ship_nr+1
        unit=VS.getUnit(ship_nr)
    if(min_enemy):
        other_fgid=min_enemy.getFgID()
    return min_enemy


def obsolete_getThreatOrEnemyInRange(un,range):
    threat=un.getThreat()
    if(threat.isNull()):
        threat=obsolete_getNearestEnemy(un,range)
    return threat

def setPreciseTargetShip (which_fgid, target_unit):
    ship_nr=0
    un=VS.getUnit(ship_nr)
    if (target_unit):
        while(un.isNull()):
            unit_fgid=un.getFgID()
            if(unit_fgid[:len(which_fgid)]==which_fgid):
                un.SetTarget(target_unit)
            ship_nr=ship_nr+1
            un=VS.getUnit(ship_nr)

def getMinDistFrom(sig1):
    sig2=getPlanet (0,0)
    mindist=100000000000000000000000000000000000000000000.0
    i=0
    while (sig2):
        tempdist = sig1.getSignificantDistance(sig2)
        if (tempdist<mindist and tempdist>0.0):
            mindist=tempdist
        i+=1
        sig2 = getPlanet (i,0)
    return mindist

def minimumSigDistApart():
    sig1=getPlanet (0,0)
    i=0
    mindist=100000000000000000000000000000000000000000000.0
    ave=0.0
    while (sig1):
        tempdist = getMinDistFrom (sig1)
        if (ave<0.9):
            mindist = tempdist
        else:
            mindist += tempdist
        ave+=1.0
        i+=1
        sig1 = getPlanet (i,0)
    if (ave!=0.0):
        mindist = mindist/ave
    return mindist

def getUnitByName (name):
    ship_nr=0
    unit = VS.getUnit(0)
    while (unit):
        if (unit.getName()==name):
            return unit
        ship_nr+=1
        unit=VS.getUnit(ship_nr)
    return unit

def getUnitByFgIDFromNumber(fgid, ship_nr):
    unit=VS.getUnit(ship_nr)
    found_unit=VS.Unit()
    while(unit and not found_unit):
        unit_fgid=unit.getFgID()
        if(unit_fgid==fgid):
            found_unit=unit
        ship_nr=ship_nr+1
        unit=VS.getUnit(ship_nr)
    return found_unit

def getUnitByFgID(fgid):
    return getUnitByFgIDFromNumber(fgid,0)

def setTargetShip(which_fgid,target_fgid):
    target_unit=getUnitByFgID(target_fgid)
    setPreciseTargetShip(which_fgid,target_unit)

def removeFg(which_fgid):
    ship_nr=0
    un=VS.getUnit(ship_nr)
    while(un):
        unit_fgid=un.getFgID()
        if(unit_fgid[:len(which_fgid)]==which_fgid):
            un.Kill()
        else:
            ship_nr=ship_nr+1
        un=VS.getUnit(ship_nr)



# A collection of functions useful for dealing with flightgroup tuples.
# Added as used.
# For more information on the types of veriables used,
# see the VS python doc in the manual.

# Cloaks or uncloaks (1 or 0) a flightgroup tuple (tup).
def TfgCloak(state,tup):
    num = len(tup)
    for i in range(num):
        tup[i].Cloak(state)
        num = num + 1

# Tells us if a tup is null
def TfgisNull(tup):
    num = 0
    for i in tup:
        if (i):
            num = num + 1
    if num == 0:
        return 1
    else:
        return 0

# Returns an integer value of the number of ships in the tup.  Not sure if it takes notice of null state.
def TfgHeadCount(tup):
    num = 0
    for i in tup:
        if (i):
            num = num + 1
    return num

# Sets a whole tupled flightgroup on a target.
def setTfgDirective(tup,tgt,dir):
    num = len(tup)
    for i in range(num):
        tup[i].SetTarget(tgt)
        tup[i].setFgDirective(dir)

# Jumps a whole fg tuple using the JumpTo command.
def TfgJumpTo(tup,system):
    num = len(tup)
    for i in range(num):
        tup[i].JumpTo(system)
