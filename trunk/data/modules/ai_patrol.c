module ai_patrol {

  import vec3;
  import random;
  import unit;

  // arguments
  class object area;
  class float range;
  class int patrol_mode;
  class object around_unit;
  class float patrol_speed;

  class object waypoint;
  class object last_order;
  class int waypoint_index;

  class object outstr;
  class object my_unit;
  class object my_order;
  class object my_fgid;

  object calcNextWaypoint(object upos){
      float x=_olist.at(upos,0);
      float y=_olist.at(upos,1);
      float z=_olist.at(upos,2);

      if(waypoint_index>5){
	waypoint_index=0;
      }

      if(waypoint_index==0){
	y=y+range;
      }
      else if(waypoint_index==1){
	x=x+range;
      }
      else if(waypoint_index==2){
	y=y-range;
      }
      else if(waypoint_index==3){
	x=x-range;
      }
      else if(waypoint_index==4){
	z=z+range;
      }
      else if(waypoint_index==5){
	z=z-range;
      }
      
      waypoint_index=waypoint_index+1;

      return vec3.new(x,y,z);
  };

  void patrolToWaypoint(){
    //    _io.printf("patrol_speed=%f\n",patrol_speed);
    object new_order=_order.newFlyToWaypoint(waypoint,patrol_speed,false,100.0);

    _order.enqueueOrder(my_order,new_order);

    last_order=new_order;
  };

  void getNextWaypoint(){
    if(patrol_mode==0){
      // random waypoints around area
      waypoint=vec3.random_around_area(area,range-(range/0.3),range);
    }
    else if(patrol_mode==1){
      // waypoints around unit
      object upos=_unit.getPosition(around_unit);

      waypoint=calcNextWaypoint(upos);
      
      _olist.delete(upos);
    }
  };

  void initai(){
    outstr=_string.new();

    my_unit=_std.getCurrentAIUnit();
    my_order=_std.getCurrentAIOrder();

    my_fgid=_unit.getFgID(my_unit);
    _io.printf("Patrolling ai: %s\n",my_fgid);
    //vec3.print(area);
    //_io.printf("\n");

    waypoint_index=random.randomint(0,5);

    getNextWaypoint();
    patrolToWaypoint();
  };

  void executeai(){
    object check_order=_order.findOrder(my_order,last_order);

    if(_std.isNull(check_order)){
      //      _io.printf("next waypoint\n");
      _olist.delete(waypoint);
      getNextWaypoint();
      patrolToWaypoint();
    }
  };

  void quitai(){
    _io.printf("%s: patrolling ai quitting\n",my_fgid);
    //    _string.delete(outstr);
  };

}
