module garbage_collect {
  import random;
  import random_encounters;
  int last_ship;
  float invalid_distance;
  void init(float invaliddis){
    invalid_distance = invaliddis;
    last_ship=0;
  };
   void loop() {
    object un= _unit.getUnit (last_ship);
    if (_std.isNull (un)) {
      last_ship=0;
    }else {
      if ((!_unit.isSignificant (un))&&(!_unit.isSun(un))) {
	float dist=2.0*invalid_distance;
	int j=0;
	bool die=false;
	object player_unit;
	while (dist>=invalid_distance){
	  player_unit=_unit.getPlayerX(j);
	  if (!_std.isNull(player_unit)) {
	    dist = _unit.getDistance (player_unit,un);
	  }else {
	    dist=0.0;
	    if (j!=0) {
	      die=true;
	    }
	  }
	  j=j+1;
	}	  
	if (die) {
	  last_ship=last_ship-1;
	  object name = _unit.getName(un);
	  _unit.removeFromGame(un);
	  
	  _io.printf ("garbage collecting %s",name);
	  _string.delete (name);
	}
      }
      last_ship=last_ship+1;
    }
    //determines if last_ship puts you in battle or cruise mode
  };
}

