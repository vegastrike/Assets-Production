##import ai_flyto_jumppoint
##current_system=""
##last_system=""
##old_system=""
##system_map={}
##outstr=""

import VS
import vsrandom
import faction_ships
import Director
import launch
def catInCatList (cat,catlist):
    for i in catlist:
        loc =cat.find (i)
        if (loc==0):
            return 1
    return 0
def adjustUnitCargo(un,cat,pr,qr):
    numcargo = un.numCargo()
    carglist =[]
    for i in range(numcargo):
        carg = un.GetCargoIndex(i)
        if (len(cat)==0 or catInCatList(carg.GetCategory(),cat)):
            carg.SetPrice (pr*carg.GetPrice())
            carg.SetQuantity (int(qr*carg.GetQuantity()))
        carglist += [carg]
    for i in range (numcargo):
        un.removeCargo (carglist[i].GetCategory(),carglist[i].GetQuantity(),1)
    for i in range (numcargo):
        un.addCargo(carglist[i])
    carglist=0
#universe.systemCargoDemand (("Natural_Products","starships",),.0001,1000)
def systemCargoDemand (category,priceratio,quantratio,ships=1,planets=1):
    i = VS.getUnitList()
    un = i.current()
    while (not un.isNull()):
        if (un.isPlayerStarship()==-1):
            isplanet = un.isPlanet()
            if ( (isplanet and planets) or ((not isplanet) and ships)):
                adjustUnitCargo(un,category,priceratio,quantratio)
        i.advance()
        un=i.current()
        
def setFirstSaveData(player,key,val):
    mylen = Director.getSaveDataLength(player,key)
    if (mylen>0):
        Director.putSaveData(player,key,0,val)
    else:
        Director.pushSaveData(player,key,val)

def getAdjacentSystems (currentsystem, sysaway, jumps=(),preferredfaction=''):
    """returns a tuple in the format ("[lastsystem]",(system1,system2,system3,...))"""
    if preferredfaction=='':
        preferredfaction=VS.GetGalaxyProperty(currentsystem,"faction")
    max=VS.GetNumAdjacentSystems(currentsystem)
    if ((sysaway<=0) or (max<=0)):
#      _io.message (1,"game","all","Your final destination is %s" % (currentsystem))
      return (currentsystem,jumps)
    else:
      syslist=[]
      numadj=VS.GetNumAdjacentSystems(currentsystem)
      for i in range(numadj):
        cursys=VS.GetAdjacentSystem(currentsystem,i)
        if preferredfaction!=None:
          if VS.GetGalaxyProperty(cursys,"faction")!=preferredfaction:
            continue
        if ((cursys in jumps) or (cursys == VS.getSystemFile())):
          continue
        syslist.append(cursys)
      if not len(syslist):
        return getAdjacentSystems(currentsystem,0,jumps)
      nextsystem=syslist[vsrandom.randrange(0,len(syslist))]
#      _io.message (1,"game","all","Jump from %s to %s." % (currentsystem,nextsystem))
      return getAdjacentSystems(nextsystem,sysaway-1,jumps+(nextsystem,))
  
#def getAdjacentSystems (currentsystem, num_systems_away):
#    return nearsys (currentsystem,num_systems_away,()) 
  
def getRandomJumppoint():
    jp_list=getJumppointList()
    size=len(jp_list)
    if (size>0):
      return jp_list[vsrandom.randrange(0,size)]
    else:
      return VS.Unit()

def getJumppointList():
    jp_list=()
    ship_nr=0
    uni=VS.getUnit(0)
    while(uni):
      if(uni.isJumppoint()):
	jp_list+=(uni,)
      ship_nr+=1
      uni=VS.getUnit(ship_nr)
    return jp_list

def getMessagePlayer(un):
    num=un.isPlayerStarship()
    if (num<0):
        return "all"
    else:
        return "p"+str(num)

def punish (you,faction,difficulty):
    if (difficulty>=2):
        VS.IOmessage (0,"mission",getMessagePlayer(you),"#ff0000Your idiocy will be punished.")
        VS.IOmessage (0,"mission",getMessagePlayer(you),"#ff0000You had better run for what little life you have left.")
        for i in range(difficulty):
            un=faction_ships.getRandomFighter(faction)
            newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 200.0,400.0,you)
            newunit.setFgDirective("B")
            newunit.SetTarget(you)


#use go_somewhere_significant instead:
##def __init__(): #(?)
##    outstr=_string.new()
##    current_system=_std.GetSystemName()
##    last_system=_std.GetSystemName()
##    old_system=_std.GetSystemName()
##    system_map=_omap.new()
##    _omap.set(system_map,current_system,current_system)
##
##def Execute():
##    jumped=false
##    current_system=_std.GetSystemName()
##    if(current_system!=last_system):
##      // we have jumped
##      _io.sprintf(outstr,"jumped from %s to %s",last_system,current_system)
##      _io.message(0,"game","all",outstr)
##      old_system=last_system
##      last_system=_std.GetSystemName()
##      jumped=true
##    return jumped

