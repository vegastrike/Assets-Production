module launch {

  import random;

  void launch_wave_in_area(object fgname,object faction,object type,object ai,float nr_ships,float radius,object pos){
    

    float x=_olist.at(pos,0.0)+random.random(0.0,radius);
    float y=_olist.at(pos,1.0)+random.random(0.0,radius);
    float z=_olist.at(pos,2.0)+random.random(0.0,radius);

    _io.PrintFloats(:s1="launching at area x,y,z,nr_ships"; x,y,z,nr_ships);
    _string.print(faction);
    _string.print(type);

    _unit.launch(fgname,faction,type,ai,nr_ships,x,y,z);
  };
}
