import quest
import Vector
import VS
import unit
import vsrandom
import launch
import faction_ships

class quest_shipyard_bomb (quest.quest):
    def __init__ (self):
        self.sysfile = VS.getSystemFile()
        self.shipyard=unit.getUnitByName('factory')
#        self.shipyard=launch.launch_wave_around_significant ('NavalShipyard','confed','factory','default',1,10000,40000,8)
    def Execute (self):
        if (VS.getSystemFile()==self.sysfile):
            playa = VS.getPlayer()
            if (playa):
                if (self.shipyard):
                    if (self.shipyard.getSignificantDistance(playa) > 1000):
                        print 'shipy ret'
                        print self.shipyard.getSignificantDistance(playa)
                        return 1
                    else:
                        print 'killing'
                        pos=self.shipyard.Position()
                        size=10*self.shipyard.rSize()
                        VS.playAnimation("explosion_orange.ani",pos,size)
                        pos=(pos[0]+.5*size,pos[1],pos[2])
                        VS.playAnimation("explosion_orange.ani",pos,size)
                        pos=(pos[0]-size,pos[1],pos[2])

                        VS.playAnimation("explosion_orange.ani",pos,size)
                        VS.playSound("explosion.wav",pos,(1,0,0))
                        self.shipyard.DealDamageToHull ((10,0,0),self.shipyard.GetHull()*.9)
                self.removeQuest()
                VS.IOmessage(0,"game","all","[Computer] Large Explosion detected... standby...%#@*")
                VS.IOmessage (0,"game","news","NAVAL SHIPYARDS HIT BY BOMB:   Disaster struck the Confederate Naval Shipyards orbiting Alpha Centauri two days ago, when a powerful explosive device detonated, crippling a fleet carrier that was nearing completion. At least a dozen casualties were reported with an unknown number of injured, and salvage crews are still working hard to clear the area of wreckage. A team from the CSP (Confederate Security Police) arrived at the shipyards mere hours after the incident, and an investigation has been launched to determine who the perpetrators of this attack were, whether they were human terrorists or agents of an alien power.")
                return 0
        return 1

class quest_shipyard_bomb_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_shipyard_bomb")
    def precondition(self,playernum):
        return 1
    def create (self):
        return quest_shipyard_bomb()
