module drone_duel {

  import unit;
  import vec3;
  import order;

  float gametime;
  float lasttime;
  int step;
  float last_step_time;
  float follow_time;

  void initgame(){
    step=0;
  };

  void gameloop(){

    //_io.printf("gameloop0\n");
    float newtime=_std.getGameTime();


    if(step==0){
      _io.message(0,"game","all","Something isn't right out here");
      _io.message(1,"game","all","in unexplored space.");
      step=step+1;
      gametime=newtime;
    }

    if((step==1)&&(newtime>(gametime+10))){
      _io.message(0,"game","all","I'm reading...something out here...");
      _io.message(1,"game","all","I'll check it out!");
    }


    gametime=newtime;
  };

  void endgame(){
  };
}
