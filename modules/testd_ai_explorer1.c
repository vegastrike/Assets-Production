module testd_ai_explorer1 {
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

    random_launch.addJPTravellers("confed","nova",1,2,1,3,100.0,500.0,5.0,20.0,0);
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
