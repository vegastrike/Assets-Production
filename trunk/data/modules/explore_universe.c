module explore_universe {
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import random_launch;
  import universe;

  float lasttime;
  float waittime;

  void initgame(){
    faction_ships.init();
    random_launch.init();
    universe.init();

    random_launch.addFighters("confed",1,1,1,2,300.0,2000.0,45.0,180.0,0);
    random_launch.addFighters("aera",1,1,1,2,1000.0,3000.0,60.0,240.0,0);
    random_launch.addFighters("rlaan",1,1,1,2,1000.0,3000.0,60.0,240.0,0);
    random_launch.addFighters("unknown",1,1,1,1,4000.0,6000.0,300.0,4000.0,0);

    // launch it in front of the player (launch_mode==1)
    random_launch.addFighters("confed",1,2,2,6,1000.0,10000.0,45.0,180.0,1);

    //debugging values - lots of ships launched fast
    //random_launch.addFighters("confed",1,4,2,6,200.0,500.0,5.0,30.0,0);
    //random_launch.addFighters("aera",1,3,2,4,200.0,500.0,5.0,30.0,0);
    //random_launch.addConvoy("noyet",1,4,5000.0,10000.0,30.0,60.0,0);
  };

  void gameloop(){
    float time=_std.getGameTime();

    random_launch.loop();
    bool jumped=universe.loop();
    if(jumped){
      // we have jumped
      object sysname=_std.GetSystemName();
      if(_string.equal(sysname,"Sol")){
	_io.message(0,"game","all","you have jumped back to Sol");
      }
      else if(_string.equal(sysname,"Demeter")){
	_io.message(0,"game","all","you have now reached Demeter");
      }
      else if(_string.equal(sysname,"Whatever")){
      }
    }
  };

  void endgame(){
  };
}
