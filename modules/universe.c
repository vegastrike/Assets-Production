module universe {

  import ai_flyto_jumppoint;

  object current_system;
  object last_system;
  object old_system;
  object system_map;
  object outstr;

  object getRandomJumppoint(){
    object jp_list=getJumppointList();

    int size=_olist.size(jp_list);

    int index=random.randomint(0,size-1);

    object jp=_olist.at(jp_list,index);

    _olist.delete(jp_list);

    return jp;
  };

  object getJumppointList(){
    object jp_list=_olist.new();

    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,patrol_fgid);
      if(_unit.isJumppoint(unit)){
	_olist.push_back(jp_list,unit);
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      _string.delete(unit_fgid);
    }

    return jp_list;
  };

  void init(){
    outstr=_string.new();

    current_system=_std.GetSystemName();
    last_system=_std.GetSystemName();
    old_system=_std.GetSystemName();

    system_map=_omap.new();
    _omap.set(system_map,current_system,current_system);
  };

  bool loop(){
    bool jumped=false;
    current_system=_std.GetSystemName();
    if(!_string.equal(current_system,last_system)){
      // we have jumped

      _io.sprintf(outstr,"jumped from %s to %s",last_system,current_system);
      _io.message(0,"game","all",outstr);

      old_system=last_system;
      last_system=_std.GetSystemName();
      jumped=true;
    }
    return jumped;
  };

}
