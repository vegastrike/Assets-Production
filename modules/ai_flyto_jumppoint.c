module ai_flyto_jumppoint {

  import vec3;
  import random;

  class object outstr;

  class object my_unit;
  class object my_order;

  class object last_head_order;
  class object last_move_order;

  // these are arguments
  class float fly_speed;
  class bool afterburner;
  class object jumppoint_unit;

  class bool _done;

  class object destpos;
  class float range;
  class float jumppoint_rsize;
  class object flyto_order;
  class object start_system;
  class object fgid;

  void initai(){
    _done=false;
    outstr=_string.new();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    fgid=_unit.getFgID(my_unit);

    start_system=_std.GetSystemName();

    destpos=_unit.getPosition(jumppoint_unit);

    jumppoint_rsize=_unit.getRSize(jumppoint_unit);
    range=jumppoint_rsize/2.0;

    flyto_order=_order.newFlyToWaypoint(destpos,fly_speed,afterburner,range);

    _order.enqueueOrder(my_order,flyto_order);
  };


  void executeai(){
   object this_system=_std.GetSystemName();

    if(!_string.equal(start_system,this_system)){
      // we have jumped
      _done=true;
      _io.printf("ai_flyto_jumppoint %s has jumped\n",fgid);
      return;
    }

    float dist=_unit.getMinDis(my_unit,destpos);

    object last_flyto=_order.findOrder(my_order,flyto_order);

    if(_std.isNull(last_flyto)){
      // the FlyToWaiypoint has exited
      _io.printf("reached waypoint1: %s dist=%f\n",fgid,dist);
      //      _unit.Jump(my_unit);
      flyto_order=_order.newFlyToWaypoint(destpos,fly_speed,afterburner,range);
      _order.enqueueOrder(my_order,flyto_order);
    }

    if(dist<jumppoint_rsize){
      _io.printf("reached waypoint2: %s dist=%f\n",fgid,dist);
      _unit.Jump(my_unit);
    }

   };

  void quitai(){
    _io.printf("ai_flyto_jumppoints1 quitting: %s\n",fgid);
    _string.delete(outstr);
  };

}
