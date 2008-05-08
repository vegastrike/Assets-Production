#---------------------------------------------------------------------------------
# Vega Strike script for a quest
# Copyright (C) 2008 Vega Strike team
# Contact: hellcatv@sourceforge.net
# Internet: http://vegastrike.sourceforge.net/
#.
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Author: pyramid
# Version: 2008-04-12
#
#---------------------------------------------------------------------------------

# This script is a start to a turorial mission (quest/adventure)
# Currently, it only works with a new campaign when launching from Atlantis
# The only implemented features is launching a drone, making it say a few words,
# and following the player ship

# import used libraries
import quest
import Vector
import VS
import unit
import vsrandom
import launch
import Director
import universe

# predefine stages
SAVE_KEY = "quest_tutorial"
STAGE_DOCKED = 0
STAGE_AWAY = 1
STAGE_ORBIT = 2
STAGE_ACCEPT = 3
COMPLETE_TUTORIAL1 = 4
COMPLETE_TUTORIAL2 = 5
COMPLETE_TUTORIAL3 = 6
COMPLETE_TUTORIAL4 = 7
COMPLETE_TUTORIAL5 = 8
STAGE_DECLINE = 98

# the class that will be executed
class quest_tutorial (quest.quest):
    # initialize quest variables
    def __init__ (self):
        #print "--- Tutorial mission loaded ---"
        # initialize variables
        self.player = VS.getPlayer()
        self.drone = VS.Unit()
        self.stage = STAGE_DOCKED
        self.dockeddistance = 0
        self.timer = VS.GetGameTime()
        self.stayputtime = 0
        self.practice = 0
        self.msgColor = "#FFFF99"
        self.objectives = []        # list of objectives
        self.objective = 0          # current objective
        self.startobjectname = ""
    def putSaveValue(self,value, key=SAVE_KEY):
        Director.eraseSaveData(self.player.isPlayerStarship(),key,0)
        Director.pushSaveData(self.player.isPlayerStarship(),key,value)
        return 1
    def getSaveValue(self,key=SAVE_KEY):
        if Director.getSaveDataLength(self.player.isPlayerStarship(),key) > 0:
            return Director.getSaveData(self.player.isPlayerStarship(),key,0)
        return 0
    # checks if the player has undocked from Atlantis. If so sets next stage.
    # Has been replaced by the more generic function playerIsUndocked
    def hasUndockedFromAtlantis(self):
        # get the planet object 
        self.startobject = unit.getUnitByName('Atlantis')
        # target the departing planet to see the distance
        self.player.SetTarget(self.startobject)
        # verify if player is still docked at the planet
        if (self.startobject.isDocked(self.player)):
            self.dockeddistance = self.startobject.getDistance(self.player)
        # if the player is not docked and at least 5km away then set next stage number
        if (not self.startobject.isDocked(self.player) and self.startobject.getDistance(self.player)>(self.dockeddistance+5000)):
            self.stage = STAGE_AWAY
    # checks if the player has undocked. if so sets next stage
    def playerIsUndocked(self):
        # dockedobject and dockeddistance must be global, i.e prefixed with self
        # otherwise the script will advance to next stage just after undocking
        # get the planet object 
        self.dockedobject = universe.getDockedBase()
        name = self.dockedobject.getName()
        # verify if player is still docked and set the reference distance
        if (not name==""):
            self.dockeddistance = self.dockedobject.getDistance(self.player)
            self.startobjectname = name
        # when starting from Atlantis, target the departing planet to see the distance
        if (name=="Atlantis"):
            self.player.SetTarget(self.dockedobject)
        # if the player was never docked or is not docked and at least 1km away then set next stage number
        if (name=="" or ((not self.startobjectname=="") and (not self.startobjectname=="Atlantis") and self.dockedobject.getDistance(self.player)>(self.dockeddistance+1000))):
            self.stage = STAGE_AWAY
            self.timer = VS.GetGameTime()+5
    # launches a unit aka the drone
    def launchNewDrone (self):
        if (not self.player.isNull()):
            # get the player's position
            vec = self.player.Position()
            # set drone position 1000m away from the player
            vec = Vector.Add(vec,(1000,0,0))
            # launch the tutorial drone.
            #VS.launch(name,type,faction,unittype,ai,nr,nrwaves,pos,squadlogo):
            self.drone = VS.launch("Oswald","Robin","neutral","unit","default",1,1,vec,'')
            # when launching give the player some text and ask him to decide if he wants to participate
            #self.player.commAnimation("com_tutorial_oswald_01.ani")
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Hello traveler.")
            VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"My name is Oswald and I am offering flight assistance.")
            VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"Would you like to refresh your space faring skills?")
            VS.IOmessage (15,"Oswald","Privateer",self.msgColor+"To participate in my tutorial mission, cut down your engines with the #9999FFBACKSPACE"+self.msgColor+" key, let me approach you, and stay put until I contact you again.")
            # on launching the drone, set its position near the player
            vec = self.player.Position()
            vec = Vector.Add (vec,(vsrandom.uniform(-1000,1000),
                                   vsrandom.uniform(-1000,1000),
                                   vsrandom.uniform(-1000,1000)))
            self.drone.SetPosition(vec)
            # get rid of all orders, so that strange maneouvers don't happen
            self.drone.PrimeOrders()
            # display the drone on HUD
            self.player.SetTarget(self.drone)
            self.timer = VS.GetGameTime()+20
            complete = self.getSaveValue()
            if (complete>0):
                self.stage = complete
            else:
                self.stage = STAGE_ORBIT
    # keeps the drone near the player
    def orbitMe (self):
    # the drone doesn't quite orbit
    # it will approach the player until 500 meters and then stop
        #self.player.SetTarget(self.drone)
        # if the drone is more than 500m away it will set
        if (self.drone.getDistance(self.player)>=500):
            # orientate the nose of the drone towards the player ship
            vec = Vector.Sub(self.player.Position(),self.drone.Position())
            self.drone.SetOrientation((1,0,0),vec)
            # set velocity proportional to distance from player
            vec = Vector.Scale(Vector.SafeNorm(vec),self.drone.getDistance(self.player)/10)
            self.drone.SetVelocity(vec)
            #self.stayputtime = VS.GetGameTime()
        # if drone has approached player until 500m then stop it
        if (self.drone.getDistance(self.player)<500):
            self.drone.SetVelocity((0,0,0))
            # this is also needed to stop rotation of the drone
            self.drone.SetAngularVelocity((0,0,0))
    def LightMinuteToMeter(self,lightminute):
        meter = 17987547500 * lightminute
        return meter
    # returns the facing angle between unit 1 and unit 2
    # when unit 1 is facing unit 2 the return value is 0
    # when unit 1 is completely turned away from unit 2 the return value is pi (~3.14)
    def facingAngleToUnit(self,unit1,unit2):
        vec = Vector.Sub(unit2.Position(),unit1.Position())
        dot = Vector.Dot(Vector.SafeNorm(unit1.GetOrientation()[2]),Vector.SafeNorm(vec))
        angle = VS.acos(dot)
        return angle
    # signed velocity is negative when the thrust is reverse
    # otherwise velocity is positive
    def getSignedVelocity(self,unit):
        velocity = Vector.Dot(Vector.SafeNorm(unit.GetOrientation()[2]),unit.GetVelocity())
        return velocity
    # check if player stays put close to the drone to accept tutorial
    def acceptTutorial (self):
        #print "--acceptTutorial?--"
        velocity = Vector.Mag(self.player.GetVelocity())
        # if the offer has been placed, and player is put for 10s and drone is near
        if (VS.GetGameTime()>self.timer and self.drone.getDistance(self.player)<600 and velocity<=10):
            #print "-set STAGE_ACCEPT-!!!!!!!!!!!!!!!!!!!!"
            self.player.SetTarget(self.drone)
            self.timer = VS.GetGameTime()
            self.stage = STAGE_ACCEPT
        if (VS.GetGameTime()>self.timer and velocity>=10):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Have a nice journey and come back for a space faring refresher anytime here in Cephid 17.")
            self.stage = STAGE_DECLINE
            #print "-set STAGE_DECLINE-!!!!!!!!!!!!!!!!!!!!"
            self.timer = VS.GetGameTime()
            self.stage = STAGE_DECLINE
    ## play the first part of the tutorial
    def tutorialComm (self):
        if (self.practice==0):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Glad I can be of help.")
            VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"In the first place let's have a look at your heads up display (HUD).")
            VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"Please do not move your ship in order to better focus on my instructions.")
            VS.IOmessage (15,"Oswald","Privateer",self.msgColor+"In the upper left corner you can see the communication messages.")
            VS.IOmessage (20,"Oswald","Privateer",self.msgColor+"Each communication message shows the sender, the game time of the sending, and the message itself, like this one.")
            VS.IOmessage (25,"Oswald","Privateer",self.msgColor+"To scroll the messages back and forth use the #9999FFPage Up"+self.msgColor+" and #9999FFPage Down"+self.msgColor+" keys. Try it out now.")
            VS.IOmessage (35,"Oswald","Privateer",self.msgColor+"Good.")
            VS.IOmessage (40,"Oswald","Privateer",self.msgColor+"Now you can send me a message by pressing the #9999FFF1"+self.msgColor+" key.")
            self.timer = VS.GetGameTime()+50
            self.practice = 1
        if (self.practice==1 and VS.GetGameTime()>self.timer):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Usually, messages assigned to keys #9999FFF1"+self.msgColor+" and #9999FFF2"+self.msgColor+" are friendly messages which slightly increase you relation with a faction, while the other keys #9999FFF3"+self.msgColor+" and #9999FFF4"+self.msgColor+" decrease your relationship.")
            VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"Sometimes it can be very useful to send multiple friendly messages to improve your relation with a hostile faction.")
            VS.IOmessage (20,"Oswald","Privateer",self.msgColor+"That's about it on the messages display.")
            self.timer = VS.GetGameTime()+30
            self.practice = 2
        if (self.practice==2 and VS.GetGameTime()>self.timer):
            # make sure to reset the counter for the next practice loops
            self.practice = 0
            self.timer = VS.GetGameTime()+0
            self.stage = COMPLETE_TUTORIAL1
            self.putSaveValue(self.stage)
    def tutorialNav (self):
        VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Now, let's review the navigation information on your HUD. Theory first, then some practice.")
        VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"In the lower left corner you will find your ship's shield (blue) and armor (orange) status.")
        VS.IOmessage (15,"Oswald","Privateer",self.msgColor+"We will come to the text indicators later.")
        VS.IOmessage (20,"Oswald","Privateer",self.msgColor+"In the middle of the bottom part you have your dashboard with the front radar on the left side and the rear radar on the right side.")
        VS.IOmessage (30,"Oswald","Privateer",self.msgColor+"The active target will display as a small cross on your radar. The other targets will be dots with their colors representing your relation to them.")
        VS.IOmessage (40,"Oswald","Privateer",self.msgColor+"Green is friendly, blue/yellow/red is hostile. Neutral and significant objects like planets, stations, wormholes, or suns are white.")
        VS.IOmessage (50,"Oswald","Privateer",self.msgColor+"The center part of the dashboard has four round indicators which begin flashing when:")
        VS.IOmessage (60,"Oswald","Privateer",self.msgColor+" (L) a hostile is having missile lock on you")
        VS.IOmessage (70,"Oswald","Privateer",self.msgColor+" (J) you are in jump point reach and your jump drive is ready")
        VS.IOmessage (80,"Oswald","Privateer",self.msgColor+" (S) your SPEC drive, needed for faster-than-light (FTL) travel, is activated")
        VS.IOmessage (90,"Oswald","Privateer",self.msgColor+" (E) your electronic counter measures (ECM) are active")
        VS.IOmessage (100,"Oswald","Privateer",self.msgColor+"Further below are three colored bars indicating")
        VS.IOmessage (105,"Oswald","Privateer",self.msgColor+" (CAPACITOR) your weapons capacitor charge")
        VS.IOmessage (115,"Oswald","Privateer",self.msgColor+" (DRIVES) your SPEC and jump drives energy charge")
        VS.IOmessage (125,"Oswald","Privateer",self.msgColor+" (FUEL) status for in-system travel and overdrive propulsion")
        VS.IOmessage (135,"Oswald","Privateer",self.msgColor+"The numbers below are your current speed to the left and your set speed to the right.")
        VS.IOmessage (145,"Oswald","Privateer",self.msgColor+"Further below there is the effective SPEC velocity to the left and the flight computer (FCMP) mode.")
        VS.IOmessage (155,"Oswald","Privateer",self.msgColor+"So much for theory. Let's do some practice now.")
        self.timer = VS.GetGameTime()+160
        self.stage = COMPLETE_TUTORIAL2
        self.putSaveValue(self.stage)
    def practiceNav (self):
        # practice intro
        if (self.practice==0):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"First some basic navigation and targetting.")
            self.timer = VS.GetGameTime()+5
            self.practice = 1
        # make the drone the players target
        if (self.practice==1):
            # explain basic targetting if dron is not already target
            if (unit.getUnitFullName(self.player.GetTarget()) != unit.getUnitFullName(self.drone)):
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"In the lower right corner you can see the target video display unit (VDU) where you can see you current target.")
                VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"Target me by repeatedly toggling the #9999FFT"+self.msgColor+" key until you see my ship on the right VDU.")
                VS.IOmessage (7,"Oswald","Privateer",self.msgColor+"Should you pass me, you may reverse the target selection sequence by pressing the #9999FFShift+T"+self.msgColor+" keys.")
            self.timer = VS.GetGameTime()+7
            self.practice = 2
        if (self.practice==2 and unit.getUnitFullName(self.player.GetTarget())==unit.getUnitFullName(self.drone)):
            nam = unit.getUnitFullName(self.drone)
            self.objective = VS.addObjective("Target %s" % nam)
            self.objectives+=[int(self.objective)]
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"OK. Now, orient your ship so that your targetting reticule (cross) points directly at me.")
            VS.IOmessage (3,"Oswald","Privateer",self.msgColor+"To get my ship into your visual range just turn in the direction of the white target arrow at the edge of your HUD.")
            VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"When my ship is in your visual range you will notice that it is framed by a target box.")
            VS.IOmessage (7,"Oswald","Privateer",self.msgColor+"Align your targetting reticule with my ship.")
            self.timer = VS.GetGameTime()+7
            self.practice = 3
        if (self.practice==3):
            # check if the player is facing the drone
            angle = self.facingAngleToUnit(self.player,self.drone)
            #print "facing: " + str(angle)
            if (angle<=0.05):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Well done.")
                VS.IOmessage (2,"Oswald","Privateer",self.msgColor+"Now, turn your ship away from my ship and accelerate to full speed using the #9999FF\\"+self.msgColor+" key.")
                self.objective = VS.addObjective("Set max velocity")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+10
                self.practice = 4
        if (self.practice==4):
            # check if the player is facing away
            angle = self.facingAngleToUnit(self.player,self.drone)
            velocity = Vector.Mag(self.player.GetVelocity())
            #check if angle to drone is at least 22 degrees (0.20 radians)
            if (angle>=0.20 and velocity>=295):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"And now set your velocity reference to zero by pressing the #9999FFBACKSPACE"+self.msgColor+" key and come to a complete stop.")
                self.objective = VS.addObjective("Set full stop")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+0
                self.practice = 5
        if (self.practice==5):
            # check if the player is stopped
            velocity = Vector.Mag(self.player.GetVelocity())
            if (velocity<=2):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"You can also increment your velocity gradually with the #9999FF+"+self.msgColor+" key. Accelerate to 100 m/s now.")
                self.objective = VS.addObjective("Set velocity reference to 100m/s")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+0
                self.practice = 6
        if (self.practice==6):
            # check if the player has velocity >100
            velocity = Vector.Mag(self.player.GetVelocity())
            if (velocity>=98 and velocity<=110):
                VS.setCompleteness(self.objectives[3],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"In the same way you can reduce your velocity gradually with the #9999FF-"+self.msgColor+" key. Deccelerate to 50 m/s.")
                self.objective = VS.addObjective("Set velocity reference to 50m/s")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+0
                self.practice = 7
        if (self.practice==7):
            # check if the player has velocity <50
            velocity = Vector.Mag(self.player.GetVelocity())
            if (velocity<=55 and velocity>=40):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Great. If you further deccelerate your velocity with the #9999FF-"+self.msgColor+" key you can actually reverse your thrust. Deccelerate now to -20 m/s.")
                self.objective = VS.addObjective("Set velocity reference to -20m/s")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+0
                self.practice = 8
        if (self.practice==8):
            # check if the player has velocity <=-20m/s
            velocity = self.getSignedVelocity(self.player)
            if (velocity<=-18):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Excellent.")
                VS.IOmessage (1,"Oswald","Privateer",self.msgColor+"You have learned how to target, orient your ship, accellerate, decellerate, and bring your ship to a stop.")
                VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"I'm sure this will come in handy during your future endeavors.")
                self.timer = VS.GetGameTime()+0
                self.practice = 9
        if (self.practice==9):
            # make sure to reset the counter for the next practice loops
            self.practice = 0
            self.timer = VS.GetGameTime()+10
            self.stage = COMPLETE_TUTORIAL3
            self.putSaveValue(self.stage)
            #print "NAV - save: " + str(self.getSaveValue())
    def practiceSpec (self):
        # practice intro
        if (self.practice==0):
            self.jump = universe.getRandomJumppoint()
            nam = unit.getUnitFullName(self.jump)
            self.objective = VS.addObjective("Target %s" % nam)
            self.objectives+=[int(self.objective)]
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Let's practice some faster than light (FTL) travel now.")
            VS.IOmessage (2,"Oswald","Privateer",self.msgColor+"Target "+unit.getUnitFullName(self.jump)+" using the #9999FFN"+self.msgColor+" or the #9999FFShift+N"+self.msgColor+" keys.")
            self.player.commAnimation("com_tutorial_oswald.ani")
            self.timer = VS.GetGameTime()+3
            self.practice = 1
        if (self.practice==1 and self.player.GetTarget()==self.jump):
            VS.setCompleteness(self.objectives[self.objective],1.0)
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Set your velocity to maximum with the #9999FF\\"+self.msgColor+" key and activate the SPEC auto pilot with the #9999FFA"+self.msgColor+" key to get there. Hold on, as this might take a while if you are close to massive objects.")
            VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"You will notice that your SPEC drive indicator (S) is flashing, which indicates that it is active.")
            VS.IOmessage (15,"Oswald","Privateer",self.msgColor+"During FTL travel your shields become inactive, as you can see below on your ship VDU.")
            VS.IOmessage (25,"Oswald","Privateer",self.msgColor+"You will also notice that your steering has no effect on your vessel since the auto pilot has taken over the controls.")
            VS.IOmessage (35,"Oswald","Privateer",self.msgColor+"You can always interrupt and resume the auto pilot toggling the #9999FFA"+self.msgColor+" key. You may try that, if you wish.")
            VS.IOmessage (45,"Oswald","Privateer",self.msgColor+"In the lower left corner, just above your ship staus you will notice two indicators.")
            VS.IOmessage (50,"Oswald","Privateer",self.msgColor+"SPEC shows you if your SPEC drive is enabled.")
            VS.IOmessage (55,"Oswald","Privateer",self.msgColor+"AUTO tells you if auto pilot is engaged.")
            #self.player.commAnimation("com_tutorial_oswald.ani")
            name = unit.getUnitFullName(self.jump)
            self.objective = VS.addObjective("Approach %s" % name)
            self.objectives+=[int(self.objective)]
            self.timer = VS.GetGameTime()+55
            self.practice = 2
        if (self.practice==2 and self.player.getDistance(self.jump)<=10000):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Almost there.")
            VS.IOmessage (2,"Oswald","Privateer",self.msgColor+"The auto pilot only gives back control only some time after the SPEC auto pilot light stopped flashing.")
            VS.IOmessage (8,"Oswald","Privateer",self.msgColor+"Notice also how your shields start recharing when leaving FTL travel mode.")
            self.timer = VS.GetGameTime()+8
            self.practice = 3
        if (self.practice==3 and self.player.getDistance(self.jump)<=3000):
            VS.setCompleteness(self.objectives[self.objective],1.0)
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Here we are.")
            VS.IOmessage (2,"Oswald","Privateer",self.msgColor+"You may try out manual FTL travel at this point in time.")
            VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"Target planet Atlantis using your significant objects targetting keys #9999FFN"+self.msgColor+" and #9999FFShift+N"+self.msgColor+".")
            self.timer = VS.GetGameTime()+10
            self.practice += 1
        if (self.practice==4 and VS.GetGameTime()>self.timer):
            self.destination = unit.getUnitByName('Atlantis')
            self.distance = self.player.getDistance(self.destination)
            name = unit.getUnitFullName(self.destination)
            self.objective = VS.addObjective("Target %s" % name)
            self.objectives+=[int(self.objective)]
            self.timer = VS.GetGameTime()
            self.practice += 1
        if (self.practice==5 and self.player.GetTarget()==self.destination):
            VS.setCompleteness(self.objectives[self.objective],1.0)
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Roger that. Turn towards the planet, set your velocity to maximum with the #9999FF\\"+self.msgColor+" key, and enable the manual SPEC with the #9999FFShift+A"+self.msgColor+" key to approach the planet.")
            VS.IOmessage (5,"Oswald","Privateer",self.msgColor+"Make sure that the planet is fairly well centered in your targetting reticule.")
            VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"Notice how your speed starts increasing gradually after leaving the jump point range.")
            self.objective = VS.addObjective("Enable manual SPEC")
            self.objectives+=[int(self.objective)]
            self.timer = VS.GetGameTime()+10
            self.practice += 1
        if (self.practice==6 and self.player.GetTarget()==self.destination):
            #disabled for now, since max velocity does not return the spec values
            #velocity = Vector.Mag(self.player.GetVelocity())
            #print "velocity=" + str(self.player.GetVelocity())
            #print "magnitude=" + str(velocity)
            #if (velocity>=5000):
            if (self.player.getDistance(self.destination)<=(self.distance*0.97)):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"If your are getting too much off course, stop the SPEC drive toggling the #9999FFShift+A"+self.msgColor+" key, recenter your target, and then re-enable the manual SPEC drive again with the same keys.")
                VS.IOmessage (10,"Oswald","Privateer",self.msgColor+"When you have approched Atlantis to 10000km please disble the SPEC drive toggling the #9999FFShift+A"+self.msgColor+" key again and then stop your ship.")
                name = unit.getUnitFullName(self.destination)
                self.objective = VS.addObjective("Approach %s" % name)
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+15
                self.practice += 1
        if (self.practice==7 and self.player.getDistance(self.destination)<=10000000):
            VS.setCompleteness(self.objectives[self.objective],1.0)
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"All right.")
            VS.IOmessage (2,"Oswald","Privateer",self.msgColor+"You have learned how to conveniently travel within the system.")
            self.timer = VS.GetGameTime()+2
            self.practice += 1
        if (self.practice==8):
            velocity = Vector.Mag(self.player.GetVelocity())
            if (velocity>=10 and self.player.getDistance(self.destination)<=2000000):
                VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Bring your ship to full stop before crashing into the planet.")
                self.objective = VS.addObjective("Stop your ship")
                self.objectives+=[int(self.objective)]
                self.timer = VS.GetGameTime()+10
                self.practice += 1
            else:
                self.practice += 2
        if (self.practice==9):
            velocity = Vector.Mag(self.player.GetVelocity())
            if (velocity<=10):
                VS.setCompleteness(self.objectives[self.objective],1.0)
                self.practice += 1
        if (self.practice==10):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"Now dock to the planet, go to the mission computer, and save your game.")
            VS.IOmessage (7,"Oswald","Privateer",self.msgColor+"Then get yourself a Jump Drive and an Overdrive and come back for more tutoring if you wish.")
            VS.IOmessage (15,"Oswald","Privateer",self.msgColor+"Turn towards the planet and press the docking clearance request key #9999FFD"+self.msgColor+". A green docking frame will appear.")
            VS.IOmessage (25,"Oswald","Privateer",self.msgColor+"You may still enable the SPEC drive until you close up on the planet and your velocity matches the set velocity.")
            VS.IOmessage (35,"Oswald","Privateer",self.msgColor+"Press again the #9999FFD"+self.msgColor+" key to dock. The docking distance will depend on the planet or station size that you are docking to.")
            VS.IOmessage (45,"Oswald","Privateer",self.msgColor+"The larger the object the further away you can dock.")
            VS.IOmessage (50,"Oswald","Privateer",self.msgColor+"For Atlantis the docking distance is roughly about 990 kilometers.")
            self.timer = VS.GetGameTime()+50
            self.practice += 1
        if (self.practice==11 and self.destination.isDocked(self.player)):
            VS.IOmessage (0,"Oswald","Privateer",self.msgColor+"That concludes the navigation part of the tutorial.")
            self.timer = VS.GetGameTime()+0
            self.practice = 99
        if (self.practice>=99):
            # make sure to reset the counter for the next practice loops
            self.practice = 0
            self.stage = COMPLETE_TUTORIAL4
            self.putSaveValue(self.stage)

    # the execute loop for (nearly) each frame
    def Execute (self):
        # do not do anything before the player undocks
        if (self.stage==STAGE_DOCKED):
              self.playerIsUndocked()
        # if the player did not die
        if (not self.player.isNull()):
            # when in space, launch the drone
            if (self.stage==STAGE_AWAY and VS.GetGameTime()>self.timer):
                # a nice way to make the tutor talk only during the intended time
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.launchNewDrone()
        if (not self.player.isNull() and not self.drone.isNull()):
            # when drone is launched, then follow player
            if (self.stage==STAGE_ORBIT):
                print "---STAGE_ORBIT---"
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.orbitMe()
                self.acceptTutorial()
            if (self.stage==STAGE_ACCEPT and VS.GetGameTime()>self.timer):
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.tutorialComm()
            if (self.stage==COMPLETE_TUTORIAL1 and VS.GetGameTime()>self.timer):
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.tutorialNav()
            if (self.stage==COMPLETE_TUTORIAL2 and VS.GetGameTime()>self.timer):
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.practiceNav()
            if (self.stage==COMPLETE_TUTORIAL3 and VS.GetGameTime()>self.timer):
                if (VS.GetGameTime()>self.timer):
                    self.player.commAnimation("com_tutorial_oswald.ani")
                self.orbitMe()
                self.practiceSpec()
            # tutorial is incomplete, so a nice excuse is required
            if (self.stage==COMPLETE_TUTORIAL4 and VS.GetGameTime()>self.timer):
                VS.IOmessage (0,"Oswald","player",self.msgColor+"Oops. Sorry, pal. My boss at the Cephid Safety Initiative has an emergency situation I must handle now.")
                VS.IOmessage (5,"Oswald","player",self.msgColor+"I apologize. Have a safe journey. And come back for more.")
                self.player.commAnimation("com_tutorial_oswald.ani")
                self.drone.SetVelocity((2000,0,0))
                self.timer = VS.GetGameTime()+10
                self.stage = 99
            # if th eturorial was declines
            if (self.stage==98 and VS.GetGameTime()>self.timer):
                self.stage += 1
            # let the drone disappear
            if (self.stage==99 and VS.GetGameTime()>self.timer):
                self.drone.PrimeOrders()
                self.playernum = -1
                self.name = "quest_tutorial"
                self.removeQuest()
                self.stage += 1
        ## keep the script alive for execution
        return 1

# call this from the adventure file
class quest_tutorial_factory (quest.quest_factory):
    def __init__ (self):
       quest.quest_factory.__init__ (self,"quest_tutorial")
    def create (self):
        return quest_tutorial()

# In order to work properly in mission scripts for testing purposes
# it must inherit the Director.Mission class *and* call its constructor.
# Unfortunately quests must inherit from the quest class, so you need to use a wrapper class
class Executor(Director.Mission):
   def __init__(self, classesToExecute):
      Director.Mission.__init__(self)
      self.classes = classesToExecute
   def Execute(self):
      for c in self.classes:
         c.Execute()
