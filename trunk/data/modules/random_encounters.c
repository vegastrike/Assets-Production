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
  void init(float sigdis, float detectiondis, float gendis, int minnships, int gennships, float capprob){
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
      object launched = launch.launch_wave_around_unit("privateer",myfaction,rnd,"default",numship,generation_distance,un);
      if ((_std.Rnd())<capship_prob) {
	launched=launch.launch_wave_around_unit("privateer",myfaction,rnd,"default",1,generation_distance,un);
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
	if (!unit.isSignificant(un)) {
	  object name = _unit.getFgName (un);
	  _io.printf ("unit not sig %d %s",num_ships,name);
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
	if (!unit.isSignificant(un)) {
	  object name = _unit.getFgName (un);
	  //	  _io.printf ("unit not sig %d %s",num_ships,name);
	  num_ships=num_ships+1;
	}
      }
      count=count+1;
      un = _unit.getUnit(count);
    }
    return num_ships>=n;
  };
 
  object decideMode() {
    object un= _unit.getUnit (last_ship);
    if (_std.isNull (un)) {
      curmode=0;
      last_ship=0;
    }else {
      object player_unit=_unit.getPlayer();
      if (!_std.isNull(player_unit)) {
	if ((_unit.getDistance(un,player_unit)<significant_distance)&&(unit.isSignificant(un))) {
	  //	  _io.printf ("playerwithin obj");
	  curmode=1;
	  last_ship=0;
	  return un;
	}	  
      }
      last_ship=last_ship+1;
    }
    _std.setNull(un);
    return un;
  };
  void loop() {
    //    _io.printf ("loop");
    object un = decideMode ();
    if (curmode!=lastmode) {
      //      _io.printf ("curmodechange %d %d",curmode,lastmode);
      lastmode=curmode;//processed this event; don't process again if in critical zone
      if (!_std.isNull(un)) {
	if (!atLeastNInsignificantUnitsNear (un,min_num_ships)) {
	  //determine whether to launch more ships next to significant thing based on ships in that range  
	  //	  _io.printf ("launch near");
	  launch_near (un);
	} 
	//	_io.printf ("found done");
      }
      //      _io.printf ("mode change done");
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

