module total_war {

  import random;
  import faction_ships;
  import launch;
  import vec3;
  import unit;

  float lasttime;
  float waittime;
  object unit_list;

  void initgame(){
    lasttime=0.0;
    waittime=random.random(5.0,10.0);
    faction_ships.make_ships_list();
  };

  void launch_new_wave(){
    object ship_list;
    object faction_name;


    float side=_std.Rnd();
    
    if(side>=0.5){
      ship_list=faction_ships.confed();
      faction_name="confed";
    }
    else{
      ship_list=faction_ships.aera();
      faction_name="aera";
    }

    object typename=faction_ships.getRandomShipType(ship_list);

    int nr_ships=random.randomint(2,6);

    object pos=vec3.new(8000.0,0.0,0.0);

    launch.launch_wave_in_area("fgname",faction_name,typename,"default",nr_ships, 1000.0, pos);
  };

  void loop(){
    float time=_std.getGameTime();

    if((time-lasttime)>waittime){
      launch_new_wave();

      _io.printMsgList();

      waittime=random.random(5.0,10.0);
      lasttime=time;
    }
  };

  void end(){
    _io.PrintFloats(:s1="endgame";);
    unit_list=unit.makeUnitList();
  };
}
