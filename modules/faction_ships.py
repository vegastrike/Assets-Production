  import random
  import ship_upgrades
  confed=0
  aera=1
  rlaan=2
  merchant=3
  retro=4
  pirates=5
  hunter=6
  militia=7
  ISO=8
  capitols
  fighters
  unknown_ships
  factions
  enemies
  friendlies
  
  get_enemy_of (factionname):
    return get_X_of (enemies, factionTo(factionname))
  
  get_friend_of (factionname):
    return get_X_of (friendlies, factionTo(factionname))
  
  get_X_of (mylist, index):
    enemylist = _olist.at (mylist,index)
    index = random.random(0,(_olist.size (enemylist))-1)
    piratestring = _string.new()
    factionname = _olist.at (enemylist,index)
    _io.sprintf (piratestring,"%s",factionname)
    return piratestring
  
  def make_factions_list ():
    factions=("confed","aera","rlaan","merchant","retro","pirates","hunter","militia","ISO")
    
    enemies =  ((aera,aera,rlaan,rlaan,retro,pirates,ISO), #confed
                (confed,confed,confed,militia,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,pirates,hunter,merchant,ISO), #aera
                (confed,confed,militia,aera,aera,aera,aera,aera,aera,aera,aera,pirates,retro,retro,retro,retro,retro,hunter),#rlaan
                (aera,aera,retro,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates), #merchant
                (confed,confed,confed,militia,rlaan,pirates,hunter,merchant,merchant,merchant,merchant,merchant,merchant,merchant,merchant,ISO,ISO,ISO,ISO), #retro
                (confed,confed,confed,militia,militia,militia,militia,rlaan,rlaan,rlaan,retro,aera,aera,aera,merchant,merchant,merchant,merchant,merchant,merchant,ISO), #pirates
                (aera,aera,retro,rlaan), #hunter
                (aera,aera,rlaan,rlaan,retro,pirates,ISO), #militia
                (confed,confed,confed,confed,confed,confed,confed,militia,militia,militia,aera,aera,aera,pirates,retro,retro,retro,hunter) #ISO
                )
    
    friendlies=((confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant), #confed
                (aera,aera,aera,aera,aera,aera,aera,retro), #aera
                (ISO,merchant,rlaan,rlaan,rlaan,rlaan), #rlaan
                (ISO,confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant,hunter,rlaan), #merchant
                (aera,retro,retro,retro), #retro
                (hunter,merchant,merchant,merchant,pirates,pirates,pirates,pirates,pirates), #pirates
                (ISO,confed,confed,militia,militia,merchant,hunter,hunter,hunter,hunter,hunter), #hunter
                (confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant,hunter), #militia
                (ISO,ISO,ISO,merchant,merchant,rlaan) #ISO
                )

void make_ships_list(use_blank):
    capitols = _olist.new()
    fighters = _olist.new()
    confed_ships=_olist.new()
    _olist.push_back(fighters,confed_ships)
    confed_capitol=_olist.new()
    _olist.push_back(capitols,confed_capitol)
    _olist.push_back(confed_capitol,"cruiser")
    _olist.push_back(confed_capitol,"starrunner")
    _olist.push_back(confed_capitol,"cruiser_mk2")
    _olist.push_back(confed_capitol,"carrier")
    _olist.push_back(confed_capitol,"fleetcarrier")
    _olist.push_back(confed_capitol,"escortcarrier")
    _olist.push_back(confed_ships,"firefly")
    _olist.push_back(confed_ships,"destiny")
    _olist.push_back(confed_ships,"tian")
    _olist.push_back(confed_ships,"nova")
    _olist.push_back(confed_ships,"puma")
    _olist.push_back(confed_ships,"mongoose")
    _olist.push_back(confed_ships,"destiny")
    _olist.push_back(confed_ships,"tian")
    _olist.push_back(confed_ships,"nova")
    _olist.push_back(confed_ships,"puma")
    _olist.push_back(confed_ships,"mongoose")
    _olist.push_back(confed_ships,"avenger")

    aera_ships=_olist.new()
    aera_capitol=_olist.new()
    _olist.push_back(capitols,aera_capitol)
    _olist.push_back(aera_capitol,"yrilan")
    _olist.push_back(fighters,aera_ships)
    _olist.push_back(aera_ships,"dagger")
    _olist.push_back(aera_ships,"aeon")
    _olist.push_back(aera_ships,"aevant")
    _olist.push_back(aera_ships,"kyta")
    _olist.push_back(aera_ships,"lekra")
    _olist.push_back(aera_ships,"osprey")
    _olist.push_back(aera_ships,"kira")
    _olist.push_back(aera_ships,"butterfly")

    rlaan_ships=_olist.new()
    _olist.push_back(fighters,rlaan_ships)
    rlaan_capitol=_olist.new()
    _olist.push_back(capitols,rlaan_capitol)
    _olist.push_back(rlaan_capitol,"rlaan_cruiser")

    _olist.push_back(rlaan_ships,"skart")
    _olist.push_back(rlaan_ships,"f109vampire")
    _olist.push_back(rlaan_ships,"starfish")
    _olist.push_back(rlaan_ships,"hispidus")
    
    merchant_ships=_olist.new()
    _olist.push_back(fighters,merchant_ships)
    _olist.push_back (merchant_ships,"wayfarer")
    _olist.push_back(merchant_ships,"longhaul")

    merchant_capitol=_olist.new()
    _olist.push_back(capitols,merchant_capitol)//double referenced
    _olist.push_back (merchant_capitol,"truck")
    _olist.push_back (merchant_capitol,"cargoship")


    Xships=_olist.new()
    _olist.push_back(fighters,Xships)
    Xcapitol=_olist.new()
    _olist.push_back(capitols,Xcapitol)
    //    retro
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"avenger")

    _olist.push_back (Xcapitol,"cruiser_mk2")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"truck")


    Xships=_olist.new()
    _olist.push_back(fighters,Xships)
    Xcapitol=_olist.new()
    _olist.push_back(capitols,Xcapitol)
    //    pirates
    _olist.push_back (Xships,"revoker")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"wayfarer")
    _olist.push_back (Xships,"katar")
    _olist.push_back (Xcapitol,"cruiser_mk2")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"truck")
    _olist.push_back (Xcapitol,"truck")

   


    Xships=_olist.new()
    _olist.push_back(fighters,Xships)
    Xcapitol=_olist.new()
    _olist.push_back(capitols,Xcapitol)
    //    hunters
    _olist.push_back (Xships,"epeellcat")
    _olist.push_back (Xships,"khanjarli")
    _olist.push_back (Xships,"katar")
    _olist.push_back (Xcapitol,"cruiser_mk2")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"cruiser")



    Xships=_olist.new()
    _olist.push_back(fighters,Xships)
    Xcapitol=_olist.new()
    _olist.push_back(capitols,Xcapitol)
    //    militia
    _olist.push_back (Xships,"mongoose")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"firefly")
    _olist.push_back (Xships,"katar")
    _olist.push_back (Xcapitol,"cruiser_mk2")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"escortcarrier")
    _olist.push_back (Xcapitol,"cruiser")


    Xships=_olist.new()
    _olist.push_back(fighters,Xships)
    Xcapitol=_olist.new()
    _olist.push_back(capitols,Xcapitol)
    //    iso
    _olist.push_back (Xships,"eagle")
    _olist.push_back (Xships,"nova")
    _olist.push_back (Xships,"metron")
    _olist.push_back (Xcapitol,"cargo")
    _olist.push_back (Xcapitol,"cruiser")
    _olist.push_back (Xcapitol,"truck")


    unknown_ships=_olist.new()
    _olist.push_back(unknown_ships,"unknown_active")    
  
  getRandomShipType(ship_list):
    size=_olist.size(ship_list)
    index=random.randomint(0,size-1)
    ship_type=_olist.at(ship_list,index)

    return ship_type
    
  
  getFigther(confed_aera_or_rlaan, fighter):
    fighterlist = _olist.at (fighters,confed_aera_or_rlaan)
    fighterlist= _olist.at (fighterlist,fighter)
    return fighterlist
  
  getRandomFighterInt(confed_aera_or_rlaan):
    lst = _olist.at (fighters,confed_aera_or_rlaan)
    return getRandomShipType(lst)
  
  getNumCapitol (confed_aera_or_rlaan):
    lst = _olist.at (capitols,confed_aera_or_rlaan)
    return _olist.size (lst)
  
  getNumFighters (confed_aera_or_rlaan):
    lst = _olist.at (fighters,confed_aera_or_rlaan)
    return _olist.size (lst)
  
  getCapitol(confed_aera_or_rlaan, fighter):
    caplist = _olist.at (capitols,confed_aera_or_rlaan)
    caplist= _olist.at (caplist,fighter)
    return caplist
  
  getRandomCapitolInt(confed_aera_or_rlaan):
    lst = _olist.at (capitols,confed_aera_or_rlaan)
    return getRandomShipType(lst)
  
  getRandomFighter(faction):
    return getRandomFighter(factionToInt(faction))
  
  getRandomCapitol (faction):
    return getRandomCapitol(factionTo(faction))
  
  

