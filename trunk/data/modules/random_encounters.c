module random_encounters {
  import random;
  import faction_ships;
  import launch_recycle;
  import launch;
  float sig_distance;//backup var
  float det_distance;//backup var
  float generation_distance;
  float capship_gen_distance;
  int min_num_ships;//the number of ships that have to be there or else more will be made
  int gen_num_ships;//the num ships to be made
  float capship_prob;//probability a capship will be there
  float fighterprob;
  float enprob;
  int player_num;
  object playerdata;//olist of player data
  object cur;
  //struct playerda
  //  int last_ship;
  //  int curmode;//are we in battle mode (true) or cruise mode (false)
  //  int lastmode;//were we in battle mode (true) or cruise mode(false)
  //  object lastsys;
  //  object sig_container;
  //  float significant_distance;
  //  float detection_distance;
  //}
  void init(float sigdis, float detectiondis, float gendis,  int minnships, int gennships, float unitprob, float enemyprob, float capprob, float capdist){
    capship_gen_distance=capdist;
    //    player_num=player;
    enprob = enemyprob;
    fighterprob = unitprob;

    faction_ships.init();
    det_distance = detectiondis;
    sig_distance = sigdis;

    generation_distance=gendis;
    min_num_ships=minnships;
    gen_num_ships=gennships;
    capship_prob=capprob;
    object px = _unit.getPlayerX(0);
    player_num=0;
    playerdata = _olist.new();
    while (!_std.isNull(px)) {
      _io.printf ("init");
      cur = _olist.new();
      _olist.push_back (playerdata,cur);

      //      last_ship=0;
      //      curmode=0;
      //      lastmode=0;
      _olist.push_back (cur,0);
      _olist.push_back (cur,0);
      _olist.push_back (cur,0);
      object lastsys = _string.new();
      _olist.push_back (cur,lastsys);

      object sig_container;
      _std.setNull(sig_container);
      _olist.push_back (cur,sig_container);
      //      significant_distance = sigdis;
      _olist.push_back (cur,sigdis);
      //      detection_distance = detectiondis;
      _olist.push_back (cur,detectiondis);

      //      CalculateSignificantDistance();//could be wrong sys
      player_num=player_num+1;
      px = _unit.getPlayerX(player_num);
    }
  };
  float getMinDistFrom(object sig1) {
    object sig2=unit.getPlanet (0,false);
    int i=0;
    float mindist=100000000000000000000000000000000000000000000.0;
    while (!_std.isNull (sig2)) {
      float tempdist = unit.getSignificantDistance(sig1,sig2);
      if (tempdist<mindist) {
	if (tempdist>0.0) {
	  mindist=tempdist;
	}
      }
      i=i+1;
      sig2 = unit.getPlanet (i,false);
      //      _io.printf ("getting planet %d",i);
    }
    return mindist;
  };
  float minimumSigDistApart() {
    object sig1=unit.getPlanet (0,false);
    int i=0;
    float mindist=100000000000000000000000000000000000000000000.0;
    float ave=0.0;
    while (!_std.isNull (sig1)) {
      float tempdist = getMinDistFrom (sig1);

      if (ave<0.9) {
	//	_io.printf ("replace %f",tempdist);
	mindist = tempdist;
      }else {
	//	_io.printf (" add %f",tempdist);
	mindist = mindist + tempdist;
      }
      ave = ave+1.0;
      //      if (tempdist<mindist) {
      //	mindist=tempdist;
      //      }
      
      i=i+1;
      sig1 = unit.getPlanet (i,false);
    }
    //    _io.printf ("mindist %f %f\n",mindist, ave);
    if (ave!=0.0) {
      mindist = mindist/ave;
    }
    //    _io.printf ("mindist %f\n",mindist);
    return mindist;
  };
  void CalculateSignificantDistance() {
    float minsig =  minimumSigDistApart();
    float significant_distance;
    float detection_distance;
    if (sig_distance>minsig*0.15) {
      significant_distance = minsig*0.15;
      _olist.set (cur,5,minsig*0.15);
    }else {
      _olist.set (cur,5,sig_distance);
            significant_distance = sig_distance;
    }
    if (det_distance>minsig*0.2) {
      _olist.set (cur,6,minsig*0.2);
            detection_distance = minsig*0.2;
    }else {
      _olist.set (cur,6,det_distance);
            detection_distance = det_distance;
    }
    _io.printf ("resetting sigdist=%f detdist=%f",significant_distance,detection_distance);
  };
  void SetEnemyProb (float enp) {
    enprob = enp;
  };

  void launch_near (object un) {
    int numfactions=random.randomint(0,3);
    if (numfactions==0) {
      numfactions=1;
    }
    int i=0;
    object sysfile = _std.getSystemFile();
    while (i<numfactions) {
      object localfaction = _std.getGalaxyProperty(sysfile,"faction");
      if (_std.Rnd() < enprob) {
	localfaction = faction_ships.get_enemy_of (localfaction);
      }else {
	localfaction = faction_ships.get_friend_of(localfaction);
      }
      object fighter = faction_ships.getRandomFighter (localfaction);

      int numship= random.randomint (1,gen_num_ships);
      float det_distance = _olist.at (cur,6);
      launch_recycle.launch_wave_around(localfaction,fighter,"default",numship,generation_distance*_std.Rnd()*0.9,un, 2.0*det_distance);
      float rnd_num = _std.Rnd();
      if (rnd_num<capship_prob) {
	if (AsteroidNear (un,_olist.at (cur,5))) {
	  _io.printf ("ast near, no cap");
	}else {
	  _io.printf ("no asty near");
	  object capship = faction_ships.getRandomCapitol (localfaction);
	  object launched=launch.launch_wave_around_unit("Capitol",localfaction,capship,"default",1,200.0,capship_gen_distance*_std.Rnd()*0.9,un);
	}
      }
      _string.delete (localfaction);
      i=i+1;
    }
    _string.delete (sysfile);
  };
  bool AsteroidNear (object unit, float how) {
    int num_ships=0;
    int count=0;
    bool retval=false;
    object un = _unit.getUnit (count);
    while (!(_std.isNull(un))) {
      float dd = _olist.at (cur,6);//detectioN_distance
      if (unit.getSignificantDistance(un,unit)<how                ) {
	if (unit.isAsteroid (un)) {
	  _io.printf ("asty near");
	  retval=true;
	  _std.setNull(un);
	}
      }
      count=count+1;
      if (!_std.isNull(un)) {
	un = _unit.getUnit(count);
      }
    }
    return retval;    
  };
  bool test_atLeastNInsignificantUnitsNear (object unit, int n) {
    int num_ships=0;
    int count=0;
    object un = _unit.getUnit (count);
    while (!(_std.isNull(un))) {
      float dd = _olist.at (cur,6);//detectioN_distance
      if (unit.getSignificantDistance(un,unit)<dd                ) {
	if ((!_unit.isSignificant(un))&&(!_unit.isSun(un))) {
	  object name = _unit.getFgName (un);
	  object testname2 = _unit.getName(un);
	  _io.printf ("unit not sig %d %s %s\n",num_ships,name,testname2);
	  num_ships=num_ships+1;
	  if (num_ships>=n){
	    _std.setNull(un);
	  }
	}
      }
      count=count+1;
      if (!_std.isNull(un)) {
	un = _unit.getUnit(count);
      }
    }
    return (num_ships>=n);
  };


  bool atLeastNInsignificantUnitsNear (object unit, int n) {
    int num_ships=0;
    int count=0;
    object un = _unit.getUnit (count);
    while (!(_std.isNull(un))) {
      float dd = _olist.at (cur,6);//detection dis
      if (unit.getSignificantDistance(unit,un)<dd*1.6) {
	if ((!_unit.isSignificant(un))&&(!_unit.isSun(un))) {
	  num_ships=num_ships+1;
	}
      }
      count=count+1;
      un = _unit.getUnit(count);
    }
    if (num_ships>=n) {
      _io.printf ("n units near");
    }
    return num_ships>=n;
  };
  void SetModeZero() {
    //    last_ship=0;
    _olist.set (cur,0,0);
    _olist.set (cur,1,0);
    //    curmode=0;
    object sig_container = _olist.at (cur,4);
    if (!_std.isNull(sig_container)) {
      _unit.deleteContainer (sig_container);
      _std.setNull(sig_container);
      _olist.set (cur,4,sig_container);
    }
  };
  void SetModeOne (object significant) {
    SetModeZero();
    //curmode=1;
    _olist.set (cur,1,1);
    object sig_container = _unit.getContainer (significant);
    _olist.set (cur,4,sig_container);
    object cursys = _std.getSystemFile();
    object lastsys = _olist.at (cur,3);
    bool oldsys = _string.equal (lastsys,cursys);
    _io.sprintf (lastsys,"%s",cursys);
    if (!oldsys) {
      CalculateSignificantDistance();
    }
    _string.delete (cursys);
  };
  object HaveWeSignificant () {
    object sig_container = _olist.at (cur,4);
    if (_std.isNull (sig_container)) {
      return sig_container;
    }
    object significant_unit=_unit.getUnitFromContainer (sig_container);
    if (_std.isNull(significant_unit)) {
      _unit.deleteContainer (sig_container);
      _std.setNull(sig_container);
      _olist.set (cur,4,sig_container);
    }
    return significant_unit;
  };
  object decideMode() {
    object player_unit=_unit.getPlayerX(player_num);
    if (_std.isNull(player_unit)) {
      SetModeZero();
      return player_unit;
    }
    
    object significant_unit = HaveWeSignificant();
    if (_std.isNull(significant_unit)) {
      int last_ship= _olist.at (cur,0);
      object un= _unit.getUnit (last_ship);
      if (_std.isNull (un)) {
	SetModeZero();
      }else {
	float sd = _olist.at (cur,5);
	if ((unit.getSignificantDistance(un,player_unit)<sd)&&(_unit.isSignificant(un))) {
	  SetModeOne (un);
	  return un;
	}	  
	last_ship=last_ship+1;
	_olist.set (cur,0,last_ship);
      }
      _std.setNull(un);
      return un;
    } else {
      //significant_unit is somethign.... lets see what it is
      object cursys = _std.getSystemFile();
      object lastsys = _olist.at (cur,3);
      if (_string.equal (cursys,lastsys)) {
	float dd = _olist.at (cur,6);//detection dist
	if (unit.getSignificantDistance (player_unit,significant_unit)>dd                ) {
	  SetModeZero ();
	  object nullity;
	  _std.setNull(nullity);
	  return nullity;
	} else {
	  return significant_unit;
	}
      } else {
	_io.printf ("different\n");
	_io.sprintf (lastsys,"%s",cursys);
	  _olist.set (cur,3,lastsys);
	SetModeZero();
	_std.setNull (significant_unit);
      }
      _string.delete (cursys);
      return significant_unit;
    }
  };
  void loop() {
    player_num=0;
    object player_unit=_unit.getPlayerX(0);
    while (!_std.isNull(player_unit)) {
      if (_unit.correctStarSystem(player_unit)) {
	cur = _olist.at (playerdata,player_num);
	object un = decideMode ();
	int curmode = _olist.at (cur,1);
	int lastmode = _olist.at (cur,2);
	if (lastmode !=curmode) {//if lastmode!=curmode
	  //lastmode=curmode;//processed this event; don't process again if in critical zone
	  _olist.set (cur,2,curmode);
	  _io.printf ("curmodechange %d",curmode);//?
	
	  if (_std.Rnd()<fighterprob) {
	    if (!_std.isNull(un)) {
	      if (!atLeastNInsignificantUnitsNear (un,min_num_ships)) {
		//determine whether to launch more ships next to significant thing based on ships in that range  
		_io.printf ("launch near");
		launch_near (player_unit);
	      } 
	    }
	  }
	}
      }
      player_num=player_num+1;
      player_unit=_unit.getPlayerX(player_num);

    }
  };
  void initstarsystem () {


    //    last_ship=0;
    //    loop();
    //    while (last_ship!=0) {
    //      loop();//goes through all ships in system to make sure enemies are there when arrive
    //    }
    //not multisafe
  };

}

