module go_somewhere_significant {
  import unit;
  import universe;
  object destination;
  object significantun;
  object jumps;
  bool baseonly;
  bool capship;
  bool jumppoint;
  bool arrivedsys;
  bool arrivedarea;
  float distfrombase;
  object youcontainer;
  bool HaveArrived () {
    return arrivedarea;
  };
  bool InSystem() {
    return arrivedsys;
  };
  //only run this function if we are InSystem();
  object SignificantUnit() {
    if (_std.isNull(significantun)) {
      return significantun;
    }
    return _unit.getUnitFromContainer (significantun);
  };
  object DestinationSystem () {
    return destination;
  };
  object JumpPoints () {
	  return jumps;
  };
  void init_base_only (object you, int numsystemsaway, float distance_away_to_trigger) {
    init (you,numsystemsaway,true,false,distance_away_to_trigger);
    baseonly = true;
  };
  void init (object you, int numsystemsaway, bool capship_only, bool jumppoint_only,  float distance_away_to_trigger) {
    _std.setNull ( significantun);
	jumps=_olist.new();
    youcontainer = _unit.getContainer (you);
    capship = capship_only;
    jumppoint = jumppoint_only;
    baseonly=false;
    distfrombase=distance_away_to_trigger;
    object sysfile = _std.getSystemFile();
    destination=universe.getAdjacentSystem(sysfile,numsystemsaway,jumps);
    _string.delete (sysfile);
    arrivedsys=false;
    arrivedarea=false;
  };
  void destroy() {
    _unit.deleteContainer (youcontainer);
    _std.setNull(youcontainer);
    _string.delete (destination);
	_olist.delete(jumps);
    _std.setNull(destination);
    if (arrivedsys) {
      if (!_std.isNull(significantun)) {
	_unit.deleteContainer (significantun);
	_std.setNull(significantun);
      }
    }
  };
  void loop() {
	  if (arrivedsys) {
	    object base=_unit.getUnitFromContainer(significantun);
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull(base)||_std.isNull(you)) {
	      return;
	    }
	    float dist=unit.getSignificantDistance(you,base);
	    if (dist<=distfrombase) {
	      arrivedarea=true;
	    }
	  } else if (!arrivedsys) {
//		  _io.printf("ff");

	    object sysfil = _std.getSystemFile();
//		  _io.printf("ee");

		if (_string.equal (sysfil,destination)) {
//		  _io.printf("gg");

			arrivedsys=true;
	      object significant;
	      if (capship) {
		int randint=random.randomint(0,128);
		significant = unit.getSignificant (randint,capship,baseonly);
	      }else {
		significant = universe.getRandomJumppoint ();
	      }
	      if (_std.isNull (significant)) {
		significant =_unit.getPlayer();
	      }
	      if (_std.isNull(significant)) {
		arrivedsys=false;
	      }else {
		object newun=significant;
		object str = _string.new();
		object name = _unit.getName (newun);
		_io.sprintf(str,"You must visit the %s",name);
		_string.delete (name);
		_io.message (0,"game","all",str);
		_string.delete(str);
       		significantun=_unit.getContainer(significant);
	      }
	    }
	    _string.delete (sysfil);
//		  _io.printf("vv");

	  }    
//		  _io.printf("ww");


  };
}