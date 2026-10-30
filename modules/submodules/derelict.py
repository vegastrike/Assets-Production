import Vector
import vsrandom
import VS

def launchNewDerelict(name, ship_type):
    player = VS.getPlayer()
    if(player == None):
        return 0
    
    # get the player's position
    vec = player.Position()
    # set derelict position approximately 10000m away from the player.
    # TODO: make configurable
    vec = Vector.Add(vec,(10000,0,0))
    vec = Vector.Add (vec,(vsrandom.uniform(-2000,2000),
                            vsrandom.uniform(-2000,2000),
                            vsrandom.uniform(-2000,2000)))
    
    # launch the derelict.
    derelict = VS.launch(name, ship_type,"neutral","unit","default",1,1,vec,'')
    derelict.Derelict()

    # get rid of all orders, so that strange maneouvers don't happen
    derelict.PrimeOrders()

    return 0
