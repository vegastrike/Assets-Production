module cargo_mission {
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
	
	void init (int factionname, int numsystemsaway, int cargoquantity, int missiondifficulty, float distance_from_base, float creds) {
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
	  quantity = _unit.addCargo(you,cargoname        ,_olist.at(list,1),_olist.at(list,2),_olist.at(list,3),_olist.at(list,4),_olist.at(list,5));  //ADD CARGO HERE
	  if (tempquantity>0) {
	    cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
	  }

	  object str = _string.new();
	  _io.sprintf(str,"Go to system %s and give the",destination);
	  _io.message (0,"game","all",str);
	  _io.sprintf(str,"cargo to a unit from our faction: %s",faction);
	  _io.message (1,"game","all",str);
	  _io.sprintf(str,"%d of the %s cargo",quantity,cargoname);
	  _io.message (2,"game","all",str);
	  _string.delete(str);
	  _olist.delete(list);
	};
	void takeCargoAndTerminate (object you) {
	  int removenum=_unit.removeCargo(you,cargoname,quantity,true);
	  if ((removenum==quantity)||(quantity==0)) {
	    _unit.addCredits(cred);
	    _std.terminateMission(true);
	  } else {
	    if (difficulty<=1) {
	      float addcred=(_std.Float(removenum)/_std.Float((quantity*(1+difficulty))))*cred;
	      _unit.addCredits(addcred);
	    } else {
	      if (difficulty>=2) {
		int i=0;
		object un;
		while (i<difficulty) {
		  un=faction_ships.getRandomFighter(faction);
		  un=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 1000.0,you);
		  _unit.setTarget(un,you);
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
	      object newunit=launch.launch_wave_around_significant("Base",faction,newship,"_ai_stationary",1,5000.0,randint);
	      basecontainer=_unit.getContainer(newunit);
	    }
	    _string.delete (sysfil);
	  }
	};
}
