module launch_recycle {
  import random;
  import unit;
  import launch;
  void move_to (object un, object where) {
    float x = _olist.at (where,0);
    float y = _olist.at (where,1);
    float z = _olist.at (where,2);
    _unit.setPosition(un,x,y,z);
    object temp=un;
    _std.setNull (temp);
    _unit.setTarget (un,temp);
    NextPos (un,where);
  };
  object whereTo (float radius, object launch_around) {
    object pos = _unit.getPosition (launch_around);    
    float rsize = ((_unit.getRSize(launch_around))*2.0)+radius;
    float x= _olist.at (pos,0);
    float y= _olist.at (pos,1);
    float z= _olist.at (pos,2);
    x=x+rsize*random.randomsign();
    y=y+rsize*random.randomsign();
    z=z+rsize*random.randomsign();
    _olist.set (pos,0,x);
    _olist.set (pos,1,y);
    _olist.set (pos,2,z);
    return pos;
  };
  void NextPos (object un, object pos) {
    float rad=_unit.getRSize (un);
    int whichcoord = random.randomint (0,2);
    float x = _olist.at (pos,whichcoord);
    x=x+3.0*rad;
    _olist.set (pos,whichcoord,x);
  };

  int look_for (object fg, object faction, int numships,object myunit,  object pos, float gcd) {
    int i=0;
    object un = _unit.getUnit (i);
    while (!_std.isNull (un)) {
      i=i+1;
      un = _unit.getUnit (i);
    }
    i=i-1; //now our i is on the last value
    while ((i>=0)&&(numships>0)) {
      un = _unit.getUnit (i);
      if (!_std.isNull(un)) {
	if (unit.getSignificantDistance(un,myunit)>gcd ) {
	  object fac = _unit.getFaction (un);
	  object fgname = _unit.getFgName (un);
	  object name = _unit.getName (un);
	  if (_string.equal (fg,fgname)) {
	    if (_string.equal (fac,faction)) {
	      if (numships>0) {
		if (_std.Rnd()<0.75) {
		  move_to (un,pos);
		  numships = numships-1;
		  _io.printf ("TTYmoving %s to current area\n",name);
		}
	      } else {
		//toast 'im!
		_unit.removeFromGame (un);
		_io.printf ("TTYaxing %s\n",name);
	      }
	    }
	  }
	  _string.delete (fac);
	  _string.delete (fgname);
	  _string.delete (name);
	}
      }
      i= i-1;
    }
    return numships;
  };

  void launch_wave_around ( object fg, object faction, object ai, int nr_ships, bool capship, float radius, object myunit, float garbage_collection_distance) {
    object pos = whereTo(radius, myunit);

    nr_ships = look_for (fg,faction,nr_ships,myunit,pos,garbage_collection_distance);
    while (nr_ships>0) {
      object type;
      if (capship) {
	type = faction_ships.getRandomCapitol(faction);
      }else {
	type = faction_ships.getRandomFighter(faction);
      }
      LaunchNext (fg,faction,type, ai, pos);

      nr_ships = nr_ships-1;
    }

    _olist.delete (pos);
  };
  void LaunchNext (object fg, object fac, object type, object ai, object pos) {
    object newship = launch.launch (fg,fac,type,ai,1,1,_olist.at (pos,0),_olist.at (pos,1),_olist.at (pos,2));
    float rad=_unit.getRSize (newship);
    _std.playAnimation ("warp.ani",_olist.at (pos,0),_olist.at (pos,1),_olist.at (pos,2),(3.0*rad));
    NextPos (newship,pos);
  }; 
}
