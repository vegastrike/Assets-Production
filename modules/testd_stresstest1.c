module testd_stresstest1 {
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
  object orderlist_alpha;
  object orderlist_omega;
  object orderlist_makkarel;
  object orderlist_herring;
  object orderlist_gamma;

  object null_pos;

  float last_time;

  void initgame(){
    visit_aera.init();

    step=0;

    null_pos=vec3.new(0.0,0.0,0.0);
    //    fighter_lpos=vec3.new(0.0-2000.0,0.0-2000.0,0.0-7000.0);
    player_unit=_unit.getPlayer();

    last_time=_std.getGameTime();
  };

  void gameloop(){
    float nowtime=_std.getGameTime();

    if(step==0){

    launch.launch_around_unit("Kalkos","green","confed","destiny","_ai_stationary",6,8);
    launch.launch_around_unit("Kalkos","red","confed","nova","_ai_stationary",6,8);

      orderlist_green=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_green,"Arados",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_green,"arados-station",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_green,"Poniferos",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_green,2000.0);
      order.orderList("green",orderlist_green);

      orderlist_red=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_red,"arados-station",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_red,"Arados",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_red,"Poniferos",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_red,5000.0);
      order.orderList("red",orderlist_red);

      step=step+1;
    }
    else if(step==1){
      if(nowtime>20.0){
	launchAttackers();
	
	step=step+1;
      }
    }
  };

  void endgame(){
  };

  void initstarsystem(){
  };

  void launchAttackers(){
    object green_unit=unit.getUnitByFgID("green-0");
    object green_pos=_unit.getPosition(green_unit);

    object red_unit=unit.getUnitByFgID("red-0");
    object red_pos=_unit.getPosition(red_unit);

    launch.launch_waves_around_area("alpha","aera","aeon","_ai_stationary",8,8,500.0,1000.0,red_pos);
    launch.launch_waves_around_area("omega","aera","aevant","_ai_stationary",8,8,500.0,1000.0,green_pos);

    orderlist_alpha=ai_orderlist.newOrderList();
    ai_orderlist.orderAttack(orderlist_alpha,5000.0);
    order.orderList("alpha",orderlist_alpha);

    orderlist_omega=ai_orderlist.newOrderList();
    ai_orderlist.orderAttack(orderlist_omega,5000.0);
    order.orderList("omega",orderlist_omega);

    launch.launch_around_unit("Poniferos","gamma","confed","destiny","_ai_stationary",6,8);

      orderlist_gamma=ai_orderlist.newOrderList();
      ai_orderlist.orderFlyTo(orderlist_gamma,"Arados",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_gamma,"arados-station",null_pos,1.0,true,500.0);
      ai_orderlist.orderFlyTo(orderlist_gamma,"Poniferos",null_pos,1.0,true,500.0);
      ai_orderlist.orderAttack(orderlist_gamma,2000.0);
      order.orderList("gamma",orderlist_gamma);


  };
}
