module earth_patrol_rnd_attack1 {
  import random;
  import faction_ships;
  import launch;
  import vec3;

  float lasttime;
  float waittime;
  object aera_ships;

  void initgame(){
    lasttime=0.0;
    waittime=random.random(10.0,30.0);
    faction_ships.make_ships_list();
    aera_ships=faction_ships.aera();
  };

  void launch_new_ships(){
    object typename=faction_ships.getRandomShipType(aera_ships);

    int nr_ships=random.randomint(2,4);

    object player=_unit.getPlayer();
    object player_pos=_unit.getPosition(player);

    launch.launch_wave_around_area("fgname","aera",typename,"default",nr_ships,500.0,2000.0,player_pos);
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
