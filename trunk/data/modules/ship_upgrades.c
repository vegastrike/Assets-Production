module ship_upgrades {
  import random;
  /// This function makes a string based on the difficulty. In this way it can be restricted to light or medium mounts when the difficulty is low, avoiding unaffordable weapons
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

  object GetRandomShield (float diff) {//gets random shield system from master part list
    object cat=GetDiffCargo(diff,"upgrades/Shield_Systems/","upgrades/Shield_Systems");
    object item=getItem(cat,"upgrades/Shield_Systems");
    _string.delete(cat);
    return item;
  };

  object getRandomEngine (float diff) {//get random engine from master part list
    float rndnum=_std.Rnd();
    object cat;
    if (rndnum<0.5) {
      cat=GetDiffCargo(diff,"upgrades/Engines/","upgrades/Engines");
    } else {
      cat=GetDiffCargo(diff,"upgrades/Engines/Engine_Enhancements_","upgrades/Engines");
    }
    object item=getItem(cat,"upgrades/Engines");
    _string.delete(cat);
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
  //this function sets up a blank unit with some basic upgrades that are really a necessecity for any sort of figthing
  void basicUnit (object un) {
    int i=0;
    int curmount=0;
    float percent;
    while (i<2) {//two lasers
      percent=_unit.upgrade(un,"laser",curmount,curmount,false,true);
      curmount=curmount+1;
      i=i+1;
    }
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
  float upgradeHelper (object un, object mylist, int curmount,float creds, bool cycle) {
     float newcreds=0.0;
     if (_olist.size(mylist)==0) {//if somehow the cargo isn't there
       _olist.delete (mylist);//deleet list
       return 0.0; //and terminate the enclosing loop by saying we're out of cash
     }else {
       object str=_olist.at(mylist,0);//otherwise our name is the 0th item
       newcreds=_olist.at (mylist,2);//and the price is the 2nd
        newcreds = newcreds*_unit.upgrade(un,str,curmount,curmount,false,cycle);
        creds = creds -newcreds;//we added some newcreds and subtracted them from credit ammt
        _olist.delete (mylist);//then we delete the list

     }
     return creds;//return new creds
  };
  

  void upgradeUnit (object un, float creds, float diff) {
    int curmount=0;
    object mylist;
    object str;
    float rndnum;
    int inc=0;
    int numammos=_std.Int(50.0*diff);//number of ammo is 50 * difficulty (lots)
    if (numammos>30) {//if it's more tan 30 total, we reduce to 30
      numammos=30;
    } else if (numammos<5) {//otherwise we clamp at 5...(too much alreadY0
      numammos=5;
    }
    //then we cycle through the ammo
    while (inc<numammos) {
      mylist=_unit.getRandCargo(0,"upgrades/Ammunition");//and get it
      if (_olist.size(mylist)<=0) {
        inc=numammos;
      } else {
        str=_olist.at(mylist,0);
        float temp=_unit.upgrade(un,str,inc,inc,false,true);//and apply it at no charge
      }
      inc=inc+1;
    }
    mylist = GetRandomHull();//ok now we get some hull upgrades
    creds =upgradeHelper (un,mylist,0,creds,false);

    mylist = GetRandomArmor();//and some random armor
    creds =upgradeHelper (un,mylist,0,creds,false);
    inc=0;
    int i=0;
    while ((creds>500.0)&&(i<100)) {
      if (inc<2) {
        mylist=GetRandomWeapon(diff);//weapons go on as first two items of loop
      }else if (inc==2) {
        mylist=GetRandomTurret();//turrets as 3rd...
      }else {
        mylist=GetRandomUpgrade();//and finally we have just random schmear from the whole list
      }
      creds =upgradeHelper (un,mylist,curmount,creds,inc<2);//we pass this in to the credits...and we only loop through all mounts if we're adding a weapon
      
      curmount=curmount+1;//increase starting mounts hardpoint
      inc = inc+1;
      i=i+1;
      if (inc>5) {//start over count after 5
	inc =0;
      }
    }
  };

  void init () {

  };
}

