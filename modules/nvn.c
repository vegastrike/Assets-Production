module nvn {
  import unit;
  import random;
  import faction_ships;
  import launch;
  import vec3;
  int begin;
  int numfriend;
  int numenemy;
  object my_faction (object stringi) {
    if (_string.equal (stringi,"aera")) {
      return faction_ships.aera();
    }
    if (_string.equal (stringi,"confed")) {
      return faction_ships.confed();
    }
    if (_string.equal (stringi,"unknown")) {
      return faction_ships.unknown();
    }
    if (_string.equal (stringi,"rlaan")) {
      return faction_ships.rlaan();
    }
    _io.printf("\nMODULE_ERROR: in function my_faction, stringi is not a faction name.\n");

    return faction_ships.confed();
  };
  object launch_new_ships(object stringi, int number, bool isequal){
    object faction_name;
    float side;
    int tmp=0;
    object ship_list;
    if (isequal) {
      faction_name=stringi;
      ship_list=my_faction(faction_name);
	  tmp=1;
	}
    while (tmp==0) {
      side=_std.Rnd();
      if ((side>0.66)&&!(_string.equal(stringi,"aera"))) {
        ship_list=faction_ships.aera();
        faction_name="aera";
        tmp=tmp+1;
      }else if ((side>0.33)&&!(_string.equal(stringi,"confed"))) {
        ship_list=faction_ships.confed();
         faction_name="confed";
         tmp=tmp+1;
      }else if (!(_string.equal(stringi,"rlaan"))){
        ship_list=faction_ships.rlaan();
        faction_name="rlaan";
        tmp=tmp+1;
      }
    }
    tmp=0;
    while (tmp<number) {
      object typename=faction_ships.getRandomShipType(ship_list);
      object player=_unit.getPlayer();
      object player_pos=_unit.getPosition(player);
      launch.launch_wave_around_area("fgname",faction_name,typename,"default",1,500.0,5000.0,player_pos);
      tmp=tmp+1;
    }
    return faction_name;
  };

  void initgame(int ours, int theirs){
    faction_ships.make_ships_list();
	begin=0;
	numfriend=ours;
	numenemy=theirs;
  };
  void loop(){
    if (begin==0) {
		_io.message(0,"game","all","use the '[' key to begin and");
		_io.message(1,"game","all","to switch control of your ships");
		_io.message(2,"game","all","or you can have fun flying");
		_io.message(3,"game","all","in a dumbfire ;)");
		begin=1;
	  	object player = _unit.getPlayer();
		object faction = _unit.getFaction(player);
		launch_new_ships(faction,numfriend,true);
	    launch_new_ships(faction,numenemy,false);
	}
  };
}
