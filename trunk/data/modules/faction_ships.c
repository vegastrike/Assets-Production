module faction_ships {
  import random;
  object capitols;
  object fighters;
  object unknown_ships;
  
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
  
  void init(){
    make_ships_list();
  };
  
  void make_ships_list(){
    capitols = _olist.new();
    fighters = _olist.new();
    object confed_ships=_olist.new();
    _olist.push_back(fighters,confed_ships);
    object confed_capitol=_olist.new();
    _olist.push_back(capitols,confed_capitol);
    _olist.push_back(confed_capitol,"cruiser");
    _olist.push_back(confed_capitol,"cruiser_mk2");
    _olist.push_back(confed_capitol,"carrier");
    _olist.push_back(confed_capitol,"fleetcarrier");
    _olist.push_back(confed_ships,"firefly");
    _olist.push_back(confed_ships,"destiny");
    _olist.push_back(confed_ships,"tian");
    _olist.push_back(confed_ships,"nova");
    _olist.push_back(confed_ships,"puma");
    _olist.push_back(confed_ships,"mongoose");

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
    _olist.push_back(rlaan_capitol,"revoker");
    _olist.push_back(rlaan_ships,"skart");
    _olist.push_back(rlaan_ships,"f109vampire");
    _olist.push_back(rlaan_ships,"starfish");
    _olist.push_back(rlaan_ships,"hispidus");

    unknown_ships=_olist.new();
    _olist.push_back(unknown_ships,"unknown_active");    
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
  object intToFaction(int fac) {
    if (fac==0) {
      return "confed";
    }else if (fac==1) {
      return "aera";
    }else if (fac==2) {
      return "rlaan";
    }
  };
  int getMaxFactions () {
    return _olist.size(fighters);
  };
  object getRandomFighter(object faction){
    object type;

    if(_string.equal(faction,"confed")){
      type=getRandomFighterInt(0);
    }
    else if(_string.equal(faction,"aera")){
      type=getRandomFighterInt(1);
    }
    else if (_string.equal(faction,"rlaan")){
      type=getRandomFighterInt(2);
    }
    else {
      type=getRandomShipType(unknown_ships);
    }

    return type;
  };
  object getRandomCapitol(object faction){
    object type;

    if(_string.equal(faction,"confed")){
      type=getRandomCapitolInt(0);
    }
    else if(_string.equal(faction,"aera")){
      type=getRandomCapitolInt(1);
    }
    else if (_string.equal(faction,"rlaan")){
      type=getRandomCapitolInt(2);
    }
    else {
      type=getRandomShipType(unknown_ships);
    }

    return type;
  };
  
}
