module launch {

  import random;

  void launch_wave_around_area(object fgname,object faction,object type,object ai,float nr_ships,float r1,float r2,object pos){
    

    float x=_olist.at(pos,0.0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1.0)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2.0)+(random.random(r1,r2)*random.randomsign());
    //    float y=_olist.at(pos,1.0)+random.random(0.0,radius);
    //float z=_olist.at(pos,2.0)+random.random(0.0,radius);

    _io.PrintFloats(:s1="launching around area x,y,z,nr_ships"; x,y,z,nr_ships);
    _string.print(faction);
    _string.print(type);

    _unit.launch(fgname,faction,type,ai,nr_ships,x,y,z);
  };


  void launch_wave_in_area(object fgname,object faction,object type,object ai,float nr_ships,float radius,object pos){
    

    float x=_olist.at(pos,0.0)+random.random((0.0-radius)/2.0,radius/2.0);
    float y=_olist.at(pos,1.0)+random.random((0.0-radius)/2.0,radius/2.0);
    float z=_olist.at(pos,2.0)+random.random((0.0-radius)/2.0,radius/2.0);
    //    float y=_olist.at(pos,1.0)+random.random(0.0,radius);
    //float z=_olist.at(pos,2.0)+random.random(0.0,radius);

    _io.PrintFloats(:s1="launching at area x,y,z,nr_ships"; x,y,z,nr_ships);
    _string.print(faction);
    _string.print(type);

    _io.message("game","all","launching new wave of fighters:");
    _io.message("game","all",type);

    _unit.launch(fgname,faction,type,ai,nr_ships,x,y,z);
  };
}
