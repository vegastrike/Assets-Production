import vsrandom
from difficulty import usingDifficulty
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
factiondict={}
for i in range(len(factions)):
    factiondict[factions[i]]=i
siegingfactions={"confed":50,
				 "aera":50,
				 "rlaan":50,
				 "ISO":200,
				 "retro":500
				 }
fightersPerFG={"confed":10
				,"aera":9
				,"ISO":8
				,"retro":4
				,"rlaan":11
				}
fighterProductionRate={"confed":.02
				,"aera":.1
				,"rlaan":.12
				,"ISO":.14
				,"default":.1
				}
capitalProductionRate={"confed":.0005
				,"aera":.005
				,"rlaan":.005
				,"ISO":.0075
				,"default":.0025
				}
homeworlds={"confed":"sol_sector/sol"
		,"aera":"enigma_sector/shelton"
		,"rlaan":"enigma_sector/shanha"
		,"ISO":"enigma_sector/defiance"
		}
useBlank = (   0    ,  0   ,   0   ,     1    ,   1   ,   1     ,    1   ,    1    ,  0  ,  0)
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
insysenemies =  ((aera,rlaan,retro,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO), #confed
            (confed,confed,confed,militia,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan,pirates,hunter,merchant,ISO), #aera
            (confed,confed,militia,aera,aera,aera,aera,aera,aera,aera,aera,pirates,retro,retro,retro,retro,retro,hunter),#rlaan
            (aera,aera,retro,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates), #merchant
            (confed,confed,confed,militia,rlaan,pirates,hunter,merchant,merchant,merchant,merchant,merchant,merchant,merchant,merchant,ISO,ISO,ISO,ISO), #retro
            (confed,confed,confed,militia,militia,militia,militia,rlaan,rlaan,retro,aera,aera,aera,merchant,merchant,merchant,merchant,merchant,merchant,ISO), #pirates
            (aera,aera,retro,rlaan), #hunter
            (aera,aera,rlaan,rlaan,retro,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO), #militia
            (confed,confed,confed,confed,confed,confed,confed,militia,militia,militia,aera,aera,pirates,retro,retro,retro,hunter), #ISO
            (confed,aera,rlaan,merchant,retro,pirates,hunter,militia,ISO) #unknown
           )




rabble =  ((retro,pirates,pirates,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO), #confed
            (rlaan,pirates,pirates,pirates,hunter,merchant,merchant,pirates,ISO), #aera
            (aera,pirates,pirates,pirates,retro,retro,retro,retro,retro,hunter),#rlaan
            (aera,aera,retro,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates), #merchant
            (confed,confed,confed,militia,rlaan,pirates,hunter,merchant,merchant,merchant,merchant,merchant,merchant,merchant,merchant,ISO,ISO,ISO,ISO), #retro
            (confed,confed,militia,militia,militia,militia,rlaan,rlaan,retro,aera,aera,aera,merchant,merchant,merchant,merchant,merchant,merchant,ISO), #pirates
            (pirates,retro), #hunter
            (aera,aera,rlaan,rlaan,retro,pirates,ISO,retro,pirates,ISO,retro,pirates,ISO), #militia
            (confed,confed,confed,confed,confed,confed,confed,militia,militia,militia,aera,pirates,retro,retro,retro,retro,retro,retro,hunter), #ISO
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
            (ISO,ISO,ISO,merchant,merchant,ISO,ISO,ISO,merchant,merchant,ISO,ISO,ISO,merchant,merchant,rlaan), #ISO
            (unknown,) #unknown
           )

fighters = (("firefly","destiny","tian","nova","puma","mongoose","destiny","tian","nova","puma","mongoose","avenger"), #confed
            ("dagger","aeon","aevant","kyta","lekra","osprey","kira","butterfly"), #aera
            ("skart","leokat","f109vampire","starfish","hispidus"), #rlaan
            ("tian","wayfarer","wayfarer","wayfarer","longhaul","longhaul","dryad"), #merchant
            ("firefly","firefly","avenger"), #retro
            ("revoker","firefly","firefly","firefly","wayfarer","katar"), #pirates
            ("epeellcat","khanjarli","katar","dryad"), #hunter
            ("mongoose","firefly","firefly","katar"), #militia
            ("eagle","nova","metron"), #ISO
            ("beholder",) #unknown
           )

isBomber = {"eagle":10,"beholder":1,"avenger":1,"butterfly":2,"khanjarli":6}

capitols = (("corvette","starrunner","cruiser","carrier","fleetcarrier","escortcarrier"), #confed
            ("yrilan",), #aera
            ("rlaan_cruiser",), #rlaan
            ("truck","cargoship"), #merchant
            ("corvette","destroyer","cruiser","truck"), #retro
            ("corvette","destroyer","truck","truck"), #pirates
            ("corvette","destroyer"), #hunter
            ("escortcarrier","escortcarrier","corvette","cruiser","destroyer"), #militia
            ("truck","cargoship","corvette","destroyer"), #ISO
            ("unknown_active",) #unknown
           )
stattable={
	"nova":(.7,.4,2,1),
	"tian":(.7,.5,1,1),
	"avenger":(.8,.3,5,2),
	"wayfarer":(.3,.2,1,1),
	"longhaul":(.5,.3,1,2),
	"khanjarli":(.4,.3,3,2),
	"epeellcat":(.6,.4,3,1),
	"firefly":(.6,.3,1,2),
	"butterfly":(.6,.3,4,1),
	"dryad":(.4,.4,1,2),
	"destroyer":(.8,.6,6,10),
	"fleetcarrier":(.4,.8,3,15),
	"carrier":(.4,.8,3,15),
	"cruiser":(.9,.7,10,14),
	"dagger":(.5,.8,2,1),
	"cargoship":(.5,.3,1,5),
	"commerce_center":(.2,.4,1,25),
	"corvette":(.7,.4,4,6),
	"destiny":(.6,.8,1,2),
	"drydock":(0,.2,0,2),
	"hispidus":(.5,.2,5,2),
	"katar":(.4,.4,2,1),
	"kira":(.8,.3,4,2),
	"kyta":(.7,.4,2,1),
	"lekra":(.6,.5,2,1),
	"leokat":(.8,.5,1,2),
	"metron":(.6,.5,1,2),
	"mongoose":(.8,.4,2,1),
	"osprey":(.6,.35,2,1),
	"relay":(.4,.3,1,10),
	"research":(.4,.2,1,12),
	"refinery":(.5,.1,1,20),
	"revoker":(.4,.5,1,20),
	"skart":(.8,.5,1,1),
	"starfish":(.9,.2,3,1),
	"starfortress":(.9,.6,15,30),
	"starrunner":(.7,.8,12,12),
	"truck":(.2,.1,1,4),
	"vark":(.5,.6,8,4),
	"vitik":(.6,.8,6,18),
	"yavok":(.9,.8,14,20),
	"yrilan":(.8,.5,2,12),
	"rlaan_cruiser":(.9,.5,2,50),
	"eagle":(.6,.4,3,2),	
	"fighter_barracks":(.4,.4,2,16),
	"escortcarrier":(.8,.5,2,12),   
	"factory":(.6,.1,2,20),
	"f109vampire":(.7,.3,2,2),
	"aeon":(.5,.5,3,1),	
	"aevant":(.5,.4,4,2),
	"beholder":(.8,.5,5,10)
   }

def GetStats ( name):
	try:
		return stattable[name]
	except:
		return (.5,.5,1,1)
capitals=capitols
capitaldict={}
for i in capitols:
	for j in i:
		capitaldict[j]=1
def isCapital(type):
	return type in capitaldict

generic_bases = ("drydock",
				 "starfortress","starfortress",
				 "research","research",
				 "fighter_barracks","fighter_barracks","fighter_barracks",
				 "relay","relay","relay",
				 "medical","medical","medical",
				 "commerce_center","commerce_center","commerce_center","commerce_center",
				 "factory","factory","factory","factory","factory","factory",
				 "MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase",
				 "refinery","refinery","refinery","refinery","refinery","refinery")
bases = (generic_bases,
		 generic_bases, #aera
		 generic_bases, #rlaan
		 generic_bases, #merchant
		 generic_bases, #retro
		 generic_bases, #pirates
		 generic_bases, #hunter
		 generic_bases, #militia
		 generic_bases, #ISO
		 generic_bases, #unknown
		 )
basedict={}
for i in bases:
  for j in i:
    basedict[j]=1

def appendName(faction):
  
  if (useBlank[faction] and usingDifficulty()):
      return ".blank"
  else:
      return ""
  
def factionToInt  (faction):
  try:
    return factiondict[faction]
  except:
    return 0
  return 0

def intToFaction (faction):
  return factions[faction]

def getMaxFactions ():
  return len(factions)

def get_X_of (mylist, index):
  enemylist = mylist[index]
  newindex = vsrandom.randrange(0,len(enemylist))
  return intToFaction(enemylist[newindex])

def get_enemy_of (factionname):
  return get_X_of (enemies, factionToInt(factionname))

def get_insys_enemy_of (factionname):
  return get_X_of (insysenemies, factionToInt(factionname))

def get_rabble_of (factionname):
  return get_X_of (rabble, factionToInt(factionname))

def get_friend_of (factionname):
  return get_X_of (friendlies, factionToInt(factionname))

def getRandomShipType(ship_list):
  index=vsrandom.randrange(0,len(ship_list))
  return ship_list[index]



def getFigher(confed_aera_or_rlaan, fighter):
  fighterlist = fighters[confed_aera_or_rlaan]
  fighterlist = fighterlist[fighter]
  return fighterlist+appendName(confed_aera_or_rlaan)

def getRandomFighterInt(confed_aera_or_rlaan):
  return getRandomShipType(fighters[confed_aera_or_rlaan])+appendName(confed_aera_or_rlaan)

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

