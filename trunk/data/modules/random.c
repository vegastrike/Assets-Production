module random {

  float randomsign(){
    float r=_std.Rnd();
    
    if(r>5.0){
      return 1.0;
    }
    else{
      return (0.0-1.0);
    }
  };

  float random(float r1,float r2){
    float r=_std.Rnd();

    float range=r2-r1;

    r=r*range;

    r=r1+r;

    _io.PrintFloats(:s1="random.random"; r1,r2,r);

    return r;
  };
}
