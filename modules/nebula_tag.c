module nebula_tag {
	import random;
	import faction_ships;
	import launch;
	import vec3;
	float lasttime;
	float waittime;

	void launch_new_ships(){
		float side=_std.Rnd();
		object ship_list;
		object faction_name;
		int nr_ships=random.randomint(1,1);
		if (side>=0.5) {
			ship_list=faction_ships.aera();
			faction_name="rlaan";
		}else {
			ship_list=faction_ships.confed();
			faction_name="confed";
		}
		object typename=faction_ships.getRandomShipType(ship_list);
		object player=_unit.getPlayer();
		object player_pos=_unit.getPosition(player);
		launch.launch_wave_around_area("fgname",faction_name,typename,"default",nr_ships,4000.0,4000.0,player_pos);
	};

	void initgame(){
		int i=0;
		lasttime=0.0;
		waittime=random.random(50.0,130.0);
		faction_ships.make_ships_list();
		while(i<3) {
			launch_new_ships();
			i=i+1;
		}
	};

	void loop(){
		float time=_std.getGameTime();
		if((time-lasttime)>waittime){
			waittime=random.random(50.0,130.0);
			launch_new_ships();
//			waittime=waittime*(_std.Rnd()*0.2+1.0);
			lasttime=time;
		}
	};
}
