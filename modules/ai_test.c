module ai_test {

  class float rnd_num;

  void initai(){
    rnd_num=_std.Rnd();

    _io.printf("ai init: rnd_num=%f\n",rnd_num);
  };

  void executeai(){
    _io.printf("ai execute: rnd_num=%f\n",rnd_num);
  };

  void quitai(){
    _io.printf("ai quit: rnd_num=%f\n",rnd_num);
  };
}
