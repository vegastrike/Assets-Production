import quest
import Vector
import VS
import unit
import vsrandom
import launch
import faction_ships
class quest_slaver (quest.quest):
    def __init__ (self):
        playa = VS.getPlayer()
        if (playa):
            confed = faction_ships.factions[faction_ships.confed]
            pirates = faction_ships.factions[faction_ships.pirates]
            illustrious=launch.launch_wave_around_unit ('Illustrious',confed,faction_ships.getRandomCapitol(confed),'default',1,1000,4000,playa)
            launch.launch_wave_around_unit ('Illustrious',confed,faction_ships.getRandomCapitol(confed),'default',2,1000,2000,illustrious)
            launch.launch_wave_around_unit ('Illustrious',confed,faction_ships.getRandomFighter(confed),'default',4,100,200,illustrious)
            launch.launch_wave_around_unit ('SlaverGuild',pirates,faction_ships.getRandomFighter(pirates),'default',4,100,200,illustrious)
            launch.launch_wave_around_unit ('SlaverGuild',pirates,faction_ships.getRandomCapitol(pirates),'default',2,100,200,illustrious)
            VS.IOmessage (3,"game","all","[Computer] Scans show the remnants of the Slaver Guild being cleaned up by Special Forces.")
    def Execute (self):
        self.removeQuest()
        return 0

class quest_slaver_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_slaver")
    def precondition(self,playernum):
        return 1
    def create (self):
        return quest_slaver()
