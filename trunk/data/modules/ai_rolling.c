module ai_rolling {

  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;
  class int aistyle;

  void initai(){
    aistyle=1;
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();
  };

  void executeai(){
    _order.SteerRollRight(my_order,1.0);
  };

  void quitai(){
  };
}
