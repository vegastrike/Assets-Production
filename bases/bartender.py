import Base
import VS
import random

thingstosay=('Hello! Lots of travellers about. Have yourself a seat and enjoy a nice cool fuzzy buzzer.',
             'Bottoms up for ye olde bartender, eh?',
             'Tilt back a nice cool one, friend.',
             "News is sparse around here, check back with me later when I've talked with some more of the haulers coming in later today.",
             'Shh looks like someone is watchin. Watch your back.',
             "Have one on the house, it's happy hour!",
             'A smuggler like you had better watch his Ps and Qs.',
             'Got any stories to tell? Last week I had a patron who just could not stop talking about his battles with pirates.',
             "A nice drink and a bit o' talk is what I live for.",
             "Have you heard what's been on the news recently. It ain't pretty!",
             "Hello there, friend. What can I get you? Sorry, I don't have any of the good stuff left. I had a transport bringing in new beverages from the Rlaan border, but there was an... accident. Apparently, some of that stuff is more flamable than napalm! How was I to know?",
             "So what's your take on the war? A friend of mine in the Navy told me the Aera have the Rlaan on the ropes now. Won't be long before everything's quiet on that front. And when that happens, the Aera will bring all of their high-tech weapons to bear on us. Things aren't looking good.",
             "This fellow brought a jhorg in here yesterday. Ever heard about the jhorg? They're small scaly creatures from New Bremen that can mimic everything you say with perfect accuracy. Forget parrots, these things are better than tape recorders!",
             "A couple of goons from the Security Police came in here earlier looking for some guy named Jensen. Wouldn't say what it was about, but let me tell you, I was just as happy when they left. I swear, half the bar found excuses to be elsewhere the moment those two guys entered, and I don't blame them.",
             "Some idiots from the ISO came in here yesterday handing out phamphlets and bothering the customers. They wouldn't take a hint, so I had them thrown out. I don't know who's worst, the ISO or those religious fanatics they fight with all the time.",
             "You know about those Rlaan? Supposedly, they never attack unarmed vessels. Well, word is there's this rogue Rlaan cruiser hiding out near here. Fled to our side of the border when their own Star Force had enough of them. I hear it attacks anything or anyone that comes in its way.",
             "The pirates out on the frontier are getting more organized by the day. I hear they've overran entire systems and colonies. Some of the guys are placing bets on what will bring about our fall first. The pirates from within or the Aera from the outside?",
             "This captain of a Wayfarer came in here the other day, looking like she could really use a drink. It turned out she had been chased by pirates across three systems! Persistant little buggers, aren't they? And the militia wasn't much help.",
             "Every so often, a Rlaan comes in here. They have their own civilian sector pretty much like our own, and sometimes a couple of their privateers find their way across the border. But let me tell you, never give them beer. One of them had that, and he got into some sort of violent spasms and threw up over the whole bar. Not a pretty sight.",
             "A woman came in here the other day carrying one of those fancy Aera energy pistols in her belt. Don't ask me how she managed to get her hands on one of those, but even the roughest of my customers made sure to stay out of her way.",
             "A mercenary outfit, the 'Red Condors', came in here a while ago. Real tough-looking types. I expected trouble, but they quietly finished their drinks and left. Glad there's still some professionalism out there.",
             "Can I get you anything? Whiskey? Vodka? Aarnbach's Acid? I'm all for being social, but I do have a business to run.",
             "There's a lot of people complaining about the pirates, but I don't mind them so much. Earth knows it needs a running merchant operation in the outlying systems, but they haven't got the resources to cover every trade lane from pirates, so they need people who can look after themselves. People like you and me. And that's why they go easy on drafting our kind.",
             "A toast to the men and women of the Confederate Armed Forces! If not for them, we'd all be learning how to speak Aera right about now. If those things even have vocal chords.",
             "Hey, did you hear the news? Word is that the 5th Fleet under Admiral Johansson managed to bag a whole bunch of those nasty Aeran cruisers in a battle not far from here! Maybe this war is winnable after all!",
             "We might have been able to pick off some of the outlying Aeran outposts, but I hear their core planets are a tough nut to crack. The HCS Zhukov tracked this huge Rlaan battle fleet as it entered orbit around one of the planets, but then it simply disappeared off their scopes! The fleet that is, not the planet.",
             )
             
(text,sound)=Base.GetRandomBarMessage()
rndnum=random.randrange(0,2)
if (rndnum==1 or text==''):
    if (len(thingstosay)>0):
        Base.Message (thingstosay[random.randrange(0,len(thingstosay))])
    else:
        Base.Message ('Hello!')
else:
    Base.Message (text)
    if (sound!=''):
        VS.playSound (sound)
