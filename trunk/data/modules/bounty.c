module bounty {
	object faction;
	object destination;
	object enemycontainer;
	bool arrived;
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
	    _io.message (1,"game","all","In order to get to your destination, you must:");
	    sys(sysfile,numsystemsaway);
	    if (quantity<1){
	      quantity=1;
	    }
	    if (tempquantity>0) {
	      cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
	    }
	    
	    _io.sprintf(str,"Kill a %s unit.",faction);
	    _io.message (2,"game","all",str);
	    _io.sprintf(str,"You will receive %d of the %s cargo",quantity,cargoname);
	    _io.message (3,"game","all",str);
	    _string.delete(str);
	  } else {
	    _std.terminateMission (false);
	  }
	};
	  _std.terminateMission(false);
	void loop () {
	  if (arrived) {
	    object base=_unit.getUnitFromContainer(basecontainer);
	    object you=_unit.getPlayer();
	    if (_std.isNull(base)||_std.isNull(you)) {
	      _std.terminateMission(false);
	      return;
	    }
	    float dist=_unit.getDistance(base,you);
	    if (dist<=distfrombase) {
	      takeCargoAndTerminate(you);		
	      return;
	    }
	  } else {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=true;
	      object newship=faction_ships.getRandomCapitol(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getSignificant (randint);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      }
	      if (_std.isNull(significant)) {
		arrived=false;
	      }else {
		if (capship) {
		  significant=launch.launch_wave_around_unit("shadow",faction,newship,"default",1,5000.0,significant);
		}
		object str = _string.new();
		object name = _unit.getName (significant);
		_io.sprintf(str,"You must drop your cargo off with the %s unit",name);
		_io.message (0,"game","all",str);
		_string.delete(str);
		
		basecontainer=_unit.getContainer(significant);
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
}