import mission_lib
import vsrandom
import Base
import VS
import quest
import Director
import fixers

class Guild:
	"""Stores information about the guild itself (name, mission types, number of missions)"""
	def __init__(self, name, min, max, missiontypes, membership):
		"""Initializes the guild"""
		self.name=name.split('/')[0]
		self.missions=missiontypes
		self.minmissions=min
		self.maxmissions=max
		self.nummissions=-1
		self.savestring="Joined"+self.name+"Guild"
		self.membership=membership

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
		if self.CanPay():
			quest.removeQuest(plrnum,self.savestring,1)
			plr.addCredits(-1*self.membership)
			Base.Message('Thank you for joining the '+str(self.name)+' Guild! Feel free to accept any of our large quantity of high-paying missions.')
		else:
			Base.Message('We have checked your account and it apperas that you do not have nough credits to join this guild. Please come back and reconsider our offer when you have recieved more credits.')

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
			Base.Python(self.room,self.index,self.x,self.y,self.wid,self.hei,self.linkdesc,self.pythonstr,False)
			if self.sprite and len(self.sprite):
				Base.Texture(self.room,self.index,self.sprite,self.x+self.wid/2,self.y+self.hei/2)
			self.state=1
	
	def removeobjs(self):
		"""Hides the button"""
		if self.state==1:
			Base.EraseLink(self.room,self.index)
			if self.sprite and len(self.sprite):
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
	
	def select(self):
		if VS.numActiveMissions()>3:
			Base.Message('You are already doing too many missions. Finish those first, and then come back to the guild.')
		else:
			self.removeobjs()
			mission_lib.BriefLastMission(self.missionname,0)
	
	def deselect(self):
		self.drawobjs()
	
	def accept(self):
		if VS.numActiveMissions()>3:
			Base.Message('You are already doing too many missions. Finish those first, and then come back to the guild.')
		else:
			self.removeobjs()
			mission_lib.SetLastMission(self.missionname);
			mission_lib.BriefLastMission(self.missionname,1)
			VS.LoadMission('internal_mission_lib.mission')
			Base.Message('Thank you. We look forward to the completion of your mission.')

class GuildRoom:
	"""Stores information about this instance of the guild room in this base."""
	def __init__(self,guild,room):
		self.buttons={}
		self.acceptbutton=None
		self.guild=guild
		self.room=room
		self.missionnum=-1
	
	def AddMissionButton(self,button):
		self.buttons[button.missionnum]=button
	
	def AddAcceptButton(self,abutton):
		self.acceptbutton=abutton
	
	def AcceptMission(self):
		if self.missionnum>=0:
			self.buttons[self.missionnum].accept()
			self.missionnum=-1
	
	def SetCurrentMission(self,missionnum):
		if self.missionnum>=0:
			self.buttons[self.missionnum].deselect()
		self.missionnum=missionnum
		if self.missionnum>=0:
			self.buttons[self.missionnum].select()
	
	def drawobjs(self):
		for a in self.buttons:
			self.buttons[a].drawobjs()
		self.acceptbutton.drawobjs()
		self.guild.MakeMissions()

guildrooms={}
guilds={
	'Merchant'  :  Guild('Merchant',  3, 5, ['Escort', 'Cargo' ], 20000.00),
	'Mercenary' :  Guild('Mercenary', 3, 5, ['Bounty', 'Defend'], 20000.00)
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
		print 'Create it ' + guildname
		for guildroom in guildrooms[guildname]:
#			if guildroom.room==room:
			if True:
				print 'true'
				guildroom.drawobjs()
def TalkToReceptionist(guildname,introtext):
	text=introtext
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
			if guild.CanPay():
				fixers.CreateChoiceButtons(Base.GetCurRoom(),[
					fixers.Choice("bases/fixers/yes.spr","#G#\nimport guilds\nguilds.JoinGuild('"+guildname+"')","Accept This Agreement"),
					fixers.Choice("bases/fixers/no.spr","bases/fixers/no.py","Decline This Agreement")])

		return

def CreateGuild(guildroom):
	guildname=guildroom.guild.name
	print 'Create it ' + guildname
#	if guildname in guildrooms:
#		guildrooms[guildname].append(guildroom)
#	else:
	if True:
		guildrooms[guildname]=[guildroom]
		print 'true'
		if guildroom.guild.HasJoined():
			print 'has joined.'
			guildroom.drawobjs()

def Clear():
	del guildrooms
	guildrooms={}
