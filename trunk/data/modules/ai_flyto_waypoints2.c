module ai_flyto_waypoints2 {

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

  void flyStraight(){
    object forward=vec3.new(0.0,0.0,vel);
    last_move_order=_order.newMatchLinearVelocity(forward,true,afterburner,false);

    _order.enqueueOrder(my_order,last_move_order);
  };

  void flyTo(object npos){
    last_head_order=_order.newChangeHeading(npos,3);

    object forward=vec3.new(0.0,0.0,vel);
    last_move_order=_order.newMatchLinearVelocity(forward,true,afterburner,false);

    _order.enqueueOrder(my_order,last_head_order);
    _order.enqueueOrder(my_order,last_move_order);
  };

  void initai(){
    outstr=_string.new();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    //    abort_range=100.0;

    _io.printf("Waypoint: ");
    vec3.print(waypoint);
    _io.printf(" vel=%f  range=%f\n",vel,abort_range);
    
    vel=vel*100.0;

    flyTo(waypoint);
  };


  void executeai(){
    float dist=_unit.getMinDis(my_unit,waypoint);

    //        _io.printf("distance=%f\n",dist);

    if(dist<abort_range){
      _io.printf("distance smaller\n");
      _order.eraseOrder(my_order,last_head_order);
      _order.eraseOrder(my_order,last_move_order);
      
      _done=true;
    }

    object lhorder=_order.findOrder(my_order,last_head_order);
    object lmorder=_order.findOrder(my_order,last_move_order);

    if(_std.isNull(lhorder)){
      _order.eraseOrder(my_order,last_move_order);
      
      flyTo(waypoint);
    }
    if(_std.isNull(lmorder)){
      _io.sprintf(outstr,"mlinvel exited");
      _io.message("game","all",outstr);
    }
  };

  void quitai(){
    _io.printf("ai_flyto_waypoints1 quitting\n");
  };

}