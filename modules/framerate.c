module framerate {

  float gametime;
  float elapsed;
  float framerate;

  void initgame(){
    gametime=0.0;
  };

  void calcFrameRate(){
    float new_gametime;
    new_gametime=_std.getGameTime();

    elapsed=new_gametime-gametime;
    gametime=new_gametime;
    framerate=1.0/elapsed;

    _io.PrintFloats(:s1="gametime,elapsed,framerate : "; gametime,elapsed,framerate);

  };
}
