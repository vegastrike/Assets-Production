module unit {
  // support for the _unit callback class

  float lasttime;

  void initgame(){
    lasttime=0.0;
  };

  void launch_test(){
    float time=_std.getGameTime();

    if((time-lasttime)>10.0){
      _unit.launch("omega","confed","hornet","default",4.0, 8000.0, 0.0-100.0, 100.0);
      _unit.launch("teta","aera","dagger","default",4.0 , 8000.0, 1000.0, 0.0-500.0);
      lasttime=time;
    }
  };

  object makeUnitList(){
    object unit_list=_olist.new();
    float ship_nr=0.0;
    object unit=_unit.getUnit(ship_nr);;

    while(!_std.isNull(unit)){
      _olist.push_back(unit_list,unit);
      
      ship_nr=ship_nr+1.0;
      unit=_unit.getUnit(ship_nr);
    }

    return unit_list;
  };

  void print_unitlist(){
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
