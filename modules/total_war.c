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
    faction_ships.init();
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

    int nr_ships=random.randomint(3,6);
    int fac = random.randomint (0,faction_ships.getMaxFactions()-1);
    faction_name = faction_ships.intToFaction(fac);
    object ship = faction_ships.getRandomFighter (faction_name);
    
    object pos=vec3.new(8000.0,0.0,0.0);
    launch.launch_wave_in_area(faction_name,faction_name,ship,"default",nr_ships, 15000.0, pos);
    _olist.delete(pos);
    object pos=vec3.new(9000.0,0.0,0.0);
    float rr = _std.Rnd();
    if (rr<0.125) {
     
    
    float r = _std.Rnd();
    if (r<0.25) {
      launch.launch_wave_in_area("fgname",faction_name,"starrunner","default",nr_ships, 15000.0, pos);
    }else if (r<0.5) {
      launch.launch_wave_in_area("fgname",faction_name,"fleetcarrier","default",nr_ships, 15000.0, pos);
    }else if (r<0.55) {
      launch.launch_wave_in_area("fgname",faction_name,"carrier","default",nr_ships, 15000.0, pos);
    }else if (r<0.75) {
      launch.launch_wave_in_area("fgname",faction_name,"yrilan","default",5, 15000.0, pos);
    }else {
      launch.launch_wave_in_area("fgname",faction_name,"escortcarrier","default",nr_ships, 15000.0, pos);
    }
    }
   
    _olist.delete(pos);
  };

  void loop(){
    float time=_std.getGameTime();

    if((time-lasttime)>waittime){
      launch_new_wave();

      _io.printMsgList();

      waittime=random.random(10.0,30.0);
      lasttime=time;
    }
  };

  void end(){
    _io.PrintFloats(:s1="endgame";);
    unit_list=unit.makeUnitList();
  };
}
