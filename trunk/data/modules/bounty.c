module bounty {
	object faction;
	object destination;
	object enemycontainer;
	int arrived;
	int difficulty;
	float cred;
	import universe;
	import random;
	import launch;
	import faction_ships;
	bool capship;
	
	void init (int numsystemsaway, float creds) {
	  faction_ships.init();
	  arrived=0;
	  cred=creds;
	  object mysys=_std.getSystemFile();
	  object sysfile = _std.getSystemFile();
	  object you=_unit.getPlayer();
	  if (!_std.isNull(you)) {
	    object name = _unit.getFaction (you);
	    int factionname=random.randomint(0,2);
	    faction=faction_ships.intToFaction(factionname);
	    while (_string.equal(name,faction)) {
	      int factionname=random.randomint(0,2);
	      faction=faction_ships.intToFaction(factionname);
	    }
	    name=_unit.getName(you);
	    object str = _string.new();
	    _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	    _io.message (0,"game","all",str);
	    _io.message (0,"game","all","In order to get to your destination, you must:");
	    destination=universe.getAdjacentSystem (sysfile,numsystemsaway);
	    _io.sprintf(str,"Once there, you must destroy a %s unit.",faction);
	    _io.message (2,"game","all",str);
	    _io.message (3,"game","all","You will then recieve lots of money as your reward");
	    _io.message (4,"game","all","(if you survive).  Good luck!");
	    _string.delete(str);
	  } else {
	    _std.terminateMission (false);
	  }
	};

	void Win (bool terminate) {
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  _io.message (0,"game","all","Your contribution to the war effort will be remembered.");
	  _unit.addCredits(cred);
	  if (terminate) {
	    _std.terminateMission(true);
	  }
	};

	void Lose (bool terminate) {
	  _io.message(0,"game","all","You have failed this mission and will not be rewarded.");
	  if (terminate) {
	    _std.terminateMission(false);
	  }
	};

	void loop () {
	  bool isSig;
	  object enemy;
	  object you=_unit.getPlayer();
	  if (arrived==2) {
	    enemy=_unit.getUnitFromContainer(enemycontainer);
	    if (_std.isNull(you)) {
	      Lose(true);
	      return;
	    }
	    if (_std.isNull(enemy)) {
	      Win(true);
	      return;
	    }
	  } else if (arrived==1) {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=2;
		  enemy=_unit.getUnitFromContainer(enemycontainer);
	      if (_std.isNull(you)) {
		Lose(true);
		return;
	      }
	      if (_std.isNull(enemy)) {
		Win(true);
		return;
	      }
		  _unit.setTarget(enemy,you);
		  _unit.setTarget(you,enemy);
	    }
	  } else {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      bool isSig=false;
	      arrived=1;
	      object newship=faction_ships.getRandomFighter(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getJumpPoint (randint);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
		  } else {
		isSig=true;
		  }
	      if (_std.isNull(significant)) {
		_std.terminateMission (false);
	      }else {
		enemy=launch.launch_wave_around_unit("Base",faction,newship,"default",1,1000.0,you);
		if (isSig) {
		  _unit.setTarget(enemy,significant);
		  _unit.Jump(enemy,significant);
		  destination=_unit.getName(significant);
		}
		object str = _string.new();
		object name = _unit.getName (enemy);
		_io.sprintf(str,"You must destroy the %s unit in this system.",name);
		_io.message (0,"game","all",str);
		_io.message (3,"game","all","oh no... He is running towards the jump point.  Catch him quick!");
		_unit.setTarget(you,enemy);
	    _io.sprintf(str,"he is going to %s",destination);
	    _io.message (4,"game","all",str);
		_string.delete(str);
		
		enemycontainer=_unit.getContainer(enemy);
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
}