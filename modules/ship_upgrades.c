module ship_upgrades {
  import random;

  object GetDiffCargo (float diff, object base_category, object all_category) {
    object cat=_string.new();
    int ch=0;
    if (diff<=0.1) {
      ch=1;
    } else if (diff<=0.3) {
      ch=2-random.randomint(0,1);
    } else if (diff<=0.5) {
      ch=3-random.randomint(0,2);
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
    if (rndnum<0.5) {
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
    if (rndnum<0.5) {
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
  object GetRandomTurret () {
    object item=getItem("upgrades/Weapons/Turrets","upgrades/Weapons");
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

  void basicUnit (object un) {
    int i=0;
    int curmount=0;
    float percent;
    while (i<2) {
      percent=_unit.upgrade(un,"laser",curmount,curmount,true,true);
      curmount=curmount+1;
      i=i+1;
    }
    percent=_unit.upgrade(un,"engine_level_0",0,0,true,false);
    percent=_unit.upgrade(un,"shield_2",0,0,true,false);
    percent=_unit.upgrade(un,"plasteel",0,0,true,false);
    percent=_unit.upgrade(un,"hull",0,0,true,false);
  };
  float upgradeHelper (object un, object mylist, int curmount,float creds, bool cycle) {
     float newcreds=0.0;
     if (_olist.size(mylist)==0) {
        _olist.delete (mylist);
        return 0.0; 
     }else {
        object str=_olist.at(mylist,0);
        newcreds=_olist.at (mylist,2);
        newcreds = newcreds*_unit.upgrade(un,str,curmount,curmount,true,cycle);
        creds = creds -newcreds;
        _olist.delete (mylist);

     }
     return creds;
  };
  
  void upgradeUnit (object un, float creds, float diff) {
    int curmount=0;
    object mylist;
    object str;
    float rndnum;
    int inc=0;
    int numammos=_std.Int(50.0*diff);
    if (numammos>30) {
      numammos=30;
    } else if (numammos<5) {
      numammos=5;
    }
    while (inc<numammos) {
      mylist=_unit.getRandCargo(0,"upgrades/Ammunition");
      if (_olist.size(mylist)<=0) {
        inc=numammos;
      } else {
        str=_olist.at(mylist,0);
        float temp=_unit.upgrade(un,str,inc,inc,false,true);
      }
      inc=inc+1;
    }
    mylist = GetRandomHull();
    creds =upgradeHelper (un,mylist,0,creds,false);

    mylist = GetRandomArmor();
    creds =upgradeHelper (un,mylist,0,creds,false);
    inc=0;
    int i=0;
    while ((creds>500.0)&&(i<100)) {
      if (inc<2) {
        mylist=GetRandomWeapon(diff);
      }else if (inc==2) {
        mylist=GetRandomTurret();
      }else {
        mylist=GetRandomUpgrade();
      }
      creds =upgradeHelper (un,mylist,curmount,creds,inc<2);
      
      _olist.delete(mylist);
      curmount=curmount+1;
      inc = inc+1;
      i=i+1;
      if (inc>5) {
	inc =0;
      }
    }
  };

  void init () {

  };
}

