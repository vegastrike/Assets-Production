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
	  jnum=false;
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

	};
	void SuccessMission(object you) {
	  _unit.addCredits (you, cred);
	  _io.message (0,"game","all","Thank you.");
	  _io.message (0,"game","all","We have credited your account.");
	  _std.terminateMission(true);
	};

	void GeneratePatrolList (object you) {
	  patrolpoints=_olist.new();
	  while (quantity>0) {
	    
	    
	    quantity=quantity-1;
	  }
    	};
	bool FinishedPatrol () {
	  object cont = _olist.at (
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
		if (FinishedPatrol()) {
		  SuccessMission(you);
		}
	      }
	    }
	  }else {
	    go_somewhere_significant.loop();//only bother looping if we're not there yet
	  }
	};
}
