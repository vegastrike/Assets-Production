
#use this to allow more interesting weightings than are feasible to manually enter
def weightedlist(tuples):
  rettuple=()
  for i in range(0,len(tuples)):
    for j in range(tuples[i][1]):
      rettuple+=tuples[i][0],
  return rettuple

confed=0
aera=1
rlaan=2
merchant=3
merchant_guild=3
luddites=4
pirates=5
hunter=6
homeland_security=7
ISO=8
unknown=9
andolian=10
highborn=11
shaper=12
unadorned=13
purist=14
forsaken=15
LIHW=16
uln=17
dgn=18
klkk=19
mechanist=20
shmrn=21
rlaan_briin=22

aeran_merchant_marine=23
rlaan_citizen=24
merchant_citizen=25
merchant_guild_citizen=25
andolian_citizen=26
highborn_citizen=27
shaper_citizen=28
unadorned_citizen=29
purist_citizen=30
forsaken_citizen=31
LIHW_citizen=32
uln_citizen=33
dgn_citizen=34
klkk_citizen=35
mechanist_citizen=36
shmrn_citizen=37

fortress_systems={"Crucible/Cephid_17":1-.03625}
invincible_systems={}

max_flightgroups={"Gemini/Troy":25,"Gemini/Penders_Star":15,"Gemini/Junction":12,"Crucible/Cephid_17":22}
min_flightgroups={"Gemini/Troy":22,"Gemini/Penders_Star":10,"Gemini/Junction":4,"Crucible/Cephid_17":22}

factions = ("confed","aera","rlaan","merchant_guild","luddites","pirates","hunter","homeland-security","ISO","unknown","andolian","highborn","shaper","unadorned","purist","forsaken","LIHW","uln","dgn","klkk","mechanist","shmrn","rlaan_briin","aeran_merchant_marine","rlaan_citizen","merchant_guild_citizen","andolian_citizen","highborn_citizen","shaper_citizen","unadorned_citizen","purist_citizen","forsaken_citizen","LIHW_citizen","uln_citizen","dgn_citizen","klkk_citizen","mechanist_citizen","shmrn_citizen")
factiondict={}
for i in range(len(factions)):
    factiondict[factions[i]]=i
factiondict["retro"]=luddites
factiondict["militia"]=homeland_security
factiondict["merchant"]=merchant_guild_citizen

siegingfactions={"confed":10
                ,"andolian":10
                ,"highborn":10
                ,"shaper":10
                ,"unadorned":10
                ,"purist":10
                ,"forsaken":100
                ,"LIHW":50
                ,"aera":10
                ,"rlaan":10
                ,"ISO":40
                ,"luddite":100
                ,"uln":150
                ,"mechanist":9
                }

fightersPerFG=  {"confed":10
                ,"andolian":10
                ,"highborn":10
                ,"shaper":10
                ,"unadorned":10
                ,"purist":10
                ,"forsaken":3
                ,"LIHW":6
                ,"aera":8
                ,"rlaan":11
                ,"ISO":8
                ,"luddite":4
                ,"uln":2
                ,"merchant_guild":3
                ,"pirates":6
                ,"hunter":1
                ,"homeland-security":6
                ,"default":10
                ,"dgn":4
                ,"klkk":4
                ,"mechanist":8
                ,"shmrn":10
                ,"rlaan_briin":2

                ,"andolian_citizen":24*2
                ,"highborn_citizen":24*2
                ,"shaper_citizen":24*2
                ,"unadorned_citizen":24*2
                ,"purist_citizen":24*2
                ,"forsaken_citizen":6*2
                ,"LIHW_citizen":12*2
                ,"aeran_merchant_marine":24*2
                ,"rlaan_citizen":36*2
                ,"uln_citizen":12*2
                ,"merchant_guild_citizen":48*2
                ,"dgn_citizen":12*2
                ,"klkk_citizen":24*2
                ,"mechanist_citizen":12*2
                ,"shmrn_citizen":12*2
                }

capitalsPerFG=  {"confed":1
                ,"andolian":1
                ,"highborn":1
                ,"shaper":1
                ,"unadorned":1
                ,"purist":1
                ,"forsaken":1
                ,"LIHW":1
                ,"aera":1
                ,"rlaan":1
                ,"ISO":1
                ,"luddite":1
                ,"uln":1
                ,"merchant_guild":1
                ,"pirates":1
                ,"hunter":1
                ,"homeland-security":1
                ,"default":1
                ,"dgn":1
                ,"klkk":1
                ,"mechanist":1
                ,"shmrn":1
                ,"rlaan_briin":1
                ,"andolian_citizen":2
                ,"highborn_citizen":1
                ,"shaper_citizen":0
                ,"unadorned_citizen":0
                ,"purist_citizen":0
                ,"forsaken_citizen":0
                ,"LIHW_citizen":0
                ,"aeran_merchant_marine":1
                ,"rlaan_citizen":0
                ,"uln_citizen":0
                ,"merchant_guild_citizen":2
                ,"dgn_citizen":0
                ,"klkk_citizen":0
                ,"mechanist_citizen":0
                ,"shmrn_citizen":0
                }

staticFighterProduction={"luddites":3, "pirates":1}

fighterProductionRate=  {"confed":.01
                        ,"andolian":.1
                        ,"highborn":.15
                        ,"shaper":.1
                        ,"unadorned":.1
                        ,"purist":.1
                        ,"forsaken":.1
                        ,"LIHW":.05
                        ,"aera":.12
                        ,"rlaan":.11
                        ,"ISO":.14
                        ,"luddite":.04
                        ,"uln":.1
                        ,"merchant_guild":.1
                        ,"pirates":.1
                        ,"hunter":.1
                        ,"homeland-security":.05
                        ,"default":.1
                        ,"dgn":.1
                        ,"klkk":.1
                        ,"mechanist":.1
                        ,"shmrn":.08
                        ,"rlaan_briin":.05

                        ,"andolian_citizen":1
                        ,"highborn_citizen":1
                        ,"shaper_citizen":1
                        ,"unadorned_citizen":1
                        ,"purist_citizen":1
                        ,"forsaken_citizen":.3
                        ,"LIHW_citizen":.60
                        ,"aeran_merchant_marine":.80
                        ,"rlaan_citizen":1.10
                        ,"uln_citizen":1.00
                        ,"merchant_guild_citizen":3.00
                        ,"dgn_citizen":.40
                        ,"klkk_citizen":1.00
                        ,"mechanist_citizen":.80
                        ,"shmrn_citizen":.20
                        }

capitalProductionRate=  {"confed":.002
                        ,"andolian":.025
                        ,"highborn":.02
                        ,"shaper":.02
                        ,"unadorned":.02
                        ,"purist":.02
                        ,"forsaken":.02
                        ,"LIHW":.01
                        ,"aera":.024
                        ,"rlaan":.022
                        ,"ISO":.028
                        ,"luddite":.004
                        ,"uln":.02
                        ,"merchant_guild":.02
                        ,"pirates":.02
                        ,"hunter":.02
                        ,"homeland-security":.001
                        ,"default":.02
                        ,"dgn":.02
                        ,"klkk":.02
                        ,"mechanist":.02
                        ,"shmrn":.001
                        ,"rlaan_briin":.001

                        ,"andolian_citizen":.1
                        ,"highborn_citizen":.05
                        ,"shaper_citizen":.01
                        ,"unadorned_citizen":.01
                        ,"purist_citizen":.01
                        ,"forsaken_citizen":.003
                        ,"LIHW_citizen":.0060
                        ,"aeran_merchant_marine":.0080
                        ,"rlaan_citizen":.110
                        ,"uln_citizen":.0100
                        ,"merchant_guild_citizen":.200
                        ,"dgn_citizen":.0040
                        ,"klkk_citizen":.00500
                        ,"mechanist_citizen":.0080
                        ,"shmrn_citizen":.0020
                        }

#FIXME homeworlds should *exist*
homeworlds={"confed":"Sol/Sol"
                ,"aera":"enigma_sector/shelton"
                ,"rlaan":"enigma_sector/shanha"
                ,"ISO":"enigma_sector/defiance"
                }
production_centers={"confed":["Sol/Sol"]
                ,"aera":["enigma_sector/shelton"]
                ,"rlaan":["enigma_sector/shanha"]
                ,"ISO":["enigma_sector/defiance"]
                }
earnable_upgrades={} #tech tree (new)

def Precache():
	pass#fixme

useStock = (   0    ,  0   ,   0   ,     1    ,   0   ,       0     ,    0   ,         0    ,      0  ,    0,         0    ,    0     ,   0   ,     0      ,   0   ,     1     ,    1 ,  1  ,  0  ,   0 , 0 ,  1 , 1  ,      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   )#close ones are all civvies

enemies =  ((aera,aera,luddites,pirates,ISO), #confed
            (confed,confed,confed,confed,confed,confed,homeland_security,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,forsaken_citizen,LIHW,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen), #aera
            (aera,aera,aera,aera,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,luddites,luddites,luddites,hunter,highborn,highborn_citizen),#rlaan
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,forsaken,forsaken_citizen), #merchant_guild
            (confed,confed,confed,homeland_security,rlaan,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,ISO,ISO,ISO,ISO,hunter,hunter,hunter,hunter,hunter), #luddites
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,luddites,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,merchant_guild,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen), #pirates
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,luddites,rlaan,rlaan_citizen,pirates,pirates,ISO), #hunter
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,forsaken,forsaken_citizen), #homeland_security
            (confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,aera,aera,aera,pirates,luddites,luddites,luddites,hunter,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen), #ISO
            (confed,aera,rlaan,merchant_guild,luddites,pirates,hunter,homeland_security,ISO,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,uln,dgn,aeran_merchant_marine,rlaan_citizen,merchant_guild_citizen,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen,uln_citizen,dgn_citizen), #unknown
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,pirates), #andolian
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,ISO), #highborn
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,ISO), #shaper
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites), #unadorned
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,ISO,ISO), #purist
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,homeland_security), #forsaken
            (aera,aera,aeran_merchant_marine,luddites), #LIHW
            (aera,rlaan,aeran_merchant_marine,rlaan_citizen,confed), #uln
            (aera,aeran_merchant_marine,pirates), #dgn
            (aera,aeran_merchant_marine,luddites,luddites,pirates), #klkk
            (luddites,luddites,pirates,aera,aera,pirates),#mechanist
            (aera,aeran_merchant_marine,rlaan,rlaan_citizen,confed), #shmrn
            (aera,aeran_merchant_marine,luddites,pirates), #rlaan_briin
            (confed,confed,confed,confed,confed,confed,homeland_security,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,forsaken_citizen,LIHW,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen), #aeran_merchant_marine
            (aera,aera,aera,aera,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,luddites,luddites,luddites,hunter,highborn,highborn_citizen),#rlaan_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,forsaken,forsaken_citizen), #merchant_guild_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,pirates), #andolian_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,ISO), #highborn_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,ISO), #shaper_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites), #unadorned_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,ISO,ISO), #purist_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,homeland_security), #forsaken_citizen
            (aera,aera,aeran_merchant_marine,luddites), #LIHW_citizen
            (aera,rlaan,aeran_merchant_marine,rlaan_citizen,confed), #uln_citizen
            (aera,aeran_merchant_marine,pirates), #dgn_citizen
            (aera,aeran_merchant_marine,luddites,luddites,pirates), #klkk_citizen
            (luddites,luddites,pirates,aera,aera,pirates),#mechanist_citizen
            (aera,aeran_merchant_marine,rlaan,rlaan_citizen,confed) #shmrn_citizen
           )


rabble  =  ((luddites,pirates,ISO,pirates,ISO,pirates,ISO,pirates,pirates,pirates,pirates,ISO,forsaken,forsaken_citizen), #confed
            (pirates,pirates,pirates,hunter,hunter,pirates,pirates,pirates,hunter,hunter,confed,andolian,rlaan,uln,uln_citizen,uln_citizen), #aera
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan
            (pirates,luddites,pirates,luddites), #merchant_guild
            (homeland_security,homeland_security,ISO,hunter,pirates), #luddites
            (hunter,luddites,ISO,homeland_security), #pirates
            (pirates,luddites,ISO), #hunter
            (luddites,pirates,ISO,forsaken,forsaken_citizen), #homeland_security
            (homeland_security,homeland_security,homeland_security,pirates,luddites,luddites,luddites,hunter), #ISO
            (pirates,pirates,pirates,pirates,luddites,ISO,forsaken,forsaken_citizen,aera,aera,aeran_merchant_marine,rlaan,confed,uln,uln_citizen,uln_citizen,dgn), #unknown
            (luddites,luddites,pirates,luddites,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,rlaan), #andolian
            (luddites,pirates,ISO,ISO,pirates,ISO,ISO,luddites,aera,aera,aeran_merchant_marine,rlaan), #highborn
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #shaper
            (pirates,luddites,luddites,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #unadorned
            (pirates,ISO,ISO,pirates,ISO,ISO,aera,aera,aeran_merchant_marine,rlaan), #purist
            (luddites,homeland_security), #forsaken
            (luddites,luddites,luddites,aera,aera,aeran_merchant_marine,rlaan), #LIHW
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan,confed), #uln
            (pirates,pirates,pirates,), #dgn,dgn_citizen
            (luddites,luddites,pirates), #klkk
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #mechanist
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan), #shmrn
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan_briin
            (pirates,pirates,pirates,hunter,hunter,pirates,pirates,pirates,hunter,hunter,confed,andolian,rlaan,uln,uln_citizen,uln_citizen), #aeran_merchant_marine
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan_citizen
            (pirates,luddites,pirates,luddites), #merchant_guild_citizen
            (luddites,luddites,pirates,luddites,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,rlaan), #andolian_citizen
            (luddites,pirates,ISO,ISO,pirates,ISO,ISO,luddites,aera,aera,aeran_merchant_marine,rlaan), #highborn_citizen
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #shaper_citizen
            (pirates,luddites,luddites,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #unadorned_citizen
            (pirates,ISO,ISO,pirates,ISO,ISO,aera,aera,aeran_merchant_marine,rlaan), #purist_citizen
            (luddites,homeland_security), #forsaken_citizen
            (luddites,luddites,luddites,aera,aera,aeran_merchant_marine,rlaan), #LIHW_citizen
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan,confed), #uln_citizen
            (pirates,pirates,pirates,), #dgn_citizen
            (luddites,luddites,pirates), #klkk_citizen
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #mechanist_citizen
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan), #shmrn_citizen
           )

insysenemies  =  enemies

friendlies=((confed,confed,confed,confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #confed
            (aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,uln,uln_citizen,uln_citizen), #aera
            (uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen), #rlaan
            (ISO,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan,rlaan_citizen,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #merchant_guild
            (luddites,luddites,luddites), #luddites
            (forsaken,forsaken_citizen,uln,uln_citizen,uln_citizen,LIHW,LIHW_citizen,pirates,pirates,pirates,pirates,pirates), #pirates
            (confed,confed,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,hunter,hunter,hunter,hunter,merchant_guild_citizen,merchant_guild_citizen,merchant_guild), #hunter
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #homeland_security
            (ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild), #ISO
            (merchant_guild_citizen,merchant_guild_citizen,merchant_guild,), #unknown
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #andolian
            (confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #highborn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #shaper
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #unadorned
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,purist,purist_citizen,highborn,highborn_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #purist
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,pirates,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #forsaken
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #LIHW
            (uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #uln
            (dgn,dgn_citizen,dgn,dgn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen), #dgn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,klkk,klkk_citizen,klkk,klkk_citizen),  #klkk
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,uln,uln_citizen,uln_citizen),  #mechanist
            (uln,uln_citizen,uln_citizen,shmrn,shmrn_citizen,shmrn,shmrn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #shmrn
            (confed,confed,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan_briin,rlaan_briin,rlaan_briin), #rlaan_briin
            (aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,uln,uln_citizen,uln_citizen), #aeran_merchant_marine
            (uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen), #rlaan_citizen
            (ISO,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan,rlaan_citizen,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #merchant_guild_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #andolian_citizen
            (confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #highborn_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #shaper_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #unadorned_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,purist,purist_citizen,highborn,highborn_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #purist_citizen
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,pirates,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #forsaken_citizen
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #LIHW_citizen
            (uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #uln_citizen
            (dgn,dgn_citizen,dgn,dgn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen), #dgn_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,klkk,klkk_citizen,klkk,klkk_citizen),  #klkk_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,uln,uln_citizen,uln_citizen),  #mechanist_citizen
            (uln,uln_citizen,uln_citizen,shmrn,shmrn_citizen,shmrn,shmrn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #shmrn_citizen
           )

fighters = (("Lancelot","Lancelot","Gawain","Lancelot","Gawain","Progeny","Progeny","Pacifier","Schroedinger","Pacifier","Schroedinger","Derivative","Convolution","Derivative","Convolution","Goddard","Franklin","Quicksilver"), #confed
                        ("Nicander","Ariston","Areus"), #aera
                        ("Shizu","Zhuangzong","Taizong"), #rlaan
                        ("Mule","Plowshare"), #merchant_guild
                        ("Redeemer",), #luddites
                        ("Hyena","Plowshare"), #pirates
                        ("Hyena","Robin","Hyena","Robin","Sickle","Hammer","Vendetta.hunter","Entourage"), #hunter
                        ("Admonisher",), #homeland_security
                        ("Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Sickle","Sickle","Franklin","Entourage"), #ISO
                        ("Beholder",), #unknown
                        ("Schroedinger","Schroedinger","Schroedinger","Schroedinger","Schroedinger","Goddard","Goddard","Franklin","Kierkegaard"),#andolian
                        ("Gawain","Lancelot"),#highborn
                        ("Ancestor","Progeny","Progeny"),#shaper
                        ("Derivative","Determinant","Convolution","Derivative","Determinant","Convolution","Franklin"),#unadorned
                        ("Pacifier","Admonisher","Plowshare"),#purist
                        ("Hyena",),#forsaken
                        ("Sickle","Robin","Robin","Robin","Robin","Robin","Hammer"),#LIHW
                        ("Ancestor","Llama","Hyena","Entourage"),#uln
                        ("Dodo","Dodo","Dodo","Quicksilver"), #dgn
                        ("Dostoevsky","Dostoevsky","Dostoevsky","Dostoevsky","Dostoevsky","Kierkegaard"), #klkk
                        ("Llama","Convolution"),#mechanist
                        ("Dirge","Dirge","Regret"),#shmrn
                        ("Zhuangzong","Zhuangzong","Zhuangzong","Gaozong","Shizong","Shizong","Shizong"), #rlaan_briin
                        ("Nicander.escort","Nicander.escort","Ariston"), #aeran_merchant_marine
                        ("Shizu.civvie","Shizu.civvie","Shizu.civvie","Shizu.civvie","Gaozong","Shizong","Shizong","Shizong","Shizong","Shizong"), #rlaan_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie","Quicksilver.civvie","Entourage"), #merchant_guild_citizen
                        ("Franklin.civvie","Sartre.civvie","Sartre.civvie","Kafka.civvie","Kafka.civvie","Llama.civvie","Quicksilver.civvie","MacGyver"),#andolian_citizen
                        ("Hidalgo.civvie","GTIO.civvie","GTIO.civvie","H496","H496","H496","Entourage","Entourage","Entourage","Entourage","Entourage"),#highborn_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie","Quicksilver.civvie","Entourage"),#shaper_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie"),#unadorned_citizen
                        ("Mule.civvie","Llama.civvie","Plowshare.civvie","Mule.civvie","Llama.civvie","Plowshare.civvie","GTIO.civvie","Quicksilver.civvie","Diligence","H496","Entourage"),#purist_citizen
                        ("Koala.civvie","Koala.civvie","Hyena.civvie","Llama.civvie","H496"),#forsaken_citizen
                        ("Koala.civvie","Llama.civvie","Llama.civvie","Llama.civvie","Quicksilver.civvie","H496"),#LIHW_citizen
                        ("Koala.civvie","Koala.civvie","Koala.civvie","Dodo.civvie","Llama.civvie","Entourage"),#uln_citizen
                        ("Koala.civvie","Dodo.civvie","Quicksilver.civvie"), #dgn_citizen
                        ("Kafka.civvie","Kafka.civvie","Sartre.civvie","Llama.civvie",), #klkk_citizen
                        ("Koala.civvie","Kafka.civvie","Llama.civvie"),#mechanist_citizen
                        ("Koala.civvie","Koala.civvie","Kafka.civvie","Kafka.civvie","Sartre.civvie"),#shmrn_citizen

           )
isBomber = {"Areus":6,"Taizong":8,"Pacifier":5,"Goddard":4,"Kierkegaard":5,"Hammer":16,"Admonisher":10,"Areus.blank":6,"Taizong.blank":8,"Pacifier.blank":5,"Goddard.blank":4,"Hammer.blank":16,"Admonisher.blank":10}
unescortable = {"Tesla":"Ox",
	"Kahan":"Mule",
	"Clydesdale":"Ox",
	"Shundi":"Zhuangzong",
	"Ruizong":"Taizong",
	"Agesipolis":"Agasicles",
	"Watson":"Mule",
	"Leonidas":"Agasicles",
	"Anaxidamus":"Agasicles"}

capitals = (("Clydesdale","Watson","Archimedes","Kahan","Hawking"), #confed
            ("Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agasicles","Agesipolis","Leonidas","Anaxidamus","Anaxidamus","Anaxidamus","Anaxidamus","Anaxidamus",), #aera
            ("Ruizong","Ruizong","Ruizong","Shundi"), #rlaan
            ("Ox","Ox","Clydesdale"), #merchant_guild
            ("Mule",), #luddites
            ("Thales","Thales","Thales","Thales","Gleaner","Gleaner","Yeoman"), #pirates
            ("Mule",), #hunter
            ("Clydesdale",), #homeland_security
            ("Thales","Mule","Gleaner"), #ISO
            ("Beholder",), #unknown
            ("Kahan","Watson","Archimedes","Tesla","Hawking"),#andolian
            ("Clydesdale",),#highborn
            ("Clydesdale","Midwife","Midwife","Midwife"),#shaper
            ("Watson","Kahan"),#unadorned
            ("Clydesdale","Vigilance","Vigilance","Vigilance"),#purist
            ("Thales",),#forsaken
            ("Ox",),#LIHW
            ("Yeoman","Yeoman","Gleaner","Gleaner","Gleaner"),#uln
            ("Dodo",), #dgn
            ("Kahan",), #klk
            ("Watson",),#mechanist
            ("Yeoman","Gleaner"), #shmrn
            ("Ruizong","Ruizong","Shenzong",), #rlaan_briin
            ("Agasicles","Charillus","Charillus","Charillus","Charillus","Charillus","Charillus","Charillus"), #aeran_merchant_marine FIXME
            ("Shenzong",), #rlaan_citizen FIXME
            ("Mule","Mule","Mule","Mule","Mule","Mule","Ox","Ox","Clydesdale"), #merchant_guild_citizen
            ("Ox","Mule"), #andolian_citizen #FIXME - all citizens a bit b0rken
            ("Ox","Mule"), #highborn_citizen
            ("Ox","Mule","Mule","Mule","Cultivator","Cultivator"), #shaper_citizen
            ("Ox","Mule"), #unadorned_citizen
            ("Ox","Mule"), #purist_citizen
            ("Yeoman","Gleaner","Mule"), #forsaken_citizen
            ("Ox","Mule"), #LIHW_citizen
            ("Gleaner","Gleaner","Gleaner","Gleaner","Mule"), #uln_citizen
            ("Ox","Mule"), #dgn_citizen
            ("Ox","Mule"), #klk_citizen
            ("Ox","Mule"), #mechanist_citizen
            ("Ox","Mule"), #shmrn_citizen
           )

stattableexp={
        #SHIPNAME:(CHANCE_TO_HIT,CHANCE_TO_DODGE,DAMAGE,SHIELDS,ORDINANCE_DAMAGE),
        "Admonisher":(0.38,0.32,100,1410,2000),
        "Ancestor":(0.48,0.58,160,410,400),
        "Archimedes":(1,0.18,60000,2292530,1000000),
        "Ariston":(0.54,0.32,500,1190,800),
        "Areus":(0.64,0.34,400,1300,300000),
        "Mk32":(1,0.18,60000,2292530,1000000), #dupe of Archimedes FIXME
        "Beholder":(1,1,5000,6940,0),
        "Convolution":(0.54,0.7,500,620,50000),
        "Thales":(0.32,0.02,1000,10000,10000),
        "Clydesdale":(1,0.14,40000,1683740,300000),
        "Cultivator":(0.68,0.16,300,286770,0),
        "Derivative":(0.5,0.46,500,1030,400),
        "Determinant":(0.5,0.62,300,590,400),
        "Diligence":(0.52,0.14,200,18720,400), # dupe of Mule FIXME
        "Dirge":(0.38,0.38,180,290,200),
        "Dodo":(0.4,0.16,10,2500,0),
        "Dostoevsky":(0.6,0.68,200,540,2000),
        "Franklin":(0.76,0.78,200,2590,2000),
        "Gaozong":(0,0.9,0,40,0), 
        "Gawain":(0.67,0.7,500,400,400),
        "Gleaner":(0.52,0.14,200,18720,400), #dupe of Mule FIXME
        "Goddard":(0.86,0.24,800,5200,500000),
        "GTIO":(0.4,0.16,10,2500,0),
        "H496":(0.4,0.16,10,2500,0),
        "Hammer":(0.36,0.28,600,550,50000),
        "Hawking":(1,0.2,80000,1887640,0),
        "Hidalgo":(0.52,0.14,200,18720,400),
        "Ruizong":(1,0.19,25000,1800000,400000),
        "Hyena":(0.44,0.52,150,300,200),
        "Kafka":(0.4,0.16,10,2500,0),
        "Koala":(0.4,0.16,10,2500,0), # dupe of Kafka FIXME
        "Kahan":(1,0.18,25000,1400000,500000),
        "Kierkegaard":(0.86,0.24,800,5200,500000), #dupe of Goddard FIXME
        "Lancelot":(0.5,0.44,540,1250,600),
        "Llama":(0.34,0.22,200,4630,400),
        "MacGyver":(0.52,0.52,40,320,0),
        "Midwife":(1,0.16,2000,269400,3210), #dupe of Watson FIXME
        "Mule":(0.52,0.14,200,18720,400),
        "Nietzsche":(1,0.18,20000,1564400,100000),
        "Nicander":(0.52,0.46,300,910,300),
        "Nicander.escort":(0.52,0.46,300,910,300),
        "Ox":(0.68,0.16,300,286770,0),
        "Pacifier":(0.3,0.2,400,1890,100000),
        "Plowshare":(0.3,0.2,100,1380,400),
        "Progeny":(0.68,0.86,200,470,400),
        "Quicksilver":(0.52,0.52,40,320,0),
        "Redeemer":(0.38,0.38,180,290,200),
        "Robin":(0.44,0.48,300,350,200),
        "Sartre":(0.3,0.2,100,1380,400),
        "Schroedinger":(0.8,0.91,120,790,400),
        "Seaxbane":(0.44,0.48,300,350,200), # dupe of Robin FIXME
        "Shenzong":(0.52,0.52,40,320,0),
        "Shizu":(0.52,0.52,40,320,0),
        "Shizu.civvie":(0.52,0.52,40,320,0),
        "Shundi":(1,0.18,50000,2017640,3210),        
        "Sickle":(0.34,0.34,480,390,800),
        "Taizong":(0.78,0.42,440,1150,100000),
        "Tesla":(1,0.22,100000,1887640,0),
        "Tridacna":(0.68,0.16,300,286770,0), #dupe of Ox FIXME
        "Agasicles":(1,0.22,20000,1366420,600000),
        "Vendetta":(0.52,0.5,440,450,0), #dupe of Zhuangzong FIXME
        "Agesipolis":(1,0.16,50000,5738710,3210),
        "Watson":(1,0.16,2000,269400,3210),
        "Leonidas":(1,0.12,300000,8138400,2000000),
        "Yeoman":(0.68,0.16,300,286770,0), # dupe of Ox FIXME
        "Anaxidamus":(1,0.24,50000,2495160,1000000),
        "Zhuangzong":(0.52,0.5,440,450,0),
        "Shizong":(0.52,0.5,440,450,0),
        "Agricultural_Station":(1,0,10,21841060,0), #dupe of Commerce_Center FIXME
        "AsteroidFighterBase":(0.52,0,200,1512400,3210), #dupe of Refinery FIXME
        "Asteroid_Refinery":(0.4,0,10,33071210,0),
        "Asteroid_Shipyard":(0.4,0,10,33071210,0), #dupe of Asteroid_Refinery FIXME
        "Commerce_Center":(1,0,10,21841060,0),
        "Diplomatic_Center":(1,0,10,21841060,0), #dupe of Commerce_Center FIXME
        "Factory":(.02,0.02,10,13987040,0),
        "Shaper_Bio_Adaptation":(0.12,0,10,9050760,3210),
        "Fighter_Barracks":(0.12,0,100,9050760,3210),
        "Gasmine":(.02,0.02,10,13987040,0), #dupe of Factory FIXME
        "Medical":(1,0,0,2230130,0),
        "MiningBase":(1,0,100,715750,0),
        "Outpost":(0.12,0,100,9050760,3210), #dupe of Fighter_Barracks FIXME
        "Refinery":(0.4,0,10,33071210,0),
        "Relay":(0.24,0,10,3228510,0),
        "Research":(0.12,0,0,5497290,0),
        "Shipyard":(0.12,0,100,9050760,3210), #dupe of Fighter_Barracks FIXME
        "Starfortress":(1,0,750000,475993990,4000000)
        }

# stattable is generated by adding your ship/base to stattableexp, and then running log_faction_ships.py ('python log_factions_ships.py')

def GetStats ( name):
    try:
        return stattable[name]
    except:
        import debug
        debug.error( 'cannot find '+name)
        return (.5,.5,1,1,1)


capitols=capitals
capitaldict={}
for i in capitols:
    for j in i:
        capitaldict[j]=1
for i in capitols:
    for j in i:
        capitaldict[j+'.blank']=1

def isCapital(type):
    return type in capitaldict

generic_bases = ("Starfortress","Starfortress",
                 "Research","Research",
                 "Medical","Medical","Medical",
                 "Commerce_Center","Commerce_Center","Commerce_Center",
                 "Diplomatic_Center","Diplomatic_Center",
                 "Agricultural_Station","Agricultural_Station","Agricultural_Station",
                 "Factory","Factory","Factory",
                 "Shipyard","Shipyard",
                 "Gasmine","Gasmine",
                 "AsteroidFighterBase",
                 "Outpost","Outpost","Outpost","Outpost",
                 "Fighter_Barracks","Fighter_Barracks","Fighter_Barracks","Fighter_Barracks",
                 "Relay","Relay","Relay","Relay","Relay",
                 "Refinery","Refinery","Refinery","Refinery","Refinery",
                 "MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase")

bases = (generic_bases,
                 generic_bases, #aera
                 generic_bases, #rlaan
                 generic_bases, #merchant_guild
                 generic_bases, #luddites
                 generic_bases, #pirates
                 generic_bases, #hunter
                 generic_bases, #homeland_security
                 generic_bases, #ISO
                 generic_bases, #unknown
                 generic_bases, #andolian
                 generic_bases, #highborn
                 generic_bases+("Shaper_Bio_Adaptation","Shaper_Bio_Adaptation"), #shaper
                 generic_bases, #unadorned
                 generic_bases, #purist
                 generic_bases, #forsaken
                 generic_bases, #LIHW
                 generic_bases+("Asteroid_Refinery","Asteroid_Refinery"), #uln
                 generic_bases, #dgn
                 generic_bases, #klkk
                 generic_bases, #mechanist
                 generic_bases, #shmrn
                 generic_bases, #rlaan_briin
                 generic_bases, #aeran_merchant_marine
                 generic_bases, #rlaan_citizen
                 generic_bases, #merchant_guild_citizen
                 generic_bases, #andolian_citizen
                 generic_bases, #highborn_citizen
                 generic_bases, #shaper_citizen
                 generic_bases, #unadorned_citizen
                 generic_bases, #purist_citizen
                 generic_bases, #forsaken_citizen
                 generic_bases, #LIHW_citizen
                 generic_bases, #uln_citizen
                 generic_bases, #dgn_citizen
                 generic_bases, #klkk_citizen
                 generic_bases, #mechanist_citizen
                 generic_bases, #shmrn_citizen

                 )
basedict={}
for i in bases:
    for j in i:
        basedict[j]=1

def appendName(faction):
    from difficulty import usingDifficulty
    if (useStock[faction] and usingDifficulty()):
	# DON'T USE .blanks directly if possible-- preserve as templates. Use .stock where possible
        return ".stock"
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

def get_non_citizen_X_of (mylist, index):
    import vsrandom
    import VS
    enemylist = mylist[index]
    newindex = vsrandom.randrange(0,len(enemylist))
    rez=intToFaction(enemylist[newindex])
    if VS.isCitizen(rez):
        while (newindex>0):
          newindex-=1
          rez=intToFaction(enemylist[newindex])
          if not VS.isCitizen(rez):
              return rez
        while (newindex+1<len(enemylist)):
          newindex+=1
          rez=intToFaction(enemylist[newindex])
          if not VS.isCitizen(rez):
              return rez
    return rez

def get_X_of (mylist, index):
    import vsrandom
    enemylist = mylist[index]
    newindex = vsrandom.randrange(0,len(enemylist))
    return intToFaction(enemylist[newindex])


def get_enemy_of (factionname):
    return get_X_of (enemies, factionToInt(factionname))

def get_insys_enemy_of (factionname):
    return get_X_of (insysenemies, factionToInt(factionname))

def get_friend_of (factionname):
    return get_X_of (friendlies, factionToInt(factionname))

def get_rabble_of (factionname):
    return get_X_of (rabble, factionToInt(factionname))

def get_enemy_of_no_citizen (factionname):
    return get_X_of (enemies, factionToInt(factionname))
    #return get_non_citizen_X_of (enemies, factionToInt(factionname))

def get_insys_enemy_of_no_citizen (factionname):
    return get_X_of (insysenemies, factionToInt(factionname))
    #return get_non_citizen_X_of (insysenemies, factionToInt(factionname))

def get_friend_of_no_citizen (factionname):
    return get_X_of (friendlies, factionToInt(factionname))
    #return get_non_citizen_X_of (friendlies, factionToInt(factionname))

def get_rabble_of_no_citizen (factionname):
    return get_X_of (rabble, factionToInt(factionname))
    #return get_non_citizen_X_of (rabble, factionToInt(factionname))

def getRandomShipType(ship_list):
    import vsrandom
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

launch_distance_factor=1
max_radius=10000
min_forward_distance=100000 
min_distance=10000 
#print len(fightersPerFG)
#print len (fighterProductionRate)
#print len(capitalProductionRate)
#print len(enemies)
#print len(rabble)
#print len (friendlies)
#print len(fighters)
#print len(capitals)
#print len(bases)
#print len(useStock)

stattable={'Sartre.civvie': (0.29999999999999999, 0.040000000000000008, 1.3316422965503592, 2.0862995208516106, 1.7294916852909843), 'Starfortress.milspec': (1, 0.0, 12.685746445864334, 18.737139278005007, 14.255519804498629), 'Archimedes.rgspec': (1, 0.14399999999999999, 12.698159139990068, 16.902807849318268, 15.945256009614795), 'Ox.blank': (0.68000000000000005, 0.016, 0.82336196767597025, 1.8129539611895122, 0.0), 'Shipyard.rgspec': (0.12, 0.0, 5.3265691862014366, 18.487686136267396, 9.3190455597806174), 'GTIO': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Entourage': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'H496': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Kierkegaard.civvie': (0.85999999999999999, 0.048000000000000001, 1.9291316864817423, 2.4689146645192404, 3.7863142909422742), 'Determinant.blank': (0.5, 0.062, 0.82336196767597025, 0.92070143201775334, 0.86474584264549215), 'Thales.civvie': (0.32000000000000001, 0.0040000000000000001, 1.9934452517671986, 2.6575713283681091, 2.6575713283681091), 'Lancelot.stock': (0.5, 0.22, 4.5397423919134079, 5.1444330370829103, 4.6156105903555931), 'Refinery.civvie': (0.40000000000000002, 0.0, 0.69188632372745962, 4.9958145078489684, 0.0), 'Admonisher.milspec': (0.38, 0.20800000000000002, 4.3278374637886676, 6.8006264771882226, 7.1282285437387323), 'Clydesdale.blank': (1, 0.014000000000000002, 1.5287748446474638, 2.0683238803480903, 1.8194607784133421), 'Seaxbane.milspec': (0.44, 0.312, 5.3518527898938064, 5.4959626931979644, 4.9731835992663038), 'Lancelot.rgspec': (0.5, 0.35200000000000004, 7.2635878270614533, 8.2310928593326569, 7.3849769445689493), 'Ox.rgspec': (0.68000000000000005, 0.128, 6.586895741407762, 14.503631689516098, 0.0), 'Determinant.milspec': (0.5, 0.40300000000000002, 5.3518527898938064, 5.9845593081153972, 5.620847977195699), 'Ruizong.rgspec': (1, 0.15200000000000002, 11.687758544867458, 16.623653021900918, 14.887715264935927), 'Medical.milspec': (1, 0.0, 0.0, 13.707653067697777, 0.0), 'Shundi.civvie': (1, 0.035999999999999997, 3.1219338656098192, 4.1888476134123094, 2.3297613899451544), 'MiningBase.milspec': (1, 0.0, 4.3278374637886676, 12.641913865945668, 0.0), 'Lancelot.civvie': (0.5, 0.088000000000000009, 1.8158969567653633, 2.0577732148331642, 1.8462442361422373), 'Diligence.milspec': (0.52000000000000002, 0.091000000000000011, 4.9731835992663038, 9.2250404216458861, 5.620847977195699), 'Nicander.stock': (0.52000000000000002, 0.23000000000000001, 4.1168098383798508, 4.9156536219010256, 4.1168098383798508), 'Dodo.milspec': (0.40000000000000002, 0.10400000000000001, 2.2486305521142436, 7.3373880724176308, 0.0), 'Determinant.stock': (0.5, 0.31, 4.1168098383798508, 4.6035071600887667, 4.3237292132274607), 'Clydesdale.civvie': (1, 0.028000000000000004, 3.0575496892949277, 4.1366477606961807, 3.6389215568266842), 'Fighter_Barracks.blank': (0.12, 0.0, 0.66582114827517958, 2.3109607670334245, 1.1648806949725772), 'Starfortress.civvie': (1, 0.0, 3.9033065987274878, 5.7652736240015408, 4.3863137859995787), 'Refinery.rgspec': (0.40000000000000002, 0.0, 2.7675452949098385, 19.983258031395874, 0.0), 'Watson.milspec': (1, 0.10400000000000001, 7.1282285437387323, 11.725607192287649, 7.5717245173217513), 'Koala.blank': (0.40000000000000002, 0.016, 0.34594316186372981, 1.128828934218097, 0.0), 'Koala.milspec': (0.40000000000000002, 0.10400000000000001, 2.2486305521142436, 7.3373880724176308, 0.0), 'Medical.rgspec': (1, 0.0, 0.0, 16.87095762178188, 0.0), 'Agricultural_Station': (1, 0.0, 2.2486305521142436, 15.847350743729406, 0.0), 'Agricultural_Station.milspec': (1, 0.0, 2.2486305521142436, 15.847350743729406, 0.0), 'Ruizong.blank': (1, 0.019000000000000003, 1.4609698181084323, 2.0779566277376147, 1.8609644081169909), 'Schroedinger.stock': (0.80000000000000004, 0.45500000000000002, 3.4594316186372978, 4.8137669422363967, 4.3237292132274607), 'Nietzsche': (1, 0.17999999999999999, 14.287784512498186, 20.577178932710801, 16.609654901315089), 'Hyena.rgspec': (0.44, 0.41600000000000004, 5.7907237914600636, 6.586895741407762, 6.1208413529431436), 'Gaozong.civvie': (0, 0.18000000000000002, 0.0, 1.0715104009236167, 0.0), 'Redeemer': (0.38, 0.38, 7.4998458870832057, 8.1848753429082848, 7.651051691178929), 'Agricultural_Station.blank': (1, 0.0, 0.34594316186372981, 2.4380539605737548, 0.0), 'Thales': (0.32000000000000001, 0.02, 9.9672262588359928, 13.287856641840545, 13.287856641840545), 'Vigilance': (0.32000000000000001, 0.02, 9.9672262588359928, 13.287856641840545, 13.287856641840545), 'Admonisher': (0.38, 0.32000000000000001, 6.6582114827517955, 10.462502272597265, 10.966505451905741), 'Watson.blank': (1, 0.016, 1.0966505451905741, 1.8039395680442536, 1.1648806949725772), 'Anaxidamus.stock': (1, 0.12, 7.8048346640245478, 10.625350738817644, 9.9657850060092468), 'Yeoman.stock': (0.68000000000000005, 0.080000000000000002, 4.1168098383798508, 9.0647698059475612, 0.0), 'Convolution.civvie': (0.54000000000000004, 0.13999999999999999, 1.7937333586390416, 1.8556898916440965, 3.1219338656098192), 'Pacifier.civvie': (0.29999999999999999, 0.040000000000000008, 1.7294916852909843, 2.1769867295899523, 3.3219309802630179), 'Yeoman.civvie': (0.68000000000000005, 0.032000000000000001, 1.6467239353519405, 3.6259079223790245, 0.0), 'Shundi.milspec': (1, 0.11699999999999999, 10.146285063231913, 13.613754743590006, 7.5717245173217513), 'AsteroidFighterBase.milspec': (0.52000000000000002, 0.0, 4.9731835992663038, 13.343466030487237, 7.5717245173217513), 'Agasicles.rgspec': (1, 0.17600000000000002, 11.43022760999855, 16.305576497433648, 15.355684303718162), 'Relay': (0.23999999999999999, 0, 3.4594316186372978, 21.622437511886723, 0.0), 'Relay.rgspec': (0.23999999999999999, 0.0, 2.7675452949098385, 17.297950009509378, 0.0), 'Admonisher.stock': (0.38, 0.16, 3.3291057413758978, 5.2312511362986323, 5.4832527259528705), 'Commerce_Center.blank': (1, 0.0, 0.34594316186372981, 2.4380539605737548, 0.0), 'Fighter_Barracks.milspec': (0.12, 0.0, 4.3278374637886676, 15.02124498571726, 7.5717245173217513), 'Kierkegaard': (0.85999999999999999, 0.23999999999999999, 9.6456584324087107, 12.344573322596201, 18.931571454711371), 'Redeemer.civvie': (0.38, 0.076000000000000012, 1.4999691774166413, 1.6369750685816571, 1.5302103382357859), 'Research.milspec': (0.12, 0.0, 0.0, 14.553688123012776, 0.0), 'Clydesdale.stock': (1, 0.070000000000000007, 7.6438742232373187, 10.34161940174045, 9.0973038920667104), 'Kahan.rgspec': (1, 0.14399999999999999, 11.687758544867458, 16.333597141592406, 15.145257163769097), 'Leonidas.stock': (1, 0.059999999999999998, 9.0973038920667104, 11.478156968395703, 10.465784645335757), 'Pacifier.milspec': (0.29999999999999999, 0.13, 5.620847977195699, 7.075206871167345, 10.796275685854809), 'Fighter_Barracks.rgspec': (0.12, 0.0, 5.3265691862014366, 18.487686136267396, 9.3190455597806174), 'Mk32.civvie': (1, 0.035999999999999997, 3.174539784997517, 4.2257019623295671, 3.9863140024036987), 'Shundi.blank': (1, 0.017999999999999999, 1.5609669328049096, 2.0944238067061547, 1.1648806949725772), 'Dostoevsky.rgspec': (0.59999999999999998, 0.54400000000000004, 6.1208413529431436, 7.2635878270614533, 8.7732043615245932), 'Beholder.rgspec': (1, 0.80000000000000004, 9.8304007117660603, 10.208742250895879, 0.0), 'Plowshare.rgspec': (0.29999999999999999, 0.16000000000000003, 5.3265691862014366, 8.3451980834064425, 6.9179667411639372), 'Mk32.rgspec': (1, 0.14399999999999999, 12.698159139990068, 16.902807849318268, 15.945256009614795), 'Kierkegaard.stock': (0.85999999999999999, 0.12, 4.8228292162043553, 6.1722866612981004, 9.4657857273556854), 'Gasmine.stock': (0.02, 0.01, 1.7297158093186489, 11.86879372628966, 0.0), 'Shipyard.stock': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'Beholder.blank': (1, 0.10000000000000001, 1.2288000889707575, 1.2760927813619849, 0.0), 'Commerce_Center': (1, 0, 3.4594316186372978, 24.380539605737546, 0.0), 'GTIO.rgspec': (0.40000000000000002, 0.128, 2.7675452949098385, 9.0306314737447764, 0.0), 'Goddard.blank': (0.85999999999999999, 0.024, 0.96456584324087113, 1.2344573322596202, 1.8931571454711371), 'Gleaner.blank': (0.52000000000000002, 0.014000000000000002, 0.76510516911789295, 1.4192369879455209, 0.86474584264549215), 'Research.rgspec': (0.12, 0.0, 0.0, 17.912231536015724, 0.0), 'Thales.stock': (0.32000000000000001, 0.01, 4.9836131294179964, 6.6439283209202724, 6.6439283209202724), 'Shipyard.blank': (0.12, 0.0, 0.66582114827517958, 2.3109607670334245, 1.1648806949725772), 'Kahan.blank': (1, 0.017999999999999999, 1.4609698181084323, 2.0416996426990508, 1.8931571454711371), 'Gleaner.civvie': (0.52000000000000002, 0.028000000000000004, 1.5302103382357859, 2.8384739758910418, 1.7294916852909843), 'Convolution': (0.54000000000000004, 0.69999999999999996, 8.968666793195208, 9.2784494582204822, 15.609669328049096), 'Watson.rgspec': (1, 0.128, 8.7732043615245932, 14.431516544354029, 9.3190455597806174), 'Goddard.stock': (0.85999999999999999, 0.12, 4.8228292162043553, 6.1722866612981004, 9.4657857273556854), 'Hidalgo': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'Dostoevsky': (0.59999999999999998, 0.68000000000000005, 7.651051691178929, 9.0794847838268158, 10.966505451905741), 'Robin.blank': (0.44, 0.048000000000000001, 0.82336196767597025, 0.84553272203045615, 0.76510516911789295), 'Outpost.civvie': (0.12, 0.0, 1.3316422965503592, 4.6219215340668489, 2.3297613899451544), 'Hammer': (0.35999999999999999, 0.28000000000000003, 9.2312211807111861, 9.105908508571158, 15.609669328049096), 'Agricultural_Station.rgspec': (1, 0.0, 2.7675452949098385, 19.504431684590038, 0.0), 'Anaxidamus': (1, 0.23999999999999999, 15.609669328049096, 21.250701477635289, 19.931570012018494), 'Archimedes': (1, 0.17999999999999999, 15.872698924987583, 21.128509811647834, 19.931570012018494), 'Thales.milspec': (0.32000000000000001, 0.013000000000000001, 6.4786970682433953, 8.6371068171963543, 8.6371068171963543), 'Gawain.blank': (0.67000000000000004, 0.069999999999999993, 0.8968666793195208, 0.86474584264549215, 0.86474584264549215), 'Sartre.rgspec': (0.29999999999999999, 0.16000000000000003, 5.3265691862014366, 8.3451980834064425, 6.9179667411639372), 'Pacifier.stock': (0.29999999999999999, 0.10000000000000001, 4.3237292132274607, 5.4424668239748808, 8.3048274506575446), 'Dostoevsky.milspec': (0.59999999999999998, 0.44200000000000006, 4.9731835992663038, 5.9016651094874302, 7.1282285437387323), 'Agasicles': (1, 0.22, 14.287784512498186, 20.38197062179206, 19.194605379647701), 'Zhuangzong.blank': (0.52000000000000002, 0.050000000000000003, 0.87846348455575218, 0.88169836232553822, 0.0), 'Mule': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'Agasicles.civvie': (1, 0.044000000000000004, 2.8575569024996375, 4.0763941243584121, 3.8389210759295405), 'Hawking.blank': (1, 0.020000000000000004, 1.6287730413124752, 2.0848152981922534, 0.0), 'MiningBase': (1, 0, 6.6582114827517955, 19.449098255301028, 0.0), 'Factory.rgspec': (0.02, 0.016, 2.7675452949098385, 18.990069962063455, 0.0), 'Progeny.milspec': (0.68000000000000005, 0.55900000000000005, 4.9731835992663038, 5.7717291122483099, 5.620847977195699), 'Agesipolis.civvie': (1, 0.032000000000000001, 3.1219338656098192, 4.4904590583620028, 2.3297613899451544), 'Dirge.blank': (0.38, 0.038000000000000006, 0.74998458870832063, 0.81848753429082854, 0.76510516911789295), 'Redeemer.milspec': (0.38, 0.24700000000000003, 4.8748998266040839, 5.3201689728903849, 4.9731835992663038), 'Schroedinger': (0.80000000000000004, 0.91000000000000003, 6.9188632372745955, 9.6275338844727933, 8.6474584264549215), 'Dodo.blank': (0.40000000000000002, 0.016, 0.34594316186372981, 1.128828934218097, 0.0), 'Dirge.rgspec': (0.38, 0.30400000000000005, 5.9998767096665651, 6.5479002743266284, 6.1208413529431436), 'Plowshare.stock': (0.29999999999999999, 0.10000000000000001, 3.3291057413758978, 5.2157488021290259, 4.3237292132274607), 'Shipyard': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'Plowshare.milspec': (0.29999999999999999, 0.13, 4.3278374637886676, 6.7804734427677342, 5.620847977195699), 'Midwife': (1, 0.16, 10.966505451905741, 18.039395680442535, 11.64880694972577), 'MiningBase.stock': (1, 0.0, 3.3291057413758978, 9.7245491276505138, 0.0), 'Agasicles.blank': (1, 0.022000000000000002, 1.4287784512498187, 2.038197062179206, 1.9194605379647702), 'Admonisher.rgspec': (0.38, 0.25600000000000001, 5.3265691862014366, 8.370001818077812, 8.7732043615245932), 'Hawking': (1, 0.20000000000000001, 16.287730413124752, 20.848152981922532, 0.0), 'Ancestor.civvie': (0.47999999999999998, 0.11599999999999999, 1.4661833756229237, 1.7365989167363367, 1.7294916852909843), 'Hammer.rgspec': (0.35999999999999999, 0.22400000000000003, 7.3849769445689493, 7.2847268068569271, 12.487735462439277), 'Hidalgo.civvie': (0.52000000000000002, 0.028000000000000004, 1.5302103382357859, 2.8384739758910418, 1.7294916852909843), 'Derivative': (0.5, 0.46000000000000002, 8.968666793195208, 10.009828617368109, 8.6474584264549215), 'Gleaner': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'Shizu': (0.52000000000000002, 0.52000000000000002, 5.3575520046180838, 8.3264294871223026, 0.0), 'Factory': (0.02, 0.02, 3.4594316186372978, 23.737587452579319, 0.0), 'Research.civvie': (0.12, 0.0, 0.0, 4.4780578840039311, 0.0), 'Research': (0.12, 0, 0.0, 22.390289420019656, 0.0), 'Dostoevsky.blank': (0.59999999999999998, 0.068000000000000005, 0.76510516911789295, 0.90794847838268167, 1.0966505451905741), 'Mule.rgspec': (0.52000000000000002, 0.11200000000000002, 6.1208413529431436, 11.353895903564167, 6.9179667411639372), 'Diligence.stock': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'Shizu.blank': (0.52000000000000002, 0.052000000000000005, 0.53575520046180836, 0.83264294871223032, 0.0), 'Tridacna': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'GTIO.civvie': (0.40000000000000002, 0.032000000000000001, 0.69188632372745962, 2.2576578684361941, 0.0), 'Dodo': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Gasmine.rgspec': (0.02, 0.016, 2.7675452949098385, 18.990069962063455, 0.0), 'Ruizong.civvie': (1, 0.038000000000000006, 2.9219396362168646, 4.1559132554752294, 3.7219288162339819), 'Gasmine.civvie': (0.02, 0.0040000000000000001, 0.69188632372745962, 4.7475174905158637, 0.0), 'Ancestor.blank': (0.47999999999999998, 0.057999999999999996, 0.73309168781146183, 0.86829945836816835, 0.86474584264549215), 'Diligence.civvie': (0.52000000000000002, 0.028000000000000004, 1.5302103382357859, 2.8384739758910418, 1.7294916852909843), 'Mk32.blank': (1, 0.017999999999999999, 1.5872698924987585, 2.1128509811647835, 1.9931570012018494), 'Leonidas.rgspec': (1, 0.096000000000000002, 14.555686227306737, 18.365051149433125, 16.745255432537213), 'Seaxbane.civvie': (0.44, 0.096000000000000002, 1.6467239353519405, 1.6910654440609123, 1.5302103382357859), 'Midwife.milspec': (1, 0.10400000000000001, 7.1282285437387323, 11.725607192287649, 7.5717245173217513), 'Sickle.milspec': (0.34000000000000002, 0.22100000000000003, 5.7914305044505276, 5.5971661182497794, 6.2696779810656622), 'Progeny.rgspec': (0.68000000000000005, 0.68800000000000006, 6.1208413529431436, 7.1036665996902277, 6.9179667411639372), 'Medical.civvie': (1, 0.0, 0.0, 4.21773940544547, 0.0), 'Commerce_Center.milspec': (1, 0.0, 2.2486305521142436, 15.847350743729406, 0.0), 'Goddard.rgspec': (0.85999999999999999, 0.192, 7.7165267459269691, 9.8756586580769614, 15.145257163769097), 'Anaxidamus.rgspec': (1, 0.192, 12.487735462439277, 17.000561182108232, 15.945256009614795), 'Relay.civvie': (0.23999999999999999, 0.0, 0.69188632372745962, 4.3244875023773446, 0.0), 'Shizu.stock': (0.52000000000000002, 0.26000000000000001, 2.6787760023090419, 4.1632147435611513, 0.0), 'Kierkegaard.milspec': (0.85999999999999999, 0.156, 6.2696779810656622, 8.02397265968753, 12.305521445562391), 'Quicksilver.blank': (0.52000000000000002, 0.052000000000000005, 0.53575520046180836, 0.83264294871223032, 0.0), 'Gawain.rgspec': (0.67000000000000004, 0.55999999999999994, 7.1749334345561664, 6.9179667411639372, 6.9179667411639372), 'Dirge.civvie': (0.38, 0.076000000000000012, 1.4999691774166413, 1.6369750685816571, 1.5302103382357859), 'GTIO.blank': (0.40000000000000002, 0.016, 0.34594316186372981, 1.128828934218097, 0.0), 'Tridacna.rgspec': (0.68000000000000005, 0.128, 6.586895741407762, 14.503631689516098, 0.0), 'Ruizong.milspec': (1, 0.12350000000000001, 9.4963038177048098, 13.506718080294496, 12.09626865276044), 'Ruizong.stock': (1, 0.095000000000000001, 7.3048490905421612, 10.389783138688074, 9.3048220405849538), 'Derivative.blank': (0.5, 0.046000000000000006, 0.8968666793195208, 1.0009828617368111, 0.86474584264549215), 'Lancelot': (0.5, 0.44, 9.0794847838268158, 10.288866074165821, 9.2312211807111861), 'Ariston.stock': (0.54000000000000004, 0.16, 4.484333396597604, 5.1089788489320567, 4.8228292162043553), 'Areus.milspec': (0.64000000000000001, 0.22100000000000003, 5.620847977195699, 6.7245134103665674, 11.826495059686724), 'Vendetta.stock': (0.52000000000000002, 0.25, 4.3923174227787607, 4.408491811627691, 0.0), 'Gleaner.stock': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'Llama.milspec': (0.34000000000000002, 0.14300000000000002, 4.9731835992663038, 7.9151202271074013, 5.620847977195699), 'Robin.civvie': (0.44, 0.096000000000000002, 1.6467239353519405, 1.6910654440609123, 1.5302103382357859), 'Sartre.blank': (0.29999999999999999, 0.020000000000000004, 0.66582114827517958, 1.0431497604258053, 0.86474584264549215), 'Taizong.rgspec': (0.78000000000000003, 0.33600000000000002, 7.0277078764460175, 8.1349376945057852, 13.287723921052072), 'Diligence.blank': (0.52000000000000002, 0.014000000000000002, 0.76510516911789295, 1.4192369879455209, 0.86474584264549215), 'Tridacna.milspec': (0.68000000000000005, 0.10400000000000001, 5.3518527898938064, 11.78420074773183, 0.0), 'Beholder.milspec': (1, 0.65000000000000002, 7.9872005783099231, 8.2946030788529015, 0.0), 'Clydesdale.rgspec': (1, 0.11200000000000002, 12.230198757179711, 16.546591042784723, 14.555686227306737), 'Agasicles.stock': (1, 0.11, 7.1438922562490932, 10.19098531089603, 9.5973026898238505), 'Anaxidamus.blank': (1, 0.024, 1.5609669328049096, 2.125070147763529, 1.9931570012018494), 'Hammer.milspec': (0.35999999999999999, 0.18200000000000002, 6.0002937674622716, 5.918840530571253, 10.146285063231913), 'Taizong.stock': (0.78000000000000003, 0.20999999999999999, 4.3923174227787607, 5.0843360590661151, 8.3048274506575446), 'Yeoman': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'Robin.stock': (0.44, 0.23999999999999999, 4.1168098383798508, 4.2276636101522804, 3.8255258455894645), 'Sickle.blank': (0.34000000000000002, 0.034000000000000002, 0.89098930837700419, 0.86110247973073539, 0.96456584324087113), 'Ariston.milspec': (0.54000000000000004, 0.20800000000000002, 5.8296334155768852, 6.6416725036116739, 6.2696779810656622), 'Gawain.stock': (0.67000000000000004, 0.34999999999999998, 4.484333396597604, 4.3237292132274607, 4.3237292132274607), 'Areus': (0.64000000000000001, 0.34000000000000002, 8.6474584264549215, 10.345405246717796, 18.194607784133421), 'Kahan.milspec': (1, 0.11699999999999999, 9.4963038177048098, 13.27104767754383, 12.305521445562391), 'Shundi': (1, 0.17999999999999999, 15.609669328049096, 20.944238067061548, 11.64880694972577), 'Shizu.civvie': (0.52000000000000002, 0.10400000000000001, 1.0715104009236167, 1.6652858974244606, 0.0),'MacGyver': (0.52000000000000002, 0.10400000000000001, 1.0715104009236167, 1.6652858974244606, 0.0), 'Shenzong': (0.52000000000000002, 0.10400000000000001, 1.0715104009236167, 1.6652858974244606, 0.0), 'Kafka.blank': (0.40000000000000002, 0.016, 0.34594316186372981, 1.128828934218097, 0.0), 'Hyena.stock': (0.44, 0.26000000000000001, 3.6192023696625397, 4.1168098383798508, 3.8255258455894645), 'Sickle.civvie': (0.34000000000000002, 0.068000000000000005, 1.7819786167540084, 1.7222049594614708, 1.9291316864817423), 'Agesipolis.milspec': (1, 0.10400000000000001, 10.146285063231913, 14.59399193967651, 7.5717245173217513), 'Determinant.civvie': (0.5, 0.124, 1.6467239353519405, 1.8414028640355067, 1.7294916852909843), 'Goddard.civvie': (0.85999999999999999, 0.048000000000000001, 1.9291316864817423, 2.4689146645192404, 3.7863142909422742), 'Gasmine.milspec': (0.02, 0.013000000000000001, 2.2486305521142436, 15.429431844176557, 0.0), 'Areus.blank': (0.64000000000000001, 0.034000000000000002, 0.86474584264549215, 1.0345405246717796, 1.8194607784133421), 'Nietzsche.blank': (1, 0.017999999999999999, 1.4287784512498187, 2.05771789327108, 1.660965490131509), 'Convolution.blank': (0.54000000000000004, 0.069999999999999993, 0.8968666793195208, 0.92784494582204824, 1.5609669328049096), 'Franklin.milspec': (0.76000000000000001, 0.50700000000000001, 4.9731835992663038, 7.3705406451170612, 7.1282285437387323), 'Franklin.rgspec': (0.76000000000000001, 0.62400000000000011, 6.1208413529431436, 9.0714346401440746, 8.7732043615245932), 'Quicksilver.civvie': (0.52000000000000002, 0.10400000000000001, 1.0715104009236167, 1.6652858974244606, 0.0), 'MiningBase.rgspec': (1, 0.0, 5.3265691862014366, 15.559278604240824, 0.0), 'Vendetta.milspec': (0.52000000000000002, 0.32500000000000001, 5.7100126496123895, 5.7310393551159988, 0.0), 'Kafka.rgspec': (0.40000000000000002, 0.128, 2.7675452949098385, 9.0306314737447764, 0.0), 'Shipyard.milspec': (0.12, 0.0, 4.3278374637886676, 15.02124498571726, 7.5717245173217513), 'Gleaner.rgspec': (0.52000000000000002, 0.11200000000000002, 6.1208413529431436, 11.353895903564167, 6.9179667411639372), 'Factory.blank': (0.02, 0.002, 0.34594316186372981, 2.3737587452579318, 0.0), 'Derivative.civvie': (0.5, 0.092000000000000012, 1.7937333586390416, 2.0019657234736221, 1.7294916852909843), 'Yeoman.rgspec': (0.68000000000000005, 0.128, 6.586895741407762, 14.503631689516098, 0.0), 'Tridacna.blank': (0.68000000000000005, 0.016, 0.82336196767597025, 1.8129539611895122, 0.0), 'Dostoevsky.civvie': (0.59999999999999998, 0.13600000000000001, 1.5302103382357859, 1.8158969567653633, 2.1933010903811483), 'Midwife.civvie': (1, 0.032000000000000001, 2.1933010903811483, 3.6078791360885072, 2.3297613899451544), 'Determinant': (0.5, 0.62, 8.2336196767597016, 9.2070143201775334, 8.6474584264549215), 'Seaxbane.blank': (0.44, 0.048000000000000001, 0.82336196767597025, 0.84553272203045615, 0.76510516911789295), 'Taizong.civvie': (0.78000000000000003, 0.084000000000000005, 1.7569269691115044, 2.0337344236264463, 3.3219309802630179), 'Tesla.milspec': (1, 0.14300000000000002, 10.796275685854809, 13.551299438249647, 0.0), 'Hyena.blank': (0.44, 0.052000000000000005, 0.72384047393250794, 0.82336196767597025, 0.76510516911789295), 'Thales.rgspec': (0.32000000000000001, 0.016, 7.9737810070687942, 10.630285313472436, 10.630285313472436), 'Franklin.stock': (0.76000000000000001, 0.39000000000000001, 3.8255258455894645, 5.6696466500900469, 5.4832527259528705), 'Plowshare.civvie': (0.29999999999999999, 0.040000000000000008, 1.3316422965503592, 2.0862995208516106, 1.7294916852909843), 'Taizong': (0.78000000000000003, 0.41999999999999998, 8.7846348455575214, 10.16867211813223, 16.609654901315089), 'Plowshare': (0.29999999999999999, 0.20000000000000001, 6.6582114827517955, 10.431497604258052, 8.6474584264549215), 'AsteroidFighterBase.civvie': (0.52000000000000002, 0.0, 1.5302103382357859, 4.1056818555345345, 2.3297613899451544), 'Nietzsche.stock': (1, 0.089999999999999997, 7.1438922562490932, 10.288589466355401, 8.3048274506575446), 'Agricultural_Station': (1, 0, 3.4594316186372978, 24.380539605737546, 0.0), 'Ancestor.stock': (0.47999999999999998, 0.28999999999999998, 3.6654584390573088, 4.3414972918408417, 4.3237292132274607), 'Quicksilver.stock': (0.52000000000000002, 0.26000000000000001, 2.6787760023090419, 4.1632147435611513, 0.0), 'Tesla.rgspec': (1, 0.17600000000000002, 13.287723921052072, 16.678522385538027, 0.0), 'Watson': (1, 0.16, 10.966505451905741, 18.039395680442535, 11.64880694972577), 'Ancestor.rgspec': (0.47999999999999998, 0.46399999999999997, 5.8647335024916947, 6.9463956669453468, 6.9179667411639372), 'Commerce_Center.civvie': (1, 0.0, 0.69188632372745962, 4.8761079211475096, 0.0), 'Taizong.blank': (0.78000000000000003, 0.042000000000000003, 0.87846348455575218, 1.0168672118132231, 1.660965490131509), 'Areus.stock': (0.64000000000000001, 0.17000000000000001, 4.3237292132274607, 5.172702623358898, 9.0973038920667104), 'AsteroidFighterBase.stock': (0.52000000000000002, 0.0, 3.8255258455894645, 10.264204638836336, 5.8244034748628852), 'Mk32.stock': (1, 0.089999999999999997, 7.9363494624937916, 10.564254905823917, 9.9657850060092468), 'Refinery.milspec': (0.40000000000000002, 0.0, 2.2486305521142436, 16.236397150509145, 0.0), 'Sickle.rgspec': (0.34000000000000002, 0.27200000000000002, 7.1279144670160335, 6.8888198378458831, 7.7165267459269691), 'Relay.milspec': (0.23999999999999999, 0.0, 2.2486305521142436, 14.05458438272637, 0.0), 'Starfortress.blank': (1, 0.0, 1.9516532993637439, 2.8826368120007704, 2.1931568929997893), 'Gaozong.stock': (0, 0.45000000000000001, 0.0, 2.6787760023090419, 0.0), 'Franklin.civvie': (0.76000000000000001, 0.15600000000000003, 1.5302103382357859, 2.2678586600360187, 2.1933010903811483), 'Gaozong.milspec': (0, 0.58500000000000008, 0.0, 3.4824088030017544, 0.0), 'Diplomatic_Center': (0.12, 0.0, 1.3316422965503592, 4.6219215340668489, 2.3297613899451544), 'Fighter_Barracks.civvie': (0.12, 0.0, 1.3316422965503592, 4.6219215340668489, 2.3297613899451544), 'Hidalgo.milspec': (0.52000000000000002, 0.091000000000000011, 4.9731835992663038, 9.2250404216458861, 5.620847977195699), 'Schroedinger.civvie': (0.80000000000000004, 0.18200000000000002, 1.3837726474549192, 1.9255067768945588, 1.7294916852909843), 'Gasmine.blank': (0.02, 0.002, 0.34594316186372981, 2.3737587452579318, 0.0), 'Starfortress.rgspec': (1, 0.0, 15.613226394909951, 23.061094496006163, 17.545255143998315), 'Watson.civvie': (1, 0.032000000000000001, 2.1933010903811483, 3.6078791360885072, 2.3297613899451544), 'Thales.blank': (0.32000000000000001, 0.002, 0.99672262588359928, 1.3287856641840545, 1.3287856641840545), 'Shizu.rgspec': (0.52000000000000002, 0.41600000000000004, 4.2860416036944669, 6.6611435896978426, 0.0), 'Agricultural_Station.civvie': (1, 0.0, 0.69188632372745962, 4.8761079211475096, 0.0), 'Midwife.stock': (1, 0.080000000000000002, 5.4832527259528705, 9.0196978402212675, 5.8244034748628852), 'Hidalgo.stock': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'Redeemer.stock': (0.38, 0.19, 3.7499229435416028, 4.0924376714541424, 3.8255258455894645), 'Sartre': (0.29999999999999999, 0.20000000000000001, 6.6582114827517955, 10.431497604258052, 8.6474584264549215), 'Mule.blank': (0.52000000000000002, 0.014000000000000002, 0.76510516911789295, 1.4192369879455209, 0.86474584264549215), 'Archimedes.stock': (1, 0.089999999999999997, 7.9363494624937916, 10.564254905823917, 9.9657850060092468), 'Robin.rgspec': (0.44, 0.38400000000000001, 6.586895741407762, 6.7642617762436492, 6.1208413529431436), 'MiningBase.blank': (1, 0.0, 0.66582114827517958, 1.9449098255301029, 0.0), 'Nietzsche.milspec': (1, 0.11699999999999999, 9.2870599331238211, 13.37516630626202, 10.796275685854809), 'Clydesdale': (1, 0.14000000000000001, 15.287748446474637, 20.683238803480901, 18.194607784133421), 'Outpost.rgspec': (0.12, 0.0, 5.3265691862014366, 18.487686136267396, 9.3190455597806174), 'Areus.rgspec': (0.64000000000000001, 0.27200000000000002, 6.9179667411639372, 8.2763241973742367, 14.555686227306737), 'Llama.rgspec': (0.34000000000000002, 0.17600000000000002, 6.1208413529431436, 9.7416864333629558, 6.9179667411639372), 'Diligence.rgspec': (0.52000000000000002, 0.11200000000000002, 6.1208413529431436, 11.353895903564167, 6.9179667411639372), 'Koala.rgspec': (0.40000000000000002, 0.128, 2.7675452949098385, 9.0306314737447764, 0.0), 'AsteroidFighterBase.blank': (0.52000000000000002, 0.0, 0.76510516911789295, 2.0528409277672672, 1.1648806949725772), 'Progeny': (0.68000000000000005, 0.85999999999999999, 7.651051691178929, 8.879583249612784, 8.6474584264549215), 'Derivative.stock': (0.5, 0.23000000000000001, 4.484333396597604, 5.0049143086840546, 4.3237292132274607), 'Anaxidamus.milspec': (1, 0.156, 10.146285063231913, 13.812955960462938, 12.955520507812022), 'Ox.civvie': (0.68000000000000005, 0.032000000000000001, 1.6467239353519405, 3.6259079223790245, 0.0), 'Franklin.blank': (0.76000000000000001, 0.078000000000000014, 0.76510516911789295, 1.1339293300180093, 1.0966505451905741), 'Midwife.blank': (1, 0.016, 1.0966505451905741, 1.8039395680442536, 1.1648806949725772), 'Shipyard.civvie': (0.12, 0.0, 1.3316422965503592, 4.6219215340668489, 2.3297613899451544), 'Mule.civvie': (0.52000000000000002, 0.028000000000000004, 1.5302103382357859, 2.8384739758910418, 1.7294916852909843), 'Kierkegaard.rgspec': (0.85999999999999999, 0.192, 7.7165267459269691, 9.8756586580769614, 15.145257163769097), 'Mule.stock': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'Leonidas.milspec': (1, 0.078, 11.826495059686724, 14.921604058914415, 13.605520038936485), 'Diligence': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'Progeny.civvie': (0.68000000000000005, 0.17200000000000001, 1.5302103382357859, 1.7759166499225569, 1.7294916852909843), 'Determinant.rgspec': (0.5, 0.496, 6.586895741407762, 7.3656114561420267, 6.9179667411639372), 'Mule.milspec': (0.52000000000000002, 0.091000000000000011, 4.9731835992663038, 9.2250404216458861, 5.620847977195699), 'Kahan.stock': (1, 0.089999999999999997, 7.3048490905421612, 10.208498213495254, 9.4657857273556854), 'Outpost.blank': (0.12, 0.0, 0.66582114827517958, 2.3109607670334245, 1.1648806949725772), 'Relay.blank': (0.23999999999999999, 0.0, 0.34594316186372981, 2.1622437511886723, 0.0), 'Leonidas.blank': (1, 0.012, 1.8194607784133421, 2.2956313936791406, 2.0931569290671517), 'Dodo.stock': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'Nietzsche.rgspec': (1, 0.14399999999999999, 11.43022760999855, 16.46174314616864, 13.287723921052072), 'Yeoman.blank': (0.68000000000000005, 0.016, 0.82336196767597025, 1.8129539611895122, 0.0), 'Ruizong': (1, 0.19, 14.609698181084322, 20.779566277376148, 18.609644081169908), 'Quicksilver': (0.52000000000000002, 0.52000000000000002, 5.3575520046180838, 8.3264294871223026, 0.0), 'Hammer.blank': (0.35999999999999999, 0.028000000000000004, 0.92312211807111866, 0.91059085085711589, 1.5609669328049096), 'Kafka.stock': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'Goddard.milspec': (0.85999999999999999, 0.156, 6.2696779810656622, 8.02397265968753, 12.305521445562391), 'Quicksilver.milspec': (0.52000000000000002, 0.33800000000000002, 3.4824088030017544, 5.4121791666294969, 0.0), 'Redeemer.rgspec': (0.38, 0.30400000000000005, 5.9998767096665651, 6.5479002743266284, 6.1208413529431436), 'Llama.stock': (0.34000000000000002, 0.11, 3.8255258455894645, 6.0885540208518467, 4.3237292132274607), 'Kierkegaard.blank': (0.85999999999999999, 0.024, 0.96456584324087113, 1.2344573322596202, 1.8931571454711371), 'Goddard': (0.85999999999999999, 0.23999999999999999, 9.6456584324087107, 12.344573322596201, 18.931571454711371), 'Archimedes.blank': (1, 0.017999999999999999, 1.5872698924987585, 2.1128509811647835, 1.9931570012018494), 'Schroedinger.blank': (0.80000000000000004, 0.091000000000000011, 0.69188632372745962, 0.96275338844727942, 0.86474584264549215), 'Leonidas.civvie': (1, 0.024, 3.6389215568266842, 4.5912627873582812, 4.1863138581343033), 'Admonisher.civvie': (0.38, 0.064000000000000001, 1.3316422965503592, 2.092500454519453, 2.1933010903811483), 'Refinery': (0.40000000000000002, 0, 3.4594316186372978, 24.979072539244839, 0.0), 'Hidalgo.rgspec': (0.52000000000000002, 0.11200000000000002, 6.1208413529431436, 11.353895903564167, 6.9179667411639372), 'Gaozong.rgspec': (0, 0.72000000000000008, 0.0, 4.2860416036944669, 0.0), 'Hyena.civvie': (0.44, 0.10400000000000001, 1.4476809478650159, 1.6467239353519405, 1.5302103382357859), 'Seaxbane.stock': (0.44, 0.23999999999999999, 4.1168098383798508, 4.2276636101522804, 3.8255258455894645), 'AsteroidFighterBase': (0.52000000000000002, 0, 7.651051691178929, 20.528409277672672, 11.64880694972577), 'Tesla.civvie': (1, 0.044000000000000004, 3.3219309802630179, 4.1696305963845068, 0.0), 'Dirge': (0.38, 0.38, 7.4998458870832057, 8.1848753429082848, 7.651051691178929), 'Seaxbane.rgspec': (0.44, 0.38400000000000001, 6.586895741407762, 6.7642617762436492, 6.1208413529431436), 'Archimedes.milspec': (1, 0.11699999999999999, 10.317254301241929, 13.733531377571094, 12.955520507812022), 'Vendetta.blank': (0.52000000000000002, 0.050000000000000003, 0.87846348455575218, 0.88169836232553822, 0.0), 'Archimedes.civvie': (1, 0.035999999999999997, 3.174539784997517, 4.2257019623295671, 3.9863140024036987), 'Fighter_Barracks.stock': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'Relay.stock': (0.23999999999999999, 0.0, 1.7297158093186489, 10.811218755943361, 0.0), 'Dodo.civvie': (0.40000000000000002, 0.032000000000000001, 0.69188632372745962, 2.2576578684361941, 0.0), 'Gleaner.milspec': (0.52000000000000002, 0.091000000000000011, 4.9731835992663038, 9.2250404216458861, 5.620847977195699), 'Derivative.rgspec': (0.5, 0.36800000000000005, 7.1749334345561664, 8.0078628938944885, 6.9179667411639372), 'Yeoman.milspec': (0.68000000000000005, 0.10400000000000001, 5.3518527898938064, 11.78420074773183, 0.0), 'Research.stock': (0.12, 0.0, 0.0, 11.195144710009828, 0.0), 'Ariston': (0.54000000000000004, 0.32000000000000001, 8.968666793195208, 10.217957697864113, 9.6456584324087107), 'Beholder.civvie': (1, 0.20000000000000001, 2.4576001779415151, 2.5521855627239698, 0.0), 'Koala.stock': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'Mk32': (1, 0.17999999999999999, 15.872698924987583, 21.128509811647834, 19.931570012018494), 'Ox.milspec': (0.68000000000000005, 0.10400000000000001, 5.3518527898938064, 11.78420074773183, 0.0), 'Hawking.milspec': (1, 0.13, 10.587024768531089, 13.551299438249647, 0.0), 'Zhuangzong.milspec': (0.52000000000000002, 0.32500000000000001, 5.7100126496123895, 5.7310393551159988, 0.0), 'Ancestor': (0.47999999999999998, 0.57999999999999996, 7.3309168781146177, 8.6829945836816833, 8.6474584264549215), 'Ariston.rgspec': (0.54000000000000004, 0.25600000000000001, 7.1749334345561664, 8.1743661582912903, 7.7165267459269691), 'Factory.civvie': (0.02, 0.0040000000000000001, 0.69188632372745962, 4.7475174905158637, 0.0), 'Medical.blank': (1, 0.0, 0.0, 2.108869702722735, 0.0), 'Seaxbane': (0.44, 0.47999999999999998, 8.2336196767597016, 8.4553272203045609, 7.651051691178929), 'Robin': (0.44, 0.47999999999999998, 8.2336196767597016, 8.4553272203045609, 7.651051691178929), 'Regret': (0.44, 0.47999999999999998, 8.2336196767597016, 8.4553272203045609, 7.651051691178929), 'Vendetta.rgspec': (0.52000000000000002, 0.40000000000000002, 7.0277078764460175, 7.0535868986043058, 0.0),'Vendetta.hunter': (0.52000000000000002, 0.40000000000000002, 7.0277078764460175, 7.0535868986043058, 0.0), 'MiningBase.civvie': (1, 0.0, 1.3316422965503592, 3.8898196510602059, 0.0), 'Ariston.blank': (0.54000000000000004, 0.032000000000000001, 0.8968666793195208, 1.0217957697864113, 0.96456584324087113), 'Agesipolis.rgspec': (1, 0.128, 12.487735462439277, 17.961836233448011, 9.3190455597806174), 'Medical.stock': (1, 0.0, 0.0, 10.544348513613674, 0.0), 'Convolution.rgspec': (0.54000000000000004, 0.55999999999999994, 7.1749334345561664, 7.4227595665763859, 12.487735462439277), 'Schroedinger.milspec': (0.80000000000000004, 0.59150000000000003, 4.4972611042284871, 6.257897024907316, 5.620847977195699), 'Vendetta.civvie': (0.52000000000000002, 0.10000000000000001, 1.7569269691115044, 1.7633967246510764, 0.0), 'Anaxidamus.civvie': (1, 0.048000000000000001, 3.1219338656098192, 4.250140295527058, 3.9863140024036987), 'Sartre.milspec': (0.29999999999999999, 0.13, 4.3278374637886676, 6.7804734427677342, 5.620847977195699), 'Ox.stock': (0.68000000000000005, 0.080000000000000002, 4.1168098383798508, 9.0647698059475612, 0.0), 'Ox': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'Charillus': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'Cultivator': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'Hidalgo.blank': (0.52000000000000002, 0.014000000000000002, 0.76510516911789295, 1.4192369879455209, 0.86474584264549215), 'Tesla.stock': (1, 0.11, 8.3048274506575446, 10.424076490961266, 0.0), 'Gawain.milspec': (0.67000000000000004, 0.45499999999999996, 5.8296334155768852, 5.620847977195699, 5.620847977195699), 'Admonisher.blank': (0.38, 0.032000000000000001, 0.66582114827517958, 1.0462502272597265, 1.0966505451905741), 'Commerce_Center.rgspec': (1, 0.0, 2.7675452949098385, 19.504431684590038, 0.0), 'Sickle': (0.34000000000000002, 0.34000000000000002, 8.9098930837700419, 8.611024797307353, 9.6456584324087107), 'Hammer.stock': (0.35999999999999999, 0.14000000000000001, 4.6156105903555931, 4.552954254285579, 7.8048346640245478), 'Pacifier': (0.29999999999999999, 0.20000000000000001, 8.6474584264549215, 10.884933647949762, 16.609654901315089), 'Nicander.civvie': (0.52000000000000002, 0.092000000000000012, 1.6467239353519405, 1.9662614487604104, 1.6467239353519405), 'AsteroidFighterBase.rgspec': (0.52000000000000002, 0.0, 6.1208413529431436, 16.422727422138138, 9.3190455597806174), 'Clydesdale.milspec': (1, 0.091000000000000011, 9.9370364902085146, 13.444105222262586, 11.826495059686724), 'Watson.stock': (1, 0.080000000000000002, 5.4832527259528705, 9.0196978402212675, 5.8244034748628852), 'Dodo.rgspec': (0.40000000000000002, 0.128, 2.7675452949098385, 9.0306314737447764, 0.0), 'Refinery.stock': (0.40000000000000002, 0.0, 1.7297158093186489, 12.48953626962242, 0.0), 'Agricultural_Station.stock': (1, 0.0, 1.7297158093186489, 12.190269802868773, 0.0), 'Progeny.stock': (0.68000000000000005, 0.42999999999999999, 3.8255258455894645, 4.439791624806392, 4.3237292132274607), 'Tridacna.stock': (0.68000000000000005, 0.080000000000000002, 4.1168098383798508, 9.0647698059475612, 0.0), 'Pacifier.blank': (0.29999999999999999, 0.020000000000000004, 0.86474584264549215, 1.0884933647949762, 1.660965490131509), 'Factory.stock': (0.02, 0.01, 1.7297158093186489, 11.86879372628966, 0.0), 'Shundi.stock': (1, 0.089999999999999997, 7.8048346640245478, 10.472119033530774, 5.8244034748628852), 'Agasicles.milspec': (1, 0.14300000000000002, 9.2870599331238211, 13.24828090416484, 12.476493496771006), 'Shundi.rgspec': (1, 0.14399999999999999, 12.487735462439277, 16.755390453649238, 9.3190455597806174), 'Hawking.rgspec': (1, 0.16000000000000003, 13.030184330499802, 16.678522385538027, 0.0), 'Zhuangzong.rgspec': (0.52000000000000002, 0.40000000000000002, 7.0277078764460175, 7.0535868986043058, 0.0), 'Shizu.milspec': (0.52000000000000002, 0.33800000000000002, 3.4824088030017544, 5.4121791666294969, 0.0), 'Research.blank': (0.12, 0.0, 0.0, 2.2390289420019656, 0.0), 'Mk32.milspec': (1, 0.11699999999999999, 10.317254301241929, 13.733531377571094, 12.955520507812022), 'Derivative.milspec': (0.5, 0.29900000000000004, 5.8296334155768852, 6.5063886012892711, 5.620847977195699), 'Nicander.blank': (0.52000000000000002, 0.046000000000000006, 0.82336196767597025, 0.98313072438020521, 0.82336196767597025), 'Sickle.stock': (0.34000000000000002, 0.17000000000000001, 4.4549465418850209, 4.3055123986536765, 4.8228292162043553), 'Hawking.stock': (1, 0.10000000000000001, 8.143865206562376, 10.424076490961266, 0.0), 'Ariston.civvie': (0.54000000000000004, 0.064000000000000001, 1.7937333586390416, 2.0435915395728226, 1.9291316864817423), 'Commerce_Center.stock': (1, 0.0, 1.7297158093186489, 12.190269802868773, 0.0), 'Lancelot.blank': (0.5, 0.044000000000000004, 0.90794847838268167, 1.0288866074165821, 0.92312211807111866), 'Quicksilver.rgspec': (0.52000000000000002, 0.41600000000000004, 4.2860416036944669, 6.6611435896978426, 0.0), 'Kafka': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Lancelot.milspec': (0.5, 0.28600000000000003, 5.9016651094874302, 6.6877629482077836, 6.0002937674622716), 'Plowshare.blank': (0.29999999999999999, 0.020000000000000004, 0.66582114827517958, 1.0431497604258053, 0.86474584264549215), 'Gawain.civvie': (0.67000000000000004, 0.13999999999999999, 1.7937333586390416, 1.7294916852909843, 1.7294916852909843), 'Zhuangzong.stock': (0.52000000000000002, 0.25, 4.3923174227787607, 4.408491811627691, 0.0), 'Tridacna.civvie': (0.68000000000000005, 0.032000000000000001, 1.6467239353519405, 3.6259079223790245, 0.0), 'GTIO.milspec': (0.40000000000000002, 0.10400000000000001, 2.2486305521142436, 7.3373880724176308, 0.0), 'Gaozong.blank': (0, 0.090000000000000011, 0.0, 0.53575520046180836, 0.0), 'Zhuangzong': (0.52000000000000002, 0.5, 8.7846348455575214, 8.816983623255382, 0.0), 'Shizong': (0.52000000000000002, 0.5, 8.7846348455575214, 8.816983623255382, 0.0), 'Sartre.stock': (0.29999999999999999, 0.10000000000000001, 3.3291057413758978, 5.2157488021290259, 4.3237292132274607), 'Kahan.civvie': (1, 0.035999999999999997, 2.9219396362168646, 4.0833992853981016, 3.7863142909422742), 'Llama.civvie': (0.34000000000000002, 0.044000000000000004, 1.5302103382357859, 2.435421608340739, 1.7294916852909843), 'Outpost.stock': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'Midwife.rgspec': (1, 0.128, 8.7732043615245932, 14.431516544354029, 9.3190455597806174), 'Koala.civvie': (0.40000000000000002, 0.032000000000000001, 0.69188632372745962, 2.2576578684361941, 0.0), 'Gawain': (0.67000000000000004, 0.69999999999999996, 8.968666793195208, 8.6474584264549215, 8.6474584264549215), 'Pacifier.rgspec': (0.29999999999999999, 0.16000000000000003, 6.9179667411639372, 8.7079469183598093, 13.287723921052072), 'Starfortress': (1, 0, 19.516532993637437, 28.826368120007704, 21.931568929997891), 'Starfortress.stock': (1, 0.0, 9.7582664968187185, 14.413184060003852, 10.965784464998945), 'Taizong.milspec': (0.78000000000000003, 0.27300000000000002, 5.7100126496123895, 6.6096368767859497, 10.796275685854809), 'Llama': (0.34000000000000002, 0.22, 7.651051691178929, 12.177108041703693, 8.6474584264549215), 'Ancestor.milspec': (0.47999999999999998, 0.377, 4.7650959707745013, 5.6439464793930947, 5.620847977195699), 'Franklin': (0.76000000000000001, 0.78000000000000003, 7.651051691178929, 11.339293300180094, 10.966505451905741), 'Outpost': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'Progeny.blank': (0.68000000000000005, 0.086000000000000007, 0.76510516911789295, 0.88795832496127847, 0.86474584264549215), 'Leonidas': (1, 0.12, 18.194607784133421, 22.956313936791407, 20.931569290671515), 'Schroedinger.rgspec': (0.80000000000000004, 0.72800000000000009, 5.5350905898196769, 7.7020271075782354, 6.9179667411639372), 'Factory.milspec': (0.02, 0.013000000000000001, 2.2486305521142436, 15.429431844176557, 0.0), 'Dostoevsky.stock': (0.59999999999999998, 0.34000000000000002, 3.8255258455894645, 4.5397423919134079, 5.4832527259528705), 'Beholder.stock': (1, 0.5, 6.1440004448537868, 6.3804639068099238, 0.0), 'Outpost.milspec': (0.12, 0.0, 4.3278374637886676, 15.02124498571726, 7.5717245173217513), 'Medical': (1, 0, 0.0, 21.088697027227347, 0.0), 'Kahan': (1, 0.17999999999999999, 14.609698181084322, 20.416996426990508, 18.931571454711371), 'Koala': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Hyena.milspec': (0.44, 0.33800000000000002, 4.7049630805613019, 5.3518527898938064, 4.9731835992663038), 'Tesla': (1, 0.22, 16.609654901315089, 20.848152981922532, 0.0), 'Nicander': (0.52000000000000002, 0.46000000000000002, 8.2336196767597016, 9.8313072438020512, 8.2336196767597016), 'Hammer.civvie': (0.35999999999999999, 0.056000000000000008, 1.8462442361422373, 1.8211817017142318, 3.1219338656098192), 'Nicander.escort': (0.52000000000000002, 0.46000000000000002, 8.2336196767597016, 9.8313072438020512, 8.2336196767597016), 'Hammer.civvie': (0.35999999999999999, 0.056000000000000008, 1.8462442361422373, 1.8211817017142318, 3.1219338656098192), 'Robin.milspec': (0.44, 0.312, 5.3518527898938064, 5.4959626931979644, 4.9731835992663038), 'Dirge.milspec': (0.38, 0.24700000000000003, 4.8748998266040839, 5.3201689728903849, 4.9731835992663038), 'Beholder': (1, 1, 12.288000889707574, 12.760927813619848, 0.0), 'Agesipolis': (1, 0.16, 15.609669328049096, 22.452295291810014, 11.64880694972577), 'Redeemer.blank': (0.38, 0.038000000000000006, 0.74998458870832063, 0.81848753429082854, 0.76510516911789295), 'Refinery.blank': (0.40000000000000002, 0.0, 0.34594316186372981, 2.4979072539244842, 0.0), 'Convolution.milspec': (0.54000000000000004, 0.45499999999999996, 5.8296334155768852, 6.0309921478433139, 10.146285063231913), 'Agesipolis.blank': (1, 0.016, 1.5609669328049096, 2.2452295291810014, 1.1648806949725772), 'Gasmine': (0.02, 0.02, 3.4594316186372978, 23.737587452579319, 0.0), 'Hawking.civvie': (1, 0.040000000000000008, 3.2575460826249505, 4.1696305963845068, 0.0), 'Areus.civvie': (0.64000000000000001, 0.068000000000000005, 1.7294916852909843, 2.0690810493435592, 3.6389215568266842), 'Nicander.milspec': (0.52000000000000002, 0.29900000000000004, 5.3518527898938064, 6.3903497084713337, 5.3518527898938064), 'Vendetta': (0.52000000000000002, 0.5, 8.7846348455575214, 8.816983623255382, 0.0), 'Kafka.milspec': (0.40000000000000002, 0.10400000000000001, 2.2486305521142436, 7.3373880724176308, 0.0), 'Fighter_Barracks': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'Hyena': (0.44, 0.52000000000000002, 7.2384047393250794, 8.2336196767597016, 7.651051691178929), 'Agesipolis.stock': (1, 0.080000000000000002, 7.8048346640245478, 11.226147645905007, 5.8244034748628852), 'Gaozong': (0, 0.90000000000000002, 0.0, 5.3575520046180838, 0.0), 'Nicander.rgspec': (0.52000000000000002, 0.36800000000000005, 6.586895741407762, 7.8650457950416417, 6.586895741407762), 'Zhuangzong.civvie': (0.52000000000000002, 0.10000000000000001, 1.7569269691115044, 1.7633967246510764, 0.0), 'GTIO.stock': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'Kafka.civvie': (0.40000000000000002, 0.032000000000000001, 0.69188632372745962, 2.2576578684361941, 0.0), 'Convolution.stock': (0.54000000000000004, 0.34999999999999998, 4.484333396597604, 4.6392247291102411, 7.8048346640245478), 'Dirge.stock': (0.38, 0.19, 3.7499229435416028, 4.0924376714541424, 3.8255258455894645), 'Llama.blank': (0.34000000000000002, 0.022000000000000002, 0.76510516911789295, 1.2177108041703695, 0.86474584264549215), 'Tesla.blank': (1, 0.022000000000000002, 1.660965490131509, 2.0848152981922534, 0.0), 'Nietzsche.civvie': (1, 0.035999999999999997, 2.8575569024996375, 4.11543578654216, 3.3219309802630179)}
