module ai_flyto_waypoint {

  // memory/unitC bug free

  import vec3;
  import random;

  class object outstr;

  class object my_unit;
  class object my_order;

  class object last_head_order;
  class object last_move_order;

  // these are arguments
  class object waypoint;
  class float abort_range;
  class float vel;
  class bool afterburner;

  class bool _done;

  class object my_fgid;
  class float my_resolution;
  class float my_last_time;
  class object my_waypoint;

  void flyStraight(){
    object forward=vec3.new(0.0,0.0,vel);
    last_move_order=_order.newMatchLinearVelocity(forward,true,afterburner,false);

    _order.enqueueOrder(my_order,last_move_order);

    _olist.delete(forward);
  };

  void flyTo(object npos){
    last_head_order=_order.newChangeHeading(npos,3);

    object forward=vec3.new(0.0,0.0,vel);
    last_move_order=_order.newMatchLinearVelocity(forward,true,afterburner,false);

    _order.enqueueOrder(my_order,last_head_order);
    _order.enqueueOrder(my_order,last_move_order);

    _olist.delete(forward);
  };

  void initai(){
    outstr=_string.new();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    my_fgid=_unit.getFgID(my_unit);
   
    my_resolution=random.random(0.0,6.0);

    //    _io.printf("Waypoint0: \n");
    my_waypoint=vec3.clone(waypoint); // so that waypoint can be deleted by the caller
    //_io.printf("Waypoint: ");
    //vec3.print(waypoint);
    //_io.printf(" vel=%f  range=%f\n",vel,abort_range);

    object vstr=vec3.string(my_waypoint);
    _io.sprintf(outstr,"fly to %s",vstr);
    _string.delete(vstr);

    _order.setActionString(my_order,outstr);

    vel=vel*100.0;

    flyTo(my_waypoint);

    my_last_time=_std.getGameTime();
  };


  void executeai(){
    float dist=_unit.getMinDis(my_unit,my_waypoint);

    //        _io.printf("distance=%f\n",dist);

    if(dist<abort_range){
      // _io.printf("distance smaller\n");
      _order.eraseOrder(my_order,last_head_order);
      _order.eraseOrder(my_order,last_move_order);
      
      _done=true;
    }

    float new_time=_std.getGameTime();

    if((my_last_time+my_resolution)<new_time){
      object lhorder=_order.findOrder(my_order,last_head_order);
      
      if(_std.isNull(lhorder)){
	// the changeheading has terminated
	float angle=_unit.getAngleToPos(my_unit,my_waypoint);
	if(angle>20.0){
	  // are we still flying to our waypoint?
	  object lmorder=_order.findOrder(my_order,last_move_order);
	  _order.eraseOrder(my_order,last_move_order);
	  //_io.printf("%s: correcting flying to wp, angle=%f\n",my_fgid,angle);
	  flyTo(my_waypoint);
	}
      }
      
      my_resolution=random.random(3.0,6.0);
    }
  };

  void quitai(){
    _io.printf("ai_flyto_waypoints1 quitting\n");
    //_string.delete(outstr);
    //_olist.delete(my_waypoint);
  };

}
