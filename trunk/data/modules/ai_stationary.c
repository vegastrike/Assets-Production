module ai_stationary {
  import vec3;
  class object my_order;

  void initai(){
    object forward=vec3.new(0.0,0.0,0.0);
    my_order=_std.getCurrentAIOrder();
    _order.enqueueOrder(my_order,_order.newMatchLinearVelocity(forward,true,false,false));
    _olist.delete(forward);
  };

  void executeai(){
  };

  void quitai(){
  };
}
