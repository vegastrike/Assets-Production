module testd_int1 {

  int  im1;
  float fm1;

  int func(int i,float f){
    int t1=1+2;
    int t2=3*t1;
    int t3=t1+t2;

    _io.printf("t1=%d t2=%d t3=%d\n",t1,t2,t3);

    float f1=1.5+2.3;
    float f2=5.1*f1;
    float f3=f1+f2;

    _io.printf("f1=%f f2=%f f3=%f\n",f1,f2,f3);

    float m1=1.5*3;
    float m2=f1*t1;

    _io.printf("m1=%f m2=%f\n",m1,m2);

    float q1=_std.Float(4);
    int q2=_std.Int(4.7);

    _io.printf("q1=%f q2=%d\n",q1,q2);

    int w1=_std.Int(4*5.4);
    _io.printf("w1=%d\n",w1);

    return t3;
  };
 
  void loop(){

    float f=_std.Rnd();
    int i=_std.Int(_std.Rnd()*10.0);

    _io.printf("i=%d f=%f\n",i,f);

    int b=func(i,f);

    _io.printf("result=%d\n",b);

    
  };


}
