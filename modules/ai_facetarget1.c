module ai_facetarget1 {

  import vec3;
  import random;

  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;
  class object last_order;

  object newOrder(){
    object new_order;
    object new_order2;

    object npos=vec3.random_around_player(200.0,1000.0);


    //  new_order=_order.newMatchLinearVelocity(npos,false,false,true);
        new_order=_order.newFaceTarget(true,true,3);
	//        new_order=_order.newChangeHeading(npos,3);

    object forward=vec3.new(0.0,0.0,1.0);

    //    new_order=_order.newMatchVelocity(forward,npos,false,false,true);

    _order.enqueueOrder(my_order,new_order);
    //    _order.enqueueOrder(my_order,new_order2);

    _io.sprintf(outstr,"ChangeHeading to %f %f %f",_olist.at(npos,0),_olist.at(npos,1),_olist.at(npos,2));
    _io.message("game","all",outstr);

    return new_order;
  };

  void initai(){
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    object player_unit=_unit.getPlayer();
    _unit.setTarget(my_unit,player_unit);

    last_order=newOrder();

  };

  void executeai(){
    object lorder=_order.findOrder(my_order,last_order);
    if(_std.isNull(lorder)){
      // the current order has exited
      last_order=newOrder();
    }
  };

  void quitai(){
  };

}
