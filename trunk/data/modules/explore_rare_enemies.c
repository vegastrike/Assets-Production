module explore_rare_enemies {
  import random;
  import faction_ships;
  import launch;
  import vec3;

  float lasttime;
  float waittime;
  int drone;
  void initgame(){
    lasttime=0.0;
    drone=0;
    waittime=random.random(10.0,30000.0);
    faction_ships.make_ships_list();
  };

  void launch_new_ships(){
    float side=_std.Rnd();
    
    object ship_list;
    object faction_name;
    int nr_ships=random.randomint(1,2);
    if (side>=0.66) {
      ship_list=faction_ships.aera();
      faction_name="aera";      
    }else if (side>=0.33) {
      ship_list=faction_ships.confed();
      faction_name="confed";      
    }else if((side>=0.33) && (drone==0)){
      drone=1;
      ship_list=faction_ships.unknown();
      faction_name="unknown";
      nr_ships=1;
    }
    else {
      ship_list=faction_ships.rlaan();
      faction_name="rlaan";      
    }

    object typename=faction_ships.getRandomShipType(ship_list);



    object player=_unit.getPlayer();
    object player_pos=_unit.getPosition(player);

    launch.launch_wave_around_area("fgname",faction_name,typename,"default",nr_ships,500.0,10000.0,player_pos);
  };

  void loop(){
    float time=_std.getGameTime();

    if((time-lasttime)>waittime){
      launch_new_ships();

      lasttime=time;
    }


  };
}
