module random_launch {
  import random;
  import faction_ships;
  import launch;
  import vec3;

  object launch_list;
  object wait_list;
  float resolution;
  object player_unit;

  void init(){
    launch_list=_olist.new();
    wait_list=_olist.new();
    resolution=5.0;
    player_unit=_unit.getPlayer();

    _io.printf("random_launch:init\n");
  };

  void addFighters(object faction,int min_nr_fg,int max_nr_fg,int min_nr_ships,int max_nr_ships,float min_range,float max_range,float min_time,float max_time,int launch_mode){
    //    _io.printf("random_launch:addf\n");
    int mode=0;

    object new_submap=_omap.new();
    //_io.printf("random_launch:afternew\n");

    _omap.set(new_submap,"mode",mode);
    _omap.set(new_submap,"faction",faction);
    //    _omap.set(new_submap,"probab",probab);
    _omap.set(new_submap,"min_nr_fg",min_nr_fg);
    _omap.set(new_submap,"max_nr_fg",max_nr_fg);
    _omap.set(new_submap,"min_nr_ships",min_nr_ships);
    _omap.set(new_submap,"max_nr_ships",max_nr_ships);
    _omap.set(new_submap,"min_range",min_range);
    _omap.set(new_submap,"max_range",max_range);
    _omap.set(new_submap,"min_time",min_time);
    _omap.set(new_submap,"max_time",max_time);
    _omap.set(new_submap,"launch_mode",launch_mode);

    _io.printf("random_launch:afterset\n");

    _olist.push_back(launch_list,new_submap);

    float thentime=calc_thentime(min_time,max_time);

    _io.printf("new thentime=%f\n",thentime);
    _olist.push_back(wait_list,thentime);
  };

  void loop(){
    checkLaunch();
  };

  void checkLaunch(){
    float nowtime=_std.getGameTime();

    int size=_olist.size(wait_list);
    int i=0;

    while(i<size){

      //_io.printf("before at waitlist\n");
      float thentime=_olist.at(wait_list,i);
      //_io.printf("i=%d nowtime=%f thentime=%f\n",i,nowtime,thentime);

      if(thentime<nowtime){
	float thentime=launch(i);
	
	_olist.set(wait_list,i,thentime);
	//_io.printf("after set of wait_list\n");
	_std.ResetTimeCompression();
      }
      i=i+1;
    }
  };

  float launch(int i){
    object submap=_olist.at(launch_list,i);

    int mode=_omap.get(submap,"mode");
    object faction=_omap.get(submap,"faction");
    int min_nr_fg=_omap.get(submap,"min_nr_fg");
    int max_nr_fg=_omap.get(submap,"max_nr_fg");
    int min_nr_ships=_omap.get(submap,"min_nr_ships");
    int max_nr_ships=_omap.get(submap,"max_nr_ships");
    float min_range=_omap.get(submap,"min_range");
    float max_range=_omap.get(submap,"max_range");
    float min_time=_omap.get(submap,"min_time");
    float max_time=_omap.get(submap,"max_time");

    _io.printf("launching mode=%d faction=%s\n",mode,faction);

    int nr_fg=random.randomint(min_nr_fg,max_nr_fg);
    int nr_ships=random.randomint(min_nr_ships,max_nr_ships);

    object type=faction_ships.getRandomFighter(faction);

    object pos=_unit.getPosition(player_unit);

    launch.launch_wave_around_area("random",faction,type,"default",nr_ships,min_range,max_range,pos);

    float thentime=calc_thentime(min_time,max_time);
    _io.printf("new thentime=%f\n",thentime);

    return thentime;

  };

  float calc_thentime(float min_time,float max_time){
     float waittime=random.random(min_time,max_time);
    float nowtime=_std.getGameTime();
    float thentime=waittime+nowtime;

    return thentime;
  };
}
