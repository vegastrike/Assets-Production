module ai_superiority {

  import vec3;
  import random;
  import unit;

  // arguments

  class object outstr;
  class object my_unit;
  class object my_order;

  class object agg_order;

  void initai(){
    outstr=_string.new();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    agg_order=_order.newAggressiveAI("default.agg.xml","default.int.xml");

    _order.enqueueOrder(my_order,agg_order);
  };

  void executeai(){
  };

  void quitai(){
  };

}
