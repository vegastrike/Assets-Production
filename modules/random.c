module random {

  float random(float r1,float r2){
    float r=_std.Rnd();

    float range=r2-r1;

    r=r*range;

    r=r1+r;

    _io.PrintFloats(:s1="random.random"; r1,r2,r);

    return r;
  };
}
