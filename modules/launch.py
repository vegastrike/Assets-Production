from difficulty import usingDifficulty
import vsrandom
import unit
import ship_upgrades
import VS
import sys
import dj_lib
def launch (fgname, faction, type,ai, nr_ships, nr_waves, vec, logo='',useani=True):
  diff=usingDifficulty()
  if useani:
    VS.playAnimation ("warp.ani",vec,300.0)
  if (not diff or (type.find(".blank")==-1)):
    ret = VS.launch (fgname,type,faction,"unit",ai,nr_ships,nr_waves,VS.SafeEntrancePoint (vec,40),logo)
    dj_lib.PlayMusik(0,dj_lib.HOSTILE_NEWLAUNCH_DISTANCE)
    return ret
  rsize=0.0
  diffic = VS.GetDifficulty()
  ret=VS.Unit()
  for i in range(nr_ships):
    mynew=VS.launch(fgname,type,faction,"unit",ai,1,nr_waves,VS.SafeEntrancePoint (vec,40),logo)
    if (i==0):
      ret = mynew
      rsize =mynew.rSize ()*1.75
    ship_upgrades.upgradeUnit ( mynew,diffic)
    vec=(vec[0]-rsize,
         vec[1],#-rsize
        vec[2]-rsize)
  dj_lib.PlayMusik(0,dj_lib.HOSTILE_NEWLAUNCH_DISTANCE)
  return ret

def launch_waves_around_area(fgname,faction,type,ai,nr_ships,nr_waves,r1,r2,pos,logo='',useani=True):
  pos=((pos[0]+vsrandom.uniform(r1,r2)*vsrandom.randrange(-1,2,2)),
       (pos[1]+vsrandom.uniform(r1,r2)*vsrandom.randrange(-1,2,2)),
       (pos[2]+vsrandom.uniform(r1,r2)*vsrandom.randrange(-1,2,2)))
  return launch(fgname,faction,type,ai,nr_ships,nr_waves,pos,logo,useani)

def launch_wave_around_area(fgname,faction,type,ai,nr_ships,r1,r2,pos,logo='',useani=True):
  return launch_waves_around_area (fgname,faction,type,ai,nr_ships,1,r1,r2,pos,logo,useani)

def launch_around_station(station_name,fgname,faction,type,ai,nr_ships,nr_waves,logo='',useani=True):
  station_unit=unit.getUnitByFgID(station_name)
  if(station_unit.isNull()):
    sys.stderr.write("launch.py:launch_around_station did not find unit %s\n" % (station_name))
    return VS.Unit()
  station_pos=station_unit.Position()
  rsize=station_unit.rSize()
  launched =launch_waves_around_area(fgname,faction,type,ai,nr_ships,nr_waves,rsize,rsize*2.0,station_pos,logo,useani)
  return launched

launch_around_unit=launch_around_station

def launch_waves_in_area(fgname,faction,type,ai,nr_ships,nr_waves,radius,pos,logo='',useani=True):
  pos=(pos[0]+vsrandom.uniform((-radius)/2,radius/2.0),
       pos[1]+vsrandom.uniform((-radius)/2,radius/2.0),
       pos[2]+vsrandom.uniform((-radius)/2,radius/2.0))
  un = launch(fgname,faction,type,ai,nr_ships,nr_waves,pos,logo,useani)

def launch_wave_in_area(fgname,faction,type,ai,nr_ships,radius,pos,logo='',useani=True):
  launch_waves_in_area(fgname,faction,type,ai,nr_ships,1,radius,pos,logo,useani)

def launchShipsAtWaypoints(waypoints,faction,type,ainame,nr,logo='',useani=True):
  i=0
  for wp in waypoints:
    outstr="wp%d" % (i)
    launch(outstr,faction,type,ainame,nr,1,wp,logo,useani)
    i+=1

def launch_wave_around_unit (fgname, faction, type, ai, nr_ships, minradius, maxradius, my_unit,logo='',useani=True):
  myvec = (0,0,0)
  if (my_unit.isNull()):
    un=launch_wave_around_area (fgname,faction,type,ai,nr_ships,minradius,maxradius,myvec,logo,useani)
    return un
  myvec=my_unit.LocalPosition()
  print myvec
  rsiz=my_unit.rSize()
  un=launch_wave_around_area (fgname,faction,type,ai,nr_ships,rsiz+minradius,rsiz+maxradius,myvec,logo,useani)
  return un

def launch_wave_around_significant (fgname,faction,type,ai,nr_ships,minradius, maxradius,significant_number,logo='',useani=True):
  significant_unit=unit.getSignificant(significant_number,0,0)
  if (significant_unit.isNull()):
    significant_unit = VS.getPlayer()
  launched = launch_wave_around_unit(fgname,faction,type,ai,nr_ships,minradius,maxradius,significant_unit,logo,useani)
  return launched

