module explore_far {
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import random_launch;

  float lasttime;
  float waittime;

  void initgame(){
    faction_ships.init();
    random_launch.init();

    random_launch.addFighters("confed",1,1,1,2,300.0,2000.0,45.0,2800.0,0);
    random_launch.addFighters("aera",1,1,1,2,1000.0,3000.0,60.0,3400.0,0);
    random_launch.addFighters("rlaan",1,2,1,1,1000.0,3000.0,60.0,3400.0,0);
    random_launch.addFighters("unknown",1,1,1,1,3000.0,6000.0,900.0,10000.0,0);
    //debugging values - lots of ships launched fast
    //random_launch.addFighters("confed",1,4,2,6,200.0,500.0,5.0,30.0,0);
    //random_launch.addFighters("aera",1,3,2,4,200.0,500.0,5.0,30.0,0);
  };

  void gameloop(){
    float time=_std.getGameTime();

    random_launch.loop();
  };

  void endgame(){
  };
}
