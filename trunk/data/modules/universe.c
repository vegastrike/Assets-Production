module universe {

  object current_system;
  object last_system;
  object old_system;
  object system_map;
  object outstr;

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
