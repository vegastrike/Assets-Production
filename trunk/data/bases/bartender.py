import Base
import VS
import vsrandom

tender={"default":('Hello! Lots of travellers about. Have yourself a seat and enjoy a nice cool fuzzy buzzer.',
             'Bottoms up for ye olde bartender, eh?',
             'Tilt back a nice cool one, friend.',
             "News is sparse around here, check back with me later when I've talked with some more of the haulers coming in later today.",
             'Shh looks like someone is watching. Watch your back.',
             "Have one on the house, it's happy hour!",
             "If you're as much a smuggler as I think you are, you had better watch your P's and Q's around this place.",
             'Got any stories to tell? Last week I had a patron who just could not stop talking about his battles with pirates.',
             "A nice drink and a bit o' talk is what I live for.",
             "Have you heard what's been on the news recently. It ain't pretty!",
             "Hello there, friend. What can I get you? Sorry, I don't have any of the good stuff left. I had a transport bringing in new beverages from the Uln border, but there was an... accident. Apparently, some of that stuff is more flamable than napalm! How was I to know?",
             "So what's your take on the war? A friend of mine in the Navy told me the Aera and Rlaan have fought each other into a standstill on their border.  Word is that both sides are moving towards some sort of unofficial cease-fire. Won't be long before everything's quiet on that front.  When that happens, the Aera will bring all of their high-tech weapons to bear on us. Things aren't looking good.",
             "This fellow brought a jhorg in here yesterday. Ever heard about the jhorg? They're small scaly creatures from New Bremen that can mimic everything you say with perfect accuracy. Forget parrots, these things are better than tape recorders!",
             "A couple of goons from the IntelSec came in here earlier looking for some guy named Jensen. Wouldn't say what it was about, but let me tell you, whatever it was, I was happy when they left. I swear, half the bar found excuses to be elsewhere the moment those two guys entered, and I don't blame them.",
             "The pirates out on the frontier are getting more organized by the day. I hear they've overrun entire systems and colonies. Some of the guys are placing bets on what will bring about our fall first. The pirates from within or the Aera from the outside?",
             "This captain of a Wayfarer came in here the other day, looking like she could really use a drink. It turned out she had been chased by pirates across three systems! Persistant little buggers, aren't they? And the militia wasn't much help.",
             "Every so often, an Uln comes in here. They have their own civilian sector pretty much like our own, and sometimes a couple of their privateers find their way across the border. But let me tell you, never give them beer. One of them had that, and he got into some sort of violent spasms and threw up over the whole bar. Not a pretty sight.",
             "A woman came in here the other day carrying one of those fancy Aera energy pistols in her belt. Don't ask me how she managed to get her hands on one of those, but even the roughest of my customers made sure to stay out of her way.",
             "A mercenary outfit, the 'Red Condors', came in here a while ago. Real tough-looking types. I expected trouble, but they quietly finished their drinks and left. Glad there's still some professionalism out there.",
             "Can I get you anything? Whiskey? Vodka? Aarnbach's Acid? I'm all for being social, but I do have a business to run.",
             "There's a lot of people complaining about the pirates, but I don't mind them so much.  The Confed and the Merchies know they need a running merchant operation in the outlying systems, but they haven't got the resources to patrol every trade lane for pirates, so they need people who can look after themselves. People like you and me. And that's why they go easy on drafting our kind.",
             "A toast to the men and women of the Confederate Armed Forces! If not for them, we'd all be learning how to speak Aera right about now. If those things even have vocal chords.",
             "Hey, did you hear the news? Word is that the 5th Fleet under Admiral Johansson managed to bag a whole bunch of those nasty Aeran cruisers in a battle not far from here! Maybe this war is winnable after all!",
             "We might have had some luck smashing some of the outlying Aeran outposts, but I hear their planets are a tough nut to crack. The HCS Zhukov tracked a Rlaan battle fleet as it entered orbit around one of the planets, but then it simply disappeared off their scopes! The fleet that is, not the planet.",
             ),
        "pirates":("You've got a lot of nerve coming in here looking like that, pal! This joint enforces a strict dress-code. Here, put this eye-patch on before you cause a scene. And ruffle your hair a bit, or someone might think you're with the Navy!",
                  "If you have a weapon on you, make sure it remains out of sight. The crews of the Skalawag and the Black Death duked it out in here a couple of hours ago, and some people got killed. The last thing we need right now is someone waving his gun around.",
                  "Some idiots from the ISO came in here yesterday handing out phamphlets and bothering the customers. They wouldn't take a hint, so I had them thrown out. I don't know who's worst, the ISO or those religious fanatics they fight with all the time.",
                  "You know about those Rlaan? Supposedly, they never attack unarmed vessels. Well, word is there's this rogue Rlaan cruiser hiding out near here. Something happened to the officers and they went all psychotic-like. Fled to our side of the border when their own Navy chased 'em down. I hear it attacks anything or anyone that comes in its way.",
                  "What are ye pesterin' me for, pal? If you want to be a pirate, you should go talk to the three important-looking pirates in the next room! Wait a second...",
                  "Kasper Foch, now there's a guy you don't want to mess with. He's the pirate captain that entered an ion storm and flew out again without a scratch, while his three Militia pursuers were never heard of again. Then there's this story going around of how he single-handedly took out a Confed Missile Cruiser, but if ya want my opinion, I think that one's bunk.",
                  "There's a lot of deserters from the Navy around here these days. Purist and Indep punks they drafted off the street, taught how to fly and then handed a ship. You figure the guys at HQ would be smarter than that.",
                  "A Rlaan transport can be a good target, if you're willing to take the risk. If those guys see you attacking one of their unarmed ships... well, sometimes they just won't stop hunting you! And you've heard what they do to humans they capture alive, haven't you?",
                  "You know, if we lose the war against the Aera, it probably won't matter much, because the majority of us won't be around to see it, but what if we win? The whole fleet would return to peacekeeping duties in human systems, and it would mean the end of space piracy as we know it!",
                  "Hey, I hope your ship has a large cargo hold. We could always use some more smugglers out there, distributing our goods. Can you believe that there are some colonists out there who still don't know the true glory of Khaisalantimin F62, or as most people just call it, 'khais'?",
                  "This assassin came in here a while ago. Ex-Special Forces guy. Apparently, the government sent some of his collegues to silence him for good after he'd carried out a particularly nasty mission in Rlaan space, but he made it out and now he'll do any job for money.",),
        "refinery":("Sorry for the broken glass on the floor. The base was shook up a bit a couple of hours ago. Apparently, some guy on approach lost control and crashed right into the side of the station. Don't worry, it's nothing our damage control crews can't handle, but the poor guy who crashed won't be flying again. Or breathing, for that matter."),
        "military":("A Special Forces unit came through here this morning. Real quiet guys. Looked like they'd seen a lot of action. From what I could gather, they were going to catch a transport out of here and into the fray again later tonight.",
                    "This Army captain had a drink here yesterday. Tall guy from Mars. Now, I've seen a lot, but this guy... half his face, both of his legs and his left arm had all been replaced with cybernetics due to injuries he'd taken on the field. If it was all with the Mechanist aesthetic, it might have been impressive, but he visually reeked of military hack job. He looked a bit clumsy, it was obvious there hadn't been many nerve endings left to connect to anything.",
                    "Some idiots from the ISO came in here yesterday handing out phamphlets and bothering the customers. They wouldn't take a hint, so I had them thrown out. I don't know who's worst, the ISO or those luddite religious fanatics that fight with you all the time.",
                    "You know about those Rlaan? Supposedly, they never attack unarmed vessels. Well, word is there's this rogue Rlaan cruiser hiding out near here. Fled to our side of the border when their own Star Force had enough of them. I hear it attacks anything or anyone that comes in its way.",
                    "A couple of guys from the Confederate Air Corp were here a while back. We don't get many of those here usually. They may rely on the Navy for transportation between planets, but those Air Corp boys and girls are solid gold when it comes to campaigns planetside!",
                    "Hey, are you a mercenary? We've got plenty of missions here for you to fly, if you're willing. The fleet is spread thin as it is, so if you want to do your part, you're more than welcome!",),
        "iso":("4B4ND0N TH3 R4NK5 0F TH3 18M 80URG301513! L1NU5 M4K35 C0MPUT3R5 F0R TH3 M0DERN PR0L3T4R14T3!",
               "J00 H4V3 N0TH1NG T0 L053 8UT J00R CH41N5!",
               "FR0M 34CH 4CC0RD1NG T0 TH31R M34N5, T0 34CH 4CC0RD1NG T0 TH31R N33D5",
               "4LL P0W3R T0 TH3 P30P13",
               "GR33D H4S P01S0N3D M3N'5 50UL5 -- H4S B4RR1C4D3D TH3 W0RLD W1TH H4T3 -- H45 G0053ST3PP3D US 1NT0 M1S3RY 4ND BL00D5H3D.",
               "W3 H4V3 D3V3L0P3D 5P33D, BUT W3 H4V3 5HUT OUR53LV35 IN M4CH1N3RY TH4T G1V35 4BUND4NC3 H45 L3FT U5 1N W4NT. 0UR KN0WL3DG3 H45 M4D3 U5 CYNIC4L; OUR CL3V3RN355 H4RD 4ND UNKIND.",
               "W3 THINK TOO MUCH 4ND F33L TOO LITTL3.",
               "MOR3 TH4N M4CHIN3RY W3 N33D HUM4NITY.",
               "MOR3 TH4N CL3V3RN355 W3 N33D KINDN355. WITHOUT TH353 QU4LITI35 LIF3 WILL B3 VIOL3NT 4ND 4LL WILL B3 LO55",
               "W3 4R3 COMING OUT OF TH3 D4RKN355 INTO TH3 LIGHT!",
               "W3 4R3 COMING INTO 4 N3W WORLD! LOOK UP H4NN4H! TH3 5OUL OF M4N H45 B33N GIV3N WING5 4ND 4T L45T H3 I5 B3GINNING TO FLY.",
               )
        }

             
def GetDefaultBartenderText():
    txt =tender.get("default")
    if (not txt):
        return ("Hello")
    return txt

def GetBartenderText(str):
    txt = tender.get (str)
    if (txt):
        return txt
    return GetDefaultBartenderText()
def Speak(thingstosay):
    (text,sound)=Base.GetRandomBarMessage()
    rndnum=vsrandom.randrange(0,2)
    if (rndnum==1 or text==''):
        mylen=len(thingstosay)
        if (mylen>0):
            Base.Message (thingstosay[vsrandom.randrange(0,mylen)])
        else:
            Base.Message ('Hello!')
    else:
        Base.Message (text)
        if (sound!=''):
            VS.playSound (sound)