module bounty {
	object faction;
	object destination;
	object enemycontainer;
	int arrived;
	int difficulty;
	float cred;
	import random;
	import launch;
	import faction_ships;
	bool capship;
	void sys (object currentsystem, int sysaway) {
	  object str = _string.new();
	  if (sysaway<=0) {
	    destination=currentsystem;
	    _io.sprintf(str,"%s will be your destination.",currentsystem);
	    _io.message (0,"game","all",str);
	  } else {
	    int max=_std.getNumAdjacentSystems(currentsystem);
	    if (max>0) {
	      int nextsysnum=random.randomint(0,max-1);
	      object nextsystem=_std.getAdjacentSystem(currentsystem,nextsysnum);
	      _io.sprintf(str,"Jump from %s to %s.",currentsystem,nextsystem);
	      _io.message (0,"game","all",str);
	      sys(nextsystem,sysaway-1);
	    } else {
	      destination="sol_sector/sol";
	    }
	  }
	  _string.delete(str);
	};
	
	void init (int int numsystemsaway, int missiondifficulty, float creds) {
	  faction_ships.init();
	  arrived=false;
	  isSig=false;
	  cred=creds;
	  distfrombase=distance_from_base;
	  difficulty=missiondifficulty;
	  object mysys=_std.getSystemFile();
	  object sysfile = _std.getSystemFile();
	  object you=_unit.getPlayer();
	  if (!_std.isNull(you)) {
	    object name = _unit.getFaction (you);
	    int factionname=random.randomint(0,2);
	    faction=faction_ships.intToFaction(factionname);
	    while (!(_string.equal(name,faction))) {
	      int factionname=random.randomint(0,2);
	      faction=faction_ships.intToFaction(factionname);
	    }
	    name=_unit.getName(you);
	    object str = _string.new();
	    _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	    _io.message (0,"game","all",str);
	    _io.message (0,"game","all","In order to get to your destination, you must:");
	    sys(sysfile,numsystemsaway);
	    if (quantity<1){
	      quantity=1;
	    }
	    if (tempquantity>0) {
	      cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
	    }
	    
	    _io.sprintf(str,"Once there, you must destroy a %s unit.",faction);
	    _io.message (2,"game","all",str);
	    _io.message (3,"game","all","You will then recieve lots of money as your reward");
	    _io.message (4,"game","all","(if you survive).  Good luck!");
	    _string.delete(str);
	  } else {
	    _std.terminateMission (false);
	  }
	};

	void Win (object who, bool terminate) {
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  _io.message (0,"game","all","Your contribution to the war effort will be remembered.");
	  _unit.addCredits(who,cred);
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
	  if (arrived==2) {
	    enemy=_unit.getUnitFromContainer(enemycontainer);
	    object you=_unit.getPlayer();
	    if (_std.isNull(you)) {
	      Lose(true);
	      return;
	    }
	    if (_std.isNull(enemy)) {
	      Win(you,true);
	      return;
	    }
	  } else if (arrived==1) {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      object you=_unit.getPlayer();
	      arrived=2;
		  enemy=_unit.getUnitFromContainer(enemycontainer);
	      if (_std.isNull(you)) {
		Lose(true);
		return;
	      }
	      if (_std.isNull(enemy)) {
		Win(you,true);
		return;
	      }
		  _unit.setTarget(enemy,you);
		  _unit.setTarget(you,enemy);
	    }
	  } else {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=1;
	      object newship=faction_ships.getRandomFighter(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getJumppoint (randint);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
		  } else {
		isSig=true;
		  }
	      if (_std.isNull(significant)) {
		_std.terminateMission (false);
	      }else {
		enemy=launch.launch_wave_around_unit("shadow",faction,newship,"default",1,10000.0,significant);
		if (isSig) {
		  _unit.setTarget(enemy,significant);
		  destination=_unit.getName(significant);
		}
		object str = _string.new();
		object name = _unit.getName (enemy);
		_io.sprintf(str,"You must destroy the %s unit in this system.",name);
		_io.message (0,"game","all",str);
		_io.message (3,"game","all","oh no... He is running towards the jump point.  Catch him quick!");
		_string.delete(str);
		
		enemycontainer=_unit.getContainer(enemy);
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
}