module bounty {
	object faction;
	object destination;
	object enemycontainer;
	object sigcont;
	object newship;
	int arrived;
	int difficulty;
	int curiter;
	float cred;
	import ai_stationary;
	import universe;
	import random;
	import launch;
	import faction_ships;
	bool istarget;
	
	void init (int numsystemsaway, float creds) {
	  faction_ships.init();
	  arrived=0;
	  curiter=0;
	  istarget=false;
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

	void Win (object un,bool terminate) {
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  _io.message (0,"game","all","Your contribution to the war effort will be remembered.");
	  _unit.addCredits(un,cred);
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
	  if (arrived==3) {
	    enemy=_unit.getUnitFromContainer(enemycontainer);
	    if (!istarget) {
	      object curun=_unit.getUnit(curiter);
	      if (_std.equal(curun,enemy)) {
		_unit.setTarget(enemy,you);
	      }
	      curiter=curiter+1;
	    }
	    if (_std.isNull(you)) {
	      Lose(true);
	      return;
	    }
	    if (_std.isNull(enemy)) {
	      Win(you,true);
	      return;
	    }
	  } else if (arrived==2) {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=3;
		  enemy=_unit.getUnitFromContainer(enemycontainer);
	      if (_std.isNull(you)) {
		Lose(true);
		return;
	      }
	      if (_std.isNull(enemy)) {
		Win(you,true);
		return;
	      }
	    } else {
	      _std.ResetTimeCompression();
	    }
	  } else if (arrived==1) {
	    object significant=_unit.getUnitFromContainer(sigcont);
		if (_unit.getDistance(you,significant)<5000.0) {
	      newship=faction_ships.getRandomFighter(faction);
	      enemy=launch.launch_wave_around_unit("Base",faction,newship,"default",1,4000.0,significant);
	      enemycontainer=_unit.getContainer(enemy);
	      _unit.setTarget(enemy,significant);
	      _unit.Jump(enemy);
	      destination=_unit.getName(significant);
	      arrived=2;
	    }
	  } else {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      bool isSig=false;
	      arrived=1;
	      object newship=faction_ships.getRandomFighter(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getJumpPoint (randint);
	      destination=_unit.getName(significant);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      } else {
		sigcont=_unit.getContainer(significant);
		isSig=true;
		  }
	      if (_std.isNull(significant)) {
		_std.terminateMission (false);
		  } else {
		if (isSig) {	//ADD OTHER JUMPING IF STATEMENT CODE HERE
		} else {
		  enemy=launch.launch_wave_around_unit("Base",faction,newship,"default",1,1000.0,significant);
		  enemycontainer=_unit.getContainer(enemy);
		  _unit.setTarget(you,enemy);
		  arrived=2;
		}
		object str = _string.new();
		_io.sprintf(str,"You must destroy the %s unit in this system.",newship);
		_io.message (0,"game","all",str);
		if (isSig) {	//ADD OTHER JUMPING IF STATEMENT CODE HERE ALS0
		  _io.message (3,"game","all","oh no... He is running towards the jump point.  Catch him quick!");
	      _io.sprintf(str,"he is going to %s",destination);
	      _io.message (4,"game","all",str);
		}
		_string.delete(str);
		
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
}
