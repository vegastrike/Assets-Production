module cargo_mission {
  import ai_stationary;
  import universe;
  object youcontainer;
	object faction;
	object destination;
	object basecontainer;
	object cargoname;
	bool arrived;
	int difficulty;
	float distfrombase;
	int quantity;
	float cred;
	import random;
	import launch;
	import faction_ships;
	bool capship;

  
	void init (int factionname, int numsystemsaway, int cargoquantity, int missiondifficulty, float distance_from_base, float creds, bool launchoncapship) {
	  _std.setNull (youcontainer);
	  _std.setNull(basecontainer);
	  capship= launchoncapship;
	  faction_ships.init();
	  faction=faction_ships.intToFaction(factionname);
	  arrived=false;
	  cred=creds;
	  distfrombase=distance_from_base;
	  difficulty=missiondifficulty;
	  object mysys=_std.getSystemFile();
	  quantity=cargoquantity;
	  object sysfile = _std.getSystemFile();
	  object you=_unit.getPlayer();
	  youcontainer=_unit.getContainer (you);
	  if (quantity<1){
	    quantity=1;
	  }
	  object list=_unit.getRandCargo(quantity);
	  int tempquantity=quantity;
	  cargoname=_olist.at(list,0);
	  object str = _string.new();
	  if (!_std.isNull(you)) {
	    quantity = _unit.addCargo(you,cargoname        ,_olist.at(list,1),_olist.at(list,2),_olist.at(list,3),_olist.at(list,4),_olist.at(list,5));  //ADD CARGO HERE
	    object name = _unit.getName (you);
	    _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	    _string.delete (name);
	  } else {
	    //don't destroy--somethign else went wrong
	    _std.terminateMission (false);
	    return;
	  }
	  if (tempquantity>0) {
	    cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
	  }
	  _io.message (0,"game","all",str);
	  destination=universe.getAdjacentSystem(sysfile,numsystemsaway);
	  _io.sprintf(str,"and give the cargo to a %s unit.",faction);
	  _io.message (2,"game","all",str);
	  _io.sprintf(str,"You will receive %d of the %s cargo",quantity,cargoname);
	  _io.message (3,"game","all",str);
	  _string.delete(str);
	  _olist.delete(list);
	};
	void destroy() {
	  _unit.deleteContainer (youcontainer);
	  if (arrived) {
	    if (!_std.isNull(basecontainer)) {
	      _unit.deleteContainer (basecontainer);
	    }
	  }
	  _string.delete (destination);
	  _string.delete (faction);
	};
	void takeCargoAndTerminate (object you) {
	  int removenum=_unit.removeCargo(you,cargoname,quantity,true);
	  if ((removenum==quantity)||(quantity==0)) {
	    _io.message (0,"game","all","Excellent work pilot.");
	    _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	    _io.message (0,"game","all","Your contribution to the war effort will be remembered.");
	    _unit.addCredits(you,cred);
	    destroy();
	    _std.terminateMission(true);
	    return;
	  } else {
	    _io.message (0,"game","all","You did not follow through on your end of the deal.");

	    if (difficulty<1) {
	      _io.message (0,"game","all","Your pay will be reduced");
	      _io.message (0,"game","all","And we will consider if we will accept you on future missions.");
	      float addcred=(_std.Float(removenum)/_std.Float((quantity*(1+difficulty))))*cred;
	      _unit.addCredits(you,addcred);
	    } else {
	      _io.message (0,"game","all","You will not be paid!");
	      if (difficulty>=2) {
		_io.message (0,"game","all","And your idiocy will be punished.");
		_io.message (0,"game","all","You had better run for what little life you have left.");
		int i=0;
		object un;


		while (i<difficulty) {
		  un=faction_ships.getRandomFighter(faction);
		  object newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 200.0,1000.0,you);
		  _unit.setTarget(newunit,you);
		  i=i+1;
		}
	      }
	    }
	    destroy();
	    _std.terminateMission(false);
	    return;
	  }
	};
	void loop () {
	  if (arrived) {
	    object base=_unit.getUnitFromContainer(basecontainer);
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull(base)||_std.isNull(you)) {
	      _io.message (0,"game","all","Mission failed. You were unable to deliver cargo.");
	      destroy();
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
	      object significant = unit.getSignificant (randint,(!capship));
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      }
	      if (_std.isNull(significant)) {
		arrived=false;
	      }else {
		object newun=significant;
		if (capship) {
		  newun=launch.launch_wave_around_unit("Base",faction,newship,"_ai_stationary",1,2000.0,5000.0,significant);
		}
		object str = _string.new();
		object name = _unit.getName (newun);
		_io.sprintf(str,"You must drop your cargo off with the %s unit.",name);
		_string.delete (name);
		_io.message (0,"game","all",str);
		if (capship) {
		  name=_unit.getName(significant);
		  _io.sprintf(str,"It is docked around the %s landmark.",name);
		  _string.delete (name);
		  _io.message (0,"game","all",str);
		  
		}
		_string.delete(str);
		
		basecontainer=_unit.getContainer(newun);
	      }
	    }
	    _string.delete (sysfil);
	  }
	};
}
