module launchtest {
  // support for the _unit callback class

  float lasttime;

  void initgame(){
    lasttime=0.0;
  };

  void launch_test(){
    float time=_std.getGameTime();

    if((time-lasttime)>5.0){
      _io.printf("launching new wave\n");
      object ret =_unit.launch("omega","confed","firefly","default",6, 8000.0, 0.0-100.0, 200.0);
      ret=_unit.launch("blabla","confed","tian","default",6, 7800.0, 0.0-100.0, 200.0);
      ret=_unit.launch("teta","aera","dagger","default",4 , 8000.0, 200.0, 0.0-500.0);
      ret=_unit.launch("teta","aera","aeon","default",4 , 8200.0, 200.0, 0.0-500.0);
      _io.printf("launch finished\n\n");
      lasttime=time;
    }
  };

}
