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

  void loop(){
    object typename=faction_ships.getRandomShipType(aera_ships);

    float nr_ships=random.random(2.0,6.0);

    object player=_unit.getPlayer();
    object player_pos=_unit.getPosition(player);

    launch.launch_wave_in_area("fgname","aera",typename,"default",nr_ships,1000.0,player_pos);

  };
}
