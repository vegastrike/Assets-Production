module ship_upgrades {
  import random;

  object GetDiffCargo (float diff, object base_category, object all_category) {
    object cat=_string.new();
    int ch=0;
    if (diff<=0.1) {
      ch=1;
    } else if (diff<=0.3) {
      ch=2-random.randomInt(0,1);
    } else if (diff<=0.5) {
      ch=3-random.randomInt(0,2);
    }
    if (ch==1) {
      _io.sprintf(cat,"%sLight",base_category);
    } else if (ch==2) {
      _io.sprintf(cat,"%sMedium",base_category);
    } else if (ch==3) {
      _io.sprintf(cat,"%sHeavy",base_category);
    } else {
      //All
      _io.sprintf(cat,"%s",all_category);
    }
    return cat;
  };

  object getItem (object cat,object parentcat) {
    object list=_unit.getRandCargo(1,cat);
    if (_olist.size(list)<=0) {
      list=_unit.getRandCargo(1,parentcat);
      if (_olist.size(list)<=0) {
        list=_unit.getRandCargo(1,"upgrades");
      }
    }
    return list;
  };

  object GetRandomWeapon (float diff) {
    float rndnum=_std.Rnd();
    object cat;
    float if (rndnum<0.5) {
      cat=GetDiffCargo(diff,"upgrades/Weapons/Beam_Arrays_","upgrades/Weapons");
    } else {
      cat=GetDiffCargo(diff,"upgrades/Weapons/Mounted_Guns_","upgrades/Weapons");
    }
    object item=getItem(cat,"upgrades/Weapons");
    _olist.delete(cat);
    return item;
  };

  object GetRandomShield (float diff) {
    object cat=GetDiffCargo(diff,"upgrades/Shield_Systems/","upgrades/Shield_Systems");
    object item=getItem(cat,"upgrades/Shield_Systems");
    _olist.delete(cat);
    return item;
  };

  object getRandomEngine (float diff) {
    float rndnum=_std.Rnd();
    object cat;
    float if (rndnum<0.5) {
      cat=GetDiffCargo(diff,"upgrades/Engines/","upgrades/Engines");
    } else {
      cat=GetDiffCargo(diff,"upgrades/Engines/Engine_Enhancements_","upgrades/Engines");
    }
    object item=getItem(cat,"upgrades/Engines");
    _olist.delete(cat);
    return item;
  };

  object GetRandomHull () {
    object item=getItem("upgrades/Hull_Upgrades","upgrades/Hull_Upgrades");
    return item;
  };

  object GetRandomArmor () {
    object item=getItem("upgrades/Armor_Modification","upgrades/Hull_Upgrades");
    return item;
  };

  object GetRandomUpgrade () {
    object item=_unit.getRandCargo(1,"upgrades");
    return item;
  };

  void init () {

  };

}
