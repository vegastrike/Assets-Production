module random_launch {
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import order;
  import unit;
  import ai_stationary;
  import ai_patrol;
  import ai_flyto_waypoint;
  import ai_superiority;
  import ai_explorer;
  import ai_flyto_waypoint_defend;

  object launch_list;
  object wait_list;
  float resolution;
  object player_unit;
  float lasttime;
  int rndcounter;
  object fgstring;

  void init(){
    launch_list=_olist.new();
    wait_list=_olist.new();
    resolution=5.0;
    player_unit=_unit.getPlayer();
    lasttime=_std.getGameTime();
    rndcounter=0;
    fgstring=_string.new();

    _io.printf("random_launch:init\n");
  };

  void addConvoy(object faction,int min_nr_trucks,int max_nr_trucks,float min_range,float max_range,float min_time,float max_time,int launch_mode){
    int mode=1;

    object new_submap=_omap.new();

    _omap.set(new_submap,"mode",mode);
    _omap.set(new_submap,"faction",faction);
    _omap.set(new_submap,"min_nr_trucks",min_nr_trucks);
    _omap.set(new_submap,"max_nr_trucks",max_nr_trucks);
    _omap.set(new_submap,"min_range",min_range);
    _omap.set(new_submap,"max_range",max_range);
    _omap.set(new_submap,"min_time",min_time);
    _omap.set(new_submap,"max_time",max_time);
    _omap.set(new_submap,"launch_mode",launch_mode);

    _olist.push_back(launch_list,new_submap);

    float thentime=calc_thentime(min_time,max_time);

    //    _io.printf("new thentime=%f\n",thentime);
    _olist.push_back(wait_list,thentime);
  };

  void addFighters(object faction,int min_nr_fg,int max_nr_fg,int min_nr_ships,int max_nr_ships,float min_range,float max_range,float min_time,float max_time,int launch_mode){
    int mode=0;

    object new_submap=_omap.new();

    _omap.set(new_submap,"mode",mode);
    _omap.set(new_submap,"faction",faction);
    _omap.set(new_submap,"min_nr_fg",min_nr_fg);
    _omap.set(new_submap,"max_nr_fg",max_nr_fg);
    _omap.set(new_submap,"min_nr_ships",min_nr_ships);
    _omap.set(new_submap,"max_nr_ships",max_nr_ships);
    _omap.set(new_submap,"min_range",min_range);
    _omap.set(new_submap,"max_range",max_range);
    _omap.set(new_submap,"min_time",min_time);
    _omap.set(new_submap,"max_time",max_time);
    _omap.set(new_submap,"launch_mode",launch_mode);

    _olist.push_back(launch_list,new_submap);

    float thentime=min_time;
      //calc_thentime(min_time,max_time);

    //_io.printf("new thentime=%f\n",thentime);
    _olist.push_back(wait_list,thentime);
  };

  void addJPTravellers(object faction,object type,int min_nr_fg,int max_nr_fg,int min_nr_ships,int max_nr_ships,float min_range,float max_range,float min_time,float max_time,int launch_mode){
    int mode=2;

    object new_submap=_omap.new();

    _omap.set(new_submap,"mode",mode);
    _omap.set(new_submap,"faction",faction);
    _omap.set(new_submap,"type",type);
    _omap.set(new_submap,"min_nr_fg",min_nr_fg);
    _omap.set(new_submap,"max_nr_fg",max_nr_fg);
    _omap.set(new_submap,"min_nr_ships",min_nr_ships);
    _omap.set(new_submap,"max_nr_ships",max_nr_ships);
    _omap.set(new_submap,"min_range",min_range);
    _omap.set(new_submap,"max_range",max_range);
    _omap.set(new_submap,"min_time",min_time);
    _omap.set(new_submap,"max_time",max_time);
    _omap.set(new_submap,"launch_mode",launch_mode);

    _olist.push_back(launch_list,new_submap);

    float thentime=min_time;
      //calc_thentime(min_time,max_time);

    //_io.printf("new thentime=%f\n",thentime);
    _olist.push_back(wait_list,thentime);
  };

  void loop(){
    float nowtime=_std.getGameTime();

    if(nowtime>(lasttime+resolution)){
      //_io.printf("checking at %f\n",nowtime);
      player_unit=_unit.getPlayer();
      if(_std.isNull(player_unit)){
	// so we avoid problems later on
	return;
      }
      checkLaunch();
      lasttime=nowtime;

      //unit.print_unitlist();
    }
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
	//_std.ResetTimeCompression();
      }
      i=i+1;
    }
  };

  void launchConvoy(object submap){
    object faction=_omap.get(submap,"faction");
    int min_nr_trucks=_omap.get(submap,"min_nr_trucks");
    int max_nr_trucks=_omap.get(submap,"max_nr_trucks");
    float min_range=_omap.get(submap,"min_range");
    float max_range=_omap.get(submap,"max_range");

    int nr_trucks=random.randomint(min_nr_trucks,max_nr_trucks);
    player_unit=_unit.getPlayer(); //player_unit can't get NULL - that's catched before
    object pos=_unit.getPosition(player_unit);

    //object type="truck_small";
    object type="cruiser";

    //    _io.sprintf(fgstring,"rnd%d",rndcounter);
    rndcounter=rndcounter+1;

    _io.message(0,"game","all","Convoy has been detected");

    launch.launch_wave_around_area(fgstring,"confed",type,"_ai_stationary",nr_trucks,min_range,max_range,pos);

    //    launch.launch_wave_around_area(fgstring,"confed","cruiser","_ai_stationary",nr_trucks/2,min_range,max_range,pos);

    object waypoint=vec3.random_around_player(min_range*10.0,max_range*30.0);
    order.flyToWaypoint(fgstring,waypoint,1.0,false,100.0);

  };

  void launchFighters(object submap){
    object faction=_omap.get(submap,"faction");
    int min_nr_fg=_omap.get(submap,"min_nr_fg");
    int max_nr_fg=_omap.get(submap,"max_nr_fg");
    int min_nr_ships=_omap.get(submap,"min_nr_ships");
    int max_nr_ships=_omap.get(submap,"max_nr_ships");
    float min_range=_omap.get(submap,"min_range");
    float max_range=_omap.get(submap,"max_range");
    int launch_mode=_omap.get(submap,"launch_mode");

    int nr_fg=random.randomint(min_nr_fg,max_nr_fg);

    object pos;
    if(launch_mode==0){
      pos=_unit.getPosition(player_unit);
    }
    else if(launch_mode==1){
      pos=vec3.ahead_of_player(min_range,max_range);
    }

    int f=0;
    while(f<nr_fg){
      int nr_ships=random.randomint(min_nr_ships,max_nr_ships);
      object type=faction_ships.getRandomFighter(faction);

      //_io.sprintf(fgstring,"rnd%d",rndcounter);
      rndcounter=rndcounter+1;

      if(launch_mode==0){
	launch.launch_wave_around_area(fgstring,faction,type,"default",nr_ships,min_range,max_range,pos);
      }
      else if(launch_mode==1){
	launch.launch_wave_around_area(fgstring,faction,type,"default",nr_ships,min_range/10.0,max_range/10.0,pos);
      }

      f=f+1;
    }
  };

  void launchJPTravellers(object submap){
    object faction=_omap.get(submap,"faction");
    object type=_omap.get(submap,"type");
    int min_nr_fg=_omap.get(submap,"min_nr_fg");
    int max_nr_fg=_omap.get(submap,"max_nr_fg");
    int min_nr_ships=_omap.get(submap,"min_nr_ships");
    int max_nr_ships=_omap.get(submap,"max_nr_ships");
    float min_range=_omap.get(submap,"min_range");
    float max_range=_omap.get(submap,"max_range");
    int launch_mode=_omap.get(submap,"launch_mode");

    int nr_fg=random.randomint(min_nr_fg,max_nr_fg);

    object pos;
    if(launch_mode==0){
      pos=_unit.getPosition(player_unit);
    }
    else if(launch_mode==1){
      pos=vec3.ahead_of_player(min_range,max_range);
    }

    int f=0;
    while(f<nr_fg){
      int nr_ships=random.randomint(min_nr_ships,max_nr_ships);
      //   object type=faction_ships.getRandomFighter(faction);

      _io.sprintf(fgstring,"rndtrav%d",rndcounter);
      rndcounter=rndcounter+1;

      if(launch_mode==0){
	launch.launch_wave_around_area(fgstring,faction,type,"_ai_explorer",nr_ships,min_range,max_range,pos);
      }
      else if(launch_mode==1){
	launch.launch_wave_around_area(fgstring,faction,type,"_ai_explorer",nr_ships,min_range/10.0,max_range/10.0,pos);
      }

      f=f+1;
    }
  };

  float launch(int i){
    object submap=_olist.at(launch_list,i);

    int mode=_omap.get(submap,"mode");

    if(mode==0){
      launchFighters(submap);
    }
    else if(mode==1){
      launchConvoy(submap);
    }
    else if(mode==2){
      launchJPTravellers(submap);
    }

    float min_time=_omap.get(submap,"min_time");
    float max_time=_omap.get(submap,"max_time");

    float thentime=calc_thentime(min_time,max_time);
    //_io.printf("new thentime=%f\n",thentime);

    return thentime;

  };

  float calc_thentime(float min_time,float max_time){
     float waittime=random.random(min_time,max_time);
    float nowtime=_std.getGameTime();
    float thentime=waittime+nowtime;

    return thentime;
  };
}
