import Director
import patrol
import cargo_mission
import bounty
import plunder
import defend
import escort_mission
import vsrandom
import universe
import faction_ships
import VS
last_constructor={}
saved_args = (1,1,1,1,)#nice patrol args
last_args ={}
last_briefing=[{},{}]

lastMission=None

def SetLastMission(which):
	global lastMission
	lastMission=str(which)
	print 'set last mission to "'+str(which)+'"'

def LoadLastMission():
	global lastMission
	which=lastMission
	if which in last_constructor and which in last_args:
		if last_constructor[which]==None:
			if type(last_args[which])==str:
				VS.LoadMissionScript(last_args[which])
			else:
				VS.LoadMissionScript(repr(last_args[which])+"()")
		else:
			cons=last_constructor[which]
			if type(cons)!=str:
				cons=cons.__name__			
			if type(last_args[which])==str:
				VS.LoadMissionScript('#\nimport '+cons+'\n'+cons+'.'+cons+last_args[which])
			else:
				VS.LoadMissionScript('#\nimport '+cons+'\n'+cons+'.'+cons+repr(last_args[which]))
		del last_args[which]
		del last_constructor[which]
	else:
		print 'No last mission with name "'+str(which)+'"'
	if which in last_briefing[0]:
		del last_briefing[0][which]
	if which in last_briefing[1]:
		del last_briefing[1][which]
	lastMission=None

def BriefLastMission(which,first,textbox=None):
	import Base
	which=str(which)
	if first<0 or first>=len(last_briefing):
		return
	if (which in last_briefing[first]):
		if textbox:
			Base.SetTextBoxText(Base.GetCurRoom(),textbox, last_briefing[first][which])
		else:
			Base.Message (last_briefing[first][which])

def AddNewMission(which,args,constructor=None,briefing0='',briefing1=''):
	which=str(which)
	last_constructor[which]=constructor
	last_args[which]=args
	last_briefing[0][which]=briefing0
	last_briefing[1][which]=briefing1

def Jumplist (jumps):
	if not len(jumps):
		return 'Your destination is this system.'
	str="First of all, you will need to fly to the %s jumppoint. "%jumps[0].split('/')[-1]
	for j in jumps[1:]:
		str+="Then jump in the %s jumppoint. "%j.split('/')[-1]
	return str

def MakePlunder(which):
	last_constructor[which] = plunder.plunder
	creds=vsrandom.randrange(15,25)*1000
	last_args[which] = (creds,'pirates',5,'Contraband',1)
	last_briefing[0][which] = 'Arr Matey. We have a target in this system that needs a lil roughin up. We need you to bag a merchant and deliver her cargo into our hands.  It\'s worth '+str(creds)+ ' to us. Up to you, ya space pirate.'
	last_briefing[1][which] = 'Ahoy! We\'ll be lookin for that cargo mighty soon!'
	return ("bases/fixers/pirate.spr","Talk with the Pirate")
def MakeContraband(which):
	last_constructor[which] = cargo_mission.cargo_mission
	numsys=vsrandom.randrange(2,5)
	jumps=universe.getAdjacentSystems(VS.getSystemFile(),numsys)[1]
	diff=vsrandom.randrange(0,3)
	creds=numsys*2500+diff*800
	last_args[which] = ('pirates', 0, 6, diff,creds, 1, 1200, 'Contraband',jumps)
	last_briefing[0][which] = 'We need some...*cough*... cargo delivered to some of our pirates in a nearby system: '+ Jumplist(jumps)+ ' It\'d be preferable if ye kept the ole po\' off yo back durin the run. Will ya do it for '+str(creds)+' creds?'
	last_briefing[1][which] = 'Thanks pal; keep it on the d&l if you know my meanin.'
	return ("bases/fixers/pirate.spr","Talk with the Pirate")

def CreateRandomMission(whichnum):
	"""This function gets a random mission and saves the infomation in
an array as the which element. Returns the sprite file and text"""
	which=str(whichnum)
	missiontype = vsrandom.random();
	fac = VS.GetGalaxyFaction(VS.getSystemFile())
	if fac=="pirates":
		if (missiontype>.5):
			return ()
		missiontype*=.2;
	elif (VS.GetRelation(fac,"pirates")<-.8 and missiontype<.1):
		missiontype=.1+.9*missiontype
	plr=VS.getPlayer().isPlayerStarship()
#	while (len (last_constructor)<=whichnum):
#		last_constructor[which]=(patrol.patrol)
#		last_args[which]=(saved_args)
#		last_briefing[0][which]=('ERROR in mission_lib.py.')
#		last_briefing[1][which]=('ERROR in mission_lib.py.')
	if (missiontype<.05):
		return MakePlunder(which)
	elif (missiontype<.1):####CONTRABAND
		return MakeContraband(which)
	else:
		goodlist=[]
		for indx in range(Director.getSaveStringLength(plr, "mission_scripts")):
			script=Director.getSaveString(plr,"mission_scripts",indx)
			if script.find("#F#")!=-1:
				goodlist.append(indx)
		goodlist.sort()
		goodlist.reverse()
		if len(goodlist):
			i=goodlist[vsrandom.randrange(len(goodlist))]
			script=Director.getSaveString(plr,"mission_scripts",i)
			desc=Director.getSaveString(plr,"mission_descriptions",i)
			Director.eraseSaveString(plr,"misson_scripts",i)
			Director.eraseSaveString(plr,"misson_descriptions",i)
			Director.eraseSaveString(plr,"misson_names",i)
			last_constructor[which]=None
			last_args[which]=script
			last_briefing[0][which]=desc
			mylist=script.split("#")  ###Skip the first two because first is always '' and second is always 'F'
			last_briefing[1][which]=mylist[4]
			return (mylist[2],mylist[3])
		else:
			# It should only get here if no fixer missions were found
			return ()  # Fixer code will generate a NoFixer hopefully.
##			  if (searchMissionNameStr("patrol")):
##					last_briefing[0][which] = 'Confed needs the help of mercs and hunters to keep our air space clean.  There are increasing reports of pirate and alien activity in these sectors and we need your sensor data. '+Jumplist(jumps) +' Will you do the patrol in said system for '+str(creds)+' credits?'
##			  if (searchMissionNameStr("cargo")):
##					last_briefing[0][which] = 'Our business needs you to run some legit goods to a base a few systems away. '+ Jumplist(jumps) + ' This is worth '+str(creds)+' to us.'
##					if (diff>=2):
##							last_briefing[0][which]+=' However, you cannot fail us!  There are consequences for your actions in this universe.'
##			  if (searchMissionNameStr("bounty")):
##					last_briefing[0][which] = 'We need you to hit a nearby target. '+Jumplist(jumps)+' Our reward is '+str(creds)+' will you do it?'
##			  if (searchMissionNameStr("defend")):
##					last_briefing[0][which] = 'We need help to secure a nearby strategic point in this system. Eliminate all enemies there. We offer '+str(encred)+' per enemy. Will you do it?'
##					if (base):
##							last_briefing[0][which] = 'One of our capitol vessels is under attack in this system! We call to the aid of all bounty hunters to defend it.  Our reward is '+str(encred)+' per enemy craft destroyed.  Will you help us?'


def CreateGuildMissions(guildname,nummissions,accepttypes):
	plr=VS.getPlayer().isPlayerStarship()
	goodlist=[]
	for indx in range(Director.getSaveStringLength(plr, "mission_scripts")):
		script=Director.getSaveString(plr,"mission_scripts",indx)
		if script.find("#G#")!=-1:
			missiontype=script[3:script.find('#',3)]
			if missiontype in accepttypes:
				goodlist.append(indx)
	if len(goodlist)<nummissions:
		nummissions=len(goodlist)
	delit=[]
	for missionnum in range(0,nummissions):
		goodi=vsrandom.randrange(len(goodlist))
		i=goodlist[goodi]
		which=guildname+'/'+str(missionnum)
		script=Director.getSaveString(plr,"mission_scripts",i)
		desc=Director.getSaveString(plr,"mission_descriptions",i)
		delit.append(i)
		last_constructor[which]=None
		last_args[which]=script
		last_briefing[0][which]=desc
		last_briefing[1][which]=''
		goodlist.pop(goodi)
	delit.sort()
	delit.reverse()
	for i in delit:
		Director.eraseSaveString(plr,"misson_scripts",i)
		Director.eraseSaveString(plr,"misson_descriptions",i)
		Director.eraseSaveString(plr,"misson_names",i)
	return nummissions

