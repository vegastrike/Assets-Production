module testd_ai_waypoints1 {

  import unit;
  import vec3;
  import ai_flyto_waypoints1;
  import waypoints1;

  float gametime;
  bool did_it;

  void changeToWp(){
    object alpha_ship=unit.getUnitByFgID("alpha-0");
    object old_order=_unit.getOrder(alpha_ship);

    object waypoint=vec3.new(9000.0,0.0,0.0);

    object new_order=_order.newFlyToWaypoint(waypoint);

    _order.enqueueOrderFirst(old_order,new_order);
  };

  void initgame(){
    gametime=_std.getGameTime();
    did_it=false;
    waypoints1.initgame();
  };

  void gameloop(){
    float newtime=_std.getGameTime();

    if((!did_it) && ((newtime-gametime)>5.0)){
      _io.printf("setting to fly waypoints\n");
      changeToWp();
      did_it=true;
    }
  };

  void endgame(){
  };
}
