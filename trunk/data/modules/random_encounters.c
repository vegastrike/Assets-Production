module random_encounters {
  import random;
  import faction_ships;
  import launch;
  int last_ship;
  float significant_distance;
  float detection_distance;
  float generation_distance;
  int min_num_ships;//the number of ships that have to be there or else more will be made
  int gen_num_ships;//the num ships to be made
  float capship_prob;//probability a capship will be there
  int curmode;//are we in battle mode (true) or cruise mode (false)
  int lastmode;//were we in battle mode (true) or cruise mode(false)
  object sig_container;
  void init(float sigdis, float detectiondis, float gendis, int minnships, int gennships, float capprob){
    _std.setNull(sig_container);
    faction_ships.init();
    detection_distance = detectiondis;
    significant_distance = sigdis;
    last_ship=0;
    curmode=0;
    lastmode=0;
    generation_distance=gendis;
    min_num_ships=minnships;
    gen_num_ships=gennships;
    capship_prob=capprob;
  };
  void launch_near (object un) {
    int numfactions=random.randomint(0,3);
    if (numfactions==0) {
      numfactions=1;
    }
    int i=0;
    while (i<numfactions) {
      int fac = random.randomint(0,faction_ships.getMaxFactions()-1);
      int numship= random.randomint (1,gen_num_ships);
      object rnd= faction_ships.getRandomFighterInt(fac);
      object myfaction = faction_ships.intToFaction(fac);
      object launched = launch.launch_wave_around_unit("privateer",myfaction,rnd,"default",numship,200.0,generation_distance,un);
      if ((_std.Rnd())<capship_prob) {
	launched=launch.launch_wave_around_unit("privateer",myfaction,rnd,"default",1,200.0,generation_distance,un);
      }
      i=i+1;
    }
  };

  bool test_atLeastNInsignificantUnitsNear (object unit, int n) {
    int num_ships=0;
    int count=0;
    object un = _unit.getUnit (count);
    while (!(_std.isNull(un))) {
      if (_unit.getDistance(unit,un)<detection_distance) {
	if ((!_unit.isSignificant(un))&&(!_unit.isSun(un))) {
	  object name = _unit.getFgName (un);
	  object testname2 = _unit.getName(un);
	  _io.printf ("unit not sig %d %s %s\n",num_ships,name,testname2);
	  num_ships=num_ships+1;
	  if (num_ships>=n){
	    return true;
	  }
	}
      }
      count=count+1;
      un = _unit.getUnit(count);
    }
    return false;
  };


  bool atLeastNInsignificantUnitsNear (object unit, int n) {
    int num_ships=0;
    int count=0;
    object un = _unit.getUnit (count);
    while (!(_std.isNull(un))) {
      if (_unit.getDistance(unit,un)<detection_distance) {
	if ((!_unit.isSignificant(un))&&(!_unit.isSun(un))) {
	  object name = _unit.getFgName (un);
	  object testname2 = _unit.getName(un);
	  float blah = _unit.getDistance(unit,un);
	  _io.printf ("unit not sig %d %f %s %s\n",num_ships,blah,name,testname2);
	  num_ships=num_ships+1;
	}
      }
      count=count+1;
      un = _unit.getUnit(count);
    }
    return num_ships>=n;
  };
  void SetModeZero() {
    last_ship=0;
    curmode=0;
    if (!_std.isNull(sig_container)) {
      _unit.deleteContainer (sig_container);
      _std.setNull(sig_container);
    }
  };
  void SetModeOne (object significant) {
    SetModeZero();
    curmode=1;
    sig_container = _unit.getContainer (significant);
  };
  object HaveWeSignificant () {
    if (_std.isNull (sig_container)) {
      return sig_container;
    }
    object significant_unit=_unit.getUnitFromContainer (sig_container);
    if (_std.isNull(significant_unit)) {
      _unit.deleteContainer (sig_container);
      _std.setNull(sig_container);
    }
    return significant_unit;
  };
  object decideMode() {
    object player_unit=_unit.getPlayer();
    if (_std.isNull(player_unit)) {
      SetModeZero();
      return player_unit;
    }
    
    object significant_unit = HaveWeSignificant();
    if (_std.isNull(significant_unit)) {
      object un= _unit.getUnit (last_ship);
      if (_std.isNull (un)) {
	SetModeZero();
      }else {
	if ((_unit.getDistance(un,player_unit)<significant_distance)&&(_unit.isSignificant(un))) {
      	  _io.printf ("playerwithin obj");
	  SetModeOne (un);
	  return un;
	}	  
	last_ship=last_ship+1;
      }
      _std.setNull(un);
      return un;
    } else {
      //significant_unit is somethign.... lets see what it is
      if (_unit.getDistance (significant_unit,player_unit)>detection_distance) {
	SetModeZero ();
	return sig_container;
      } else {
	return significant_unit;
      }
    }
  };
  void loop() {
    //    _io.printf ("loop");
    object un = decideMode ();
    if (curmode!=lastmode) {
      _io.printf ("curmodechange %d %d",curmode,lastmode);
      lastmode=curmode;//processed this event; don't process again if in critical zone
      if (!_std.isNull(un)) {
	if (!atLeastNInsignificantUnitsNear (un,min_num_ships)) {
	  //determine whether to launch more ships next to significant thing based on ships in that range  
      	  _io.printf ("launch near");
	  launch_near (un);
	} 
       	_io.printf ("found done");
      }
      _io.printf ("mode change done");
    }
    //    _io.printf ("loopdone");
  };
  void initstarsystem () {
    last_ship=0;
    loop();
    while (last_ship!=0) {
      loop();//goes through all ships in system to make sure enemies are there when arrive
    }
  };

}

