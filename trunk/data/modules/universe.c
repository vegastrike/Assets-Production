module universe {
  import ai_flyto_jumppoint;


  object current_system;
  object last_system;
  object old_system;
  object system_map;
  object outstr;

  object nearsys (object currentsystem, int sysaway, object str) {
    int max=_std.getNumAdjacentSystems(currentsystem);
    if ((sysaway<=0)||(max<=0)) {
      _io.sprintf(str,"Your final destination is %s",currentsystem);
      _io.message (1,"game","all",str);
      return currentsystem;
    } else {
      int nextsysnum=random.randomint(0,max-1);
      object nextsystem=_std.getAdjacentSystem(currentsystem,nextsysnum);
      _io.sprintf(str,"Jump from %s to %s.",currentsystem,nextsystem);
      _io.message (1,"game","all",str);
      return nearsys(nextsystem,sysaway-1,str);
    }
  };
  
  object getAdjacentSystem (object currentsystem, int num_systems_away) {
    object str = _string.new();
    object temp=nearsys (currentsystem,num_systems_away,str);
    _string.delete(str);
    return temp;
  };

  
  object getRandomJumppoint(){
    object jp_list=getJumppointList();
    object jp;
    int size=_olist.size(jp_list);
    if (size>0) {
      int index=random.randomint(0,size-1);

      jp=_olist.at(jp_list,index);

      _olist.delete(jp_list);
    }else {
      _std.setNull(jp);
    }
    return jp;
  };

  object getJumppointList(){
    object jp_list=_olist.new();

    int ship_nr=0;
    object unit=_unit.getUnit(ship_nr);

    while((!_std.isNull(unit))){
      //      object unit_fgid=_unit.getFgID(unit);
      //_io.printf("matching %s with %s\n",unit_fgid,patrol_fgid);
      if(_unit.isJumppoint(unit)){
	_olist.push_back(jp_list,unit);
      }
      ship_nr=ship_nr+1;
      unit=_unit.getUnit(ship_nr);
      //_string.delete(unit_fgid);
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
