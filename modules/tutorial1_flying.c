module tutorial1_flying {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import waypoints1;
  import order;
  import ai_superiority;
  import ai_patrol;

  float gametime;
  bool did_it;
  object outstr;

  object player_unit;
  object teacher_unit;
  object teacher_fgid;
  object cruiser_fgid;

  int step;
  float last_step_time;
  float follow_time;

  void initgame(){
    gametime=_std.getGameTime();
    last_step_time=gametime;

    outstr=_string.new();

    player_unit=_unit.getPlayer();

    teacher_unit=unit.getUnitByFgID("teacher-0");

    step=0;
    teacher_fgid="teacher-0";
    cruiser_fgid="silver-0";

    _io.printf("init done\n");
  };

  void gameloop(){

    //_io.printf("gameloop0\n");
    float newtime=_std.getGameTime();
    player_unit=_unit.getPlayer();
    float angle=_unit.getAngle(player_unit,teacher_unit);

    object teacher_pos=_unit.getPosition(teacher_unit);
    float dist=_unit.getMinDis(player_unit,teacher_pos);

    object players_target=_unit.getTarget(player_unit);
    object target_fgid="none";

    //_io.printf("gameloop1\n");
    if(_std.isNull(players_target)){
      _io.printf("player has no target\n");
    }
    else{
      target_fgid=_unit.getFgID(players_target);
    }
    

    //_io.printf("angle to teacher: %f dist=%f\n",angle,dist);

    if(step==0){
      _io.message(0,"game","all","Welcome to the flying tutorial");
      _io.message(2,"game","all","you will now learn how to fly and steer your ship");
      _io.message(4,"game","all","you have to do exactly what your teacher tells you");
      _io.message(5,"game","all","leave your hands off the control unless you're told so");
      _io.message(7,"game","all","your first task is to target your teachers ship");
      _io.message(8,"game","all","your teachers ship is in front of you");
      _io.message(9,"game","all","use your cursor-keys or the joystick");
      _io.message(9,"game","all","to get the teachers ship in the center of your display");

      step=step+1;
    }

    if(step==1){
      if(angle<3.0){
	_io.message(0,"game","all","Fine! You have centered your ship on the teacher");
	_io.message(1,"game","all","now press [p] to pick your teachers ship as a target");
	_io.message(2,"game","all","you can see that you have targeted the teacher");
	_io.message(3,"game","all","when there's a purple box around the ship");

	step=step+1;
      }
    }

    if(step==2){
      if( _string.equal(teacher_fgid,target_fgid) ){
	_io.message(0,"game","all","Fine again! You have now targetted the teacher");
	_io.message(1,"game","all","you can also see that you've targetted the teacher");
	_io.message(2,"game","all","by having a look at your radar");
	_io.message(3,"game","all","your target is painted as a purple blip");
	_io.message(6,"game","all","now your job is to face the cruiser");
	_io.message(7,"game","all","steer your ship until you face the cruiser");
	_io.message(8,"game","all","and press [p] again to target it");

	step=step+1;
      }
    }

    if(step==3){
      object cruiser_unit=unit.getUnitByFgID("silver-0");
      float cruiser_angle=_unit.getAngle(player_unit,cruiser_unit);

      if((cruiser_angle<10.0) && (_string.equal(cruiser_fgid,target_fgid))){
	_io.message(0,"game","all","you have now targeted the cruiser");
	_io.message(1,"game","all","now again turn to face your teacher");
	_io.message(2,"game","all","and target him again");
	
	step=step+1;
      }
    }

    //_io.printf("step=%d\n",step);
    if(step==4){
      //_io.printf("checking step 4\n");
      if(  _string.equal(teacher_fgid,target_fgid) && (angle<5.0)){
	_io.message(0,"game","all","ok - now your teacher will fly around");
	_io.message(1,"game","all","follow your teachers ship");
	_io.message(2,"game","all","keep your teacher in the center");
	_io.message(2,"game","all","and try to keep a distance of 30-100");

	order.patrolFg(0,"teacher-0","none",300.0,0.2);
	step=step+1;
	last_step_time=gametime;
	follow_time=0.0;
      }

    }

    if(step==5){
      if(( angle<20.0) && ((dist>30.0) && (dist<100.0))){
	// we follow correctly
	if(follow_time>20.0){
	  _io.message(0,"game","all","ok - you're fine following the teacher");

	  step=step+1;
	}
	else{
	  follow_time=follow_time+(newtime-gametime);
	}
      }
      else{
	_io.printf("resetting following time\n");
	follow_time=0.0;
      }
    }
    _olist.delete(teacher_pos);

    gametime=newtime;
  };

  void endgame(){
  };
}
