module testd_patrol1 {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import ai_patrol;
  import launch;

  float gametime;

  void patrolFg(object fgid){
    object around_unit;
    _std.setNull(around_unit);

    object unit=unit.getUnitByFgID(fgid);
    object unit_order=_unit.getOrder(unit);

    object upos=_unit.getPosition(unit);

    object new_order=_order.newPatrol(0,upos,300.0,around_unit);

    _order.enqueueOrderFirst(unit_order,new_order);
  };

  void patrol(int pmode,object patrol_fgid,object around_fgid){
    object around_unit=unit.getUnitByFgID(around_fgid);


    object unit=unit.getUnitByFgID(patrol_fgid);
    object unit_order=_unit.getOrder(unit);

    object upos=_unit.getPosition(unit);

    object new_order=_order.newPatrol(pmode,upos,300.0,around_unit);

    _order.enqueueOrderFirst(unit_order,new_order);
  };

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
    patrolFg("makkarel-0");
    patrolFg("makkarel-1");
    patrolFg("makkarel-2");
    patrolFg("makkarel-3");

    patrol(1,"herring-0","gold-0");
    patrol(1,"herring-1","gold-0");
    patrol(1,"herring-2","gold-0");
    patrol(1,"herring-3","gold-0");
  };

  void gameloop(){
    float newtime=_std.getGameTime();
  };

  void endgame(){
  };
}
