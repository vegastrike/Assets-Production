module test_ais {
  import visit_aera;
  import universe;

  float lasttime;
  float waittime;

  int step;

  object silver_lpos;
  object gold_lpos;
  object fighter_lpos;
  object left_lpos;
  object right_lpos;
  object jumppoint_mars;
  object jumppoint_mars_unit;
  object player_unit;

  
  void test_ai_flyto_jumppoint(){
      launch.launch_wave_in_area("silver","confed","cruiser","_ai_stationary",2,2000.0,silver_lpos);
      launch.launch_wave_in_area("gold","confed","cruiser","_ai_stationary",2,4000.0,gold_lpos);

      launch.launch_wave_in_area("green","confed","firefly","_ai_stationary",6,1000.0,fighter_lpos);
      launch.launch_wave_in_area("red","confed","nova","_ai_stationary",6,1000.0,fighter_lpos);


      //order.flyToWaypoint("silver-",jumppoint_mars,1.0,false,100.0);
      order.flyToJumppoint("gold-",jumppoint_mars_unit,1.0,false);

      order.flyToJumppoint("green-",jumppoint_mars_unit,1.0,true);
      order.flyToJumppoint("red-",jumppoint_mars_unit,1.0,true);
  };

  void test_ai_flyto_waypoint_defend(){
      launch.launch_wave_in_area("silver","confed","cruiser","_ai_stationary",1,2000.0,silver_lpos);
      launch.launch_wave_in_area("gold","confed","cruiser","_ai_stationary",1,4000.0,gold_lpos);

      launch.launch_wave_in_area("green","confed","firefly","_ai_stationary",6,300.0,left_lpos);
      launch.launch_wave_in_area("red","confed","nova","_ai_stationary",6,300.0,left_lpos);

      vec3.print(left_lpos);
      _io.printf("\n");


      order.flyToWaypointDefend("silver-",jumppoint_mars,1.0,false,100.0,500.0);
      order.flyToWaypointDefend("gold-",jumppoint_mars,1.0,false,100.0,500.0);

      _io.printf("test1\n");
      order.flyToWaypointDefend("green-",right_lpos,1.0,false,100.0,200.0);
      _io.printf("test2\n");
      order.flyToWaypointDefend("red-",right_lpos,1.0,false,100.0,200.0);
      _io.printf("test3\n");

  };


  void initgame(){
    visit_aera.init();

    silver_lpos=vec3.new(0.0-6000.0,1000.0,5000.0);
    gold_lpos=vec3.new(0.0-3000.0,4000.0,0.0-5000.0);

    //    fighter_lpos=vec3.new(0.0-2000.0,0.0-2000.0,0.0-7000.0);
    player_unit=_unit.getPlayer();
    
    fighter_lpos=_unit.getPosition(player_unit);

    left_lpos=vec3.new(0.0,0.0,0.0-8000.0);
    right_lpos=vec3.new(0.0-3000.0,0.0,0.0-10000.0);

    jumppoint_mars_unit=unit.getUnitByFgID("jumppoint-pluto");
    jumppoint_mars=_unit.getPosition(jumppoint_mars_unit);

    //test_ai_flyto_jumppoint();
    test_ai_flyto_waypoint_defend();

  };

  void gameloop(){
  };

  void endgame(){
  };
}
