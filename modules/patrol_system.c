module patrol_system {
  import ai_stationary;
  import universe;
  import go_somewhere_significant;
  import random;
  import launch;
  import faction_ships;
  import go_somewhere_significant;

  object youcontainer;
  float distance;
  int quantity;//num jump points
  float cred;
  object patrolpoints;
  int jnum;//to check for jump point closeness
  bool anything;
  void initrandom (int minsysaway, int maxsysaway, int minsigtopatrol, int maxsigtopatrol, float mincred, float maxcred) {
    int nsys = random.randomint (minsysaway, maxsysaway);
    int nsig = random.randomint (minsigtopatrol, maxsigtopatrol);
    init (nsys,
	  nsig,
	  random.random(100.0,300.0),
	  (1+(_std.Float (nsys)*0.5))*_std.Float(nsig)*random.random (mincred,maxcred));
  };
  void init (int numsystemsaway, int num_significants_to_patrol, float distance_from_base, float creds) {
	  jnum=0;
	  anything=true;
	  distance = distance_from_base;
	  cred=creds;

	  quantity=num_significants_to_patrol;
	  object you=_unit.getPlayer();
	  youcontainer=_unit.getContainer (you);

	  object name;
	  if (!_std.isNull(you)) {
	    name = _unit.getName (you);
	  } else {
	    _std.terminateMission (false);
	    return;
	  }
	  object str = _string.new();
	  _io.sprintf(str,"Greetings, %s. You must patrol a system for us:",name);
	  _string.delete (name);
	  _io.message (0,"game","all",str);
	  go_somewhere_significant.init(you,numsystemsaway,false,false,distance_from_base);

	  _io.sprintf(str,"When you complete this mission we will reward you %f credits.",creds);
	  _io.message (0,"game","all",str);
	  _string.delete(str);
	  patrolpoints=_olist.new();
	};
	void destroy() {
	  int i=0;
	  go_somewhere_significant.destroy();
	  _unit.deleteContainer (youcontainer);
	  while (i<_olist.size(patrolpoints)) {
	    object cont = _olist.at (patrolpoints,i);
	    _unit.deleteContainer (cont);
	    i=i+1;
	  }
	  _olist.delete (patrolpoints);
	};
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","[Computer] Transmitting data...");
	  _io.message (0,"game","all","Thank you! Patrol Complete.");
	  _io.message (0,"game","all","We have credited your account.");
	  destroy();
	  _std.terminateMission(true);
	};
	void GeneratePatrolList (object you) {
	  object str =_string.new ();
	  _io.sprintf (str,"You must get within %f klicks of the following units:",distance);
	  _io.message (0,"game","all",str);
	  while (quantity>0) {
	    int signum = random.randomint (0,64);
	    object sig = unit.getSignificant (signum,false,false);
	    if (!_std.isNull(sig)) {
	      object fac =_unit.getFaction(sig);
	      object nam =_unit.getName (sig);
	      _io.sprintf (str,"%s owned %s",fac, nam);
	      _string.delete (fac);
	      _string.delete (nam);
	      _io.message (0,"game","all",str);
	      object cont = _unit.getContainer (sig);
	      _olist.push_back (patrolpoints,cont);
	    }
	    quantity=quantity-1;
	  }
	  _string.delete (str);
    	};
	bool FinishedPatrol (object you) {
	  if (jnum<_olist.size(patrolpoints)) {
	    object tmp =_olist.at (patrolpoints,jnum);
	    object jpoint = _unit.getUnitFromContainer (tmp);
	    bool visited = _std.isNull(jpoint);
	    if (!_std.isNull(jpoint)) {
	      if (unit.getSignificantDistance (you,jpoint)<distance) {
		object str = _string.new();
		object nam = _unit.getName(jpoint);
		_io.sprintf (str,"[Computer] %s scanned, data saved...",nam);
		_io.message (0,"game","all",str);
		_string.delete (nam);
		_string.delete (str);
		visited =true;
	      }
	    } 
	    if (visited) {
	      object tmp2=_olist.at (patrolpoints,jnum);
	      _unit.deleteContainer (tmp2);
	      _olist.erase (patrolpoints,jnum);
	    }
	    jnum=jnum+1;
	  }else {
	    jnum=0;
	  }
	  return (_olist.size(patrolpoints)==0);
	};
	void loop () {
	  if (go_somewhere_significant.InSystem()) {
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull (you)) {
	      destroy();
	      _std.terminateMission(false);
	    }else {
	      if (quantity>0) {//generate jump point olist
		GeneratePatrolList (you);
	      }else {
		if (FinishedPatrol(you)) {
		  SuccessMission(you);
		}
	      }
	    }
	  }else {
	    go_somewhere_significant.loop();//only bother looping if we're not there yet
	  }
	};

	void initbriefing() {

	};
	void loopbriefing() {

	};
	void endbriefing() {
	  
	};
}
