module ai_stationary {

  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;

  void initai(){
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();
  };

  void executeai(){
  };

  void quitai(){
  };
}
