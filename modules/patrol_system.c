module attack_jumppoint {
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
	  go_somewhere_significant.init(you,numsystemsaway,true,distance_from_base);
	  _string.delete(str);
	  patrolpoints=_olist.new();
	};
	void destroy() {
	  int i=0;
	  go_somewhere_significant.destroy();
	  _unit.deleteContainer (youcontainer);
	  while (i<_olist.size(patrolpoints)) {
	    _unit.deleteContainer (_olist.at (patrolpoints,i));
	  }
	  _olist.delete (patrolpoints);
	}
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","Thank you.");
	  _io.message (0,"game","all","We have credited your account.");
	  _std.terminateMission(true);
	};
	void GeneratePatrolList (object you) {
	  object str =_string.new ();
	  _io.sprintf (str,"You must get within %f klicks of the following units:",distance);
	  _io.message (0,"game","all",str);
	  while (quantity>0) {
	    int signum = random.randomint (0,64);
	    object sig = unit.getSignificant (signum,false);
	    if (!_std.isNull(sig)) {
	      object fac =_unit.getFaction(sig);
	      object nam =_unit.getName (sig);
	      _io.sprintf (str,"%s owned %s",fac, nam);
	      _string.delete (fac);
	      _string.delete (nam);
	      _io.message (0,"game","all",str);
	      object cont = _unit.getContainer ();
	      _olist.push_back (patrolpoints,cont);
	    }
	    quantity=quantity-1;
	  }
	  _string.delete (str);
    	};
	bool FinishedPatrol (object you) {
	  if (jnum<_olist.size(patrolpoints)) {
	    object jpoint = _unit.getContainer (_olist.at (patrolpoints,jnum));
	    bool visited = _std.isNull(jpoint);
	    if (!_std.isNull(jpoint)) {
	      if (_unit.getDistance (you,jpoint)<distance) {
		visited =true;
	      }
	    } 
	    if (visited) {
	      _unit.deleteContainer (_olist.at (patropoints,jnum));
	      _olist.erase (patrolpoints,jnum);
	    }
	    jnum=jnum+1;
	  }else {
	    jnum=0;
	  }
	  return (_olist.size(patrolpoints)==0);
	}
	void loop () {
	  if (go_somewhere_significant.InSystem()) {
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull (you)) {
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
}
