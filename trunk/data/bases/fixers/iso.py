intro_string="Have you heard of the Interplanetary Socialist Organization? We are a revolutionary organization trying to rid the Star Confederacy of its tired oligarchy. We are here to defend the rights of the poor workers! We are here to cause the downfall of the bourgeoise and enable the rise of the proletariat!"

import Base
import fixers
import Director
def AssignMission ():
	fixers.DestroyActiveButtons ()
	fixers.CreateChoiceButtons(Base.GetCurRoom(),[
		fixers.Choice("bases/fixers/yes.spr","bases/fixers/iso_mission.py","Accept This Agreement"),
		fixers.Choice("bases/fixers/no.spr","bases/fixers/iso_decline.py","Decline This Agreement")])

playa = VS.getPlayer();
playernum = playa.isPlayerStarship()
len=Director.getSaveDataLength (playernum,"kills");
kills=0
if (len!=0):
	kills=Director.getSaveData(playernum,"kills",len-1)
if (kills<0):
	Base.Message("Hello Pilot. " + intro_string + " We are actively seeking new members in our organization.  However to fly defense runs, you need some more experience. Come back when your record is somewhat more interesting and then together we can overthrow the confederacy!");
else:
	if (Director.getSaveDataLength (playernum,"iso_mission1")==0):
		AssignMission()
		Base.Message("Hello Mercenary. " + intro_string + " We are actively seeking mercenaries to help us defend our supplies and our party members.  There is a precious in this system vessel carrying several key party members and some valuable sensor data with them.  We offer 18000 credits if you will defend these starships, comrade! Do you accept our offer?")
#And then if you fail.......
	elif (fixers.checkSaveValue (playernum,"iso_mission1",-1)):
		Base.Message ("You conspirator! I should have realized you were a kepitalizt pig when I first smelled our foul stench! You probably got paid to destroy our vessel. If I shared in your lack of honor I would kill you where you stand.  But instead I shall ask my operatives to rid you of your ship. Fly you fool! Fly if you wish to have any shred of your starship left!")
		fixers.setSaveValue (playernum,"decided_iso_evil",1)
		type = faction_ships.getRandomFighter ("ISO")
		fgname="Lenin'sRevenge"
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		type = faction_ships.getRandomFighter ("ISO")
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
	else:
		if (fixers.checkSaveValue (playernum,"iso_mission1",1) and Director.getSaveDataLength(playernum,"iso_mission2")==0):			
			Base.Message ("Congratulations!")#assign mis 2
			AssignMission()
		elif (fixers.checkSaveValue (playernum,"iso_mission2",1) and Director.getSaveDataLength(playernum,"iso_mission3")==0):			
			Base.Message ("Congradulations")#assign mis 3:
			AssignMission()
		elif (fixers.checkSaveValue (playernum,"iso_mission3",1) and Director.getSaveDataLength(playernum,"iso_mission4")==0):
			Base.Message ("Congraduati")#assign mis 4
			AssignMission()
		elif (fixers.checkSaveValue(playernum,"iso_mission4",1)):
			Base.Message ("You have helped the ISO when we have needed it. Your talent and dedication shall not be forgotten. They will be sung of in revolution and written in epics.  Thank you kind Socialist. You have earned your name as a man of the people.")
		else:
			Base.Message ("Make haste for the people! Tardiness is the opium for the masses!") 