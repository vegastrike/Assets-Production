import mission_lib
import vsrandom
import Base
import VS
import quest
import Director
import fixers
letters="123456789a0bcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def hashLetter(l):
	return letters.find(l[0])+1
def CanMerchantGuild():
	import universe
	basename=universe.getDockedBaseName()
	if (len(basename[0])==0 or len(basename[1])==0):
		return 0
	return (hashLetter(basename[0][0])+hashLetter(basename[1][0]))%2==0
def CanMercenaryGuild():
	import universe
	basename=universe.getDockedBaseName()
	if (len(basename[0])==0 or len(basename[1])==0):
		return 0	
	return (hashLetter(basename[0][0])+hashLetter(basename))%4<=1
class Guild:
	"""Stores information about the guild itself (name, mission types, number of missions)"""
	def __init__(self, name, min, max, missiontypes, membership,tech=[]):
		"""Initializes the guild"""
		self.name=name.split('/')[0]
		self.missions=missiontypes
		self.minmissions=min
		self.maxmissions=max
		self.nummissions=-1
		self.savestring="Joined"+self.name+"Guild"
		self.membership=membership
		self.tech=tech

	def MakeMissions(self):
		"""Creates the missions using the mission_lib interface"""
		self.nummissions=vsrandom.randrange(self.minmissions,self.maxmissions+1)
		self.nummissions=mission_lib.CreateGuildMissions(self.name, self.nummissions, self.missions)
	
	def HasJoined(self):
		plr=VS.getPlayer().isPlayerStarship()
		return quest.checkSaveValue(plr,self.savestring)
	
	def CanPay(self):
		plr=VS.getPlayer()
		if self.membership<plr.getCredits():
			return True
		return False
	
	def Join(self):
		plr=VS.getPlayer()
		plrnum=plr.isPlayerStarship()
		VS.StopAllSounds()
		if self.CanPay():
			quest.removeQuest(plrnum,self.savestring,1)
			plr.addCredits(-1*self.membership)
			for tt in self.tech:
				import universe
				universe.addTechLevel(tt)
			Base.Message('Thank you for joining the '+str(self.name)+' Guild! Feel free to accept any of our large quantity of high-paying missions.')
			VS.playSound("guilds/"+str(self.name).lower()+"accept.wav",(0,0,0),(0,0,0))
		else:
			Base.Message('We have checked your account and it apperas that you do not have nough credits to join this guild. Please come back and reconsider our offer when you have recieved more credits.')
			VS.playSound("guilds/"+str(self.name).lower()+"notenoughmoney.wav",(0,0,0),(0,0,0))

class Button:
	"""A button that you can click on."""
	def __init__(self,spritefile,x,y,wid,hei,room,linkdesc,index,pythonstr):
		"""Initializes the button (but does not draw it; use drawobjs())"""
		self.sprite=spritefile
		self.x=x
		self.y=y
		self.wid=wid
		self.hei=hei
		self.room=room
		self.linkdesc=linkdesc
		self.index=index
		self.pythonstr=pythonstr
		self.state=0
	
	def drawobjs(self):
		"""Creates the button in the guild room"""
		if self.state==0:
			Base.Python(self.room,self.index,self.x,self.y,self.wid,self.hei,self.linkdesc,self.pythonstr,True)
			if self.sprite and type(self.sprite)==tuple and len(self.sprite)>2:
				print 'Drawing sprite!'
				Base.Texture(self.room,self.index,self.sprite[0],self.sprite[1],self.sprite[2])
			else:
				print "no sprite!"
			self.state=1
	
	def removeobjs(self):
		"""Hides the button"""
		if self.state==1:
			Base.EraseLink(self.room,self.index)
			if self.sprite and type(self.sprite)==tuple and len(self.sprite)>2:
				Base.EraseObj(self.room,self.index)
			self.state=0

class AcceptButton(Button):
	def __init__(self,spritefile,x,y,wid,hei,guildroom):
		Button.__init__(self,spritefile,x,y,wid,hei,guildroom.room,"Accept this Mission","accept","#G#\nimport guilds\nguilds.AcceptMission("+str(guildroom.room)+",'"+guildroom.guild.name+"')")
		self.guild=guildroom

class MissionButton(Button):
	def __init__(self,spritefile,x,y,wid,hei,guildroom,missionnum):
		pythonstr='#G#\nimport guilds\nguilds.SetCurrentMission('+str(guildroom.room)+",'"+guildroom.guild.name+"',"+str(missionnum)+')'
		desc="View Mission Description (Mission " + str(missionnum+1)+")"
		Button.__init__(self,spritefile,x,y,wid,hei,guildroom.room,desc,"missiondesc_guild_"+guildroom.guild.name+"_"+str(missionnum),pythonstr)
		self.guild=guildroom
		self.missionnum=missionnum
		self.missionname=guildroom.guild.name+'/'+str(missionnum)
		self.isactive=False
	
	def select(self):
		if VS.numActiveMissions()>3:
			Base.Message('You are already doing too many missions. Finish those first, and then come back to the guild.')
		else:
			self.removeobjs()
			mission_lib.BriefLastMission(self.missionname,0, self.guild.textbox)
	
	def deselect(self):
		self.drawobjs()

	def drawobjs(self):
		if not self.isactive:
			if (self.missionnum<self.guild.guild.nummissions):
				Button.drawobjs(self)
	
	def accept(self):
		if VS.numActiveMissions()>3:
			Base.Message('You are already doing too many missions. Finish those first, and then come back to the guild.')
		else:
			self.isactive=True
			self.removeobjs()
			mission_lib.SetLastMission(self.missionname);
			mission_lib.BriefLastMission(self.missionname,1,self.guild.textbox)
			mission_lib.LoadLastMission()
#			Base.Message('Thank you. We look forward to the completion of your mission.')

class GuildRoom:
	"""Stores information about this instance of the guild room in this base."""
	def __init__(self,guild,room):
		self.buttons={}
		self.acceptbutton=None
		self.textbox=None
		self.guild=guild
		self.room=room
		self.missionnum=-1
	
	def AddMissionButton(self,button):
		self.buttons[button.missionnum]=button
	
	def AddAcceptButton(self,abutton):
		self.acceptbutton=abutton
	
	def AddTextBox(self,textbox):
		self.textbox=textbox
	
	def AcceptMission(self):
		if self.missionnum>=0:
			self.buttons[self.missionnum].accept()
			self.missionnum=-1
	
	def SetCurrentMission(self,missionnum):
		if self.missionnum>=0:
			self.buttons[self.missionnum].deselect()
		elif missionnum>=0:
			self.acceptbutton.drawobjs()
		for a in self.buttons:
			self.buttons[a].removeobjs()
		for a in self.buttons:
			self.buttons[a].drawobjs()
		self.missionnum=missionnum
		if self.missionnum>=0:
			self.buttons[self.missionnum].select()
	
	def drawobjs(self):
		print 'len buttons'
		print len(self.buttons)
		print 'num missions'
		print self.guild.nummissions
		print 'button list'
		print self.buttons
		for m in range(min(len(self.buttons),self.guild.nummissions)):
			print 'draw button'
			self.buttons[m].drawobjs()

guildrooms={}
guilds={
	'Merchant'  :  Guild('Merchant',  3, 5, ['Escort', 'Cargo' ], 1000.00,["merchant"]),
	'Mercenary' :  Guild('Mercenary', 3, 5, ['Bounty', 'Defend'], 5000.00,["hunter"])
	}
def AcceptMission(room,guildname):
	if guildname in guildrooms:
		for guildroom in guildrooms[guildname]:
			if guildroom.room==room:
				guildroom.AcceptMission()
				return True
	return False

def SetCurrentMission(room,guildname,missionnum):
	if guildname in guildrooms:
		for guildroom in guildrooms[guildname]:
			if guildroom.room==room:
				guildroom.SetCurrentMission(missionnum)
				return True
	return False
def JoinGuild(guildname):
	guilds[guildname].Join()
	fixers.DestroyActiveButtons()
	print 'Creahte it ' + guildname
	if guildname in guildrooms:
		print 'Create it ' + str(guildrooms[guildname])
		for guildroom in guildrooms[guildname]:
			print "drawing"
			guildroom.drawobjs()
def TalkToReceptionist(guildname,introtext):
	text=introtext
	import campaign_lib
	if campaign_lib.doTalkingHeads():
		campaign_lib.AddConversationStoppingSprite("Receptionist","bases/heads/"+guildname.lower()+".spr",(.582,-.2716),(3.104,2.4832),"Return_To_Guild").__call__(Base.GetCurRoom(),None)
	print 'start ('+str(guildname)+','+str(introtext)+')'
	if guildname in guilds:
		guild=guilds[guildname]
		if not guild.HasJoined():
			text+='  Membership is '+str(guild.membership)+' credits.  Please consider joining our guild'
			if not guild.CanPay():
				text+=' when you have more money'
			text+='.'
		Base.Message (text)
		if not guild.HasJoined():
			VS.StopAllSounds()
			if guild.CanPay():
				fixers.CreateChoiceButtons(Base.GetCurRoom(),[
					fixers.Choice("bases/fixers/yes.spr","#G#\nimport guilds\nguilds.JoinGuild('"+guildname+"')","Accept This Agreement"),
					fixers.Choice("bases/fixers/no.spr","bases/fixers/no.py","Decline This Agreement")])

				VS.playSound("guilds/"+str(guild.name).lower()+"invite.wav",(0,0,0),(0,0,0))
			else:
				VS.playSound("guilds/"+str(guild.name).lower()+"notenoughmoney.wav",(0,0,0),(0,0,0))			
		return

def CreateGuild(guildroom):
	guildname=guildroom.guild.name
	print 'Create it ' + guildname
#	if guildname in guildrooms:
#		guildrooms[guildname].append(guildroom)
#	else:
	if True:
		print 'make missions'
		guildroom.guild.MakeMissions()
		guildrooms[guildname]=[guildroom]
		print 'true'
		if guildroom.guild.HasJoined():
			print 'has joined.'
			guildroom.drawobjs()

def Clear():
	del guildrooms
	guildrooms={}
