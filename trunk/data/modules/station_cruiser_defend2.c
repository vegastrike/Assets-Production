module station_cruiser_defend2 {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import waypoints1;
  import order;
  import ai_superiority;
  import ai_patrol;

  float gametime;
  bool did_it;
  object outstr;

  object launchpos;
  object jumppoint;
  object enemy_launchpos;

  bool flag_distress_call;
  bool flag_jumppoint_reached;
  bool flag_enemy_attack;
  bool flag_ship_return;

  void initgame(){
    gametime=_std.getGameTime();
    outstr=_string.new();

    order.flyToOtherShip("gold-0","silver-0",0.5,false,1000.0);
    order.patrolFg(0,"green-","-nothing-",1000.0,0.6);
    order.patrolFg(1,"yellow-","gold-0",300.0,0.6);


    _io.message(0,"confed","confed","It's another nice day lad");
    _io.message(1,"confed","confed","nothing to worry about");
    _io.message(2,"confed","confed","we are expecting no attacks");
    _io.message(5,"confed","confed","here are your orders for today:");
    _io.message(6,"confed","confed","we are moving the cruiser gold-0");
    _io.message(7,"confed","confed","to our carrier silver-0");
    _io.message(10,"confed","confed","green has orders to patrol around the station");
    _io.message(11,"confed","confed","yellow has orders to follow gold-0 and secure it");
    _io.message(12,"confed","confed","blue, your task is it to fly support when needed");

    flag_distress_call=true;
    flag_jumppoint_reached=true;
    flag_enemy_attack=true;
    flag_ship_return=true;

    launchpos=vec3.new(10000.0,0.0,7000.0);
    enemy_launchpos=vec3.new(10000.0,0.0-2000.0,7000.0);
    jumppoint=vec3.new(12000.0,0.0,5000.0);

    unit.print_unitlist();
  };

  void gameloop(){
    float newtime=_std.getGameTime();

    if(flag_distress_call && newtime>20.0){
      _io.message(0,"confed","confed","we have got an emergecy call from pluto");
      _io.message(0,"confed","confed","our HQ is getting attacked");
      _io.message(0,"confed","confed","we will send support");
      _io.message(2,"confed","confed","yellow, red and brown will do it");
      _io.message(2,"confed","confed","blue, green, it's now to you to protect");
      _io.message(2,"confed","confed","the station and the cruiser");

      launch.launch_wave_in_area("red","confed","firefly","_ai_stationary",4,200.0,launchpos);
      launch.launch_wave_in_area("brown","confed","tian","_ai_stationary",4,200.0,launchpos);

      order.flyToWaypoint("red-",jumppoint,1.0,false,100.0);
      order.flyToWaypoint("brown-",jumppoint,1.0,false,100.0);
      order.flyToWaypoint("yellow-",jumppoint,1.0,false,100.0);
      
      flag_distress_call=false;
    }

    if(flag_jumppoint_reached && newtime>30.0){
      unit.removeFg("red-");
      unit.removeFg("brown-");
      unit.removeFg("yellow-");

      _io.message(0,"confed","confed","red,brown and yellow have jumped");

      flag_jumppoint_reached=false;
    }
    if(flag_enemy_attack && newtime>40.0){
      launch.launch_wave_in_area("alpha","aera","aeon","_ai_stationary",4,200.0,enemy_launchpos);
      launch.launch_wave_in_area("beta","aera","aevant","_ai_stationary",4,200.0,enemy_launchpos);

      order.spaceSuperiority("alpha-");
      order.spaceSuperiority("beta-");

      unit.setTargetShip("alpha-","gold-0");
      unit.setTargetShip("beta-","mars-station");

      _io.message(0,"confed","confed","Alert! Aera ships have jumped in");
      _io.message(0,"confed","confed","Defend our Installations");
      _io.message(2,"aera","all","Die, you earthling scum!");

      order.spaceSuperiority("green-");
      unit.setTargetShip("green-","beta-0");

      flag_enemy_attack=false;
    }
    if(flag_ship_return && newtime>60.0){
      launch.launch_wave_in_area("yellow","confed","tian","_ai_stationary",4,200.0,jumppoint);
      launch.launch_wave_in_area("red","confed","firefly","_ai_stationary",4,200.0,jumppoint);
      launch.launch_wave_in_area("brown","confed","tian","_ai_stationary",4,200.0,jumppoint);

      order.spaceSuperiority("yellow-");
      order.spaceSuperiority("brown-");
      order.spaceSuperiority("red-");

      unit.setTargetShip("yellow-","alpha-0");
      unit.setTargetShip("red-","alpha-0");
      unit.setTargetShip("brown-","beta-0");

      _io.message(0,"confed","confed","our ships are returning from Pluto!");
      _io.message(1,"confed","confed","it was a fake distress call");

      flag_ship_return=false;
    }
  };

  void endgame(){
  };
}
