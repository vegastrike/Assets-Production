module faction_ships {
  import random;
  import ship_upgrades;
  object capitols;
  object fighters;
  object unknown_ships;
  object factions;
  object enemies;
  object friendlies;
  object confed(){
    object cf = _olist.at (fighters,0);
    return cf;
  };
  object unknown(){
    return unknown_ships;
  };
  object aera(){
    object ae = _olist.at (fighters,1);
    return ae;
  };
  object rlaan(){
    object rl = _olist.at (fighters,2);
    return rl;
  };
  object intToFaction(int fac) {
    if (fac>(_olist.size (factions))) {
      return "unknown";
    }
    object ret = _olist.at (factions,fac);
    return ret;
  };
  int factionToInt (object faction) {
    int whichfaction=0;
    int rez=0;
    while (whichfaction<(_olist.size(factions))) {
      object fac = _olist.at (factions,whichfaction);
      if (_string.equal (fac,faction)) {
	rez = whichfaction;
	whichfaction=_olist.size (factions);//stop loop
      }
      whichfaction=whichfaction+1;
    }
    return rez;
  };
  int getMaxFactions () {
    return _olist.size(factions);
  };
  void init_no_blank() {
    make_factions_list();
    make_ships_list (false);
    ship_upgrades.init();
  };
  void init(){
    bool useblank = (difficulty.getCredDifficulty()!=0.0);
    make_factions_list();
    make_ships_list(useblank);
    ship_upgrades.init();
  };
  object get_enemy_of (object factionname) {
    return get_X_of (enemies, factionToInt (factionname));
  };
  object get_friend_of (object factionname) {
    return get_X_of (friendlies, factionToInt (factionname));
  };
  object get_X_of (object mylist, int index) {
    object enemylist = _olist.at (mylist,index);
    index = random.randomint (0,(_olist.size (enemylist))-1);
    object piratestring = _string.new();
    object factionname = _olist.at (enemylist,index);
    _io.sprintf (piratestring,"%s",factionname);
    return piratestring;
  };
  void make_factions_list () {
    factions= _olist.new();
    enemies = _olist.new();
    friendlies = _olist.new();
    _olist.push_back (factions,"confed");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);

    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"ISO");

    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"hunter");

    _olist.push_back (factions,"aera");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);
    
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"hunter");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"ISO");


    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"retro");



    _olist.push_back (factions,"rlaan");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);

    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"hunter");

    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"rlaan");
    _olist.push_back (flist,"rlaan");
    _olist.push_back (flist,"rlaan");
    _olist.push_back (flist,"rlaan");


    _olist.push_back ( factions, "merchant");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);


    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"pirates");

    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"rlaan");

    _olist.push_back ( factions, "retro");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"hunter");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"ISO");
    _olist.push_back (curlist,"ISO");
    _olist.push_back (curlist,"ISO");
    _olist.push_back (curlist,"ISO");

    _olist.push_back (flist,"aera");
    _olist.push_back (flist,"retro");
    _olist.push_back (flist,"retro");
    _olist.push_back (flist,"retro");


    _olist.push_back (factions, "pirates");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);

    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"merchant");
    _olist.push_back (curlist,"ISO");


    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"merchant");//too odd?
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"pirates");
    _olist.push_back (flist,"pirates");
    _olist.push_back (flist,"pirates");
    _olist.push_back (flist,"pirates");
    _olist.push_back (flist,"pirates");



    _olist.push_back (factions,"hunter");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);


    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"rlaan");

    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"hunter");
    _olist.push_back (flist,"hunter");


    _olist.push_back (factions,"militia");
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"rlaan");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"ISO");

    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"confed");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"militia");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"hunter");

    _olist.push_back (factions,"ISO"); 
    object curlist = _olist.new();
    _olist.push_back (enemies,curlist);
    object flist = _olist.new();
    _olist.push_back (friendlies,flist);


    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"militia");
    _olist.push_back (curlist,"confed");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"aera");
    _olist.push_back (curlist,"pirates");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"retro");
    _olist.push_back (curlist,"hunter");

    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"ISO");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"merchant");
    _olist.push_back (flist,"rlaan");
  };
void make_ships_list(bool use_blank){
    capitols = _olist.new();
    fighters = _olist.new();
    object confed_ships=_olist.new();
    _olist.push_back(fighters,confed_ships);
    object confed_capitol=_olist.new();
    _olist.push_back(capitols,confed_capitol);
    _olist.push_back(confed_capitol,"cruiser");
    _olist.push_back(confed_capitol,"starrunner");
    _olist.push_back(confed_capitol,"cruiser_mk2");
    _olist.push_back(confed_capitol,"carrier");
    _olist.push_back(confed_capitol,"fleetcarrier");
    _olist.push_back(confed_capitol,"escortcarrier");
    _olist.push_back(confed_ships,"firefly");
    _olist.push_back(confed_ships,"destiny");
    _olist.push_back(confed_ships,"tian");
    _olist.push_back(confed_ships,"nova");
    _olist.push_back(confed_ships,"puma");
    _olist.push_back(confed_ships,"mongoose");
    _olist.push_back(confed_ships,"avenger");

    object aera_ships=_olist.new();
    object aera_capitol=_olist.new();
    _olist.push_back(capitols,aera_capitol);
    _olist.push_back(aera_capitol,"yrilan");
    _olist.push_back(fighters,aera_ships);
    _olist.push_back(aera_ships,"dagger");
    _olist.push_back(aera_ships,"aeon");
    _olist.push_back(aera_ships,"aevant");
    _olist.push_back(aera_ships,"kyta");
    _olist.push_back(aera_ships,"lekra");
    _olist.push_back(aera_ships,"osprey");
    _olist.push_back(aera_ships,"kira");
    _olist.push_back(aera_ships,"metron");
    _olist.push_back(aera_ships,"butterfly");

    object rlaan_ships=_olist.new();
    _olist.push_back(fighters,rlaan_ships);
    object rlaan_capitol=_olist.new();
    _olist.push_back(capitols,rlaan_capitol);
    _olist.push_back(rlaan_capitol,"rlaan_cruiser");

    _olist.push_back(rlaan_ships,"skart");
    _olist.push_back(rlaan_ships,"f109vampire");
    _olist.push_back(rlaan_ships,"starfish");
    _olist.push_back(rlaan_ships,"hispidus");
    
    object merchant_ships=_olist.new();
    _olist.push_back(fighters,merchant_ships);
    _olist.push_back (merchant_ships,"wayfarer");
    _olist.push_back(rlaan_capitol,"longhaul");

    object merchant_capitol=_olist.new();
    _olist.push_back(capitols,merchant_capitol);//double referenced
    _olist.push_back (merchant_capitol,"longhaul");
    _olist.push_back (merchant_capitol,"khanjarli");


    object Xships=_olist.new();
    _olist.push_back(fighters,Xships);
    object Xcapitol=_olist.new();
    _olist.push_back(capitols,Xcapitol);
    //    retro
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"wayfarer");
    _olist.push_back (Xships,"wayfarer");
    _olist.push_back (Xships,"avenger");
    _olist.push_back (Xships,"tian");
    _olist.push_back (Xships,"tian");

    _olist.push_back (Xcapitol,"cruiser_mk2");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"truck");


    object Xships=_olist.new();
    _olist.push_back(fighters,Xships);
    object Xcapitol=_olist.new();
    _olist.push_back(capitols,Xcapitol);
    //    pirates
    _olist.push_back (Xships,"revoker");
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"wayfarer");
    _olist.push_back (Xships,"wayfarer");
    _olist.push_back (Xships,"tian");
    _olist.push_back (Xcapitol,"cruiser_mk2");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"cargo");
    _olist.push_back (Xcapitol,"truck");
    _olist.push_back (Xcapitol,"cargo");
    _olist.push_back (Xcapitol,"truck");

   


    object Xships=_olist.new();
    _olist.push_back(fighters,Xships);
    object Xcapitol=_olist.new();
    _olist.push_back(capitols,Xcapitol);
    //    hunters
    _olist.push_back (Xships,"puma");
    _olist.push_back (Xships,"eagle");
    _olist.push_back (Xships,"avenger");
    _olist.push_back (Xcapitol,"cruiser_mk2");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"cruiser");



    object Xships=_olist.new();
    _olist.push_back(fighters,Xships);
    object Xcapitol=_olist.new();
    _olist.push_back(capitols,Xcapitol);
    //    militia
    _olist.push_back (Xships,"mongoose");
    _olist.push_back (Xships,"firefly");
    _olist.push_back (Xships,"tian");
    _olist.push_back (Xcapitol,"cruiser_mk2");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"escortcarrier");
    _olist.push_back (Xcapitol,"cruiser");


    object Xships=_olist.new();
    _olist.push_back(fighters,Xships);
    object Xcapitol=_olist.new();
    _olist.push_back(capitols,Xcapitol);
    //    iso
    _olist.push_back (Xships,"eagle");
    _olist.push_back (Xships,"nova");
    _olist.push_back (Xships,"tian");
    _olist.push_back (Xcapitol,"cargo");
    _olist.push_back (Xcapitol,"cruiser");
    _olist.push_back (Xcapitol,"truck");


    unknown_ships=_olist.new();
    _olist.push_back(unknown_ships,"unknown_active");    

    if (use_blank) {
      int i=0;
      while (i<_olist.size (fighters)) {
	object f = _olist.at (fighters,i);
	int j=0;
	while (j<_olist.size (f)) {
	  _io.printf ("reforming list");
	  object str = _olist.at (f,j);
	  object bak = _string.new();
	  _io.sprintf (bak,"%s.blank",str);
	  _io.sprintf (str,"%s",bak);
	  _string.delete (bak);
	  j=j+1;
	}
	i=i+1;
      }
    }
  };
  
  object getRandomShipType(object ship_list){
    int size=_olist.size(ship_list);
    int index=random.randomint(0,size-1);
    object ship_type=_olist.at(ship_list,index);

    return ship_type;
    };
  
  object getFigther(int confed_aera_or_rlaan, int fighter) {
    object fighterlist = _olist.at (fighters,confed_aera_or_rlaan);
    fighterlist= _olist.at (fighterlist,fighter);
    return fighterlist;
  };
  object getRandomFighterInt(int confed_aera_or_rlaan) {
    object lst = _olist.at (fighters,confed_aera_or_rlaan);
    return getRandomShipType(lst);
  };
  int getNumCapitol (int confed_aera_or_rlaan) {
    object lst = _olist.at (capitols,confed_aera_or_rlaan);
    return _olist.size (lst);
  };
  int getNumFighters (int confed_aera_or_rlaan) {
    object lst = _olist.at (fighters,confed_aera_or_rlaan);
    return _olist.size (lst);
  };
  object getCapitol(int confed_aera_or_rlaan, int fighter) {
    object caplist = _olist.at (capitols,confed_aera_or_rlaan);
    caplist= _olist.at (caplist,fighter);
    return caplist;
  };
  object getRandomCapitolInt(int confed_aera_or_rlaan) {
    object lst = _olist.at (capitols,confed_aera_or_rlaan);
    return getRandomShipType(lst);
  };
  object getRandomFighter(object faction){
    return getRandomFighterInt (factionToInt(faction));
  };
  object getRandomCapitol (object faction) {
    return getRandomCapitolInt (factionToInt (faction));
  };
  
}
