module testd_ai_orderlist1 {
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import random_launch;
  import universe;

  float lasttime;
  float waittime;

  object orderlist1;
  object ppos;
  object wppos;
  object player;

  void initgame(){
    faction_ships.init();
    random_launch.init();
    universe.init();
    ai_orderlist.init();

    player=_unit.getPlayer();
    ppos=_unit.getPosition(player);

    orderlist1=ai_orderlist.newOrderList();

    ai_orderlist.orderFlyTo(orderlist1,"station-mars",wppos,0.7,false,500.0);
    ai_orderlist.orderDefend(orderlist1,500.0);

    launch.launch_wave_around_area("makkarel","confed","nova","_ai_stationary",1,100.0,300.0,ppos);

    order.orderList("makkarel",orderlist1);
  };

  void gameloop(){
    float time=_std.getGameTime();

    random_launch.loop();
    bool jumped=universe.loop();
  };

  void endgame(){
  };
}
