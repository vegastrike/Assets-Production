module cargo_mission {
	object faction;
	object destination;
	object basecontainer;
	object cargoname;
	bool arrived;
	int difficulty;
	float distfrombase;
	int quantity;
	float cred;
	import random;
	import launch;
	import faction_ships;
	void sys (object currentsystem, int sysaway) {
		if (sysaway<=0) {
			destination=currentsystem;
		} else {
			int max=_std.getNumAdjacentSystems(currentsystem);
			int nextsysnum=random.randomint(0,max);
			object nextsystem=_std.getAdjacentSystem(currentsystem,nextsysnum);
			sys(nextsystem,sysaway-1);
		}
	};

	void init (int factionname, int numsystemsaway, int cargoquantity, int missiondifficulty, float distance_from_base, float creds) {
		faction_ships.init();
		faction=faction_ships.intToFaction(factionname);
		arrived=false;
		cred=creds;
		distfrombase=distance_from_base;
		difficulty=missiondifficulty;
		object mysys=_std.getSystemFile();
		quantity=cargoquantity;
		object sysfile = _std.getSystemFile();
		sys(sysfile,numsystemsaway);
		object you=_unit.getPlayer();
		object list=_unit.getRandCargo(quantity);
		_unit.addCargo(you,_olist.at(list,0),_olist.at(list,1),_olist.at(list,2),_olist.at(list,3),_olist.at(list,4),_olist.at(list,5));  //ADD CARGO HERE
		_olist.delete(list);
		_io.printf("Go to system %s and give the",destination);
		_io.printf("starbase named, '%s'",basename);
		_io.printf("%d of the %s cargo",quantity,cargoname);
	};
	void loop () {
		if (arrived) {
			object base=_unit.getUnitFromContainer(basecontainer);
			object you=_unit.getPlayer();
			if (_std.isNull(base)||_std.isNull(you)) {
				_std.terminateMission(false);
				return;
			}
			float dist=_unit.getDistance(base,you);
			if (dist<=distfrombase) {
				int removenum=_unit.removeCargo(cargoname,quantity,true);
				if (removenum==quantity) {
					_unit.addCredits(cred);
					_std.terminateMission(true);
				} else {
					if (difficulty<1) {
						float addcred=(_std.Float(removenum)/_std.Float(quantity))*cred;
						_unit.addCredits(addcred);
					} else {
						if (difficulty>=2) {
							int i=0;
							object un;
							while (i<difficulty) {
								un=faction_ships.getRandomFighter(faction);
								un=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 1000,you);
								_unit.setTarget(un,you);
							}
						}
					}
					_std.terminateMission(false);
				}
				return;
			}
		} else {
			if (getSystemFile==destination) {
				arrived=true;
				object newship=faction_ships.getRandomCapitol(faction);
				int randint=random.randomInt(0,50);
				newship=launch.launch_wave_around_significant("Base",faction,newship,"default",1,5000,randint);
				basecontainer=_unit.getContainer(newship);
			}
		}
	};
}