
confed=0
aera=1
rlaan=2
merchant=3
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
factions = ("confed","aera","rlaan","merchant","luddites","pirates","hunter","homeland-security","ISO","unknown","andolian","highborn","shaper","unadorned","purist","forsaken","LIHW","uln","dgn","klkk","mechanist","shmrn","rlaan_briin")
factiondict={}
for i in range(len(factions)):
    factiondict[factions[i]]=i
factiondict["retro"]=luddites
factiondict["militia"]=homeland_security

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
		,"merchant":3
		,"pirates":6
		,"hunter":1
		,"homeland-security":6
		,"default":10
		,"dgn":4
		,"klkk":4
		,"mechanist":8
		,"shmrn":2
		,"rlaan_briin":2
		}

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
			,"merchant":.1
			,"pirates":.1
			,"hunter":.1
			,"homeland-security":.05
			,"default":.1
			,"dgn":.1
			,"klkk":.1
			,"mechanist":.1
			,"shmrn":.1
			,"rlaan_briin":.05
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
			,"merchant":.02
			,"pirates":.02
			,"hunter":.02
			,"homeland-security":.001
			,"default":.02
			,"dgn":.02
			,"klkk":.02
			,"mechanist":.02
			,"shmrn":.001
			,"rlaan_briin":.001
			}
homeworlds={"confed":"sol_sector/sol"
		,"aera":"enigma_sector/shelton"
		,"rlaan":"enigma_sector/shanha"
		,"ISO":"enigma_sector/defiance"
		}


useBlank = (   0    ,  0   ,   0   ,     1    ,   1   ,       1     ,    1   ,         0    ,      0  ,    0,         0    ,    0     ,   0   ,     0      ,   0   ,     1     ,    1 ,  1  ,  0  ,   1 , 1 ,  1 , 1)


#FIXME
#useBlank = (   0    ,  0   ,   0   ,     0    ,   0  ,       0     ,    0   ,         0    ,      0  ,    0,         0    ,    0     ,   0   ,     0      ,   0   ,     0     ,    0 ,  0  ,  0  ,   0 , 1  ,  1)


enemies =  ((aera,aera,luddites,pirates,ISO), #confed
            (confed,confed,confed,confed,confed,confed,homeland_security,rlaan,rlaan,rlaan,rlaan,rlaan,pirates,hunter,merchant,ISO,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW), #aera
            (aera,aera,aera,aera,aera,aera,aera,aera,pirates,luddites,luddites,luddites,luddites,luddites,hunter,highborn),#rlaan
            (aera,aera,luddites,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,forsaken), #merchant
            (confed,confed,confed,homeland_security,rlaan,pirates,hunter,merchant,merchant,merchant,merchant,merchant,merchant,merchant,merchant,ISO,ISO,ISO,ISO,hunter,hunter,hunter,hunter,hunter), #luddites
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,rlaan,rlaan,rlaan,luddites,aera,aera,aera,merchant,merchant,merchant,merchant,merchant,merchant,ISO,andolian,highborn,shaper,unadorned,purist), #pirates
            (aera,aera,luddites,luddites,luddites,rlaan,pirates,pirates,ISO), #hunter
            (aera,aera,luddites,pirates,ISO,forsaken), #homeland_security
            (confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,aera,aera,aera,pirates,luddites,luddites,luddites,hunter,highborn,shaper,purist), #ISO
            (confed,aera,rlaan,merchant,luddites,pirates,hunter,homeland_security,ISO,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,uln,dgn), #unknown
            (aera,aera,luddites,luddites,pirates), #andolian
            (aera,aera,luddites,pirates,ISO,ISO), #highborn
            (aera,aera,pirates,luddites,luddites,ISO), #shaper
            (aera,aera,pirates,luddites,luddites), #unadorned
            (aera,aera,pirates,ISO,ISO), #purist
            (aera,aera,luddites,homeland_security), #forsaken
            (aera,aera,luddites), #LIHW
            (aera,rlaan,confed), #uln
            (aera,pirates), #dgn
            (aera,aera,luddites,luddites,pirates), #klkk
            (luddites,luddites,pirates,aera,aera,pirates),#mechanist
            (aera,rlaan,confed), #shmrn
            (aera,luddites,pirates), #rlaan_briin
           )


rabble  =  ((luddites,pirates,ISO,pirates,ISO,pirates,ISO,pirates,pirates,pirates,pirates,ISO,forsaken), #confed
            (pirates,pirates,pirates,hunter,hunter,pirates,pirates,pirates,hunter,hunter,confed,rlaan,uln), #aera
            (pirates,pirates,pirates,pirates,aera,confed,hunter,hunter,hunter,uln),#rlaan
            (pirates,luddites,pirates,luddites), #merchant
            (homeland_security,homeland_security,ISO,hunter,pirates), #luddites
            (hunter,luddites,ISO,homeland_security), #pirates
            (pirates,luddites,ISO), #hunter
            (luddites,pirates,ISO,forsaken), #homeland_security
            (homeland_security,homeland_security,homeland_security,pirates,luddites,luddites,luddites,hunter), #ISO
            (pirates,pirates,pirates,pirates,luddites,ISO,forsaken,aera,rlaan,confed,uln,dgn), #unknown
			(luddites,luddites,pirates,luddites,pirates,pirates,pirates,aera,rlaan), #andolian
            (luddites,pirates,ISO,ISO,pirates,ISO,ISO,luddites,aera,rlaan), #highborn
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,rlaan), #shaper
            (pirates,luddites,luddites,pirates,luddites,luddites,ISO,aera,rlaan), #unadorned
            (pirates,ISO,ISO,pirates,ISO,ISO,aera,rlaan), #purist
            (luddites,homeland_security), #forsaken
            (luddites,luddites,luddites,aera,rlaan), #LIHW
            (hunter,hunter,hunter,aera,rlaan,confed), #uln
            (pirates,pirates,pirates,), #dgn
            (luddites,luddites,pirates), #klkk
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,rlaan), #mechanist
            (hunter,hunter,hunter,aera,rlaan), #shmrn
            (pirates,pirates,pirates,pirates,aera,confed,hunter,hunter,hunter,uln),#rlaan_briin
           )


insysenemies  =  enemies






friendlies=((confed,confed,confed,confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,dgn,uln), #confed
            (aera,aera,aera,aera,aera,aera,aera,aera,aera,aera,aera,aera,aera,aera,uln), #aera
            (uln,merchant,rlaan,rlaan,rlaan,rlaan,merchant,rlaan,rlaan,rlaan,rlaan), #rlaan
            (ISO,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,hunter,rlaan,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,dgn,uln), #merchant
            (luddites,luddites,luddites), #luddites
            (forsaken,uln,LIHW,pirates,pirates,pirates,pirates,pirates), #pirates
            (confed,confed,homeland_security,homeland_security,merchant,hunter,hunter,hunter,hunter,hunter,merchant), #hunter
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,dgn,uln), #homeland_security
            (ISO,ISO,ISO,merchant,merchant,ISO,ISO,ISO,merchant,merchant,ISO,ISO,ISO,merchant,merchant), #ISO
            (merchant,), #unknown
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,andolian,andolian,andolian,andolian,andolian,andolian,andolian,andolian,andolian,andolian,unadorned,forsaken,LIHW,dgn,uln),  #andolian
            (confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,highborn,highborn,highborn,highborn,highborn,highborn,highborn,highborn,highborn,highborn,highborn,shaper,purist,unadorned,shaper,purist,unadorned,dgn,uln),  #highborn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,LIHW,highborn,highborn,highborn,shaper,shaper,highborn,highborn,shaper,shaper,shaper,shaper,shaper,shaper,shaper,shaper,shaper,unadorned,dgn,dgn,dgn,dgn,dgn,dgn,dgn,dgn,dgn,uln),  #shaper
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,andolian,andolian,andolian,unadorned,unadorned,unadorned,unadorned,unadorned,unadorned,unadorned,unadorned,forsaken,LIHW,dgn,uln),  #unadorned
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,highborn,purist,highborn,purist,purist,purist,purist,purist,purist,purist,dgn,uln),  #purist
            (forsaken,forsaken,pirates,merchant,merchant,merchant,LIHW,LIHW,LIHW,LIHW), #forsaken
            (forsaken,forsaken,homeland_security,merchant,merchant,LIHW,LIHW,LIHW,LIHW), #LIHW
            (uln,uln,uln,merchant,pirates,rlaan,forsaken), #uln
            (dgn,dgn,merchant,shaper,shaper,shaper,shaper,shaper), #dgn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,andolian,andolian,andolian,andolian,andolian,andolian,andolian,unadorned,forsaken,LIHW,klkk,klkk),  #klkk			
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant,merchant,merchant,merchant,merchant,LIHW,highborn,highborn,highborn,mechanist,mechanist,mechanist,mechanist,mechanist,mechanist,shaper,shaper,shaper,shaper,unadorned,uln),  #mechanist
            (uln,shmrn,shmrn,merchant,pirates,rlaan,forsaken), #shmrn
            (confed,confed,rlaan,rlaan,rlaan,merchant,merchant,merchant,hunter,rlaan_briin,rlaan_briin,rlaan_briin) #rlaan_briin
           )

fighters = (("lancelot","lancelot","gawain","lancelot","gawain","progeny","progeny","pacifier","schroedinger","pacifier","schroedinger","derivative","convolution","derivative","convolution","goddard","franklin"), #confed
            ("aeon","aelar","aevant"), #aera
            ("idun","thrud","vidar"), #rlaan
            ("mule","plowshare","llama"), #merchant
            ("redeemer",), #luddites
            ("hyena","plowshare"), #pirates
            ("hyena","robin"), #hunter
            ("admonisher",), #homeland_security
            ("hammer","sickle","hammer","sickle","hammer","sickle","hammer","sickle","hammer","sickle","sickle","sickle","franklin"), #ISO
            ("beholder",), #unknown
			("schroedinger","schroedinger","schroedinger","schroedinger","schroedinger","goddard","goddard","franklin"),#andolian
			("gawain","lancelot"),#highborn
			("ancestor","progeny"),#shaper
			("derivative","determinant","convolution","derivative","determinant","convolution","franklin"),#unadorned
			("pacifier","admonisher","plowshare"),#purist
			("hyena",),#forsaken
			("llama","robin"),#LIHW
			("dodo","llama","hyena"),#uln
			("dodo",), #dgn
			("dostoevsky",), #klkk
			("llama","convolution"),#mechanist
			("dodo",),#shmrn
			("thrud",), #rlaan_briin
           )
isBomber = {"aevant":6,"vidar":8,"pacifier":5,"goddard":4,"hammer":16,"admonisher":10,"aevant.blank":6,"vidar.blank":8,"pacifier.blank":5,"goddard.blank":4,"hammer.blank":16,"admonisher.blank":10}

capitals = (("clydesdale","watson","archimedes","kahan","tesla"), #confed
            ("vark","vitik","yavok","yrilan"), #aera
            ("huldra","lodur"), #rlaan
            ("ox","clydesdale"), #merchant
            ("mule",), #luddites
            ("corvette",), #pirates
            ("mule",), #hunter
            ("clydesdale",), #homeland_security
            ("corvette","mule"), #ISO
            ("beholder",), #unknown
			("kahan","watson","archimedes","tesla"),#andolian
			("clydesdale",),#highborn
			("clydesdale",),#shaper
			("watson","kahan"),#unadorned
			("clydesdale",),#purist
			("corvette",),#forsaken
			("ox",),#LIHW
			("mule",),#uln
			("dodo",), #dgn
			("kahan",), #klk
			("watson",),#mechanist
			("dodo",), #shmrn
			("huldra",), #rlaan_briin
           )

stattableexp={
	#SHIPNAME:(CHANCE_TO_HIT,CHANCE_TO_DODGE,DAMAGE,SHIELDS,ORDINANCE_DAMAGE),
	"redeemer":(0.38,0.38,180,290,200),
	"ancestor":(0.48,0.58,160,410,400),
	"gawain":(0.67,0.7,500,400,400),
	"dostoevsky":(0.6,0.68,200,540,2000),
	"robin":(0.44,0.48,300,350,200),
	"hyena":(0.44,0.52,150,300,200),
	"beholder":(1,1,5000,6940,0),
	"determinant":(0.5,0.62,300,590,400),
	"sickle":(0.34,0.34,480,390,800),
	"idun":(0.52,0.52,40,320,0),
	"convolution":(0.54,0.7,500,620,50000),
	"progeny":(0.68,0.86,200,470,400),
	"thrud":(0.52,0.5,440,450,0),
	"schroedinger":(0.8,0.91,120,790,400),
	"hammer":(0.36,0.28,600,550,50000),
	"aeon":(0.52,0.46,300,910,300),
	"derivative":(0.5,0.46,500,1030,400),
	"lancelot":(0.5,0.44,540,1250,600),
	"aelar":(0.54,0.32,500,1190,800),
	"aevant":(0.64,0.34,400,1300,300000),
	"vidar":(0.78,0.42,440,1150,100000),
	"admonisher":(0.38,0.32,100,1410,2000),
	"pacifier":(0.3,0.2,400,1890,100000),
	"plowshare":(0.3,0.2,100,1380,400),
	"franklin":(0.76,0.78,200,2590,2000),
	"dodo":(0.4,0.16,10,2500,0),
	"goddard":(0.86,0.24,800,5200,500000),
	"llama":(0.34,0.22,200,4630,400),
	"mule":(0.52,0.14,200,18720,400),
	"corvette":(0.32,0.02,1000,10000,10000),
	"watson":(1,0.16,2000,269400,3210),
	"ox":(0.68,0.16,300,286770,0),
	"MiningBase":(1,0,100,715750,0),
	"vark":(1,0.22,20000,1366420,600000),
	"huldra":(1,0.2,25000,1408430,3210),
	"AsteroidFighterBase":(0.52,0,200,1512400,3210),
	"neitzsche":(1,0.18,20000,1564400,100000),
	"clydesdale":(1,0.14,40000,1683740,300000),
	"tesla":(1,0.22,100000,1887640,0),
	"lodur":(1,0.18,50000,2017640,3210),
	"medical":(1,0,0,2230130,0),
	"archimedes":(1,0.18,60000,2292530,1000000),
	"yrilan":(1,0.24,50000,2495160,1000000),
	"relay":(0.24,0,10,3228510,0),
	"research":(0.12,0,0,5497290,0),
	"vitik":(1,0.16,50000,5738710,3210),
	"yavok":(1,0.12,300000,8138400,2000000),
	"fighter_barracks":(0.12,0,100,9050760,3210),
	"factory":(.02,0.02,10,13987040,0),
	"commerce_center":(1,0,10,21841060,0),
	"refinery":(0.4,0,10,33071210,0),
	"starfortress":(1,0,750000,475993990,4000000),
	"kahan":(1,0.18,25000,1400000,500000)
	}

stattable={'admonisher.blank': (0.38, 0.16, 3.3291057413758978, 5.2312511362986323, 5.4832527259528705), 'archimedes': (1, 0.17999999999999999, 15.872698924987583, 21.128509811647834, 19.931570012018494), 'convolution': (0.54000000000000004, 0.69999999999999996, 8.968666793195208, 9.2784494582204822, 15.609669328049096), 'AsteroidFighterBase.blank': (0.52000000000000002, 0.0, 3.8255258455894645, 10.264204638836336, 5.8244034748628852), 'sickle': (0.34000000000000002, 0.34000000000000002, 8.9098930837700419, 8.611024797307353, 9.6456584324087107), 'factory.blank': (0.02, 0.01, 1.7297158093186489, 11.86879372628966, 0.0), 'pacifier': (0.29999999999999999, 0.20000000000000001, 8.6474584264549215, 10.884933647949762, 16.609654901315089), 'thrud': (0.52000000000000002, 0.5, 8.7846348455575214, 8.816983623255382, 0.0), 'vark': (1, 0.22, 14.287784512498186, 20.38197062179206, 19.194605379647701), 'progeny': (0.68000000000000005, 0.85999999999999999, 7.651051691178929, 8.879583249612784, 8.6474584264549215), 'corvette': (0.32000000000000001, 0.02, 9.9672262588359928, 13.287856641840545, 13.287856641840545), 'derivative': (0.5, 0.46000000000000002, 8.968666793195208, 10.009828617368109, 8.6474584264549215), 'starfortress': (1, 0, 19.516532993637437, 28.826368120007704, 21.931568929997891), 'idun.blank': (0.52000000000000002, 0.26000000000000001, 2.6787760023090419, 4.1632147435611513, 0.0), 'relay.blank': (0.23999999999999999, 0.0, 1.7297158093186489, 10.811218755943361, 0.0), 'pacifier.blank': (0.29999999999999999, 0.10000000000000001, 4.3237292132274607, 5.4424668239748808, 8.3048274506575446), 'determinant': (0.5, 0.62, 8.2336196767597016, 9.2070143201775334, 8.6474584264549215), 'yavok.blank': (1, 0.059999999999999998, 9.0973038920667104, 11.478156968395703, 10.465784645335757), 'relay': (0.23999999999999999, 0, 3.4594316186372978, 21.622437511886723, 0.0), 'beholder': (1, 1, 12.288000889707574, 12.760927813619848, 0.0), 'clydesdale.blank': (1, 0.070000000000000007, 7.6438742232373187, 10.34161940174045, 9.0973038920667104), 'corvette.blank': (0.32000000000000001, 0.01, 4.9836131294179964, 6.6439283209202724, 6.6439283209202724), 'huldra': (1, 0.20000000000000001, 14.609698181084322, 20.425657456149413, 11.64880694972577), 'watson': (1, 0.16, 10.966505451905741, 18.039395680442535, 11.64880694972577), 'aevant.blank': (0.64000000000000001, 0.17000000000000001, 4.3237292132274607, 5.172702623358898, 9.0973038920667104), 'yrilan': (1, 0.23999999999999999, 15.609669328049096, 21.250701477635289, 19.931570012018494), 'llama': (0.34000000000000002, 0.22, 7.651051691178929, 12.177108041703693, 8.6474584264549215), 'MiningBase': (1, 0, 6.6582114827517955, 19.449098255301028, 0.0), 'plowshare': (0.29999999999999999, 0.20000000000000001, 6.6582114827517955, 10.431497604258052, 8.6474584264549215), 'lodur.blank': (1, 0.089999999999999997, 7.8048346640245478, 10.472119033530774, 5.8244034748628852), 'vitik.blank': (1, 0.080000000000000002, 7.8048346640245478, 11.226147645905007, 5.8244034748628852), 'aelar.blank': (0.54000000000000004, 0.16, 4.484333396597604, 5.1089788489320567, 4.8228292162043553), 'refinery': (0.40000000000000002, 0, 3.4594316186372978, 24.979072539244839, 0.0), 'beholder.blank': (1, 0.5, 6.1440004448537868, 6.3804639068099238, 0.0), 'aevant': (0.64000000000000001, 0.34000000000000002, 8.6474584264549215, 10.345405246717796, 18.194607784133421), 'thrud.blank': (0.52000000000000002, 0.25, 4.3923174227787607, 4.408491811627691, 0.0), 'yavok': (1, 0.12, 18.194607784133421, 22.956313936791407, 20.931569290671515), 'dodo': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'redeemer': (0.38, 0.38, 7.4998458870832057, 8.1848753429082848, 7.651051691178929), 'admonisher': (0.38, 0.32000000000000001, 6.6582114827517955, 10.462502272597265, 10.966505451905741), 'robin.blank': (0.44, 0.23999999999999999, 4.1168098383798508, 4.2276636101522804, 3.8255258455894645), 'ancestor.blank': (0.47999999999999998, 0.28999999999999998, 3.6654584390573088, 4.3414972918408417, 4.3237292132274607), 'derivative.blank': (0.5, 0.23000000000000001, 4.484333396597604, 5.0049143086840546, 4.3237292132274607), 'vark.blank': (1, 0.11, 7.1438922562490932, 10.19098531089603, 9.5973026898238505), 'lodur': (1, 0.17999999999999999, 15.609669328049096, 20.944238067061548, 11.64880694972577), 'vidar': (0.78000000000000003, 0.41999999999999998, 8.7846348455575214, 10.16867211813223, 16.609654901315089), 'neitzsche': (1, 0.17999999999999999, 14.287784512498186, 20.577178932710801, 16.609654901315089), 'convolution.blank': (0.54000000000000004, 0.34999999999999998, 4.484333396597604, 4.6392247291102411, 7.8048346640245478), 'kahan': (1, 0.17999999999999999, 14.609698181084322, 20.416996426990508, 18.931571454711371), 'archimedes.blank': (1, 0.089999999999999997, 7.9363494624937916, 10.564254905823917, 9.9657850060092468), 'dodo.blank': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'progeny.blank': (0.68000000000000005, 0.42999999999999999, 3.8255258455894645, 4.439791624806392, 4.3237292132274607), 'starfortress.blank': (1, 0.0, 9.7582664968187185, 14.413184060003852, 10.965784464998945), 'tesla': (1, 0.22, 16.609654901315089, 20.848152981922532, 0.0), 'lancelot.blank': (0.5, 0.22, 4.5397423919134079, 5.1444330370829103, 4.6156105903555931), 'schroedinger.blank': (0.80000000000000004, 0.45500000000000002, 3.4594316186372978, 4.8137669422363967, 4.3237292132274607), 'clydesdale': (1, 0.14000000000000001, 15.287748446474637, 20.683238803480901, 18.194607784133421), 'dostoevsky': (0.59999999999999998, 0.68000000000000005, 7.651051691178929, 9.0794847838268158, 10.966505451905741), 'vidar.blank': (0.78000000000000003, 0.20999999999999999, 4.3923174227787607, 5.0843360590661151, 8.3048274506575446), 'plowshare.blank': (0.29999999999999999, 0.10000000000000001, 3.3291057413758978, 5.2157488021290259, 4.3237292132274607), 'yrilan.blank': (1, 0.12, 7.8048346640245478, 10.625350738817644, 9.9657850060092468), 'fighter_barracks.blank': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'AsteroidFighterBase': (0.52000000000000002, 0, 7.651051691178929, 20.528409277672672, 11.64880694972577), 'hammer': (0.35999999999999999, 0.28000000000000003, 9.2312211807111861, 9.105908508571158, 15.609669328049096), 'goddard': (0.85999999999999999, 0.23999999999999999, 9.6456584324087107, 12.344573322596201, 18.931571454711371), 'hyena': (0.44, 0.52000000000000002, 7.2384047393250794, 8.2336196767597016, 7.651051691178929), 'franklin.blank': (0.76000000000000001, 0.39000000000000001, 3.8255258455894645, 5.6696466500900469, 5.4832527259528705), 'redeemer.blank': (0.38, 0.19, 3.7499229435416028, 4.0924376714541424, 3.8255258455894645), 'aeon.blank': (0.52000000000000002, 0.23000000000000001, 4.1168098383798508, 4.9156536219010256, 4.1168098383798508), 'vitik': (1, 0.16, 15.609669328049096, 22.452295291810014, 11.64880694972577), 'factory': (0.02, 0.02, 3.4594316186372978, 23.737587452579319, 0.0), 'research': (0.12, 0, 0.0, 22.390289420019656, 0.0), 'llama.blank': (0.34000000000000002, 0.11, 3.8255258455894645, 6.0885540208518467, 4.3237292132274607), 'refinery.blank': (0.40000000000000002, 0.0, 1.7297158093186489, 12.48953626962242, 0.0), 'huldra.blank': (1, 0.10000000000000001, 7.3048490905421612, 10.212828728074706, 5.8244034748628852), 'ancestor': (0.47999999999999998, 0.57999999999999996, 7.3309168781146177, 8.6829945836816833, 8.6474584264549215), 'sickle.blank': (0.34000000000000002, 0.17000000000000001, 4.4549465418850209, 4.3055123986536765, 4.8228292162043553), 'commerce_center': (1, 0, 3.4594316186372978, 24.380539605737546, 0.0), 'ox': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'ox.blank': (0.68000000000000005, 0.080000000000000002, 4.1168098383798508, 9.0647698059475612, 0.0), 'mule': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'medical.blank': (1, 0.0, 0.0, 10.544348513613674, 0.0), 'idun': (0.52000000000000002, 0.52000000000000002, 5.3575520046180838, 8.3264294871223026, 0.0), 'gawain': (0.67000000000000004, 0.69999999999999996, 8.968666793195208, 8.6474584264549215, 8.6474584264549215), 'hyena.blank': (0.44, 0.26000000000000001, 3.6192023696625397, 4.1168098383798508, 3.8255258455894645), 'research.blank': (0.12, 0.0, 0.0, 11.195144710009828, 0.0), 'fighter_barracks': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'aeon': (0.52000000000000002, 0.46000000000000002, 8.2336196767597016, 9.8313072438020512, 8.2336196767597016), 'kahan.blank': (1, 0.089999999999999997, 7.3048490905421612, 10.208498213495254, 9.4657857273556854), 'commerce_center.blank': (1, 0.0, 1.7297158093186489, 12.190269802868773, 0.0), 'neitzsche.blank': (1, 0.089999999999999997, 7.1438922562490932, 10.288589466355401, 8.3048274506575446), 'aelar': (0.54000000000000004, 0.32000000000000001, 8.968666793195208, 10.217957697864113, 9.6456584324087107), 'determinant.blank': (0.5, 0.31, 4.1168098383798508, 4.6035071600887667, 4.3237292132274607), 'medical': (1, 0, 0.0, 21.088697027227347, 0.0), 'MiningBase.blank': (1, 0.0, 3.3291057413758978, 9.7245491276505138, 0.0), 'goddard.blank': (0.85999999999999999, 0.12, 4.8228292162043553, 6.1722866612981004, 9.4657857273556854), 'lancelot': (0.5, 0.44, 9.0794847838268158, 10.288866074165821, 9.2312211807111861), 'robin': (0.44, 0.47999999999999998, 8.2336196767597016, 8.4553272203045609, 7.651051691178929), 'watson.blank': (1, 0.080000000000000002, 5.4832527259528705, 9.0196978402212675, 5.8244034748628852), 'dostoevsky.blank': (0.59999999999999998, 0.34000000000000002, 3.8255258455894645, 4.5397423919134079, 5.4832527259528705), 'franklin': (0.76000000000000001, 0.78000000000000003, 7.651051691178929, 11.339293300180094, 10.966505451905741), 'tesla.blank': (1, 0.11, 8.3048274506575446, 10.424076490961266, 0.0), 'gawain.blank': (0.67000000000000004, 0.34999999999999998, 4.484333396597604, 4.3237292132274607, 4.3237292132274607), 'mule.blank': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'schroedinger': (0.80000000000000004, 0.91000000000000003, 6.9188632372745955, 9.6275338844727933, 8.6474584264549215), 'hammer.blank': (0.35999999999999999, 0.14000000000000001, 4.6156105903555931, 4.552954254285579, 7.8048346640245478)}



def GetStats ( name):
	try:
		return stattable[name]
	except:
		print 'cannot find '+name
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

generic_bases = ("starfortress","starfortress",
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
		 generic_bases, #luddites
		 generic_bases, #pirates
		 generic_bases, #hunter
		 generic_bases, #homeland_security
		 generic_bases, #ISO
		 generic_bases, #unknown
		 generic_bases,#andolian
		 generic_bases,#highborn
		 generic_bases,#shaper
		 generic_bases,#unadorned
		 generic_bases,#purist
		 generic_bases,#forsaken
		 generic_bases,#LIHW
		 generic_bases,#uln
		 generic_bases, #dgn
		 generic_bases, #klkk		 
		 generic_bases, #mechanist		 
		 generic_bases, #shmrn
		 generic_bases, #rlaan_briin
		 )
basedict={}
for i in bases:
  for j in i:
    basedict[j]=1

def appendName(faction):
  from difficulty import usingDifficulty
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
  import vsrandom
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

