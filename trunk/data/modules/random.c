module random {

  float randomsign(){
    float r=_std.Rnd();
    
    if(r>0.5){
      return 1.0;
    }
    else{
      return (0.0-1.0);
    }
  };

  int randomint(int r1,int r2){
    float r=_std.Rnd();
    int range=r2-r1;
    range=range+1;

    r=r*range;
    
    int i=r1+_std.Int(r);
    
    return i;
  };

  float random(float r1,float r2){
    float r=_std.Rnd();
    float range=r2-r1;

    r=r*range;
    r=r1+r;

    //    _io.PrintFloats(:s1="random.random"; r1,r2,r);
    return r;
  };
}
