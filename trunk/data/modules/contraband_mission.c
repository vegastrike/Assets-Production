module contraband_mission {
	import random;
	import launch;
	import faction_ships;
	import universe;
	import starships_jumped_and_killed;
	import go_somewhere_significant;

	object youcontainer;
	object cargoname;
	int stage;
	int nr_waves;
	float dist;
	int nr_ships;
	int difficulty;
	float cred;
	object goodolist;
	object badolist;
	float badchance;

	void init (object cargo, int num_systems_away, float distance, float creds, int diff, int ships, float bad_pct) {
		object you=_unit.getPlayer();
		if (_std.isNull(you)) {
			_std.terminateMission (false);
			return;
		}
		faction_ships.init();

		nr_ships=ships;
		nr_waves=0;
		badchance=bad_pct;
		goodolist=_olist.new();
		badolist=_olist.new();
		stage=0;
		difficulty=diff;
		if ((nr_ships<=0)||(bad_pct<=0.0)) {
			_std.terminateMission(false);
		}
		cred=creds;
		dist=distance;
		cargoname=cargo;
		youcontainer=_unit.getContainer (you);
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
	void Terminate (object you) {

		_unit.deleteContainer(youcontainer);
		if (_std.isNull(you)||stage==0) {
			go_somewhere_significant.destroy();
			if (stage>0) {
			  starships_jumped_and_killed.destroy(badolist);
			  starships_jumped_and_killed.destroy(goodolist);
			}
			_std.terminateMission(false);
			return;
		}
		object jump=go_somewhere_significant.SignificantUnit();
	        int bad_left = starships_jumped_and_killed.ships_alive (badolist);
	        int good_dest = starships_jumped_and_killed.original_num_ships(goodolist) -
		                starships_jumped_and_killed.ships_alive (goodolist);
		if ((bad_left==0)&&(good_dest==0)) {
			_io.message (0,"game","all","Thank you for eliminating these smuggling contraband shippers.");
			if (random.random(0.0,1.0)<0.2) {
			  _io.message (0,"game","all","Enjoy your reward, and remember: don't drink and drive.");
			} if (random.random(0.0,1.0)<0.25) {
			  _io.message (0,"game","all","Drugs and contraband are bad.");
			  _io.message (0,"game","all","Here is your cash. Remember: Just say no.");
			}else {
			  _io.message (0,"game","all","These scum have deserved to eat dust for a long time.");
			  _io.message (0,"game","all","It is a pleasure to see such idiots go down without a fight!");
			}
			_unit.addCredits(you,cred);
			starships_jumped_and_killed.destroy(goodolist);
			starships_jumped_and_killed.destroy(badolist);
			go_somewhere_significant.destroy();
			_std.terminateMission(true);
			return;
		} else {
			_io.message (0,"game","all","How could you fail us.");

			if ((difficulty<1)&&((bad_left+good_dest)<nr_waves)) {
				_io.message (0,"game","all","We cannot compensate you for fouling up a critical job.");
				_io.message (0,"game","all","Be glad we even spared a dime.");
				float addcred=cred-((bad_left+good_dest)/nr_waves);
				_unit.addCredits(you,addcred);
			} else {
				_io.message (0,"game","all","Drug trafficker and fiend!");
				if (random.random(0.0,1.0)<0.2) {
				  _io.message (0,"game","all","You probably smoked half of the contraband shipped");
				}
				if (difficulty>=2) {
					_io.message (0,"game","all","You will pay for your smuggling crimes.");
					if (random.random(0.0,1.0)<0.5) {
					  _io.message (0,"game","all","Run MSF, Run.");//minimum spanning forest: see forest gump
					}
					int i=0;
					object un;
					if ((bad_left+good_dest)>nr_waves) {
						difficulty=difficulty*((bad_left+good_dest)/nr_waves);
					}
					object faction;
					object youfaction=_unit.getFaction(you);
					if (_std.isNull(jump)) {
						jump=you;
					}
					while (i<difficulty) {
						faction=faction_ships.intToFaction(random.randomint(0,2));
						while (!_string.equal(faction,youfaction)) {
							faction=faction_ships.intToFaction(random.randomint(0,2));
						}
						un=faction_ships.getRandomFighter(faction);
						object newunit=launch.launch_wave_around_unit("shadow", faction, un, "default", 1, 1000.0,jump);
						_unit.setTarget(newunit,you);
						i=i+1;
					}
				}
			}
			starships_jumped_and_killed.destroy(goodolist);
			starships_jumped_and_killed.destroy(badolist);
			go_somewhere_significant.destroy();
			_std.terminateMission(false);
			return;
		}
	};
	void loop () {
	  
		object you=_unit.getUnitFromContainer(youcontainer);

		if (stage==1) {
			_std.ResetTimeCompression();
			object jump=go_somewhere_significant.SignificantUnit();
			starships_jumped_and_killed.loop (badolist);
			starships_jumped_and_killed.loop (goodolist);
			if (starships_jumped_and_killed.ships_alive(badolist)!=
			    starships_jumped_and_killed.ships_in_system(badolist)) {  //a contraband ship left the system...
				Terminate(you);
				return;
			}
			int all_left = starships_jumped_and_killed.ships_alive(badolist)+starships_jumped_and_killed.ships_in_system(goodolist);
			if (all_left==0) {
				Terminate(you);
				return;
			}
		} else if (stage==0) {
			go_somewhere_significant.loop();
			if (go_somewhere_significant.HaveArrived()) {

				object jump = go_somewhere_significant.SignificantUnit();


				stage=1;
				int i=0;
				int j;
				int cargonum;
				int cargonum2;
				object notlist;
				object newfighter;
				object randcargo;
				float price=_std.Rnd()*50000;
				float mass=_std.Rnd();
				if (mass<=0.5) {
					mass=0.01;
				} else {
					mass=_std.Rnd()*10;
				}
				float volume=_std.Rnd();
				if (volume<=0.8) {
					volume=1.0;
				} else {
					volume=_std.Rnd()*100;
				}
				int rndint;
				object starships_bad =_olist.new();
				object starships_good =_olist.new();
				while ((i<nr_ships)||(_olist.size(starships_bad)==0)||(_olist.size(starships_good)==0)) {
					cargonum=random.randomint(0,8);
					cargonum2=random.randomint(0,10-cargonum);
					notlist=faction_ships.getRandomFighter("merchant");
					newfighter=launch.launch_wave_around_unit("Base", "merchant",notlist,"default",1,_std.Rnd()*100000,jump);
					_unit.setTarget(newfighter,jump);
					_unit.Jump(newfighter);
					j=0;
					while (j<cargonum) {
						rndint=random.randomint(1,10);
						randcargo=_unit.getRandCargo(rndint);
						rndint=_unit.addCargo(newfighter,_olist.at(randcargo,0),_olist.at(randcargo,1),_olist.at(randcargo,2),_olist.at(randcargo,3),_olist.at(randcargo,4),_olist.at(randcargo,5));  //ADD CARGO HERE
						j=j+1;
					}
					if ((_std.Rnd())<badchance) {
						cargonum2=cargonum2-1;
						_olist.push_back(starships_bad,_unit.getContainer(newfighter));
						nr_waves=nr_waves+1;
						rndint=_unit.addCargo(newfighter,cargoname,"illegal",price,random.randomint(1,10),mass,volume);
					} else {
						_olist.push_back(starships_good,_unit.getContainer(newfighter));
					}
					j=0;
					while (j<cargonum2) {
						rndint=random.randomint(1,10);
						randcargo=_unit.getRandCargo(rndint);
						rndint=_unit.addCargo(newfighter,_olist.at(randcargo,0),_olist.at(randcargo,1),_olist.at(randcargo,2),_olist.at(randcargo,3),_olist.at(randcargo,4),_olist.at(randcargo,5));  //ADD CARGO HERE
						j=j+1;
					}
					i=i+1;
				}
				starships_jumped_and_killed.init (goodolist,starships_good);
				starships_jumped_and_killed.init (badolist,starships_bad);
				PrintIntro (jump);
			}
		}
	};
	void PrintIntro (object jumppoint) {
	  object str = _string.new();
	  object jname = _unit.getName(jumppoint);
	  _io.sprintf (str,"Assure no %s cargo heading to the %s", cargoname,jname); 
	  _io.message (0,"game","all",str);
	  _io.message (1,"game","all","jump point leaves the system, and");
	  _io.message (2,"game","all","destroy anyone with said cargo.  Destroying");
	  _io.message (3,"game","all","fighters without this cargo is illegal");
	  _io.message (4,"game","all","and could result in an enormus penalty.");
	  _io.message (10,"game","all","It might take a little time to ensure");
	  _io.sprintf (str,"that no %s cargo has left",cargoname);
	  _io.message (11,"game","all",str);
	  _io.message (12,"game","all","that system and to reward your account");
	  _io.message (13,"game","all","with the credits.");
	  _string.delete (str);
	  _string.delete (jname);
	};

}
