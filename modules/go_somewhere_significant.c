module go_somewhere_significant {
  object destination;
  object significantun;
  bool capship;
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
    return _unit.getUnitFromContainer (significantun);
  };
  object DestinationSystem () {
    return destination;
  };
  void init (object you, int numsystemsaway, bool usecap, float distance_away_to_trigger) {
    _std.setNull ( significantun);
    youcontainer = _unit.getContainer (you);
    capship = usecap;
    distfrombase=distance_away_to_trigger;
    object sysfile = _std.getSystemFile();
    destination=universe.getAdjacentSystem(sysfile,numsystemsaway);
    arrivedsys=false;
    arrivedarea=false;
  };
  void destroy() {
    _unit.deleteContainer (youcontainer);
    _std.setNull(youcontainer);
    _string.delete (destination);
    _std.setNull(destination);
    if (arrivedsys) {
      _unit.deleteContainer (significant);
      _std.setNull(significant);
    }
  }
  void loop() {
	  if (arrivedsys) {
	    object base=_unit.getUnitFromContainer(significantun);
	    object you=_unit.getUnitFromContainer(youcontainer);
	    if (_std.isNull(base)||_std.isNull(you)) {
	      return;
	    }
	    float dist=_unit.getDistance(base,you);
	    if (dist<=distfrombase) {
	      arrivedarea=true;
	    }
	  } else if (!arrivedsys) {
	    object sysfil = _std.getSystemFile();
	    if (_string.equal (sysfil,destination)) {
	      arrivedsys=true;
	      int randint=random.randomint(0,50);
	      object significant = unit.getSignificant (randint,!capship);
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
		_io.message (0,"game","all",str);
		_string.delete(str);
       		significantun=_unit.getContainer(significant);
	      }
	    }
	    _string.delete (sysfil);
	  }    

  };
}
