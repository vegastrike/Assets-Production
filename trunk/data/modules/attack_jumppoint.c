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
  int ship_check_count;
  bool defend;
  
	void init (int factionname, int numsystemsaway, int enemyquantity, float distance_from_base, float escape_distance, float creds, bool defend_base) {
	  ship_check_count=0;
	  defend = defend_base;
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
	    //don't destruct...something else went wrong
	    _std.terminateMission (false);
	    return;
	  }
	  object str = _string.new();
	  _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	  _string.delete (name);
	  _io.message (0,"game","all",str);
	  go_somewhere_significant.init(you,numsystemsaway,defend,false,distance_from_base);

	  _io.sprintf(str,"And there eliminate any %s starships at a point.",faction);
	  _io.message (2,"game","all",str);
	  _string.delete(str);
	};
	void destroy () {
	  _unit.deleteContainer (youcontainer);
	  _std.setNull (youcontainer);
	  _string.delete (faction);
	  _std.setNull (faction);
	  go_somewhere_significant.destroy();
	};
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  destroy();
	  _std.terminateMission(true);
	};
	void FailMission(object you) {
	  cred = 0.0-cred;
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","You Allowed the base you were to protect to be destroyed.");
	  _io.message (0,"game","all","You are a failure to your race!");
	  _io.message (1,"game","all","We have contacted your bank and informed them of your failure to deliver on credit. They have removed a number of your credits for this inconvenience. Let this serve as a lesson.");
       	  destroy();
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
	  if (defend) {
	    if (!_std.isNull(jp)) {
	      object nam = _unit.getName (jp);
	      _io.sprintf (str,"You must protect %s.",nam);
	      _string.delete (nam);
	      _io.message (0,"game","all",str);
	    }
	  }
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
	      destroy();
	      _std.terminateMission(false);
	    }else {
	      object base = go_somewhere_significant.SignificantUnit();
	      if (_std.isNull(base)) {
		if (defend) {
		  FailMission(you);
		}else {
		  SuccessMission(you);
		}
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
