module station_cruiser_defend1 {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import waypoints1;

  float gametime;
  bool did_it;

  void moveCruiser(){
    object alpha_ship=unit.getUnitByFgID("gold-0");
    object old_order=_unit.getOrder(alpha_ship);

    object carrier_ship=unit.getUnitByFgID("silver-0");
    object carrier_pos=_unit.getPosition(carrier_ship);

    object waypoint=carrier_pos;

    object new_order=_order.newFlyToWaypoint(waypoint,0.5,false,1000.0);

    _order.enqueueOrderFirst(old_order,new_order);
  };

  void initgame(){
    gametime=_std.getGameTime();

    moveCruiser();
  };

  void gameloop(){
    float newtime=_std.getGameTime();

  };

  void endgame(){
  };
}
