module visit_aera {
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import random_launch;
  import universe;
  import ai_orderlist;

  float lasttime;
  float waittime;

  void init(){
    faction_ships.init();
    random_launch.init();
    universe.init();
    ai_orderlist.init();
  };

  void loop(){
    float time=_std.getGameTime();

    random_launch.loop();
    bool jumped=universe.loop();
    if(jumped){
      // we have jumped
      object sysname=_std.GetSystemName();
    }
  };

  void end(){
  };
}
