module ship_upgrades {
  import random;
  /// This function makes a string based on the difficulty. In this way it can be restricted to light or medium mounts when the difficulty is low, avoiding unaffordable weapons
  int GetDiffInt (float diff) {
    int ch=0;
    if (diff<=0.1) {
      ch=0;
    } else if (diff<=0.3) {
      ch=1-random.randomint(0,1);
    } else if (diff<=0.5) {
      ch=2-random.randomint(0,2);
    } else if (diff<=0.7) {
      ch=3-random.randomint(0,3);
    } else if (diff<=0.9) {
      ch=4-random.randomint(0,4);
    } else {
      ch=5-random.randomint(0,5);
    }
    return ch;
  };
  object GetDiffCargo (float diff, object base_category, object all_category) {
    object cat=_string.new();
    int ch=0;
    if (diff<=0.1) {
      ch=1;
    } else if (diff<=0.3) {
      ch=2-random.randomint(0,1);
    } else if (diff<=0.5) {
      ch=3-random.randomint(0,2);
    }//ch is 0 if it is any upgrades/Weapon  otherwise it coudl be light, medium or heavy or some random set between Light and X (l,med,or heavy)
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
  ///this gets a random cargo listed on the master part list.
  object getItem (object cat,object parentcat) {
    object list=_unit.getRandCargo(1,cat);//try to get a cargo from said category
    if (_olist.size(list)<=0) {//if no such cargo exists in this cateogry
      list=_unit.getRandCargo(1,parentcat);//get it from the parent category
      if (_olist.size(list)<=0) {//otherwise get cargo from upgrades category
        list=_unit.getRandCargo(1,"upgrades");//this always succeeds
      }
    }
    return list;
  };

  object GetRandomWeapon (float diff) {//gets random beam or mounted gun from master part list
    float rndnum=_std.Rnd();
    object cat;
    if (rndnum<0.5) {
      cat=GetDiffCargo(diff,"upgrades/Weapons/Beam_Arrays_","upgrades/Weapons");
    } else {
      cat=GetDiffCargo(diff,"upgrades/Weapons/Mounted_Guns_","upgrades/Weapons");
    }
    object item=getItem(cat,"upgrades/Weapons");
    _string.delete(cat);
    return item;
  };
  int getRandIncDec (int type) {
    type = type + random.randomint (0-1,1);
    if (type<0) {
      type=0;
    }
    if (type>5) {
      type=5;
    }
    return type;
  };
  object GetRandomShield (int faces,int type) {//gets random shield system from master part list
    object cat=_string.new();
    type = getRandIncDec (type);
    _io.sprintf (cat,"shield_%d_Level%d",faces.type);
    return cat;
  };

  object GetRandomAfterburner (float diff) {//get random afterburner from master part list
    object cat;
    cat=GetDiffCargo(diff,"upgrades/Engines/Engine_Enhancements_","upgrades/Engines");
    object item=getItem(cat,"upgrades/Engines");
    _string.delete(cat);
    return item;
  };

  object getRandomRadar () {
    int myint=random.randomint(0,2);
    object item=_string.new();
    if (myint<=0) {
      _io.sprintf(item,"radar_windows_2k");
    } else if (myint==1) {
      _io.sprintf(item,"radar_linux_SuSe");
    } else {
      _io.sprintf(item,"radar_free_bsd");
    }
    return item;
  };
  void UpgradeRadar (object un) {
    float temp;
    object cat = getRandomRadar ();
    temp=_unit.upgrade (un,cat,0,0,true,false);    
    _string.delete (cat);
  };
  void UpgradeAfterburner (object un,float diff) {
    float temp;
    float i=0.0;
    while (i<diff*3.0) {
      object cat = GetRandomAfterburner(diff);
      object name = _olist.at (cat,0);
      temp=_unit.upgrade (un,name,0,0,true,false);    
      _olist.delete (cat);
      i=i+1.0;
    }

  };
  int getRandomEngine (float diff, object cat) { //get random engine from master part list
    //WARNING: CAT MUST BE NEWED BEFORE PASSING IT IN.
    int myint=GetDiffInt(diff);
    _io.sprintf(cat,"engine_level_%d",myint);
    return myint;
  };
  void UpgradeEngine (object un, float diff) {
    object cat = _string.new();
    float temp;
    int type = getRandomEngine (diff,cat);
    if (type!=0) {
      temp=_unit.upgrade (un,cat,0,0,true,false);    
      _io.printf ("Upgrading Engine %s percent %f",cat,temp); 
      if (temp>0.0) {
	_string.delete (cat);
	cat = GetRandomShield (2,type);
	temp=_unit.upgrade (un,cat,0,0,true,false);
	_io.printf ("Upgrading Shield %s percent %f",cat,temp); 
	_string.delete (cat);
	cat = GetRandomShield (4,type);
	temp=_unit.upgrade (un,cat,0,0,true,false);
	_io.printf ("Upgrading Shield4 %s percent %f",cat,temp); 
      }

    }
    _string.delete (cat);
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
  object GetRandomAmmo () {
    object item=getItem ("upgrades/Ammunition/3pack","upgrades/Ammunition");
    return item;
  };
  object GetRandomRepairSys () {
    object item=getItem("upgrades/Repair_Systems/Research","upgrades/Repair_Systems");
    return item;
  };
  //this function sets up a blank unit with some basic upgrades that are really a necessecity for any sort of figthing
  void basicUnit (object un, float diff) {
    int i=0;
    float percent;
    while (i<2) {//two lasers
      percent=_unit.upgrade(un,"laser",i,i,false,true);
      i=i+1;
    }
    UpgradeEngine (un,diff);
    UpgradeRadar (un);
    // if ((_std.Rnd()<0.9) &&(_std.Rnd()<(diff*4.0))) {
      UpgradeAfterburner(un,diff);
      // }
    //and after some careful review of the code in question, it appears upgrades below are already offered by default on blank ships...only need to give 'em a pair of guns

    //some engines
    //    percent=_unit.upgrade(un,"engine_level_0",0,0,false,false);
    //    percent=_unit.upgrade(un,"shield_2",0,0,false,false);
    //both shield 2 and 4 depending on ship type!
    //    percent=_unit.upgrade(un,"shield_4",0,0,false,false);
    //some dumb armor
    //    percent=_unit.upgrade(un,"plasteel",0,0,false,false);
    //and at least a few hitpoints
    //    percent=_unit.upgrade(un,"hull",0,0,false,false);
  };



  //this function does the dirty work of the upgrade unit function... Given the list that contains a piece of cargo, it upgrades it, subtracts the price, and slaps it on your ship, and returns the new number of creds the computer player has.  It may well be negative cus we thought that these guys may go in debt or something
  float upgradeHelper (object un, object mylist, int curmount,float creds, bool force, bool cycle) {
     float newcreds=0.0;
     if (_olist.size(mylist)==0) {//if somehow the cargo isn't there
       _io.printf ("error.. crgo not found");
       _olist.delete (mylist);//deleet list
       return 0.0; //and terminate the enclosing loop by saying we're out of cash
     }else {
       object str=_olist.at(mylist,0);//otherwise our name is the 0th item
       newcreds=_olist.at (mylist,2);//and the price is the 2nd
        newcreds = newcreds*_unit.upgrade(un,str,curmount,curmount,force,cycle);
        creds = creds -newcreds;//we added some newcreds and subtracted them from credit ammt
        _olist.delete (mylist);//then we delete the list

     }
     return creds;//return new creds
  };
  

  void upgradeUnit (object un, float diff) {
    float creds=0.0;
    int curmount=0;
    object mylist;
    object str;
    float rndnum;
    int inc=0;
    basicUnit(un,diff);

    mylist = GetRandomHull();//ok now we get some hull upgrades
    creds =upgradeHelper (un,mylist,0,creds,true,false);

    mylist = GetRandomArmor();//and some random armor
    creds =upgradeHelper (un,mylist,0,creds,true,false);
    inc=0;
    int i=0;
    rndnum=_std.Rnd()*2;
    if (rndnum<diff) {
      mylist = GetRandomRepairSys();//here there is a small chance that you will get a repair system.
      creds =upgradeHelper (un,mylist,0,creds,true,false);
    }
    object turret=un;
    int turretcount=0;
    while (!_std.isNull (turret)) {
      turret = _unit.getTurret (un,turretcount);
      turretcount = turretcount+1;
    }
    turretcount=turretcount-1;
    while (i<turretcount) {
      int j=0;
      while (j<4) {
        mylist=GetRandomTurret();//turrets as 3rd...
        creds = upgradeHelper (un,mylist,i,creds,false,false);      
        j=j+1;
      }
      i=i+1;
    }
    turretcount=_std.Int(diff*50.0);
    if (turretcount>24) {
      turretcount=24;
    } else if (turretcount<3) {
      turretcount=3;
    }
    i=0;

    while (i<turretcount) {
      if (_std.Rnd()<0.66) {
        mylist=GetRandomWeapon(diff);//weapons go on as first two items of loop
      }else {
        mylist=GetRandomAmmo();
      }
      creds =upgradeHelper (un,mylist,curmount,creds,false,true);//we pass this in to the credits...and we only loop through all mounts if we're adding a weapon
      
      curmount=curmount+1;//increase starting mounts hardpoint
      i=i+1;
    }
  };

  void init () {

  };
}

