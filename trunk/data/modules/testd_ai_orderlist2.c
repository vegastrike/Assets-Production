module testd_ai_orderlist2 {
  import visit_aera;

  float lasttime;
  float waittime;

  int step;

  object silver_lpos;
  object gold_lpos;
  object fighter_lpos;
  object jp_neb_pos;

  object jumppoint_mars_unit;
  object jumppoint_mars;
  object jumppoint_nebula;

  object player_unit;

  object orderlist_green;
  object orderlist_red;

  object null_pos;

  void initgame(){
    visit_aera.init();

    step=0;
    silver_lpos=vec3.new(0.0-6000.0,1000.0,5000.0);
    gold_lpos=vec3.new(0.0-500.0,0.0-1000.0,0.0-9000.0);
    null_pos=vec3.new(0.0,0.0,0.0);
    //    fighter_lpos=vec3.new(0.0-2000.0,0.0-2000.0,0.0-7000.0);
    player_unit=_unit.getPlayer();
    
    fighter_lpos=_unit.getPosition(player_unit);

    jumppoint_mars_unit=unit.getUnitByFgID("jumppoint-mars");
    jumppoint_mars=_unit.getPosition(jumppoint_mars_unit);
  };

  void gameloop(){
    if(step==0){
      _io.message(0,"game","all","we have an emergency call from mars");
      _io.message(1,"game","all","our station is under attack");
      _io.message(2,"game","all","proceed to jumppoint-mars quickly");

      //      launch.launch_wave_in_area("brown","confed","truck_small","_ai_stationary",2,5000.0,silver_lpos);
      launch.launch_wave_in_area("silver","confed","cruiser","_ai_stationary",2,2000.0,silver_lpos);
      launch.launch_wave_in_area("gold","confed","cruiser","_ai_stationary",2,4000.0,gold_lpos);

      launch.launch_waves_in_area("green","confed","firefly","_ai_stationary",6,2,1000.0,fighter_lpos);
      launch.launch_waves_in_area("red","confed","nova","_ai_stationary",6,2,1000.0,fighter_lpos);


      //order.flyToJumppoint("silver-",jumppoint_mars_unit,1.0,true);
      //order.flyToJumppoint("gold-",jumppoint_mars_unit,1.0,true);

      //order.spaceSuperiority("green-");
      //order.spaceSuperiority("red-");
      //order.flyToJumppoint("green-",jumppoint_mars_unit,1.0,true);
      //order.flyToJumppoint("red-",jumppoint_mars_unit,1.0,true);

      orderlist_green=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_green,"station-north",null_pos,1.0,true,500.0);
      //      ai_orderlist.orderFlyTo(orderlist_green,"station-west",null_pos,1.0,true,500.0);
      //ai_orderlist.orderFlyTo(orderlist_green,"station-south",null_pos,1.0,true,500.0);
      order.orderList("green",orderlist_green);

      orderlist_red=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_red,"jumppoint-mars",null_pos,1.0,true,100.0);
      ai_orderlist.orderDefend(orderlist_red,200.0);
      ai_orderlist.orderAttack(orderlist_red,1000.0);

      //      order.orderList("red",orderlist_red);

      step=step+1;
    }
    else if(step==1){
    }
  };

  void endgame(){
  };

  void initstarsystem(){
    object sname=_std.GetSystemName();

    if(_string.equal(sname,"Mars")){
      populateMarsSystem();
    }
    else{
      _io.message(0,"game","all","blue-0 - immediately leave this system");
      _io.message(1,"game","all","blue-0 - proceed back to earth");
      _io.message(2,"game","all","blue-0 - and then to mars");
    }
  };

  void populateMarsSystem(){
    bool retval=launch.launch_around_station("mars-station","purple","confed","destiny","_ai_stationary",4,2);
    retval=launch.launch_around_station("mars-station","pink","confed","nova","_ai_stationary",4,2);

    order.spaceSuperiority("purple-");
    order.spaceSuperiority("pink-");

    jumppoint_nebula=unit.getUnitByFgID("jumppoint-nebula");
    jp_neb_pos=_unit.getPosition(jumppoint_nebula);

    launch.launch_waves_in_area("herring","pirates","mongoose","_ai_stationary",6,4,300.0,jp_neb_pos);
    launch.launch_waves_in_area("makkarel","pirates","puma","_ai_stationary",6,4,300.0,jp_neb_pos);

    order.spaceSuperiority("herring-");
    order.spaceSuperiority("makkarel-");

    _io.message(0,"game","all","Milita flightgroup have jumped in on Mars Station");

  };
}
