module ai_flyto2 {

  import vec3;
  import random;

  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;
  class object last_head_order;
  class object last_move_order;
  class object last_waypoint;
  class int waypoint_index;
  object waypoints; // shared by all ai instances

  void nextWaypoint(){
    int size=_olist.size(waypoints);

    waypoint_index=waypoint_index+1;

    if(waypoint_index>=size){
      waypoint_index=0;
    }

    object wp=_olist.at(waypoints,waypoint_index);

    float x=_olist.at(wp,0);
    float y=_olist.at(wp,1);
    float z=_olist.at(wp,2);

    _io.sprintf(outstr,"Waypoint %d: %f %f %f",waypoint_index,x,y,z);
    _io.message("game","all",outstr);

    last_waypoint=wp;
  };

  void flyStraight(){
    object forward=vec3.new(0.0,0.0,100.0);
    last_move_order=_order.newMatchLinearVelocity(forward,true,false,false);

    _order.enqueueOrder(my_order,last_move_order);

    //    _io.sprintf(outstr,"FlyingStraight");
    //_io.message("game","all",outstr);
  };

  void flyTo(object npos){
    //  new_order=_order.newMatchLinearVelocity(npos,false,false,true);
    //    last_head_order=_order.newFaceTarget(true,true,3);
    last_head_order=_order.newChangeHeading(npos,3);

    object forward=vec3.new(0.0,0.0,100.0);
    last_move_order=_order.newMatchLinearVelocity(forward,true,false,false);

    _order.enqueueOrder(my_order,last_head_order);
    _order.enqueueOrder(my_order,last_move_order);

    //    _io.sprintf(outstr,"Flying to %f %f %f",_olist.at(npos,0),_olist.at(npos,1),_olist.at(npos,2));
    //_io.message("game","all",outstr);
  };

  void initai(){
    _io.printf("init flyto2 ai\n");
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    object player_unit=_unit.getPlayer();
    _unit.setTarget(my_unit,player_unit);

    waypoint_index=0-1;

    waypoints=waypoints1.getWaypoints();

    nextWaypoint();
    flyTo(last_waypoint);
  };


  void executeai(){
    float dist=_unit.getMinDis(my_unit,last_waypoint);

    _io.printf("distance=%f\n",dist);

    if(dist<100.0){
      _io.printf("distance smaller\n");
      _order.eraseOrder(my_order,last_head_order);
      _order.eraseOrder(my_order,last_move_order);
      
      nextWaypoint();
      flyTo(last_waypoint);
    }

    object lhorder=_order.findOrder(my_order,last_head_order);
    object lmorder=_order.findOrder(my_order,last_move_order);

    //if((!flystraight) && _std.isNull(lhorder)){
      
      //      flyStraight();

    if(_std.isNull(lhorder)){
      //_io.sprintf(outstr,"changehead exited");
      //_io.message("game","all",outstr);

      _order.eraseOrder(my_order,last_move_order);
      
      flyTo(last_waypoint);
    }
    if(_std.isNull(lmorder)){
      _io.sprintf(outstr,"mlinvel exited");
      _io.message("game","all",outstr);
    }
  };

  void quitai(){
  };

}
