module ai_test2 {

  // demonstrates the bug/feature in Orders::MoveTo
  import random;
  import vec3;

  class float rnd_num;
  class object dest_pos;
  class object my_order;
  class object my_unit;
  class float wait_time;
  class float gametime;
  class bool did_it;

  void randomMoveTo(){
    float x=9000.0;
    float y=2000.0;
    float z=100.0; // set z to values >1000.0 to see the bug

    object myvec=vec3.new(x,y,z);
    object fgid=_unit.getFgId(my_unit);
    object outstr=_string.new();

    _io.printf("moving %s to random %f %f %f\n",fgid,x,y,z);
    _io.sprintf(outstr,"moving %s to %f %f %f",fgid,x,y,z);
    _io.message("game","all",outstr);

    object new_order=_order.newMoveTo(myvec,true,1);

    _order.enqueueOrder(my_order,new_order);
  };

  void initai(){
    rnd_num=_std.Rnd();

    wait_time=10.0;
    gametime=_std.getGameTime();
    _io.printf("ai init: rnd_num=%f  wait=%f\n",rnd_num,wait_time);
    did_it=false;
  };

  void executeai(){
    //_io.printf("ai execute: rnd_num=%f\n",rnd_num);
    if(did_it){
      return;
    }
    my_unit=_std.getCurrentAIUnit();
    //my_order=_unit.getOrder(my_unit);
    my_order=_std.getCurrentAIOrder();

    float newgametime=_std.getGameTime();
    if((newgametime-gametime) > wait_time){
      randomMoveTo();
      gametime=newgametime;
      did_it=true;
    }
    
  };

  void quitai(){
    _io.printf("ai quit: rnd_num=%f\n",rnd_num);
  };
}
