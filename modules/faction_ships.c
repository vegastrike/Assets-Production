module faction_ships {
  import random;

  object confed_ships;
  object aera_ships;

  object confed(){
    return confed_ships;
  };

  object aera(){
    return aera_ships;
  };

  void init(){
    make_ships_list();
  };

  void make_ships_list(){
    confed_ships=_olist.new();

    _olist.push_back(confed_ships,"firefly");
    _olist.push_back(confed_ships,"destiny");
    _olist.push_back(confed_ships,"tian");
    _olist.push_back(confed_ships,"nova");

    aera_ships=_olist.new();

    _olist.push_back(aera_ships,"dagger");
    _olist.push_back(aera_ships,"aeon");
    _olist.push_back(aera_ships,"aevant");
    _olist.push_back(aera_ships,"kyta");
    _olist.push_back(aera_ships,"lekra");
  };

  object getRandomShipType(object ship_list){
    int size=_olist.size(ship_list);

    int index=random.randomint(0,size-1);

    object ship_type=_olist.at(ship_list,index);
   
    return ship_type;
  };

  object getRandomFighter(object faction){
    object type;

    if(_string.equal(faction,"confed")){
      type=getRandomShipType(confed_ships);
    }
    else if(_string.equal(faction,"aera")){
      type=getRandomShipType(aera_ships);
    }

    return type;
  };
}
