import fixers
import Base
fixers.DestroyActiveButtons ()
playernum = VS.getPlayer().isPlayerStarship()
if (not Director.getSaveDataLength(playernum,"iso_mission1")):
	fixers.setSaveValue (playernum,"iso_mission1",0)
	#load mission 1
	VS.LoadMission ("mission/defend/iso/defend_iso_mission1.mission")
elif ((not Director.getSaveDataLength (playernum,"iso_mission2")) and fixers.checkSaveValue (playernum,"iso_mission1",1)):
	fixers.setSaveValue (playernum,"iso_mission2",0)
	VS.LoadMission ("mission/escort/iso/escort_iso_mission2.mission")
	#load mission 2
elif ((not Director.getSaveDataLength (playernum,"iso_mission3")) and fixers.checkSaveValue (playernum,"iso_mission2",1)):
	fixers.setSaveValue (playernum,"iso_mission3",0)
	VS.LoadMission ("mission/cargo/iso/cargo_contraband_mission3.mission")
	#load mission 3
elif ((not Director.getSaveDataLength (playernum,"iso_mission4")) and fixers.checkSaveValue (playernum,"iso_mission3",1)):
	fixers.setSaveValue (playernum,"iso_mission4",0)
	VS.LoadMission ("mission/defend/defend_iso_mission4.mission")
	#load mission 4
else:
	Base.message ("Excuse me... I have an urgent holo-call from the party...")