module unit {
  // support for the _unit callback class

  void print_unitlist(){
    float ship_nr=0.0;

    while(ship_nr<5.0){
      object unit=_unit.getUnit(ship_nr);

      object pos=_unit.getPosition(unit);
      object fgid=_unit.getFgId(unit);

      float i=_olist.at(pos,0.0);
      float j=_olist.at(pos,1.0);
      float k=_olist.at(pos,2.0);

      _string.print(fgid);
      _io.PrintFloats(:s1=" Unit Nr, i,j,k "; ship_nr,i,j,k);
      ship_nr=ship_nr+1.0;
    }
  };

}
