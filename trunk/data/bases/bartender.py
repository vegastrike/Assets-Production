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
