module trading {
  import random;
  int quantity;
  int last_ship;
  float price_instability;
  void init(){
    lasttime=0.0;
    last_ship=0;
    price_instability=0.01;
    quantity=4;
  };
  void SetPriceInstability(float inst) {
    price_instability=inst
  }
  void SetMaxQuantity (int quant) {
    quantity=quant;
  }
  void trade_cargo(){
    int incdec_ships=random.randomint(1,2);
    int quant = random.randomint (1,quantity);
    object un = _unit.getUnit (last_ship);
    if (_std.isNull(un)) {
      last_ship=0;
    } else {
      object player = _unit.getPlayer();
      if (player!=un) {
	if (incdec_ships==1) {
	  _unit.incrementCargo(un,1-(quant*price_instability),quant);
	}else {
	  _unit.decrementCargo(un,1+(quant*price_instability),quant);
	}
      }
      last_ship=last_ship+1;
    }
  };
}
