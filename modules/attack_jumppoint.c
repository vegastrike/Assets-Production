module attack_jumppoint {
  import ai_stationary;
  import universe;
  object youcontainer;
	object faction;
	object destination;
	object basecontainer;
	object cargoname;
	int arrived;

	float distfrombase;
	float escdist;
	int quantity;
	float cred;
	import random;
	import launch;
	import faction_ships;
	int ship_check_count;

  
	void init (int factionname, int numsystemsaway, int enemyquantity, float distance_from_base, float escape_distance, float creds) {
	  ship_check_count=0;
	  faction_ships.init();
	  faction=faction_ships.intToFaction(factionname);
	  escdist = escape_distance;
	  arrived=0;
	  cred=creds;
	  distfrombase=distance_from_base;

	  object mysys=_std.getSystemFile();
	  quantity=enemyquantity;
	  object sysfile = _std.getSystemFile();
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
	  destination=universe.getAdjacentSystem(sysfile,numsystemsaway);
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
	  if (!_string.equal(destination,cur)) {
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
	  while (count<quantity) {
	    object randtype = faction_ships.getRandomFighter(faction);
	    object launched = launch.launch_wave_around_unit ("Shadow",faction,randtype,"default",1,4500.0,jp);
	    _unit.setTarget (launched,you);//make 'em attack you
	    count = count+1;
	  }
    	};
	void loop () {
	  if (arrived==2) {
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull (you)) {
	      _std.terminateMission(false);
	    }else {
	      object base = _unit.getUnitFromContainer (basecontainer);
	      if (_std.isNull(base)) {
		SuccessMission(you);
	      }else {
		if (NoEnemiesInArea (base)) {
		  SuccessMission(you);
		}
	      }
	    }
	  }

	  if (arrived==1) {
	    object base=_unit.getUnitFromContainer(basecontainer);
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull(base)||_std.isNull(you)) {
	      _std.terminateMission(false);
	      return;
	    }
	    float dist=_unit.getDistance(base,you);
	    if (dist<=distfrombase) {
	      arrived=2;
	      GenerateEnemies (base,you);
	    }
	  } else if (arrived==0) {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=1;
	      object newship=faction_ships.getRandomCapitol(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getSignificant (randint,false);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      }
	      if (_std.isNull(significant)) {
		arrived=0;
	      }else {
		object newun=significant;
		object str = _string.new();
		object name = _unit.getName (newun);
		_io.sprintf(str,"You must visit the %s, and eliminate all %s ships there.",name,faction);
		_io.message (0,"game","all",str);
		_string.delete(str);
       		basecontainer=_unit.getContainer(significant);
	      }
	    }
	    _string.delete (sysfil);
	  }

	};
}
