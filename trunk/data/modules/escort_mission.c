module escort_mission {
  import ai_stationary;
  import universe;
  import unit;
  import faction_ships;
  object youcontainer;
  object escortee;
  object faction;
  object destination;
  object escortee;//only active after stage >=1
  object basecontainer;//pnly active after stage >=2
  object cargoname;
  int stage;//stage 0 is until he gets near enough to jump point
  //stage 1 is when the escortee is generated and badguys start coming
  //        we search for being a) in a different system and b) finding a starship equal to our friend escortee if so 
  //        go to stage 2
  //stage 2 create capship and henceforth check for escort being close enough to dock
  int other_system_comp;
  int difficulty;
  float distfrombase;
  float distfromjump;
  float ourdistfromjump;
  float cred;
  object beginningSystem;
  import random;
  import launch;
  import faction_ships;
  bool capship;
  float my_timer;
  void AddCargoToUnit (object un, int quantity) {
	  object list=_unit.getRandCargo(quantity);
	  cargoname=_olist.at(list,0);
	  int quantity = _unit.addCargo(un,cargoname,_olist.at(list,1),_olist.at(list,2),_olist.at(list,3),_olist.at(list,4),_olist.at(list,5));  
	  _olist.delete(list);
  }
  void ActivateStage1 (object jumppoint) {
    object escname=faction_ships.getRandomFighter("merchant");
    object esc =launch.launch_wave_around_unit("Base",faction,escname,"default",1,distfromjump,jumppoint);
    AddCargoToUnit(esc,100);
    _unit.setName(esc,"Freighter");
    _unit.setTarget (esc,jumppoint);
    _unit.Jump(esc);
    escortee=_unit.getContainer (esc);
    stage=1;
  };
  void ActivateStage2 (object esc) {
    //esc is not null when we are here
    object capname = faction_ships.getRandomCapitol(faction);
    object un = launch.launch_wave_around_unit ("base",faction,capname,"default",1,distfrombase,esc);
    stage=2;
  };
  bool ReadyForStage2() {
    object un =_unit.getShip(other_system_comp);
    if (_std.isNull (un)) {
      other_system_comp=0;
    }else {
      other_system_comp=other_system_comp+1;
      return ((!_string.equal(beginningSystem,_std.getSystemFile))&&(_unit.equal(un,_unit.getUnitFromContainer(escortee))));
    }
    return false;
  };
  void init (int factionname, int missiondifficulty, float our_dist_from_jump, float dist_from_jump, float distance_from_base, float creds, float enemy_time) {
    
	  faction_ships.init();
	  enemytime=enemy_time;
	  my_timer=_std.getGameTime()-enemy_time;//will start with enemies;
	  _std.setNull (escortee);
	  _std.setNull (basecontainer);
	  other_system_comp=0;
	  faction=faction_ships.intToFaction(factionname);
	  stage=0;
	  cred=creds;
	  distfrombase=distance_from_base;
	  distfromjump=dist_from_jump;
	  ourdistfromjump=out_dist_from_jump;
	  difficulty=missiondifficulty;
	  object mysys=_std.getSystemFile();
	  beginningSystem = _std.getSystemFile();
	  object you=_unit.getPlayer();
	  youcontainer=_unit.getContainer (you);
	  if (!_std.isNull(you)) {
	    _io.sprintf(str,"Good Day, %s. Our %s ship near the",_unit.getName (you),faction);
	  } else {
	    _std.terminateMission (false);
	    return;
	  }
	  _io.message (0,"game","all",str);
	  object destpoint=universe.getRandomJumppoint();
	  if (!_std.isNull(destpoint)) {
	    destination = _unit.getContainer (destpoint);
	    _io.sprintf(str,"%s jump point. Requires assistance",_unit.getName (destpoint));
	    _io.message (2,"game","all",str);
	    _io.sprintf(str,"You must see her to our capitol starship on the other side.");
	    _io.message (3,"game","all",str);
	    if (missiondifficulty>1) {
	      _io.message (4,"game","all","Do not falter here. We will not take failure lightly.");
	    }
	  }else {
	    terminateMission(false);
	  }
	  _string.delete(str);

	};
	void takeCargoAndTerminate (object play, object you) {
	  int removenum=0;
	  if (!_std.isNull(you)) {
	    removenum=_unit.removeCargo(you,cargoname,100,true);
	  }
	  if ((removenum>0)) {
	    if (difficulty==0) {
	      _io.message (0,"game","all","Thank you kind privateer.");
	      _io.message (0,"game","all","You have been rewarded for your escorting effort.");
	      _io.message (0,"game","all","Your small escort may save billions of lives.");
	    }
	    if (difficulty==1) {
	      _io.message (0,"game","all","Nice work, privateer.");
	      _io.message (0,"game","all","You have been rewarded for escorting.");
	      _io.message (0,"game","all","We look forward to conducting business with you in the future.");
	    } 
	    if (difficulty>1) {
	      _io.message (0,"game","all","You have been paid.");
	      _io.message (0,"game","all","We suggest you get out of here.");
	      _io.message (0,"game","all","These waters aren't as friendly as some skies.");
	    }
	    _unit.addCredits(play,cred);
	    _std.terminateMission(true);
	  } else {
	    _io.message (0,"game","all","You did not follow through on your end of the deal.");
	    _io.message (0,"game","all","You will not be paid");
	    _io.message (0,"game","all","And we will consider if we will accept you on future missions.");
	    if (difficulty>=2) {
	      _io.message (0,"game","all","And your idiocy will be punished.");
	      _io.message (0,"game","all","You had better run for what little life you have left.");
	      int i=0;
	      object un;
	      while (i<difficulty) {
		un=faction_ships.getRandomFighter(faction);
		object newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 1000.0,play);
		_unit.setTarget(newunit,play);
		i=i+1;
		
	      }
	    }
	    _std.terminateMission(false);

	  }
	};
	void GenerateEnemies (object esc) {
	  if ((_std.GetGameTime()-my_timer)>enemytime) {
	    if (_string.equal("pirates",faction)) {
	      object randomtype = faction_ships.getRandomFighter ("confed");
	      launch.launch_wave_around_unit("Shadow","confed",randomtype,"default",difficulty+1,4000,esc);
	    }else {
	      object randtype = faction_ships.getRandomFighterInt(random.randomint(0,faction_ships.getMaxFactions()-1));
	      launch.launch_wave_around_unit ("Shadow","pirates",randtype,"default",difficulty+1,4500,esc);
	    }
	    my_timer = _std.getGameTime();
	  }
	};
	CheckForCompletion(play,esc) {
	      object dockingbase = _unit.getUnitFromContainer (basecontainer);
	      if (_std.isNull(dockingbase)) {
		takeCargoAndTerminate (play,dockingbase);//will get mad for null docking base
	      }else {
		_unit.setTarget(esc,dockingbase);//stay on target
		if (_unit.getDistance(esc,dockingbase)<400) {
		  object nil;
		  _std.setNull(nil);
		  _unit.setTarget(esc,nil);
		  takeCargoAndTerminate(play,esc);
		}
	      }
	};

	void loop () {
	  object play = _unit.getUnitFromContainer (youcontainer);
	  if (_std.isNull(play)) {
	    _std.terminateMission(false);
	    return;
	  }
	  if (stage==0) {
	    object jumppoint = _unit.getUnitFromContainer (destination);
	    if (!_std.isNull(jumppoint)) {
	      if (_unit.getDistance (jumppoint,play)<ourdistfromjump) {
		ActivateStage1();
	      }
	    }else {
	      _std.terminateMission(false);
	      return;
	    }
	  } else {
	    //running part of mission
	    object esc = _unit.getUnitFromContainer (escortee);
	    if (std.isNull(esc)) {//if guy dies you're dead, man
	      takeCargoAndTerminate (play, esc);
	      return;
	    }//else generate baddies targetting the escort container
	    GenerateEnemies (esc);
	    if (stage==1) {
	      if (ReadyForStage2()) {
		ActivateStage2(esc);
	      }
	    }
	    if (stage==2) {
	      CheckForCompletion(play,esc);
	    }
	  }
	};
}
