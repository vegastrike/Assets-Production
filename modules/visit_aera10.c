module visit_aera10 {
  import visit_aera;

  float lasttime;
  float waittime;

  int step;

  object silver_lpos;
  object gold_lpos;
  object fighter_lpos;
  object jumppoint_mars;
  object player_unit;

  void initgame(){
    visit_aera.init();

    step=0;
    silver_lpos=vec3.new(0.0-6000.0,1000.0,5000.0);
    gold_lpos=vec3.new(0.0-3000.0,4000.0,0.0-5000.0);

    //    fighter_lpos=vec3.new(0.0-2000.0,0.0-2000.0,0.0-7000.0);
    player_unit=_unit.getPlayer();
    
    fighter_lpos=_unit.getPosition(player_unit);

    object jumppoint_mars_unit=unit.getUnitByFgID("jumppoint-mars");
    jumppoint_mars=_unit.getPosition(jumppoint_mars_unit);
  };

  void gameloop(){
    if(step==0){
      _io.message(0,"game","all","we have an emergency call from mars");
      _io.message(1,"game","all","our station is under attack");
      _io.message(2,"game","all","proceed to jumppoint-mars quickly");

      launch.launch_wave_in_area("silver","confed","cruiser","_ai_stationary",2,2000.0,silver_lpos);
      launch.launch_wave_in_area("gold","confed","cruiser","_ai_stationary",2,4000.0,gold_lpos);

      launch.launch_wave_in_area("green","confed","firefly","_ai_stationary",6,1000.0,fighter_lpos);
      launch.launch_wave_in_area("red","confed","nova","_ai_stationary",6,1000.0,fighter_lpos);

      order.flyToWaypoint("silver-",jumppoint_mars,1.0,false,100.0);
      order.flyToWaypoint("gold-",jumppoint_mars,1.0,false,100.0);

      order.flyToWaypoint("green-",jumppoint_mars,1.0,true,100.0);
      order.flyToWaypoint("red-",jumppoint_mars,1.0,true,100.0);
      
      step=step+1;
    }
    else if(step==1){
    }
  };

  void endgame(){
  };
}
