module attack_jumppoint {
  import ai_stationary;
  import universe;
  import go_somewhere_significant;
  object youcontainer;
  object faction;
  

  float escdist;
  int quantity;
  float cred;
  import random;
  import launch;
  import faction_ships;
  int ship_check_count;
  bool defend;
  object attackers;
  int targetiter;  
  object defendee;
  bool defendbase;
  void initrandom (object factionname, int numsystemsaway, int minenquant, int maxenquant, float credperenemy, bool defend, bool defend_base) {
    int enq = random.randomint (minenquant,maxenquant);
    init (factionname, numsystemsaway, enq, 8000.0,50000.0, _std.Float (enq)*credperenemy,defend,defend_base);
  };
	void init (object factionname, int numsystemsaway, int enemyquantity, float distance_from_base, float escape_distance, float creds, bool defendthis, bool defend_base) {
	  defendbase = defend_base;
	  _std.setNull(defendee);
	  attackers = _olist.new ();
	  targetiter = 0;
	  ship_check_count=0;
	  defend = defendthis;
	  faction_ships.init();

	  faction=_string.new();
	  _io.sprintf (faction,"%s",factionname);
	  escdist = escape_distance;
	  cred=creds;

	  quantity=enemyquantity;

	  
	  object you=_unit.getPlayer();
	  youcontainer=_unit.getContainer (you);

	  object name;
	  if (!_std.isNull(you)) {
	    name = _unit.getName (you);
	  } else {
	    //don't destruct...something else went wrong
	    _std.terminateMission (false);
	    return;
	  }
	  object str = _string.new();
	  _io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
	  _string.delete (name);
	  _io.message (0,"game","all",str);
	  if (defend_base) {
	    go_somewhere_significant.init_base_only(you,numsystemsaway,distance_from_base);
	  }else {
	    go_somewhere_significant.init(you,numsystemsaway,defend,false,distance_from_base);
	  }
	  _io.sprintf(str,"And there eliminate any %s starships at a point.",faction);
	  _io.message (2,"game","all",str);
	  _string.delete(str);
	};
	void destroy () {
	  int i=0;
	  if (!_std.isNull (defendee)) {
	    _unit.deleteContainer (defendee);
	  }
	  while (i<_olist.size(attackers)) {
	    object cont = _olist.at (attackers,i);
	    _unit.deleteContainer (cont);
	    i=i+1;
	  }
	  _olist.delete (attackers);
	  _unit.deleteContainer (youcontainer);
	  _std.setNull (youcontainer);
	  _string.delete (faction);
	  _std.setNull (faction);
	  go_somewhere_significant.destroy();
	};
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","Excellent work pilot.");
	  _io.message (0,"game","all","You have been rewarded for your effort as agreed.");
	  destroy();
	  _std.terminateMission(true);
	};
	void FailMission(object you) {
	  cred = 0.0-cred;
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","You Allowed the base you were to protect to be destroyed.");
	  _io.message (0,"game","all","You are a failure to your race!");
	  _io.message (1,"game","all","We have contacted your bank and informed them of your failure to deliver on credit. They have removed a number of your credits for this inconvenience. Let this serve as a lesson.");
       	  destroy();
	  _std.terminateMission(true);
	};

	bool NoEnemiesInArea (object jp) {
	  object cur = _std.getSystemFile();
	  object tmpdst = go_somewhere_significant.DestinationSystem();
	  if (!_string.equal(tmpdst,cur)) {
	    return false;
	  }
	  object un= _unit.getUnit (ship_check_count);
	  ship_check_count=ship_check_count+1;
	  if (_std.isNull (un)) {
	    return true;
	  }
	  object fac = _unit.getFaction (un);
	  object me = _unit.getUnitFromContainer (youcontainer);
	  if (!_unit.equal (un,me)) {
	    if (_string.equal (fac,faction)) {
	      if (_unit.getDistance (jp,un)<escdist) {
		ship_check_count=0;
	      }
	    }
	  }
	  return false;
	};
	void GenerateEnemies (object jp,object you) {
	  int count=0;
	  object str = _string.new();
	  _io.sprintf(str,"Eliminate all %s ships here.",faction);
	  _io.message (0,"game","all",str);
	  if (defend) {
	    if (!_std.isNull(jp)) {
	      object nam = _unit.getName (jp);
	      _io.sprintf (str,"You must protect %s.",nam);
	      _string.delete (nam);
	      _io.message (0,"game","all",str);
	    }
	  }
	  _string.delete(str);
	  
	  while (count<quantity) {
	    object randtype = faction_ships.getRandomFighter(faction);
	    object launched = launch.launch_wave_around_unit ("Shadow",faction,randtype,"default",1,2000.0,4500.0,jp);
	    if ((defend)&&(!_std.isNull(jp))) {
	      _unit.setTarget (launched,jp);
	    }else {
	      _unit.setTarget (launched,you);//make 'em attack you
	    }
	    _unit.setFgDirective(launched,"B");
	    _olist.push_back (attackers,_unit.getContainer (launched));
	    count = count+1;
	  }
	  quantity=0;
    	};
	void loop () {

	  go_somewhere_significant.loop();

	  if (go_somewhere_significant.HaveArrived()) {
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull (you)) {
	      destroy();
	      _std.terminateMission(false);
	    }else {
	      if (_std.isNull (defendee)) {
		object def;
		_std.setNull(def);
		if ((!defend)||(defendbase)) {
		  def =go_somewhere_significant.SignificantUnit();
		}else {
		  object temp = go_somewhere_significant.SignificantUnit();
		  if (_std.isNull (temp)) {
		    temp = you;
		  }

		  object fac = faction_ships.get_enemy_of (faction);
		  object randtype = faction_ships.getRandomCapitol (fac);

		  def = launch.launch_wave_around_unit ("Halo",fac,randtype,"default",1,2000.0,2500.0,temp);		  
		  _string.delete (fac);
		}
		defendee = _unit.getContainer (def);
	      }

	      object base = _unit.getUnitFromContainer (defendee);

	      if (_std.isNull(base)) {
		if (defend) {
		  FailMission(you);
		}else {
		  SuccessMission(you);
		}
	      }else {
		if (quantity>0) {

		  GenerateEnemies (base,you);
		}
		if (targetiter>=_olist.size(attackers)) {
		  targetiter=0;
		}else {

		  object cont =  _olist.at (attackers,targetiter);
		  object un = _unit.getUnitFromContainer (cont);
		  if (!_std.isNull(un)) {
		    if (defend) {
		      //		      _io.printf ("targetting base");
		      _unit.setTarget (un,base);
		    }else {
		      _unit.setTarget (un,you);
		    }
		  }

		  targetiter=targetiter+1;
		}
		if (NoEnemiesInArea (base)) {
		  SuccessMission(you);
		}
	      }
	    }
	  }
	};
	void initbriefing() {

	};
	void loopbriefing () {

	};
	void endbriefing() {

	};
}
