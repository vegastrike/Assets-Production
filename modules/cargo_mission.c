module cargo_mission {
  //  import ai_stationary;
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
	float mission_time;
	int brief_you;
	int jump_ani;
	float begintime;
	float time;
	int brief_stage;
	object jumps;
	float rnd_y;
	bool added_warp;
	void initbriefing() {
		jump_ani=0;
		rnd_y=0.0;
		added_warp=true;
		brief_stage=0;
		begintime= _std.getGameTime()-6.0;
		_io.printf ("starting briefing");
		object un= _unit.getUnitFromContainer(youcontainer);
		if (_std.isNull(un)) {
			_std.terminateMission(false);
			_briefing.terminate();
		}
		object faction=_unit.getFaction(un);
		object name=_unit.getName(un);
		brief_you=_briefing.addShip(name,faction,0.0,0.0,80.0);
		//int b=_briefing.addShip("starrunner","confed",0.0,0.0,1000.0);
		//int c=_briefing.addShip("starrunner","confed",0.0,0.0,10000.0);
		//int d=_briefing.addShip("starrunner","confed",100.0,0.0,00.0);
		object str=_string.new();
		_io.sprintf(str,"Your mission for today will be to deliver some %s cargo to the %s system.\nIn order to get there, you must follow this route that we have planned out for you.",cargoname,destination);
		_io.message (0,"game","briefing",str);
		_string.delete(str);
		//_briefing.enqueueOrder (b,4000.0,0.0-10.0,2000.0,15.0);
		//_briefing.enqueueOrder (c,1000.0,10.0,1000.0,15.0);
		//_briefing.enqueueOrder (d,4000.0,0.0-10.0,2000.0,15.0);
	};
	void loopbriefing() {
		int size=_olist.size(jumps);
		time = _std.getGameTime();
		_briefing.setCamPosition(1.6*(time-begintime)*brief_stage,0.0,0.0);
		if (((time-begintime)>=5.0)&&added_warp){
			jump_ani=_briefing.addShip("brief_warp",faction,20.0*(brief_stage),rnd_y,79.5+rnd_y);
			added_warp=false;
		}
		if (((time-begintime)>=6.0)){
			if (jump_ani!=0) {
				_briefing.removeShip(jump_ani);
			}
		}
		if ((size==brief_stage)&&((time-begintime)>=6.0)) {
			_io.message(0,"game","briefing","Once there, you must drop the cargo off at a specified unit");
			brief_stage=size+1;
			added_warp=false;
			time=0.0;
		} else if ((brief_stage>size)&&((time-begintime)>=11.0)) {
			_briefing.terminate();
		} else if (((time-begintime)>=6.0)&&(brief_stage<size)){
			added_warp=true;
			rnd_y=(_std.Rnd()*40.0)-20.0;
			int dumb=_briefing.addShip("brief_jump",faction,20.0*(brief_stage+1),rnd_y,79.6+rnd_y);
			_briefing.enqueueOrder (brief_you,20.0*(brief_stage+1),rnd_y,80.0+rnd_y,5.0);
			begintime=time;
			object str = _string.new();
			object myname=_olist.at(jumps,brief_stage);
			_io.sprintf (str,"You must go to the '%s' jump point",myname);
			_io.message (0,"game","briefing",str);
			_string.delete(str);
			brief_stage=brief_stage+1;
		}
	  
	  //if ((time-begintime)>6.0) {
	  //_briefing.setCloak (0,1.0);//1-(time-begintime)/6.0);	 
	  //  }
	};
	void endbriefing() {
		_io.printf ("endinging briefing");
	};
	void initrandom (object factionname, int missiondifficulty,float creds_per_jump, bool launchoncapship, int sysmin, int sysmax, float time_to_complete, object category) {
	  int numsys = random.randomint (sysmin,sysmax);
	  init(factionname,numsys, random.randomint(4,15), missiondifficulty,400.0,creds_per_jump*_std.Float(1+numsys),launchoncapship, 10.0, category);
	};
	void init (object factionname, int numsystemsaway, int cargoquantity, int missiondifficulty, float distance_from_base, float creds, bool launchoncapship, float time_to_complete, object category) {
	  mission_time=_std.getGameTime()+time_to_complete*100*_std.Float(1+numsystemsaway);
	  _std.setNull (youcontainer);
	  _std.setNull(basecontainer);
	  capship= launchoncapship;
	  faction_ships.init();
	  faction=_string.new();
	  _io.sprintf (faction,"%s",factionname);
	  arrived=false;
	  cred=creds;
	  jumps=_olist.new();
	  universe.init();
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
	  object list=_unit.getRandCargo(quantity,category);
	  if (_olist.size(list)==0) {
	    _olist.delete (list);
	    list = _unit.getRandCargo(quantity);
	  }
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
          float creds_deducted = _olist.at(list,2);
          creds_deducted = creds_deducted * _std.Float(quantity)*(_std.Rnd()+1.0);
          cred = cred + creds_deducted;
	  if (tempquantity>0) {
	    cred=cred *_std.Float(quantity)/_std.Float(tempquantity);
          }else {
            _io.sprintf (str,"You do not have space to add our cargo to the mission. Mission failed.");
	    _io.message (2,"game","all",str);
            _std.terminateMission(false);
	  _string.delete(str);
	  _olist.delete(list);
            return;
          }
          if (quantity==0) {
            _io.sprintf (str,"You do not have space to add our cargo to the mission. Mission failed.");
	    _io.message (2,"game","all",str);
            _std.terminateMission(false);
	  _string.delete(str);
	  _olist.delete(list);
            return;
          }
	  _io.message (0,"game","all",str);
	  destination=universe.getAdjacentSystem(sysfile,numsystemsaway,jumps);
	  _io.sprintf(str,"and give the cargo to a %s unit.",faction);
	  _io.message (2,"game","all",str);
	  _io.sprintf(str,"You will receive %d of the %s cargo",quantity,cargoname);
	  _io.message (3,"game","all",str);
          int tempo = _std.Int (creds_deducted);
	  _io.sprintf(str,"We will deduct %d credits from your account for the cargo needed.",tempo);
	  _io.message (4,"game","all",str);
          tempo= _std.Int (creds);
	  _io.sprintf(str,"You will earn %d more credits when you deliver our cargo.",tempo);
	  _io.message (5,"game","all",str);
          creds_deducted= 0.0-creds_deducted;
          _unit.addCredits (you,creds_deducted);

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
	  _olist.delete (jumps);
	};
	void takeCargoAndTerminate (object you, bool remove) {
	  int removenum=0; //if you terminate without remove, you are SKREWED
	  if (remove) {
	    removenum=_unit.removeCargo(you,cargoname,quantity,true);
	  }
	  if ((removenum==quantity)||(quantity==0)) {
	    _io.message (0,"game","all","Excellent work pilot.");
	    _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	    _io.message (0,"game","all","Your excellent work will be remembered.");
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
		  object newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 200.0,400.0,you);
		  _unit.setFgDirective(newunit,"B");
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
	  /*
	  if (_std.getGameTime()>mission_time) {
	    _io.message (0,"game","all","You Have failed to deliver your cargo in a timely manner.");
	    _io.message (0,"game","all","The cargo is no longer of need to us.");
	    object you = _unit.getUnitFromContainer (youcontainer);
	    if (!_std.isNull(you)) {
	      takeCargoAndTerminate(you,false);
	    }
	    return;
	  }
	  */
	  if (arrived) {
	    object base=_unit.getUnitFromContainer(basecontainer);
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull(base)||_std.isNull(you)) {
	      _io.message (0,"game","all","Mission failed. You were unable to deliver cargo.");
	      destroy();
	      _std.terminateMission(false);
	      return;
	    }
	    float dist=unit.getSignificantDistance(you,base);
	    if (dist<=distfrombase) {
	      takeCargoAndTerminate(you,true);		
	      return;
	    }
	  } else {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrived=true;
	      object newship=faction_ships.getRandomCapitol(faction);
	      int randint=random.randomint(0,50);
	      object significant = unit.getSignificant (randint,(!capship),false);
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      }
	      if (_std.isNull(significant)) {
		arrived=false;
	      }else {
		object newun=significant;
		if (capship) {
		  newun=launch.launch_wave_around_unit("Base",faction,newship,"sitting_duck",1,2000.0,5000.0,significant);
		}
		object str = _string.new();
		object name = _unit.getName (newun);
		_io.sprintf(str,"You must drop your cargo off with the %s.",name);
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

