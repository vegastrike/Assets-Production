module bounty {
	object faction;
	object destination;
	object enemycontainer;
	object youcontainer;
	object sigcont;
	object newship;
	int arrived;
	int difficulty;
	int curiter;
	int difficulty;
	float cred;
	//	import ai_stationary;
	import universe;
	import random;
	import launch;
	import faction_ships;
	bool istarget;
	bool runaway;
	object systemlist;
	void destroy () {
	  _olist.delete (systemlist);
	  _string.delete (faction);
	  _string.delete (destination);
	  if (!_std.isNull(sigcont)) {
	    _unit.deleteContainer (sigcont);
	  }
	  if (!_std.isNull(youcontainer)) {
	     _unit.deleteContainer (youcontainer);
	  }
	  if (!_std.isNull(enemycontainer)) {
	    _unit.deleteContainer (enemycontainer);
	  }
	};
	void initrandom (int minns, int maxns, float credsmin, float credsmax, bool run_away, int minshipdifficulty, int maxshipdifficulty) {
	  faction_ships.init();	    
	  object you=_unit.getPlayer();
	  object tempfaction;
	  if (!_std.isNull(you)) {
	    object name = _unit.getFaction (you);
	    int factionname=random.randomint(0,faction_ships.getMaxFactions()-1);
	    tempfaction=faction_ships.intToFaction(factionname);
	    while (_string.equal(name,tempfaction)) {
	      int factionname=random.randomint(0,faction_ships.getMaxFactions()-1);
	      tempfaction=faction_ships.intToFaction(factionname);
	    }
	    int sd = random.randomint (minshipdifficulty,maxshipdifficulty);
	    initstage2 (minns,maxns,(1.0+(_std.Float(sd)*0.5))*random.random (credsmin, credsmax),run_away,sd,tempfaction);
	    _string.delete (name);
	  }else {
	    _std.terminateMission(false);
	  }
	};
	void init (int minnumsystemsaway, int maxnumsystemsaway, float creds, bool run_away, int shipdifficulty, object tempfaction) {
	  faction_ships.init();	    
	  initstage2 (minnumsystemsaway,maxnumsystemsaway,creds,run_away,shipdifficulty,tempfaction);
	};
	void initstage2 (int minnumsystemsaway, int maxnumsystemsaway, float creds, bool run_away, int shipdifficulty, object tempfaction) {

	  systemlist = _olist.new();
	  faction = tempfaction;	  
	  _std.setNull(newship);
	  _std.setNull(sigcont);
	  _std.setNull(enemycontainer);
	  _std.setNull(youcontainer);
	  difficulty = shipdifficulty;
	  runaway=run_away;

	  arrived=0;
	  curiter=0;
	  istarget=false;
	  cred=creds;
	  object mysys=_std.getSystemFile();
	  object sysfile = _std.getSystemFile();
	  object you=_unit.getPlayer();
	  youcontainer = _unit.getContainer (you);
	  if (!_std.isNull(you)) {

	    object name=_unit.getName(you);
	   
	    object str = _string.new();
	    _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	    _string.delete (name);
	    _io.message (0,"game","all",str);
	    _io.message (0,"game","all","In order to get to your destination, you must:");
	    destination=universe.getAdjacentSystem (sysfile,random.randomint (minnumsystemsaway,maxnumsystemsaway),systemlist);
	    _io.sprintf(str,"Once there, you must destroy a %s unit.",faction);
	    _io.message (2,"game","all",str);
	    _io.message (3,"game","all","You will then recieve credits as your reward");
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
	    destroy();
	    _std.terminateMission(true);
	  }
	};

	void Lose (bool terminate) {
	  _io.message(0,"game","all","You have failed this mission and will not be rewarded.");
	  if (terminate) {
	    destroy();
	    _std.terminateMission(false);
	  }
	};

	void loop () {
	  bool isSig;
	  object enemy;
	  object you=_unit.getUnitFromContainer(youcontainer);
	  if (_std.isNull(you)) {
	    Lose (true);
	    return;
	  }
	  if (arrived==3) {
	    enemy=_unit.getUnitFromContainer(enemycontainer);
	    if (!istarget) {
	      object curun=_unit.getUnit(curiter);
	      if (!_std.isNull (enemy)) {
		if (_std.equal(curun,enemy)) {
		  _unit.setTarget(enemy,you);
		}
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
	    if (!_string.equal (sysfil,destination)) {
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
	    if (_std.isNull (significant)) {
	      _std.terminateMission(false);
	    }else {
	      if (unit.getSignificantDistance(you,significant)<10000.0) {
		if (_std.isNull(newship)) {
		  newship=faction_ships.getRandomFighter(faction);
		}
		enemy=launch.launch_wave_around_unit("Base",faction,newship,"default",1+difficulty,3000.0,4000.0,significant);
		enemycontainer=_unit.getContainer(enemy);
		if (!_std.isNull(enemy)) {
		  if (runaway) {
		    _unit.setTarget(enemy,significant);
		    _unit.Jump(enemy);
		    arrived=2;
		  } else {
		    arrived=3;
		  }
		}
	      }
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
		sigcont=_unit.getContainer(significant);
		isSig=true;
	      }
	      if (_std.isNull(significant)) {
		a_std.terminateMission (false);
	      } else {
		object localdestination=_unit.getName(significant);
		if (isSig) {	//ADD OTHER JUMPING IF STATEMENT CODE HERE
		} else {
		  enemy=launch.launch_wave_around_unit("Base",faction,newship,"default",1+difficulty,500.0,1000.0,significant);
		  enemycontainer=_unit.getContainer(enemy);
		  _unit.setTarget(you,enemy);
		  arrived=2;
		}
		object str = _string.new();
		_io.sprintf(str,"You must destroy the %s unit in this system.",newship);
		_io.message (0,"game","all",str);
		if (isSig) {	//ADD OTHER JUMPING IF STATEMENT CODE HERE ALS0
		  if (runaway) {
		    _io.message (3,"game","all","oh no... He is running towards the jump point.  Catch him quick!");
		    _io.sprintf(str,"he is going to %s",localdestination);
		  }else {
		    _io.message (3,"game","all","Scanners are picking up a metallic object!");
		    _io.sprintf(str,"Coordinates appear near %s",localdestination);
		  }
		  _io.message (4,"game","all",str);
		}
		_string.delete(str);
		
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
	void initbriefing() {
	  
	};
	void loopbriefing() {
	  
	};
	void endbriefing() {
	  
	};
}
