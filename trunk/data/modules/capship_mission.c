module capship_mission {
	import go_somewhere_significant;
	import launch;
	object youcontainer;
	object capshipcontainer;
	int stage;
	float time;
	int protectors;
	void init (int numprotectors, float betweentime) {
		object you=_unit.getPlayer();
		if (_std.isNull(you)) {
			_std.terminateMission (false);
			return;
		}
		stage=0;
		time=betweentime;
		protectors=numprotectors;
		object str=_string.new();
		object name=(_unit.getName(you));
		_io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
		_string.delete(name);
		go_somewhere_significant.init(you,num_systems_away,false,true,distance);
		_io.message (1,"game","all",str);
		_io.sprintf(str,"We heard that there is a lot of %s cargo being",cargoname);
		_io.message (2,"game","all",str);
		name=(go_somewhere_significant.DestinationSystem());
		_io.sprintf(str,"transported illegally out of the %s system.",name);
		_io.message (3,"game","all",str);
		_string.delete(str);
	};
	void terminate () {
		go_somewhere_significant.destroy();
		_std.terminateMission(true);
		return;
		//
	};
	void loop () {
		if (stage==1) {
			//
		} else if (stage==0) {
			go_somewhere_significant.loop();
			if (go_somewhere_significant.HaveArrived()) {
				//
			}
		}
	};
}