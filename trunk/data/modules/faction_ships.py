import random
import VS
confed=0
aera=1
rlaan=2
merchant=3
retro=4
pirates=5
hunter=6
militia=7
ISO=8
unknown=9
factions = ("confed","aera","rlaan","merchant","retro","pirates","hunter","militia","ISO","unknown")
enemies =  ((aera,aera,rlaan,rlaan,retro,pirates,ISO), #confed
            (confed,confed,confed,militia,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,pirates,hunter,merchant,ISO), #aera
            (confed,confed,militia,aera,aera,aera,aera,aera,aera,aera,aera,pirates,retro,retro,retro,retro,retro,hunter),#rlaan
            (aera,aera,retro,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates), #merchant
            (confed,confed,confed,militia,rlaan,pirates,hunter,merchant,merchant,merchant,merchant,merchant,merchant,merchant,merchant,ISO,ISO,ISO,ISO), #retro
            (confed,confed,confed,militia,militia,militia,militia,rlaan,rlaan,rlaan,retro,aera,aera,aera,merchant,merchant,merchant,merchant,merchant,merchant,ISO), #pirates
            (aera,aera,retro,rlaan), #hunter
            (aera,aera,rlaan,rlaan,retro,pirates,ISO), #militia
            (confed,confed,confed,confed,confed,confed,confed,militia,militia,militia,aera,aera,aera,pirates,retro,retro,retro,hunter), #ISO
            (confed,aera,rlaan,merchant,retro,pirates,hunter,militia,ISO) #unknown
           )

friendlies=((confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant), #confed
            (aera,aera,aera,aera,aera,aera,aera,retro), #aera
            (ISO,merchant,rlaan,rlaan,rlaan,rlaan), #rlaan
            (ISO,confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant,hunter,rlaan), #merchant
            (aera,retro,retro,retro), #retro
            (hunter,merchant,merchant,merchant,pirates,pirates,pirates,pirates,pirates), #pirates
            (ISO,confed,confed,militia,militia,merchant,hunter,hunter,hunter,hunter,hunter), #hunter
            (confed,confed,confed,militia,militia,militia,militia,merchant,merchant,merchant,merchant,hunter), #militia
            (ISO,ISO,ISO,merchant,merchant,rlaan), #ISO
            (unknown,) #unknown
           )

fighters = (("firefly","destiny","tian","nova","puma","mongoose","destiny","tian","nova","puma","mongoose","avenger"), #confed
            ("dagger","aeon","aevant","kyta","lekra","osprey","kira","butterfly"), #aera
            ("skart","f109vampire","starfish","hispidus"), #rlaan
            ("wayfarer","longhaul"), #merchant
            ("firefly","firefly","avenger"), #retro
            ("revoker","firefly","firefly","firefly","wayfarer","katar"), #pirates
            ("epeellcat","khanjarli","katar"), #hunter
            ("mongoose","firefly","firefly","katar"), #militia
            ("eagle","nova","metron"), #ISO
            ("unknown_active",) #unknown
           )

capitols = (("cruiser","starrunner","cruiser_mk2","carrier","fleetcarrier","escortcarrier"), #confed
            ("yrilan",), #aera
            ("rlaan_cruiser",), #rlaan
            ("truck","cargoship"), #merchant
            ("cruiser_mk2","cruiser","cruiser","truck"), #retro
            ("cruiser_mk2","cruiser","cruiser","truck","truck"), #pirates
            ("cruiser_mk2","cruiser","cruiser"), #hunter
            ("escortcarrier","cruiser_mk2","cruiser","cruiser"), #militia
            ("truck","cargo","cruiser"), #ISO
            ("unknown_active",) #unknown
           )
def factionToInt  (faction):
  for i in range(len(factions)):
    if (factions[i]==faction):
      return i

def intToFaction (faction):
  return factions[faction]

def getMaxFactions ():
  return len(factions)

def get_X_of (mylist, index):
  enemylist = mylist[index]
  newindex = random.randrange(0,len(enemylist))
  return intToFaction(enemylist[newindex])

def get_enemy_of (factionname):
  return get_X_of (enemies, factionToInt(factionname))

def get_friend_of (factionname):
  return get_X_of (friendlies, factionToInt(factionname))

def getRandomShipType(ship_list):
  index=random.randrange(0,len(ship_list))
  return ship_list[index]

def getFigther(confed_aera_or_rlaan, fighter):
  fighterlist = fighters[confed_aera_or_rlaan]
  fighterlist = fighterlist[fighter]
  return fighterlist

def getRandomFighterInt(confed_aera_or_rlaan):
  return getRandomShipType(fighters[confed_aera_or_rlaan])

def getNumCapitol (confed_aera_or_rlaan):
  return len(capitols[confed_aera_or_rlaan])

def getNumFighters (confed_aera_or_rlaan):
  lst = fighters[confed_aera_or_rlaan]
  return len(lst)

def getCapitol(confed_aera_or_rlaan, fighter):
  caplist = capitols[confed_aera_or_rlaan]
  caplist = caplist[fighter]
  return caplist

def getRandomCapitolInt(confed_aera_or_rlaan):
  lst = capitols[confed_aera_or_rlaan]
  return getRandomShipType(lst)

def getRandomFighter(faction):
  return getRandomFighterInt (factionToInt (faction))

def getRandomCapitol (faction):
  return getRandomCapitolInt (factionToInt (faction))

