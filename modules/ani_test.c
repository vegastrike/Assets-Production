module ani_test {
  import random;
  float x;
  float y;
  float z;
  float s;
  void init (float xx, float yy, float zz, float si) {
    x = xx;
    y=yy;
    z=zz;
    s = si;
  };
  void loopdie () {
    float xx = x + (random.random(((0.0-1.0)*s),s)*random.randomsign()); 
    float yy = y + (random.random(((0.0-1.0)*s),s)*random.randomsign()); 
    float zz = z + (random.random(((0.0-1.0)*s),s)*random.randomsign()); 
    _std.playAnimation ("warp.ani",xx,yy,zz,500.0);
  };
  void loop() {
    loopdie();
    loopdie();    loopdie();    
  };
}
