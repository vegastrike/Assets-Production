module ai_test {

  import random;

  class float rnd_num;
  class object dest_pos;
  class object my_order;
  class object my_unit;
  class float wait_time;
  class float gametime;

  void randomMoveTo(){
    object player=_unit.getPlayer();
    object ppos=_unit.getPosition(player);
    
    float r1=500.0;
    float r2=2000.0;

    float x=_olist.at(ppos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(ppos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(ppos,2)+(random.random(r1,r2)*random.randomsign());

    object myvec=vec3.new(x,y,z);

    _io.printf("moving to random %f %f %f\n",x,y,z);

    object pos=_unit.getPosition(my_unit);

    float x=_olist.at(pos,0);
    float y=_olist.at(pos,1);
    float z=_olist.at(pos,2);

    object fgid=_unit.getFgId(my_unit);

    _io.printf("pos: %f %f %f fgid=%s\n",x,y,x,fgid);

    object new_order=_order.newMoveTo(myvec,true,1);

    _order.print(my_order);
    _order.print(new_order);

    _order.enqueueOrder(my_order,new_order);
  };

  void aggrAI(){
    object order=_order.newAggressiveAI("default","default");
  };

  void moveTo(object target_pos,bool afterburn, int nr_switchbacks){
    object order=_order.newMoveTo(target_pos,afterburn,nr_switchbacks);
  };

  void initai(){
    rnd_num=_std.Rnd();

    wait_time=random.random(5.0,20.0);
    gametime=_std.getGameTime();
    _io.printf("ai init: rnd_num=%f  wait=%f\n",rnd_num,wait_time);
  };

  void executeai(){
    //_io.printf("ai execute: rnd_num=%f\n",rnd_num);

    my_unit=_std.getCurrentAIUnit();
    my_order=_unit.getOrder(my_unit);

    float newgametime=_std.getGameTime();
    if((newgametime-gametime) > wait_time){
      randomMoveTo();
      gametime=newgametime;
    }
    
  };

  void quitai(){
    _io.printf("ai quit: rnd_num=%f\n",rnd_num);
  };
}
