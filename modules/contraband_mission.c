module contraband_mission {
	import universe;
	object youcontainer;
	object jumpcontainer;
	object cargoname;
	int stage;
	int nr_waves;
	float dist;
	int nr_ships;
	int difficulty;
	float cred;
	import random;
	import launch;
	import faction_ships;
	object goodolist;
	object badolist;
	float badchance;
	int good_iterator;
	int bad_iterator;
	int sys_giterator;
	int sys_biterator;
	int bad_left;
	int all_left;
	int good_dest;

	void init (object cargo, float distance, float creds, int diff, int ships, float bad_pct) {
		faction_ships.init();
		nr_ships=ships;
		sys_giterator=0;
		sys_biterator=0;
		nr_waves=0;
		good_iterator=0;
		bad_iterator=0;
		good_dest=0;
		bad_left=0;
		badchance=bad_pct;
		all_left=ships;
		goodolist=_olist.new();
		badolist=_olist.new();
		stage=0;
		object jump=unit.getJumpPoint(random.randomint(0,50));
		jumpcontainer=_unit.getContainer(jump);
		difficulty=diff;
		if ((nr_ships<=0)||(bad_pct<=0.0)) {
			_std.terminateMission(false);
		}
		cred=creds;
		dist=distance;
		cargoname=cargo;
		object you=_unit.getPlayer();
		youcontainer=_unit.getContainer (you);
		if (_std.isNull(you)) {
			_std.terminateMission (false);
			return;
		}
		object str=_string.new();
		object name=(_unit.getName(you));
		_io.sprintf(str,"Good Day, %s. Your mission is as follows:",name);
		_io.message (1,"game","all",str);
		_io.sprintf(str,"We heard that there is a lot of %s cargo being",cargoname);
		_io.message (2,"game","all",str);
		name=(_unit.getName(jump));
		_io.sprintf(str,"transported illegally into the %s system.",name);
		_io.message (3,"game","all",str);
		_io.message (4,"game","all","Guard that jump point for the cargo and");
		_io.message (5,"game","all","destroy anyone with the cargo.  Destroying");
		_io.message (6,"game","all","fighters without this cargo is illegal");
		_io.message (7,"game","all","and could result in an enormus penalty.");
		_io.message (12,"game","all","It might take a little time to ensure");
		_io.sprintf (str,"that no %s cargo has left",cargoname);
		_io.message (13,"game","all",str);
		_io.message (14,"game","all","this system and to reward your account");
		_io.message (15,"game","all","with the credits.");
		_string.delete(str);
	};
	void Terminate (object you) {
		_olist.delete(goodolist);
		_olist.delete(badolist);
		if (_std.isNull(you)) {
			_std.terminateMission(false);
		}
		if ((bad_left==0)&&(good_dest==0)) {
			_io.message (0,"game","all","Excellent work pilot.");
			_io.message (0,"game","all","You have been rewarded for your effort as agreed.");
			_io.message (0,"game","all","Your contribution to the war effort will be remembered.");
			_unit.addCredits(you,cred);
			_std.terminateMission(true);
			return;
		} else {
			_io.message (0,"game","all","You did not follow through on your end of the deal.");

			if ((difficulty<1)&&((bad_left+good_dest)<nr_waves)) {
				_io.message (0,"game","all","Your pay will be reduced");
				_io.message (0,"game","all","And we will consider if we will accept you on future missions.");
				float addcred=cred-((bad_left+good_dest)/nr_waves);
				_unit.addCredits(you,addcred);
			} else {
				_io.message (0,"game","all","You will not be paid!");
				if (difficulty>=2) {
					_io.message (0,"game","all","And your idiocy will be punished.");
					_io.message (0,"game","all","You had better run for what little life you have left.");
					int i=0;
					object un;
					if ((bad_left+good_dest)>nr_waves) {
						difficulty=difficulty*((bad_left+good_dest)/nr_waves);
					}
					object faction;
					object youfaction=_unit.getFaction(you);
					object jump=_unit.getUnitFromContainer(jumpcontainer);
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
			_std.terminateMission(false);
			return;
		}
	};
	void loop () {
		object jump=_unit.getUnitFromContainer(jumpcontainer);
		object you=_unit.getUnitFromContainer(youcontainer);
		if (stage==1) {
			_std.ResetTimeCompression();
			object gunit=_unit.getUnit(sys_giterator);
			if (_std.isNull(gunit)) {  //a good ship left the system
				all_left=all_left-1;
			}
			object bunit=_unit.getUnit(sys_biterator);
			if (_std.isNull(bunit)) {  //a contraband ship left the system...
				all_left=all_left-1;
				Terminate(you);
			}
			object olistcont=_olist.at(goodolist,good_iterator);
			object olistun=_unit.getUnitFromContainer(olistcont);
			if ((_std.isNull(gunit))||  //resetting iterators for good ships
					(_std.equal(olistun,gunit))) {
				sys_giterator=0;
				good_iterator=good_iterator+1;
				if (good_iterator>=_olist.size(goodolist)) {
					good_iterator=0;
				}
				olistcont=_olist.at(goodolist,good_iterator);
				olistun=_unit.getUnitFromContainer(olistcont);
				if (_std.isNull(olistun)) {
					good_dest=good_dest+1;
					all_left=all_left-1;
					_olist.erase(goodolist,good_iterator);
				}
			}
			if ((_std.isNull(bunit))||  //resetting iterators for bad ships
					(_std.equal(olistun,bunit))) {
				sys_biterator=0;
				bad_iterator=bad_iterator+1;
				if (bad_iterator>=_olist.size(badolist)) {
					bad_iterator=0;
				}
				olistcont=_olist.at(badolist,bad_iterator);
				olistun=_unit.getUnitFromContainer(olistcont);
				if (_std.isNull(olistun)) {
					bad_left=bad_left-1;
					all_left=all_left+1;
					_olist.erase(badolist,bad_iterator);
				}
			}
			sys_giterator=sys_giterator+1;
			sys_biterator=sys_biterator+1;
			if (all_left==0) {
				Terminate(you);
			}
		} else if (stage==0) {
			if (_unit.getDistance(you,jump)<=dist) {
				_io.message (0,"game","all","DEBUG: creating enemies...");  //delete this after it works...
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
				while ((i<nr_ships)||(_olist.size(badolist)==0)||(_olist.size(goodolist)==0)) {
					cargonum=random.randomint(0,8);
					cargonum2=random.randomint(0,10-cargonum);
					notlist=faction_ships.getRandomFighter("merchant");
					newfighter=launch.launch_wave_around_unit("Base", "merchant",notlist,"default",1,_std.Rnd()*100000,jump);
					j=0;
					while (j<cargonum) {
						rndint=random.randomint(1,10);
						randcargo=_unit.getRandCargo(rndint);
						rndint=_unit.addCargo(newfighter,_olist.at(randcargo,0),_olist.at(randcargo,1),_olist.at(randcargo,2),_olist.at(randcargo,3),_olist.at(randcargo,4),_olist.at(randcargo,5));  //ADD CARGO HERE
						j=j+1;
					}
					if ((_std.Rnd())<badchance) {
						cargonum2=cargonum2-1;
						_olist.push_back(badolist,_unit.getContainer(newfighter));
						bad_left=bad_left+1;
						nr_waves=nr_waves+1;
						rndint=_unit.addCargo(newfighter,cargoname,"illegal",price,random.randomint(1,10),mass,volume);
					} else {
						_olist.push_back(goodolist,_unit.getContainer(newfighter));
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
			}
		}
	};
}
