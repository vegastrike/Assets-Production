module visit_aera10 {
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
  object orderlist_pink;
  object orderlist_purple;
  object orderlist_makkarel;
  object orderlist_herring;

  object null_pos;

  void initgame(){
    visit_aera.init();

    step=0;
    silver_lpos=vec3.new(0.0-6000.0,1000.0,5000.0);
    gold_lpos=vec3.new(0.0-500.0,0.0-1000.0,0.0-9000.0);
    null_pos=vec3.new(0.0,0.0,0.0);
    //    fighter_lpos=vec3.new(0.0-2000.0,0.0-2000.0,0.0-7000.0);
    player_unit=_unit.getPlayer();
    if (!_std.isNull(player_unit)) {
      fighter_lpos=_unit.getPosition(player_unit);
    } else {
      fighter_lpos=vec3.new (0.0,0.0,0.0);
    }
    jumppoint_mars_unit=unit.getUnitByFgID("jumppoint-mars");
    if(_std.isNull(jumppoint_mars_unit)){
      _io.printf("did not find mars jumppoint\n");
    }
    jumppoint_mars=_unit.getPosition(jumppoint_mars_unit);
  };

  void gameloop(){
    player_unit=_unit.getPlayer();

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
      ai_orderlist.orderFlyTo(orderlist_green,"jumppoint-mars",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_green,5000.0);
      order.orderList("green",orderlist_green);

      orderlist_red=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_red,"jumppoint-mars",null_pos,1.0,true,100.0);
      ai_orderlist.orderAttack(orderlist_red,5000.0);
      order.orderList("red",orderlist_red);

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
    // the confed defenders
    bool purple_ok=launch.launch_around_station("mars-station","purple","confed","destiny","_ai_stationary",4,2);
    bool pink_ok=launch.launch_around_station("mars-station","pink","confed","nova","_ai_stationary",4,2);

    if(purple_ok){
      orderlist_purple=ai_orderlist.newOrderList();
      ai_orderlist.orderAttack(orderlist_purple,5000.0);
      order.orderList("purple",orderlist_purple);
    }

    if(pink_ok){
      orderlist_pink=ai_orderlist.newOrderList();
      ai_orderlist.orderAttack(orderlist_pink,5000.0);
      order.orderList("pink",orderlist_pink);
    }
    // the pirate attackers

    jumppoint_nebula=unit.getUnitByFgID("jumppoint-nebula");
    if(_std.isNull(jumppoint_nebula)){
      _io.printf("nebula jumppoint not found\n");
      return;
    }
    jp_neb_pos=_unit.getPosition(jumppoint_nebula);

    launch.launch_waves_in_area("herring","pirates","mongoose","_ai_stationary",6,4,300.0,jp_neb_pos);
    launch.launch_waves_in_area("makkarel","pirates","puma","_ai_stationary",6,4,300.0,jp_neb_pos);

      orderlist_herring=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_herring,"mars-station",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_herring,5000.0);
      order.orderList("herring",orderlist_herring);

      orderlist_makkarel=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_makkarel,"mars-station",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_makkarel,5000.0);
      order.orderList("makkarel",orderlist_makkarel);

    _io.message(0,"game","all","Milita flightgroup have jumped in on Mars Station");

  };
}