module waypoints1 {

  import ai_stationary;

  object waypoints;
  object outstr;

  object getWaypoints(){
    return waypoints;
  };

  void initWaypoints(){
        waypoints=_olist.new();
    object wp0=vec3.new(8000.0,500.0,500.0);
    object wp1=vec3.new(8000.0,500.0,0.0-500.0);
    object wp2=vec3.new(8000.0,0.0-500.0,0.0-500.0);
    object wp3=vec3.new(8000.0,0.0-500.0,500.0);
    object wp4=vec3.new(9000.0,0.0,0.0);

    _olist.push_back(waypoints,wp0);
    _olist.push_back(waypoints,wp2);
    _olist.push_back(waypoints,wp1);
    _olist.push_back(waypoints,wp4);
    _olist.push_back(waypoints,wp3);

    launchShipsAtWaypoints();
  };

  void launchShipsAtWaypoints(){
    int i=0;
    
    while(i<_olist.size(waypoints)){
      _io.sprintf(outstr,"wp%d",i);

      object wp=_olist.at(waypoints,i);
      float x=_olist.at(wp,0);
      float y=_olist.at(wp,1);
      float z=_olist.at(wp,2);

      _unit.launch(outstr,"neutral","dagger","_ai_stationary",1,1,x,y,z);
      i=i+1;
    }
  };

  void initgame(){
    outstr=_string.new();
    _io.printf("waypoints1\n");
    initWaypoints();
  };

  void gameloop(){
  };
}
