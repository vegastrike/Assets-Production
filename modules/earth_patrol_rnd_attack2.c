module earth_patrol_rnd_attack2 {
  import random;
  import faction_ships;
  import launch;
  import vec3;

  float lasttime;
  float waittime;

  void initgame(){
    lasttime=0.0;
    waittime=random.random(10.0,30.0);
    faction_ships.make_ships_list();
  };

  void launch_new_ships(){
    float side=_std.Rnd();
    _io.PrintFloats(:s1="launching new wave side="; side);
    
    object ship_list;
    object faction_name;

    if(side>=0.5){
      ship_list=faction_ships.confed();
      faction_name="confed";
    }
    else{
      ship_list=faction_ships.aera();
      faction_name="aera";
    }

    object typename=faction_ships.getRandomShipType(ship_list);

    float nr_ships=random.random(2.0,4.0);

    object player=_unit.getPlayer();
    object player_pos=_unit.getPosition(player);

    launch.launch_wave_around_area("fgname",faction_name,typename,"default",nr_ships,500.0,2000.0,player_pos);
  };

  void loop(){
    float time=_std.getGameTime();

    if((time-lasttime)>waittime){
      launch_new_ships();

      waittime=random.random(10.0,30.0);
      lasttime=time;
    }


  };
}
