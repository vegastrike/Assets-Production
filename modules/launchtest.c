module launchtest {
  // support for the _unit callback class

  float lasttime;

  void initgame(){
    lasttime=0.0;
  };

  void launch_test(){
    float time=_std.getGameTime();

    if((time-lasttime)>5.0){
      _unit.launch("omega","confed","ferret","default",6.0, 8000.0, 0.0-100.0, 200.0);
      _unit.launch("blabla","confed","rapier","default",6.0, 7800.0, 0.0-100.0, 200.0);
      _unit.launch("teta","aera","dagger","default",4.0 , 8000.0, 200.0, 0.0-500.0);
      _unit.launch("teta","aera","aeon","default",4.0 , 8200.0, 200.0, 0.0-500.0);
      lasttime=time;
    }
  };

  void print_unitlist(){
    return;

    float ship_nr=0.0;

    object unit=_unit.getUnit(ship_nr);;

    while(!_std.isNull(unit)){

      object pos=_unit.getPosition(unit);
      object fgid=_unit.getFgId(unit);

      float i=_olist.at(pos,0.0);
      float j=_olist.at(pos,1.0);
      float k=_olist.at(pos,2.0);

      _string.print(fgid);
      _io.PrintFloats(:s1=" Unit Nr, i,j,k "; ship_nr,i,j,k);

      object blah="bbl";

      _string.print(blah);

      //      _io.printf("fgid=%s  ship_nr=%f pos: %f %f %f\n",blah,ship_nr,i,j,k);

      ship_nr=ship_nr+1.0;
      unit=_unit.getUnit(ship_nr);
    }
  };

}
