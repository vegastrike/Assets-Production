module ai_switching2 {

  import random;
  import vec3;

  class float rnd_num;
  class object dest_pos;
  class object my_order;
  class object my_unit;
  class float wait_time;
  class float gametime;
  class bool did_it;
  class int mode;
  class object last_order;
  class object outstr;

  object switchOrders(){
    float x=9000.0;
    float y=3000.0;
    float z=0.0-1000.0;

    object myvec=vec3.new(x,y,z);
    object fgid=_unit.getFgId(my_unit);
    
    object new_order;
    if(mode==0){
      new_order=_order.newMoveTo(myvec,true,1);
      _io.sprintf(outstr,"moving %s %f %f %f",fgid,x,y,z);
    }
    else{
      new_order=_order.newAggressiveAI("default.agg.xml","default.int.xml");
      _io.sprintf(outstr,"being aggressive");
    }
    _order.enqueueOrder(my_order,new_order);

    _io.message("game","all",outstr);

    return new_order;
  };

  void initai(){
    outstr=_string.new();
    wait_time=15.0;
    gametime=_std.getGameTime();
    _io.printf("ai init: rnd_num=%f  wait=%f\n",rnd_num,wait_time);
    did_it=false;
    mode=0;

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    last_order=switchOrders();
  };

  void executeai(){
    float newgametime=_std.getGameTime();
    if(mode==0){
      // we are moving
      // wait until we are there
      object lorder=_order.findOrder(my_order,last_order);

      if(_std.isNull(lorder)){
	// we have finished moving
	_io.sprintf(outstr,"last order is null");
	_io.message("game","all",outstr);

	mode=1;
	last_order=switchOrders();
	gametime=newgametime;
      }
    }
    else{
      //we are fighting

      // we are waiting waittime
      if((newgametime-gametime) > wait_time){
	object lorder=_order.findOrder(my_order,last_order);
	_order.eraseOrder(my_order,lorder);
	mode=0;
	last_order=switchOrders();
      }
    }
  };

  void quitai(){
    _io.printf("ai quit:\n");
  };
}
