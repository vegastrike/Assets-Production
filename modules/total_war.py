import random
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import Director
class total_war (Director.Mission):
    def __init__(self):
        VS.SetDifficulty(.9)
        Director.Mission.__init__(self)
        self.lasttime=0.0
        self.waittime=10.0
    def launch_new_wave(self):
        side = random.randrange(0,2)
        faction="confed"
        ai = random.randrange(0,2)
        if (ai==0):
            ai = "printhello.py"
        else:
            ai = "default"
        if (side==0):
            faction=faction_ships.get_enemy_of("confed")
        else:
            faction=faction_ships.get_friend_of("confed")
        launched = launch.launch_wave_around_unit ("Shadow",faction,faction_ships.getRandomFighter(faction),ai,random.randrange(1,10),2000.0,4000.0,VS.getPlayer(),'')
        
    def Execute (self):
        time = VS.GetGameTime()
        if (time-self.lasttime>self.waittime):
            self.launch_new_wave()
            self.waittime=random.randrange(10.0,30.0)
            self.lasttime=time
    def initbriefing(self):
        print "ending briefing"                
    def loopbriefing(self):
        print "loop briefing"
        Briefing.terminate();
    def endbriefing(self):
        print "ending briefing"        
