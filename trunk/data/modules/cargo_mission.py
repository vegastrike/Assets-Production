import universe
import random
import launch
import faction_ships
import VS
import Briefing
class cargo_mission:
	you=VS.Unit()
	faction=""
	destination=""
	base=VS.Unit()
	cargoname=""
	arrived=0
	difficulty=1
	distfrombas=0
	quantity=1
	cred=0
	capship=0
	mission_time=0
	jumps=()
        mplay=self.mplay
	def initbriefing(self):
		self.jump_ani=0
		self.rnd_y=0.0
		self.added_warp=1
		self.brief_stage=0
		self.begintime= VS.getGameTime()-6.0
		print "starting briefing"
		if (self.you.isNull()):
			VS.terminateMission(0)
			Briefing.terminate()
			return
		faction=you.getFaction()
		name=you.getName()
		self.brief_you=Briefing.addShip(name,faction,(0.0,0.0,80.0))
		VS.IOmessage (0,"cargo mission","briefing","Your mission for today will be to deliver some %s cargo to the %s system.\nIn order to get there, you must follow this route that we have planned out for you." % (cargoname,destination))
	
	def loopbriefing(self):
		size=len(jumps)
		time = VS.getGameTime()
		Briefing.setCamPosition((1.6*(time-self.begintime)*self.brief_stage,0.0,0.0))
		if (((time-self.begintime)>=5.0) and added_warp):
			self.jump_ani=Briefing.addShip("brief_warp",faction,(20.0*(brief_stage),rnd_y,79.5+rnd_y))
			self.added_warp=0
		if (((time-self.begintime)>=6.0)):
			if (self.jump_ani!=0):
				Briefing.removeShip(self.jump_ani)
				self.jump_ani=0
		if ((size==self.brief_stage) and ((time-self.begintime)>=6.0)):
			VS.IOmessage(0,"cargo mission","briefing","Once there, you must drop the cargo off at a specified unit")
			self.brief_stage=size+1
			self.added_warp=0
			self.time=0.0
		elif ((self.brief_stage>size) and ((time-self.begintime)>=11.0)):
			Briefing.terminate()
			return
		elif (((time-self.begintime)>=6.0) and (self.brief_stage<size)):
			self.added_warp=1
			self.rnd_y=(random.random()*40.0-20.0)
			Briefing.addShip("brief_jump",faction,(20.0*(self.brief_stage+1),self.rnd_y,79.6+self.rnd_y))
			Briefing.enqueueOrder (self.brief_you,(20.0*(self.brief_stage+1),self.rnd_y,80.0+self.rnd_y,5.0))
			self.begintime=time
			myname=self.jumps[self.brief_stage]
			VS.IOmessage (0,"cargo mission","briefing","You must go to the '%s' jump point" % (myname))
			self.brief_stage+=1
	
	def endbriefing(self):
		print "endinging briefing"
		del self.jump_ani
		del self.rnd_y
		del self.added_warp
		del self.brief_stage
		del self.begintime
	
	def __init__ (self,factionname, numsystemsaway, cargoquantity, missiondifficulty, distance_from_base, creds, launchoncapship, time_to_complete, category):
	  self.mission_time=VS.getGameTime()+time_to_complete*100*float(1+numsystemsaway)
	  self.capship= launchoncapship
	  self.faction=factionname
	  self.cred=creds
#####	  universe.init()
	  self.distfrombase=distance_from_base
	  self.difficulty=missiondifficulty
	  mysys=VS.getSystemFile()
	  self.quantity=cargoquantity
	  sysfile = mysys
	  self.you=VS.getPlayer()
	  mplay=universe.getMessagePlayer(self.you)
	  if (self.quantity<1):
	    self.quantity=1
	  carg=VS.getRandCargo(quantity,category)
	  if (carg.GetQuantity()==0):
	    carg = VS.getRandCargo(quantity,"")
	  tempquantity=self.quantity
	  self.cargoname=carg.GetContent()
	  name = you.getName ()
	  if (self.you):
	    quantity = self.you.addCargo(carg)  #I add some cargo
	  else:
	    VS.terminateMission (0)
	    return
	  creds_deducted = (carg.GetPrice()*float(self.quantity)*random.random()+1)
	  self.cred += creds_deducted
	  if (tempquantity>0):
	    self.cred*=float(quantity)/float(tempquantity)
	  else:
	    VS.IOmessage (2,"cargo mission",self.mplay,"You do not have space to add our cargo to the mission. Mission failed.")
	    VS.terminateMission(0)
	  return
	  
	  if (quantity==0):
	    VS.IOmessage (2,"cargo mission",self.mplay,"You do not have space to add our cargo to the mission. Mission failed.")
	    VS.terminateMission(0)
 	    return
	  
	  VS.IOmessage (0,"cargo mission",self.mplay,"Good Day, %s. Your mission is as follows:" % (name))
	  (self.destination,self.jumps)=universe.getAdjacentSystems(sysfile,numsystemsaway)
	  VS.IOmessage (2,"cargo mission",self.mplay,"and give the cargo to a %s unit." % (faction))
	  VS.IOmessage (3,"cargo mission",self.mplay,"You will receive %d of the %s cargo" % (quantity,cargoname))
	  VS.IOmessage (4,"cargo mission",self.mplay,"We will deduct %.2f credits from your account for the cargo needed." % (creds_deducted))
	  VS.IOmessage (5,"cargo mission",self.mplay,"You will earn %.2f more credits when you deliver our cargo." % (creds))
	  self.you.addCredits (-creds_deducted)
	
	def takeCargoAndTerminate (self,you, remove):
	  removenum=0 #if you terminate without remove, you are SKREWED
	  if (remove):
	    removenum=you.removeCargo(cargoname,quantity,1)
	  
	  if ((removenum==self.quantity) or (self.quantity==0)):
	    VS.IOmessage (0,"cargo mission",self.mplay,"Excellent work pilot.")
	    VS.IOmessage (0,"cargo mission",self.mplay,"You have been rewarded for your effort as agreed.")
	    VS.IOmessage (0,"cargo mission",self.mplay,"Your excellent work will be remembered.")
	    you.addCredits(self.cred)
	    VS.terminateMission(1)
	    return
	  else:
	    VS.IOmessage (0,"cargo mission",self.mplay,"You did not follow through on your end of the deal.")
	    if (self.difficulty<1):
	      VS.IOmessage (0,"cargo mission",self.mplay,"Your pay will be reduced")
	      VS.IOmessage (0,"cargo mission",self.mplay,"And we will consider if we will accept you on future missions.")
	      addcred=(float(removenum)/float((self.quantity*(1+self.difficulty))))*self.cred
	      VS.addCredits(you,addcred)
	    else:
	      VS.IOmessage (0,"cargo mission",self.mplay,"You will not be paid!")
	      if (self.difficulty>=2):
		VS.IOmessage (0,"cargo mission",self.mplay,"And your idiocy will be punished.")
		VS.IOmessage (0,"cargo mission",self.mplay,"You had better run for what little life you have left.")
		for i in range(self.difficulty):
		  un=faction_ships.getRandomFighter(self.faction)
		  newunit=launch.launch_wave_around_unit("shadow", self.faction, un, "default", 1, 200.0,400.0,you)
		  newunit.setFgDirective("B")
		  newunit.setTarget(you)
	    VS.terminateMission(0)
	    return
	  
	
	def Execute (self):
##	  if (VS.getGameTime()>mission_time):
##	    VS.IOmessage (0,"cargo mission",self.mplay,"You Have failed to deliver your cargo in a timely manner.")
##	    VS.IOmessage (0,"cargo mission",self.mplay,"The cargo is no longer of need to us.")
##	    if (you):
##	      takeCargoAndTerminate(you,0)
##	    return
	  if (arrived):
	    if (self.base.isNull() or self.you.isNull()):
	      VS.IOmessage (0,"cargo mission",self.mplay,"Mission failed. You were unable to deliver cargo.")
	      VS.terminateMission(0)
	      return
	    dist=you.getSignificantDistance(base)
	    if (dist<=self.distfrombase):
	      self.takeCargoAndTerminate(self.you,1)		
	      return
	  else:
	    sysfil = VS.getSystemFile()
	    if (sysfil==destination):
	      self.arrived=1
	      newship=faction_ships.getRandomCapitol(faction)
	      randint=random.randrange(0,50)
	      significant = unit.getSignificant (randint,(not capship),0)
	      if (_std.isNull (significant)):
		significant =VS.getPlayer()
	      if (_std.isNull(significant)):
		self.arrived=0
	      else:
		newun=significant
		if (self.capship):
		  newun=launch.launch_wave_around_unit("Base",self.faction,newship,"sitting_duck",1,2000.0,5000.0,significant)
		name = newun.getName ()
		VS.IOmessage (0,"cargo mission",self.mplay,"You must drop your cargo off with the %s." % (name))
		if (capship):
		  name=significant.getName()
		  VS.IOmessage (0,"cargo mission",self.mplay,"It is docked around the %s landmark." % (name))
		self.base=newun

def initrandom (factionname, missiondifficulty,creds_per_jump, launchoncapship, sysmin, sysmax, time_to_complete, category):
	return cargo_mission(factionname,random.random(sysmin,sysmax), random.randrange(4,15), missiondifficulty,400.0,creds_per_jump*float(1+numsys),launchoncapship, 10.0, category)

