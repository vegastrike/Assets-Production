module garbage_collect {
  import random;
  import random_encounters;
  int last_ship;
  float invalid_distance;
  void init(float invaliddis){
    invalid_distance = invaliddis;
    last_ship=0;
  };
   void Loop() {
    object un= _unit.getUnit (last_ship);
    if (_std.isNull (un)) {
      last_ship=0;
    }else {
      object player_unit=_unit.getPlayer();
      if (!std.isNull(player_unit)) {
	if (_unit.getDistance(un,player_unit)>invalid_distance&&(!_unit.isSignificant(un))&&(!_unit.isSun(un))) {
	  last_ship=last_ship-1;
	  _unit.removeFromGame(un);
	}	  
      }
      last_ship=last_ship+1;
    }
    //determines if last_ship puts you in battle or cruise mode
  };
}

