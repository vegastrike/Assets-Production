module cargo_mission {
  import ai_stationary;
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
	void sys (object currentsystem, int sysaway) {
	  if (sysaway<=0) {
	    destination=currentsystem;
	  } else {
	    int max=_std.getNumAdjacentSystems(currentsystem);
	    if (max>0) {
	      int nextsysnum=random.randomint(0,max-1);
	      object nextsystem=_std.getAdjacentSystem(currentsystem,nextsysnum);
	      sys(nextsystem,sysaway-1);
	    } else {
	      destination="sol_sector/sol";
	    }
	  }
	};
	
	void init (int factionname, int numsystemsaway, int cargoquantity, int missiondifficulty, float distance_from_base, float creds, bool launchoncapship) {
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
	  sys(sysfile,numsystemsaway);
	  object you=_unit.getPlayer();
	  if (quantity<1){
	    quantity=1;
	  }
	  object list=_unit.getRandCargo(quantity);
	  int tempquantity=quantity;
	  cargoname=_olist.at(list,0);
	  if (!_std.isNull(you)) {
	    quantity = _unit.addCargo(you,cargoname        ,_olist.at(list,1),_olist.at(list,2),_olist.at(list,3),_olist.at(list,4),_olist.at(list,5));  //ADD CARGO HERE
	    if (tempquantity>0) {
	      cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
	    }
	    
	    object str = _string.new();
	    object name = _unit.getName (you);
	    _io.sprintf(str,"Good Day, %s",name);
	    _io.message (0,"game","all",str);
	    _io.sprintf(str,"Go to system %s and give the",destination);
	    _io.message (1,"game","all",str);
	    _io.sprintf(str,"cargo to a unit from our faction: %s",faction);
	    _io.message (2,"game","all",str);
	    _io.sprintf(str,"%d of the %s cargo",quantity,cargoname);
	    _io.message (3,"game","all",str);
	    _string.delete(str);
	    _olist.delete(list);
	  } else {
	    _std.terminateMission (false);
	  }
	};
	void takeCargoAndTerminate (object you) {
	  int removenum=_unit.removeCargo(you,cargoname,quantity,true);
	  if ((removenum==quantity)||(quantity==0)) {
	    _io.message (0,"game","all","Excellent work pilot.");
	    _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	    _io.message (0,"game","all","Your contribution to the war effort will be remembered.");
	    _unit.addCredits(cred);
	    _std.terminateMission(true);
	  } else {
	    _io.message (0,"game","all","You did not follow through on your end of the deal.");

	    if (difficulty<1) {
	      _io.message (0,"game","all","Your pay will be reduced");
	      _io.message (0,"game","all","And we will consider if we will accept you on future missions.");
	      float addcred=(_std.Float(removenum)/_std.Float((quantity*(1+difficulty))))*cred;
	      _unit.addCredits(addcred);
	    } else {
	      _io.message (0,"game","all","You will not be paid!");
	      if (difficulty>=2) {
		_io.message (0,"game","all","And your idiocy will be punished.");
		_io.message (0,"game","all","You had better run for what little life you have left.");
		int i=0;
		object un;


		while (i<difficulty) {
		  un=faction_ships.getRandomFighter(faction);
		  object newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 1000.0,you);
		  _unit.setTarget(newunit,you);
		  i=i+1;
		}
	      }
	    }
	    _std.terminateMission(false);

	  }
	};
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
	      }else {
		object fgname = _unit.getFgName (significant);
		while (!((_unit.isPlanet(significant))||(_string.equal(fgname,"Base")))&&(randint<1024)) {
		  _string.delete (fgname);
		  randint=randint+1;
		  significant =unit.getSignificant(randint);
		  fgname = _unit.getFgName (significant);
		}
	      }
	      if (_std.isNull(significant)) {
		arrived=false;
	      }else {
		if (capship) {
		  significant=launch.launch_wave_around_unit("Base",faction,newship,"_ai_stationary",1,5000.0,significant);
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
