import quest
import quest_drone
import random
import quest_racene
import quest_disappear
import quest_rlaan_spy
import quest_slaver
import quest_shipyard_bomb
import quest_abu_dhabi
import quest_rogue_militia
import quest_teleport
import quest_surplus
import VS
import quest_isowing
#VS is only for news
adventures = {"gemini_sector/delta_prime":quest_drone.quest_drone_factory(),
              "enigma_sector/callimanchius":quest_surplus.quest_surplus_factory(('Supplies/Medical','Research/Environmental',),1.5,.5,0,1,('callimanchius_disaster',),),
              "sol_sector/alpha_centauri":quest_surplus.quest_surplus_factory(('Supplies/Construction_Supplies','Manufactured_Goods',),1.5,.5,0,1,('holman_population',),),
              "enigma_sector/racene":quest_racene.quest_racene_factory(),
              "enigma_sector/defiance":quest_isowing.quest_isowing_factory(),
              "enigma_sector/axis":quest_disappear.quest_disappear_factory(),
              "enigma_sector/novaya_kiev":quest_rlaan_spy.quest_rlaan_spy_factory(),
              "enigma_sector/rigel":quest_slaver.quest_slaver_factory(),
              "sol_sector/sirius":quest_abu_dhabi.quest_abu_dhabi_factory(),
              "sol_sector/alpha_centauri":quest_shipyard_bomb.quest_shipyard_bomb_factory(),
              "enigma_sector/heinlein":quest_rogue_militia.quest_rogue_militia_factory(),
              "enigma_sector/enigma":quest_teleport.quest_teleport_factory()}

persistent_adventures = [quest_drone.quest_drone_factory(),
                         quest_isowing.quest_isowing_factory()]

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
    if (random.randrange(0,4)==0):
        (key,val,news)=quest_surplus.makeSurplusShortage()
        if (not adventures.get(key)):
            adventures.setdefault(key,val)
            VS.IOmessage (0,"game","news",news)
    return
