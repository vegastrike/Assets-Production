module gauntlet {
  import unit;
  import random;
  import faction_ships;
  import launch;
  import vec3;
  import nvn;
  int waittime;
  int begin;
  int numfriend;
  int numenemy;
  void initgame(int ours, int theirs){
    nvn.initgame(ours,theirs);
    begin=0;
    waittime=101;
    numfriend=ours;
    numenemy=theirs;
  };
  void loop(){
    if (begin==0) {
      object player = _unit.getPlayer();
      if (!_std.isNull(player)) {
	object faction = _unit.getFaction(player);
	object badunit= unit.getNearestEnemy(player,50000.0);
	if (_std.isNull(badunit)) {
	  nvn.reset_loop (numfriend,numenemy);
	  nvn.loop();
	  _io.message(0,"game","all","use the '[' key to begin and");
	  _io.message(1,"game","all","to switch control of your ships");
	  _io.message(2,"game","all","New Round...");
	  _io.message(3,"game","all","FIGHT!");
	  if (waittime==101) {
	    numfriend=numfriend-1;//do not count 'you'
	    waittime=100;
	  }
	}
      }
    }
    begin=begin+1;
    if (begin>waittime) {
      begin=0;
    }
  };
}
