module waypoints {

  import ai_stationary;

  object outstr;

  void launchShipsAtWaypoints(waypoints,object faction,object type,object ainame,int nr){
    int i=0;
    
    while(i<_olist.size(waypoints)){
      _io.sprintf(outstr,"wp%d",i);

      object wp=_olist.at(waypoints,i);
      float x=_olist.at(wp,0);
      float y=_olist.at(wp,1);
      float z=_olist.at(wp,2);

      object launched =_unit.launch(outstr,"neutral","dagger","_ai_stationary",1,x,y,z);
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
