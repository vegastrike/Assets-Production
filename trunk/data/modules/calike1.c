module calike1 {
  globals {
    float gf1;
    float gf2;
    bool gb1;
    object go1;
  };

  //import common;

  void loop(){
    float counter;
    counter=0.0;

    while(counter<20.0){
      float r;
      r=_std.Rnd();

      _io.PrintFloats(:s1="rnd is ";:s2=" end"; r);
      
      counter=counter+1.0;
    };

    _io.PrintFloats(:s1="end of loop";);
  };

}
