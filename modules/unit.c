module unit {
  // support for the _unit callback class

  float lasttime;

  void setTargetShip(object which_fgid,object target_fgid){
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);
    object target_unit=unit.getUnitByFgID(target_fgid);
    
    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,which_fgid);
      if(_string.begins(unit_fgid,which_fgid)){
	//_io.printf("setTarget found match: %s %s\n",unit_fgid,target_fgid);

	_unit.setTarget(unit,target_unit);
      }
      _string.delete(unit_fgid);
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
    }
  };


  void removeFg(object which_fgid){
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("removeFg: matching %s with %s\n",unit_fgid,which_fgid);
      if(_string.begins(unit_fgid,which_fgid)){
	//_io.printf("removeFg: found match: %s %s\n",unit_fgid,which_fgid);

	_unit.removeFromGame(unit);
      }
      else{
	ship_nr=ship_nr+1;
      }
      _string.delete(unit_fgid);
      unit=_unit.getUnit(ship_nr);
    }
 
  };

  object getUnitByFgID(object fgid){
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);
    object found_unit;
    _std.setNull(found_unit);

    while((!_std.isNull(unit)) && _std.isNull(found_unit)){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,fgid);
      if(_string.equal(unit_fgid,fgid)){
	//_io.printf("found match: %s %s\n",unit_fgid,fgid);
	found_unit=unit;
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      _string.delete(unit_fgid);
    }

    return found_unit;
  };

  void initgame(){
    lasttime=0.0;
  };

  void launch_test(){
    float time=_std.getGameTime();

    if((time-lasttime)>10.0){
      _unit.launch("omega","confed","hornet","default",4, 8000.0, 0.0-100.0, 100.0);
      _unit.launch("teta","aera","dagger","default",4, 8000.0, 1000.0, 0.0-500.0);
      lasttime=time;
    }
  };

  object makeUnitList(){
    object unit_list=_olist.new();
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);;
    
    while(!_std.isNull(unit)){
      _olist.push_back(unit_list,unit);
      
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
    }

    return unit_list;
  };

  void print_unitlist(){
    int ship_nr=0;

    object unit=_unit.getUnit(ship_nr);;

    while(!_std.isNull(unit)){

      object pos=_unit.getPosition(unit);
      object fgid=_unit.getFgId(unit);

      float i=_olist.at(pos,0);
      float j=_olist.at(pos,1);
      float k=_olist.at(pos,2);

      _io.printf("fgid=%s  ship_nr=%d pos: %f %f %f\n",fgid,ship_nr,i,j,k);

      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);

      _string.delete(fgid);
    }
  };

}
