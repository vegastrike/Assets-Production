  import random
  import unit
  import launch
  import VS
  import faction_ships

  def NextPos (un, pos):
    rad=_unit.getRSize (un)
    whichcoord = random.random(0,2)
    x = _olist.at (pos,whichcoord)
    x=x+3.0*rad
    _olist.set (pos,whichcoord,x)
  
  def move_to (un, where):
    un.setPosition(where)
    un.setTarget (VS.Unit())
    NextPos (un,where)
  
  def whereTo (radius, launch_around):
    pos = launch_around.getPosition ()    
    rsize = ((launch_around.rSize())*2.0)+radius
    pos=(pos[0]+rsize*random.randomsign()
         pos[1]+rsize*random.randomsign()
         pos[2]+rsize*random.randomsign())
    return pos
  
  def look_for (fg, faction, numships,myunit,  pos, gcd):
    i=0
    un = VS.getUnit (i)
    while (un):
      i+=1
      un = VS.getUnit (i)
    i-=1 #now our i is on the last value
    while ((i>=0)&&(numships>0)):
      un = VS.getUnit (i)
      if (un):
	if (un.getSignificantDistance(myunit)>gcd ):
	  fac = un.getFaction ()
	  fgname = un.getFlightgroupName ()
	  name = un.getName ()
	  if (fg==fgname)):
	    if (fac==faction)):
	      if (numships>0):
		if (random.random()<0.75):
		  move_to (un,pos)
		  numships-=1
		  print "TTYmoving %s to current area" % (name)
	      else:
		#toast 'im!
		un.Kill()
		print "TTYaxing %s" % (name)
      i-=1
    return numships
  
  def LaunchNext (fg, fac, type, ai, pos, logo):
    newship = launch.launch (fg,fac,type,ai,1,1,pos,logo)
    rad=_unit.getRSize (newship)
    VS.playAnimation ("warp.ani",pos,(3.0*rad))
    NextPos (newship,pos)

  def launch_wave_around ( fg, faction, ai, nr_ships, capship, radius, myunit, garbage_collection_distance,logo):
    pos = whereTo(radius, myunit)
    nr_ships = look_for (fg,faction,nr_ships,myunit,pos,garbage_collection_distance)
    while (nr_ships>0):
      type=""
      if (capship):
	type = faction_ships.getRandomCapitol(faction)
      else:
	type = faction_ships.getRandomFighter(faction)
      LaunchNext (fg,faction,type, ai, pos,logo)
      nr_ships-=1
   
