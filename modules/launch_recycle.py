import random
import unit
import launch
import VS
import faction_ships

def NextPos (un, pos):
  rad=un.rSize ()
  whichcoord = random.randrange(0,3)
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
  return (pos[0]+rsize*random.randrange(-1,2,2),
          pos[1]+rsize*random.randrange(-1,2,2),
          pos[2]+rsize*random.randrange(-1,2,2))

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
              if (random.random()<0.75):
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
  rad=newship.rSize ()
  VS.playAnimation ("warp.ani",pos,(3.0*rad))
  return NextPos (newship,pos)

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
 
