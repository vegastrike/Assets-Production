import patrol
import cargo_mission
import bounty
import plunder
import defend
import escort_mission
import vsrandom
import universe
import faction_ships
import Base
import VS
last_constructor=[]
saved_args = (1,1,1,1,)#nice patrol args
last_args =[]
last_briefing=[[],[]]
def LoadLastMission(which):
	if (len(last_constructor)>which and len(last_args)> which):
		apply (last_constructor[which],last_args[which])
def BriefLastMission(which,first):
	if first<0 or first>=len(last_briefing):
		return
	if (len(last_briefing[first])>which):
		Base.Message (last_briefing[first][which])

def Jumplist (jumps):
	if not len(jumps):
		return 'Your destination is this system.'
	str="First of all, you will need to fly to the %s jumppoint. "%jumps[0].split('/')[-1]
	for j in jumps[1:]:
		str+="Then jump in the %s jumppoint. "%j.split('/')[-1]
	return str

def CreateRandomMission(which):
	"""This function gets a random mission and saves the infomation in
an array as the which element. Returns the sprite file and text"""
	missiontype = vsrandom.random();
	while (len (last_constructor)<=which):
		last_constructor.append(patrol.patrol)
		last_args.append(saved_args)
		last_briefing[0].append('ERROR in mission_lib.py.')
		last_briefing[1].append('ERROR in mission_lib.py.')
	if (missiontype<.19): # 19%
		last_constructor[which] = patrol.patrol
		numsys=vsrandom.randrange(2,6)
		jumps=universe.getAdjacentSystems(VS.getSystemFile(),numsys)[1]
		numsig=vsrandom.randrange(3,9)
		creds=numsys*1500+numsig*500
		last_args[which] = (0,numsig,300,creds,jumps)
		last_briefing[0][which] = 'Confed needs the help of mercs and hunters to keep our air space clean.  There are increasing reports of pirate and alien activity in these sectors and we need your sensor data. '+Jumplist(jumps) +' Will you do the patrol in said system for '+str(creds)+' credits?'
		last_briefing[1][which] = 'Thank you.  Your help makes space a safer place.'
		return ("bases/fixers/confed.spr","Talk to the Confed Officer")
	elif (missiontype <.23): # 4%
		last_constructor[which] = plunder.plunder
		creds=vsrandom.randrange(15,25)*1000
		last_args[which] = (creds,'pirates',5,'Contraband',True)
		last_briefing[0][which] = 'Arr Matey. We have a target in this system that needs a lil roughin up. We need you to bag a merchant and deliver her cargo into our hands.  It\'s worth '+str(creds)+ ' to us. Up to you, ya space pirate.'
		last_briefing[1][which] = 'Ahoy! We\'ll be lookin for that cargo mighty soon!'
		return ("bases/fixers/pirate.spr","Talk with the Pirate")
	elif (missiontype <.5): # 27%
		last_constructor[which] = cargo_mission.cargo_mission
		numsys=vsrandom.randrange(2,6)
		jumps=universe.getAdjacentSystems(VS.getSystemFile(),numsys)[1]
		diff=vsrandom.randrange(0,5)
		creds=numsys*2000+diff*500
		last_args[which] = ('merchant', 0, 6,diff ,creds  , 0, 1200, '',jumps)
		last_briefing[0][which] = 'Our business needs you to run some legit goods to a base a few systems away. '+ Jumplist(jumps) + ' This is worth '+str(creds)+' to us.'
		if (diff>=2):
                    last_briefing[0][which]+=' However, you cannot fail us!  There are consequences for your actions in this universe.'    
		last_briefing[1][which] = 'Thank you. I entrust you will make the delivery successfully'
		return ("bases/fixers/merchant.spr","Talk to the Merchant")
	elif (missiontype <.62): # 12%
		last_constructor[which] = cargo_mission.cargo_mission
		numsys=vsrandom.randrange(2,5)
		jumps=universe.getAdjacentSystems(VS.getSystemFile(),numsys)[1]
		diff=vsrandom.randrange(0,3)
		creds=numsys*2500+diff*800
		last_args[which] = ('pirates', 0, 6, diff,creds, 1, 1200, 'Contraband',jumps)
		last_briefing[0][which] = 'We need some...*cough*... cargo delivered to some of our pirates in a nearby system: '+ Jumplist(jumps)+ ' It\'d be preferable if ye kept the ole po\' off yo back durin the run. Will ya do it for '+str(creds)+' creds?'
		last_briefing[1][which] = 'Thanks pal; keep it on the d&l if you know my meanin.'
		return ("bases/fixers/pirate.spr","Talk with the Pirate")
	elif (missiontype <.81): # 19%
		last_constructor[which] = bounty.bounty
		numsys=vsrandom.randrange(0,2)
		jumps=universe.getAdjacentSystems(VS.getSystemFile(),numsys)[1]
		diff=vsrandom.randrange(0,4)
		fact=faction_ships.factions[vsrandom.randrange(0,len(faction_ships.factions))]
		creds=9000+diff*500+1500*numsys
		rand=vsrandom.random()
		run=0
		if rand<.25:
			run=1
		last_args[which] = (0, 0, creds, run, diff, fact,jumps)
		last_briefing[0][which] = 'We need you to hit a nearby target. '+Jumplist(jumps)+' Our reward is '+str(creds)+' will you do it?'
		last_briefing[1][which] = 'We will pay you on mission completion.  And as far as anyone knows-- we never met.'
		if (run):
                    last_briefing[1][which] += ' Also-- we have information that the target may be informed about your attack and may be ready to run. Be quick!'
		return ("bases/fixers/hunter.spr","Talk with the Bounty Hunter")
	else:                    # 19%
		last_constructor[which] = defend.initrandom
		fact=faction_ships.get_enemy_of('confed')
		rand=vsrandom.random()
		base=0
		numenemymin=3
		numenemymax=6
		encred=3000
		if rand<.4:
			numenemymax=1
			numenemymax=3
			encred=6000
			base=1
			
		last_args[which] = (fact, 0, numenemymin, numenemymax, encred, base, base,'confed')
		last_briefing[0][which] = 'We need help to secure a nearby strategic point in this system. Eliminate all enemies there. We offer '+str(encred)+' per enemy. Will you do it?'
		if (base):
                    last_briefing[0][which] = 'One of our capitol vessels is under attack in this system! We call to the aid of all bounty hunters to defend it.  Our reward is '+str(encred)+' per enemy craft destroyed.  Will you help us?'
            
		last_briefing[1][which] = 'Thank you. Your defense will help confed in the long run.  We appreciate the support of the bounty hunting community.'
		return ("bases/fixers/merchant.spr","Talk to the Confed Officer")
	


