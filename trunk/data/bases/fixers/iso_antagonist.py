import Base
import fixers
import Director
import quest
playa=VS.getPlayer()
playernum = playa.isPlayerStarship()
#only want this var if you agreed to the quest at some point--so we want it to return fasle if len is 0
if (not Director.getSaveDataLength(playernum,"iso_mission1")):
	Base.Message("Good day, stranger.  I do not know you, and I do not wish to know you. However, in the face of our mutual situation, perhaps you could come to an agreement with Rowenna of the ISO.  Talk to her. But before you leave, talk to me. I may have an offer that you simply cannot refuse.")
else:
	fixers.DestroyActiveButtons ()
	if (fixers.checkSaveValue(playernum,"iso_mission1",0)):
		Base.Message("Excellent! You accepted the mission.  I will offer you 38,000 credits to do one thing: destroy that vessel. You should have help from a few of my elite force; however, I expect the ISO to put up a fight, so be wary and beware. I trust you will accept my offer, my young....friend")
	elif (fixers.checkSaveValue(playernum,"iso_mission1",1)):
		Base.Message("There is only one thing I despise more than a member of the Interplanetary Socialist Organization: and that is one of their mercenary lapdogs. You are not worth the spit I paid to have them destroy your starship. Run now if you dare-- your ship is in peril")
		type = faction_ships.getRandomFighter ("confed")
		fgname="AlphaElite"
		fixers.setSaveValue (playernum,"decided_iso_good",1)
		launch.launch_wave_around_unit (fgname,"confed",type,"default",1,80,100,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"confed",type,"default",1,80,100,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"confed",type,"default",1,80,100,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"confed",type,"default",1,80,100,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"confed",type,"default",1,80,100,playa).SetTarget(playa)
	else:
		fixers.CreateChoiceButtons(Base.GetCurRoom(),[
			fixers.Choice("bases/fixers/yes.spr","bases/fixers/iso_antagonist_mission.py","Accept This Agreement"),
			fixers.Choice("bases/fixers/no.spr","bases/fixers/iso_antagonist_decline.py","Decline This Agreement")])
	
