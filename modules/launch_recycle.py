import vsrandom
import unit
import launch
import VS
import faction_ships

def NextPos (un, pos):
  rad=un.rSize ()
  whichcoord = vsrandom.randrange(0,3)
  x = pos[whichcoord]
  pos = list(pos)
  x=x+3.0*rad
  pos[whichcoord]=x
  return tuple(pos)

def move_to (un, where):
  un.SetPosition(where)
  un.SetTarget (VS.Unit())
  return NextPos (un,where)

def whereTo (radius, launch_around):
  pos = launch_around.Position ()    
  rsize = ((launch_around.rSize())*5.0)+5.0*radius
  return (pos[0]+rsize*vsrandom.randrange(-1,2,2),
          pos[1]+rsize*vsrandom.randrange(-1,2,2),
          pos[2]+rsize*vsrandom.randrange(-1,2,2))

def look_for (fg, faction, numships,myunit,  pos, gcd):
  i=0
  un = VS.getUnit (i)
  while (un):
    i+=1
    un = VS.getUnit (i)
  i-=1 #now our i is on the last value
  while ((i>=0) and (numships>0)):
    un = VS.getUnit (i)
    if (un):
      if (un.getSignificantDistance(myunit)>gcd ):
        fac = un.getFactionName ()
        fgname = un.getFlightgroupName ()
        name = un.getName ()
        if ((fg==fgname) and (fac==faction)):
            if (numships>0):
              if (vsrandom.random()<0.75):
                pos=move_to (un,pos)
                numships-=1
                print "TTYmoving %s to current area" % (name)
            else:
              #toast 'im!
              un.Kill()
              print "TTYaxing %s" % (name)
    i-=1
  return (numships,pos)

def LaunchNext (fg, fac, type, ai, pos, logo):
  newship = launch.launch (fg,fac,type,ai,1,1,pos,logo)
  import dynamic_universe
  dynamic_universe.TrackLaunchedShip(fg,fac,type,newship)
  rad=newship.rSize ()
  VS.playAnimation ("warp.ani",pos,(3.0*rad))
  return NextPos (newship,pos)

def launch_types_around ( fg, faction, typenumbers, ai, radius, myunit, garbage_collection_distance,logo):
  pos = whereTo(radius, myunit)
  nr_ships=0
  for t in typenumbers:
    nr_ships+=t[1]
  print "before"+str(nr_ships)
  (nr_ships,pos) = look_for (fg,faction,nr_ships,myunit,pos,garbage_collection_distance)
  print "after "+str(nr_ships)
  count=0
  for tn in typenumbers:
    num = tn[1]
    if num>nr_ships:
      num=nr_ships
    for i in range(num):
      pos = LaunchNext (fg,faction,tn[0], ai, pos,logo)
    nr_ships-=num
    if (nr_ships==0):
      return


def launch_wave_around ( fg, faction, ai, nr_ships, capship, radius, myunit, garbage_collection_distance,logo):
  pos = whereTo(radius, myunit)
  print "before"+str(nr_ships)
  (nr_ships,pos) = look_for (fg,faction,nr_ships,myunit,pos,garbage_collection_distance)
  print "after "+str(nr_ships)
  while (nr_ships>0):
    type=""
    if (capship):
      type = faction_ships.getRandomCapitol(faction)
    else:
      type = faction_ships.getRandomFighter(faction)
    pos = LaunchNext (fg,faction,type, ai, pos,logo)
    nr_ships-=1
 
