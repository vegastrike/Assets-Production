module testd_patrol1 {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import ai_patrol;
  import launch;
  import order;

  float gametime;
  bool did_it;

  void initgame(){
    gametime=_std.getGameTime();

    order.flyToOtherShip("gold-0","silver-0",0.5,false,1000.0);

    order.patrolFg(0,"makkarel-","-nothing-",1000.0);

    order.patrolFg(1,"herring-","gold-0",300.0);

    did_it=false;
  };

  void gameloop(){
    float newtime=_std.getGameTime();

    if((!did_it) && newtime>10.0){
      _io.printf("\nremoving thuna\n");
      object unit=unit.getUnitByFgID("thuna-0");

      _unit.removeFromGame(unit);
      did_it=true;
    }
  };

  void endgame(){
  };
}
