module attack_jumppoint {
  import ai_stationary;
  import universe;
  import go_somewhere_significant;
  object youcontainer;
  object faction;
  

  float escdist;
  int quantity;
  float cred;
  import random;
  import launch;
  import faction_ships;
  import go_somewhere_significant;
  int ship_check_count;

  
	void init (int factionname, int numsystemsaway, int enemyquantity, float distance_from_base, float escape_distance, float creds) {
	  ship_check_count=0;
	  faction_ships.init();

	  faction=faction_ships.intToFaction(factionname);
	  escdist = escape_distance;
	  cred=creds;

	  quantity=enemyquantity;

	  
	  object you=_unit.getPlayer();
	  youcontainer=_unit.getContainer (you);

	  object name;
	  if (!_std.isNull(you)) {
	    name = _unit.getName (you);
	  } else {
	    _std.terminateMission (false);
	    return;
	  }
	  object str = _string.new();
	  _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	  _io.message (0,"game","all",str);
	  go_somewhere_significant.init(you,numsystemsaway,true,distance_from_base);

	  _io.sprintf(str,"And there eliminate any %s starships at a point.",faction);
	  _io.message (2,"game","all",str);
	  _string.delete(str);
	};
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  _std.terminateMission(true);
	};

	bool NoEnemiesInArea (object jp) {
	  object cur = _std.getSystemFile();
	  object tmpdst = go_somewhere_significant.DestinationSystem();
	  if (!_string.equal(tmpdst,cur)) {
	    return false;
	  }
	  object un= _unit.getUnit (ship_check_count);
	  ship_check_count=ship_check_count+1;
	  if (_std.isNull (un)) {
	    return true;
	  }
	  object fac = _unit.getFaction (un);
	  object me = _unit.getUnitFromContainer (youcontainer);
	  if (!_unit.equal (un,me)) {
	    if (_string.equal (fac,faction)) {
	      if (_unit.getDistance (jp,un)<escdist) {
		ship_check_count=0;
	      }
	    }
	  }
	  return false;
	};
	void GenerateEnemies (object jp,object you) {
	  int count=0;
	  object str = _string.new();
	  _io.sprintf(str,"Eliminate all %s ships here.",faction);
	  _io.message (0,"game","all",str);
	  _string.delete(str);
	  
	  while (count<quantity) {
	    object randtype = faction_ships.getRandomFighter(faction);
	    object launched = launch.launch_wave_around_unit ("Shadow",faction,randtype,"default",1,4500.0,jp);
	    _unit.setTarget (launched,you);//make 'em attack you
	    count = count+1;
	  }
	  quantity=0;
    	};
	void loop () {
	  go_somewhere_significant.loop();
	  if (go_somewhere_significant.HaveArrived()) {
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull (you)) {
	      _std.terminateMission(false);
	    }else {
	      object base = go_somewhere_significant.SignificantUnit();
	      if (_std.isNull(base)) {
		SuccessMission(you);
	      }else {
		if (quantity>0) {
		  GenerateEnemies (base,you);
		}
		if (NoEnemiesInArea (base)) {
		  SuccessMission(you);
		}
	      }
	    }
	  }
	};
}
