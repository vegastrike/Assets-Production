##import ai_flyto_jumppoint
##current_system=""
##last_system=""
##old_system=""
##system_map={}
##outstr=""

import VS
import random
import faction_ships
import launch
def getAdjacentSystems (currentsystem, sysaway, jumps=()):
    """returns a tuple in the format ("[lastsystem]",(system1,system2,system3,...))"""
    max=VS.GetNumAdjacentSystems(currentsystem)
    if ((sysaway<=0) or (max<=0)):
#      _io.message (1,"game","all","Your final destination is %s" % (currentsystem))
      return (currentsystem,jumps)
    else:
      for i in range (10):
        nextsystem=VS.GetAdjacentSystem(currentsystem,random.randrange(0,max))
        if (not (nextsystem in jumps) and (not (nextsystem == VS.getSystemFile()))):
          break
      else:
        return getAdjacentSystems(currentsystem,0,jumps)
#      _io.message (1,"game","all","Jump from %s to %s." % (currentsystem,nextsystem))
      return getAdjacentSystems(nextsystem,sysaway-1,jumps+(nextsystem,))
  
#def getAdjacentSystems (currentsystem, num_systems_away):
#    return nearsys (currentsystem,num_systems_away,()) 
  
def getRandomJumppoint():
    jp_list=getJumppointList()
    size=len(jp_list)
    if (size>0):
      return jp_list[random.randrange(0,size)]
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

