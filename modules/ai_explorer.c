module ai_explorer {

  import universe;

  class object outstr;
  class float gametime;
  class object my_unit;
  class object my_order;

  class object jumppoint;
  class object flyto_order;
  class object current_system;
  class object fgid;

  void select_jumppoint(){
    jumppoint=universe.getRandomJumppoint();

    object jpname=_unit.getFgID(jumppoint);
    _io.printf("explorer %s flying to %s\n",fgid,jpname);

    flyto_order=_order.newFlyToJumppoint(jumppoint,1.0,true);
    _order.enqueueOrderFirst(my_order,flyto_order);

    current_system=_std.GetSystemName();
  };

  void initai(){
    outstr=_string.new();
    gametime=_std.getGameTime();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    fgid=_unit.getFgID(my_unit);

    select_jumppoint();
  };

  void executeai(){
    object new_system=_std.GetSystemName();
    if(!_string.equal(current_system,new_system)){
      // we have jumped
      _io.printf("explorer %s jumped from %s to %s\n",fgid,current_system,new_system);
      object last_flyto=_order.findOrder(my_order,flyto_order);

      if(!_std.isNull(last_flyto)){
	_order.eraseOrder(my_order,last_flyto);
      }

      select_jumppoint();

    }
    _string.delete(new_system);
  };

  void quitai(){
    //    _string.delete(fgid);
    //_string.delete(current_system);
  };
}
