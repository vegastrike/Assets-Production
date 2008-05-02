import quest
import quest_drone
import vsrandom
import quest_racene
import quest_disappear
import quest_rlaan_spy
import quest_slaver
import quest_shipyard_bomb
import quest_abu_dhabi
import quest_rogue_militia
#import quest_contraband_truck
#import dantestmission
import quest_teleport
import quest_surplus
import VS
import quest_isowing
#VS is only for news

adventures = {}
#adventures = {"Crucible/Cephid_17" : quest_intro.quest_introduction_factory()}

persistent_adventures = list()

adventures = {
	"Gemini/deltaprime":quest_drone.quest_drone_factory(),
#	"Enigma/callimanchius":quest_surplus.quest_surplus_factory(('Supplies/Medical','Research/Environmental',),1.5,.5,0,1,('callimanchius_disaster',),),
#	"Sol/alpha_centauri":quest_surplus.quest_surplus_factory(('Supplies/Construction_Supplies','Manufactured_Goods',),1.5,.5,0,1,('holman_population',),),
#	"Enigma/racene":quest_racene.quest_racene_factory(),
#	"Enigma/defiance":quest_isowing.quest_isowing_factory(),
#	"Enigma/axis":quest_disappear.quest_disappear_factory(),
#	"Enigma/novaya_kiev":quest_rlaan_spy.quest_rlaan_spy_factory(),
#	"Enigma/rigel":quest_slaver.quest_slaver_factory(),
#	"Sol/sirius":quest_abu_dhabi.quest_abu_dhabi_factory(),
#	"Sol/alpha_centauri":quest_shipyard_bomb.quest_shipyard_bomb_factory(),
#	"Enigma/heinlein":quest_rogue_militia.quest_rogue_militia_factory(),
#	"Enigma/klondike":quest_contraband_truck.quest_contraband_truck_factory(),
#	"Enigma/dantestmission":dantestmission.dantestmission_factory(),
#	"Enigma/enigma":quest_teleport.quest_teleport_factory(),
#
	}
persistent_adventures = [
	quest_drone.quest_drone_factory(),
#	quest_isowing.quest_isowing_factory()]
	]

def removePersistentAdventure(newq):
    mylen = len(persistent_adventures)
    if (mylen):
        for x in range (mylen):
            if (persistent_adventures[x]==newq):
                del persistent_adventures[x]
                return

def newAdventure(playernum,oldsys,newsys):
    newfac=adventures.get (newsys)
    if (newfac):
        newq = newfac.factory(playernum)
        if (newq):#only remove it if that player hasn't done it before
            del adventures[newsys]
            removePersistentAdventure(newfac)
        return newq
    return
#that returns false

def persistentAdventure(playernum):
    for index in range (len(persistent_adventures)):
        ret = persistent_adventures[index].persistent_factory(playernum)
        if (ret):
            del persistent_adventures[index]
            return ret
    if (vsrandom.randrange(0,4)==0):
        (key,val,news)=quest_surplus.makeSurplusShortage()
        if (not adventures.get(key)):
            adventures.setdefault(key,val)
            VS.IOmessage (0,"game","news",news)
    return
