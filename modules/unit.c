module unit {
  // support for the _unit callback class

  float lasttime;

  object obsolete_getNearestEnemy(object my_unit,float range){
    int ship_nr=0;
    float min_dist=9999999.0;
    object min_enemy;

    _std.setNull(min_enemy);

    object unit=_unit.getUnit(ship_nr);
    
    while((!_std.isNull(unit))){
      //_io.printf("checking ship %d\n",ship_nr);
      object unit_pos=_unit.getPosition(unit);
      float dist=_unit.getMinDis(my_unit,unit_pos);
      
      //      float relation=0.0;
      float relation=_unit.getRelation(my_unit,unit);
      //_io.printf("relation %f\n",relation);

      if(relation<0.0){
	if((!_std.equal(my_unit,unit)) && (dist<range) && (dist<min_dist)){
	  min_dist=dist;
	  min_enemy=unit;
	}
      }
      _olist.delete(unit_pos);
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
    }

    //_io.printf("check-end\n");
    if(!_std.isNull(min_enemy)){
      object other_fgid=_unit.getFgID(min_enemy);
      //_io.printf("enemy is %s\n",other_fgid);
    }
    //_io.printf("check-end2\n");
    return min_enemy;
  };

  object obsolete_getThreatOrEnemyInRange(object unit,float range){
    //_io.printf("check1\n");
    object threat=_unit.getThreat(unit);
    //        return threat;

    //_io.printf("check2\n");
    if(_std.isNull(threat)){
      //_io.printf("check3\n");
      threat=obsolete_getNearestEnemy(unit,range);
      //_io.printf("check4\n");
      //threat=threat2;
      //_io.printf("check5\n");
    }

    return threat;
  };

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
  object getUnitByFgID(object fgid) {
    return getUnitByFgIDFromNumber(fgid,0);
  };
  object getUnitByFgIDFromNumber(object fgid, int ship_nr){
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
      _unit.launch("omega","confed","nova","default",4,1, 8000.0, 0.0-100.0, 100.0);
      _unit.launch("teta","aera","dagger","default",4,1, 8000.0, 1000.0, 0.0-500.0);
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
      float rsize=_unit.getRSize(unit);

      float i=_olist.at(pos,0);
      float j=_olist.at(pos,1);
      float k=_olist.at(pos,2);

      _io.printf("%d:%s: r=%f + ss=%b pl=%b jp=%b + [%f %f %f]\n",ship_nr,fgid,rsize,_unit.isStarShip(unit),_unit.isPlanet(unit),_unit.isJumppoint(unit),i,j,k);

      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);

      _string.delete(fgid);
    }
  };

}
