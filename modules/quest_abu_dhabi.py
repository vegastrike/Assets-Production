import quest
import Vector
import VS
import unit
import vsrandom
import launch
import faction_ships
class quest_abu_dhabi (quest.quest):
    def __init__ (self):
        playa = VS.getPlayer()
        if (playa):
            launch.launch_wave_around_unit ('AbuDhabi','neutral',faction_ships.getRandomCapitolInt(faction_ships.confed),'default',1,1000,4000,playa)
    def Execute (self):
        self.removeQuest()
        return 0

class quest_abu_dhabi_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_abu_dhabi")
    def precondition(self,playernum):
        return quest.findQuest (playernum,"abu_dhabi_return")
    def create (self):
        return quest_abu_dhabi()
