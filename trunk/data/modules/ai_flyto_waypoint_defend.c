module ai_flyto_waypoint_defend {

  // fly to waitpoint and defend yourself when attacked
  // then resume flight to wp

  import vec3;
  import random;

  class object outstr;

  class object my_unit;
  class object my_order;


  // these are arguments
  class object waypoint;
  class float abort_range;
  class float vel;
  class bool afterburner;
  class float defend_range;

  class bool _done;

  class object fgid;
  class object last_order;
  class int mode;
  class object null_target;

  class float resolution;
  class float last_time;

  void checkModes(){
    // _io.printf("before threat\n");
    object threat=unit.getThreatOrEnemyInRange(my_unit,defend_range);
    //_io.printf("after threat\n");
    if(mode==0){
      // we are in flyto-mode
      //_io.printf("unit %s in flyto-mode\n",fgid);
      if(!_std.isNull(threat)){
	// we have a threat
	mode=1; // defense mode
	object threat_fgid=_unit.getFgID(threat);
	_io.printf("unit %s switched from flyto to defend against %s\n",fgid,threat_fgid);

	_order.eraseOrder(my_order,last_order);

	object new_order=_order.newAggressiveAI("default.agg.xml","default.int.xml");
	_order.enqueueOrder(my_order,new_order);

	last_order=new_order;
	_string.delete(threat_fgid);

	_io.printf("end1\n");
      }
    }
    else if(mode==1){
      // defense mode
      if(_std.isNull(threat)){
	// we have no threat
	mode=0; // flyto-mode
	_io.printf("unit %s switched from defend to flyto\n",fgid);

	_order.eraseOrder(my_order,last_order);

	object new_order=_order.newFlyToWaypoint(waypoint,vel,afterburner,abort_range);

	_order.enqueueOrder(my_order,new_order);

	last_order=new_order;

	_unit.setTarget(my_unit,null_target);
      }

    }
  };

  void initai(){
    outstr=_string.new();
    _std.setNull(null_target);

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    fgid=_unit.getFgID(my_unit);

    mode=0;
    resolution=2.0;

    last_order=_order.newFlyToWaypoint(waypoint,vel,afterburner,abort_range);
    _order.enqueueOrder(my_order,last_order);

    checkModes();

    _done=false;

    last_time=_std.getGameTime();
  };


  void executeai(){
    float new_time=_std.getGameTime();

    if((last_time+resolution)<new_time){
      _io.printf("CJHECK\n");
      float dist=_unit.getMinDis(my_unit,waypoint);
      
      checkModes();
      if((mode==0) && (dist<abort_range)){
	_io.printf("unit %s reached end flyto_wp_defend\n",fgid);
	_done=true;
      }
      last_time=new_time;
    }
  };

  void quitai(){
    _io.printf("ai_flyto_waypoints_defend quitting\n");
    _string.delete(outstr);
  };

}
