module station_cruiser_defend2 {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import waypoints1;
  import order;
 
  float gametime;
  bool did_it;
  object outstr;

  object launchpos;
  object jumppoint;
  object enemy_launchpos;

  bool flag_distress_call;
  bool flag_jumppoint_reached;
  bool flag_enemy_attack;

  void initgame(){
    gametime=_std.getGameTime();
    outstr=_string.new();

    order.flyToOtherShip("gold-0","silver-0",0.5,false,1000.0);
    order.patrolFg(0,"green-","-nothing-",1000.0);
    order.patrolFg(1,"yellow-","gold-0",300.0);

    _io.message("confed","confed","It's another nice day lad");
    _io.message("confed","confed","nothing to worry about");
    _io.message("confed","confed","we are expecting no attacks");
    _io.message("confed","confed","here are your orders for today:");
    _io.message("confed","confed","we are moving the cruiser gold-0");
    _io.message("confed","confed","to our carrier silver-0");
    _io.message("confed","confed","green has orders to patrol around the station");
    _io.message("confed","confed","yellow has orders to follow gold-0 and secure it");
    _io.message("confed","confed","blue, your task is it to fly support when needed");

    flag_distress_call=true;
    flag_jumppoint_reached=true;
    flag_enemy_attack=true;

    launchpos=vec3.new(10000.0,0.0,7000.0);
    enemy_launchpos=vec3.new(10000.0,0.0-2000.0,7000.0);
    jumppoint=vec3.new(12000.0,0.0,5000.0);
  };

  void gameloop(){
    float newtime=_std.getGameTime();

    if(flag_distress_call && newtime>10.0){
      _io.message("confed","confed","we have got an emergecy call from pluto");
      _io.message("confed","confed","our HQ is getting attacked");
      _io.message("confed","confed","we will send support");
      _io.message("confed","confed","yellow, red and brown will do it");
      _io.message("confed","confed","blue, green, it's now to you to protect");
      _io.message("confed","confed","the station and the cruiser");

      launch.launch_wave_in_area("red","confed","firefly","_ai_stationary",4,200.0,launchpos);
      launch.launch_wave_in_area("brown","confed","tian","_ai_stationary",4,200.0,launchpos);

      order.flyToWaypoint("red-",jumppoint,1.0,false,100.0);
      order.flyToWaypoint("brown-",jumppoint,1.0,false,100.0);
      order.flyToWaypoint("yellow-",jumppoint,1.0,false,100.0);
      
      flag_distress_call=false;
    }

    if(flag_jumppoint_reached && newtime>30.0){
      //unit.removeFg("red-");
      //unit.removeFg("brown-");
      //unit.removeFg("yellow-");

      _io.message("confed","confed","red,brown and yellow have jumped");

      flag_jumppoint_reached=false;
    }
    if(flag_enemy_attack && newtime>40.0){
      launch.launch_wave_in_area("alpha","aera","aeon","_ai_stationary",4,200.0,enemy_launchpos);
      launch.launch_wave_in_area("beta","aera","aevant","_ai_stationary",4,200.0,enemy_launchpos);

      // da fehlt noch was

      _io.message("confed","confed","Alert! Aera ships have jumped in");
      _io.message("confed","confed","Defend our Installations");
      _io.message("aera","all","Die, you earthling scum!");

      flag_enemy_attack=false;
    }
  };

  void endgame(){
  };
}
