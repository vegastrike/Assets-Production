module order {

  import unit;
  import vec3;
  import ai_flyto_waypoint;
  import ai_patrol;
  import launch;

  float gametime;
  bool did_it;

  void patrolFg(int pmode,object patrol_fgid,object around_fgid,float range,float patrol_speed){
    // sends each flightgroup matching patrol_fgid to either
    // patrol around the first flightgroup matching around_fdid or
    // patrol in the area around fg patrol_fgid

    object around_unit=unit.getUnitByFgID(around_fgid);

    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,patrol_fgid);
      if(_string.begins(unit_fgid,patrol_fgid)){
	//_io.printf("found match: %s %s\n",unit_fgid,patrol_fgid);

	object unit_order=_unit.getOrder(unit);
	object upos=_unit.getPosition(unit);
	object new_order=_order.newPatrol(pmode,upos,range,around_unit,patrol_speed);
	_order.enqueueOrderFirst(unit_order,new_order);
	
	_olist.delete(upos);
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      _string.delete(unit_fgid);
    }
  };

  void patrolShip(int pmode,object patrol_fgid,object around_fgid,float range,float patrol_speed){
    // sends a flightgroup patrol_fgid to either
    // patrol around flightgroup around_fdid or
    // patrol in the area around fg patrol_fgid

    object around_unit=unit.getUnitByFgID(around_fgid);

    object unit=unit.getUnitByFgID(patrol_fgid);
    object unit_order=_unit.getOrder(unit);

    object upos=_unit.getPosition(unit);

    object new_order=_order.newPatrol(pmode,upos,range,around_unit,patrol_speed);

    _order.enqueueOrderFirst(unit_order,new_order);

    _olist.delete(upos);
  };

  void flyToOtherShip(object which_fg,object dest_fg,float vel,bool afburn,float range){
    // sends flighgroup which_fg to flightgroup dest_fg

    object alpha_ship=unit.getUnitByFgID(which_fg);
    object old_order=_unit.getOrder(alpha_ship);

    object carrier_ship=unit.getUnitByFgID(dest_fg);
    object waypoint=_unit.getPosition(carrier_ship);

    object new_order=_order.newFlyToWaypoint(waypoint,vel,afburn,range);

    _order.enqueueOrderFirst(old_order,new_order);

    _olist.delete(waypoint);
  };

  void flyToWaypoint(object which_fgid,object dest_vec3,float vel,bool afburn,float range){
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,patrol_fgid);
      if(_string.begins(unit_fgid,which_fgid)){
	//_io.printf("found match: %s %s\n",unit_fgid,patrol_fgid);

	object unit_order=_unit.getOrder(unit);

	object new_order=_order.newFlyToWaypoint(dest_vec3,vel,afburn,range);
	_order.enqueueOrderFirst(unit_order,new_order);
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      _string.delete(unit_fgid);
    }
  };

  void spaceSuperiority(object which_fgid){
    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,patrol_fgid);
      if(_string.begins(unit_fgid,which_fgid)){
	//_io.printf("found match: %s %s\n",unit_fgid,patrol_fgid);

	object unit_order=_unit.getOrder(unit);

	object new_order=_order.newSuperiority();
	_order.enqueueOrderFirst(unit_order,new_order);
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      _string.delete(unit_fgid);
    }
  };


}
