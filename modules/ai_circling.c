module ai_circling {

  class int aistyle;
  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;

  void initai(){
    aistyle=1;
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();
  };

  void executeai(){
    _order.SteerUp(my_order,0.3);
    _order.SteerAccel(my_order,1.0);
  };

  void quitai(){
  };
}
