module launch {

  import random;
  import unit;

  bool launch_around_station(object station_name,object fgname,object faction,object type,object ai,int nr_ships,int nr_waves){
    object station_unit=unit.getUnitByFgID(station_name);
    if(_std.isNull(station_unit)){
      _io.printf("launch.c:launch_around_station did not find unit %s\n",station_name);
      return false;
    }
    object station_pos=_unit.getPosition(station_unit);

    float rsize=_unit.getRSize(station_unit);

    object launched =launch_waves_around_area(fgname,faction,type,ai,nr_ships,nr_waves,rsize,rsize*2.0,station_pos);
    _olist.delete(station_pos);

    return true;
  };

  bool launch_around_unit(object station_name,object fgname,object faction,object type,object ai,int nr_ships,int nr_waves){
    return launch_around_station(station_name,fgname,faction,type,ai,nr_ships,nr_waves);
  };

  object launch_waves_around_area(object fgname,object faction,object type,object ai,int nr_ships,int nr_waves,float r1,float r2,object pos){
    float x=_olist.at(pos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2)+(random.random(r1,r2)*random.randomsign());

    // _io.printf("launching %d ships type=%s faction=%s around area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);
    return _unit.launch(fgname,faction,type,ai,nr_ships,nr_waves,x,y,z);
  };
  object launch_wave_around_area(object fgname,object faction,object type,object ai,int nr_ships,float r1,float r2,object pos){
    return launch_waves_around_area (fgname,faction,type,ai,nr_ships,1,r1,r2,pos);
    //    return launched;
  };



  void launch_waves_in_area(object fgname,object faction,object type,object ai,int nr_ships,int nr_waves,float radius,object pos){

    float x=_olist.at(pos,0)+random.random((0.0-radius)/2.0,radius/2.0);
    float y=_olist.at(pos,1)+random.random((0.0-radius)/2.0,radius/2.0);
    float z=_olist.at(pos,2)+random.random((0.0-radius)/2.0,radius/2.0);
    object un = _unit.launch(fgname,faction,type,ai,nr_ships,nr_waves,x,y,z);
  };
  void launch_wave_in_area(object fgname,object faction,object type,object ai,int nr_ships,float radius,object pos){
    launch_waves_in_area(fgname,faction,type,ai,nr_ships,1,radius,pos);
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

      object leader =_unit.launch(outstr,faction,type,ainame,nr,1,x,y,z);
      i=i+1;
    }
  };
  object launch_wave_around_unit (object fgname, object faction, object type, object ai, int nr_ships, float radius, object my_unit) {
    object myvec;
    if (_std.isNull(my_unit)) {
      myvec = _olist.new();
      _olist.push_back(myvec,0);
      _olist.push_back(myvec,0);
      _olist.push_back(myvec,0);
      object un=launch_wave_around_area (fgname,faction,type,ai,nr_ships,0.0,radius,myvec);
      _olist.delete(myvec);
      return un;
    }
    myvec=_unit.getPosition(my_unit);
    float rsiz=_unit.getRSize(my_unit)*2;
    radius = rsiz+radius;
    object un=launch_wave_around_area (fgname,faction,type,ai,nr_ships,rsiz,radius,myvec);
    return un;
  };
  object launch_wave_around_significant (object fgname,object faction,object type,object ai,int nr_ships,float radius,int significant_number) {
    object significant_unit=unit.getSignificant(significant_number,false);
    if (_std.isNull(significant_unit)) {
      significant_unit = _unit.getPlayer();
    }
    object launched = launch_wave_around_unit(fgname,faction,type,ai,nr_ships,radius,significant_unit);
    return launched;
 };

}
