module ai_switching1 {

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

  void randomMoveTo(){
    object player=_unit.getPlayer();
    object ppos=_unit.getPosition(player);
    
    float r1=500.0;
    float r2=2000.0;

    float x=9000.0;
    float y=3000.0;
    float z=0.0-5000.0;

    object myvec=vec3.new(x,y,z);
    object fgid=_unit.getFgId(my_unit);
    object outstr=_string.new();

    object pos=_unit.getPosition(my_unit);

    float x=_olist.at(pos,0);
    float y=_olist.at(pos,1);
    float z=_olist.at(pos,2);
    
    object new_order;
    _io.printf("mode=%d\n",mode);
    if(mode==0){
      new_order=_order.newMoveTo(myvec,true,1);
      _io.sprintf(outstr,"moving %s to  %f %f %f",fgid,x,y,z);
    }
    else{
      new_order=_order.newAggressiveAI("default.agg.xml","default.int.xml");
      _io.sprintf(outstr,"being aggressive");
    }
    _order.enqueueOrder(my_order,new_order);

    _io.message("game","all",outstr);

  };

  void initai(){
    rnd_num=_std.Rnd();

    wait_time=5.0;
    gametime=_std.getGameTime();
    _io.printf("ai init: rnd_num=%f  wait=%f\n",rnd_num,wait_time);
    did_it=false;
    mode=1;
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
      if(mode==1){
	mode=0;
      }
      else{
	mode=mode+1;
      }
      randomMoveTo();
      gametime=newgametime;
      //      did_it=true;
    }
    
  };

  void quitai(){
    _io.printf("ai quit: rnd_num=%f\n",rnd_num);
  };
}
