module launch {

  import random;

  void launch_around_station(object station_name,object fgname,object faction,object type,object ai,int nr_ships,int nr_waves){
    object station_unit=unit.getUnitByFgID(station_name);
    object station_pos=_unit.getPosition(station_unit);

    float rsize=_unit.getRSize(station_unit);

    launch_waves_around_area(fgname,faction,type,ai,nr_ships,nr_waves,rsize,rsize*2.0,station_pos);
    _olist.delete(station_pos);
  };

  void launch_wave_around_area(object fgname,object faction,object type,object ai,int nr_ships,float r1,float r2,object pos){
    

    float x=_olist.at(pos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2)+(random.random(r1,r2)*random.randomsign());

    // _io.printf("launching %d ships type=%s faction=%s around area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _unit.launch(fgname,faction,type,ai,nr_ships,1,x,y,z);
  };
  void launch_waves_around_area(object fgname,object faction,object type,object ai,int nr_ships,int nr_waves,float r1,float r2,object pos){
    

    float x=_olist.at(pos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2)+(random.random(r1,r2)*random.randomsign());

    // _io.printf("launching %d ships type=%s faction=%s around area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _unit.launch(fgname,faction,type,ai,nr_ships,nr_waves,x,y,z);
  };


  void launch_wave_in_area(object fgname,object faction,object type,object ai,int nr_ships,float radius,object pos){

    float x=_olist.at(pos,0)+random.random((0.0-radius)/2.0,radius/2.0);
    float y=_olist.at(pos,1)+random.random((0.0-radius)/2.0,radius/2.0);
    float z=_olist.at(pos,2)+random.random((0.0-radius)/2.0,radius/2.0);

    //    _io.printf("launching %d ships type=%s faction=%s in area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _unit.launch(fgname,faction,type,ai,nr_ships,1,x,y,z);
  };

  void launch_waves_in_area(object fgname,object faction,object type,object ai,int nr_ships,int nr_waves,float radius,object pos){

    float x=_olist.at(pos,0)+random.random((0.0-radius)/2.0,radius/2.0);
    float y=_olist.at(pos,1)+random.random((0.0-radius)/2.0,radius/2.0);
    float z=_olist.at(pos,2)+random.random((0.0-radius)/2.0,radius/2.0);

    //    _io.printf("launching %d ships type=%s faction=%s in area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _unit.launch(fgname,faction,type,ai,nr_ships,nr_waves,x,y,z);
  };

  void launchShipsAtWaypoints(object waypoints,object faction,object type,object ainame,int nr){
    int i=0;
    object outstr=_string.new();

    while(i<_olist.size(waypoints)){
      _io.sprintf(outstr,"wp%d",i);

      object wp=_olist.at(waypoints,i);
      float x=_olist.at(wp,0);
      float y=_olist.at(wp,1);
      float z=_olist.at(wp,2);

      _unit.launch(outstr,faction,type,ainame,nr,1,x,y,z);
      i=i+1;
    }
  };


}
