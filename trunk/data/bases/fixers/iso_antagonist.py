import Base
import fixers
import Director
import quest
playernum = VS.getPlayer().isPlayerStarship()
#only want this var if you agreed to the quest at some point--so we want it to return fasle if len is 0
if (not Director.getSaveDataLength(playernum,"iso_mission1")):
	Base.Message("Good day, stranger.  I do not know you, and I do not wish to know you. However, in the face of our mutual situation, perhaps you could come to an agreement with Rowenna of the ISO.  Talk to her. But before you leave, talk to me. I may have an offer that you simply cannot refuse.")
else:
	fixers.DestroyActiveButtons ()
	fixers.CreateChoiceButtons(Base.GetCurRoom(),[
		fixers.Choice("bases/fixers/yes.spr","bases/fixers/iso_mission1.py","Accept This Agreement"),
		fixers.Choice("bases/fixers/no.spr","bases/fixers/iso_decline.py","Decline This Agreement")])
	Base.Message("Hello Mercenary. " + intro_string + " We are actively seeking mercenaries to help us defend our supplies and our party members.  There is a precious vessel carrying several key party members and some valuable sensor data with them.  We offer 18000 credits if you will defend these starships, comrade! Do you accept our offer?");
