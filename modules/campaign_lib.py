
class Condition:
	def __init__(self):
		pass
	
	def __call__(self):
		return True
	

def checkSaveValue (playernum,questname, value):
	import quest
	return quest.checkSaveValue(playernum,questname,value)
def setSaveValue (playernum,name,value):
	import quest
	quest.removeQuest(playernum,name,value);
def incSaveValue(playernum,name):
	import Director
	mylen = Director.getSaveDataLength(int(playernum),str(name))
	val=0
	if (mylen>0):
		val=Director.getSaveData(int(playernum),str(name),mylen-1)
	val+=1
	setSaveValue(playernum,name,val)
class SaveVariableCondition(Condition):
	def __init__(self,varname,varvalue):
		Condition.__init__(self)
		self.name=str(varname)
		self.value=int(varvalue)
	
	def __call__(self):
		import VS
		print "*** Checking \'%s : %d\'"%(self.name,self.value)
		checked=checkSaveValue(VS.getCurrentPlayer(),self.name,self.value)
		print "*** Returning: " + str(checked)
		return checked
class HaveCredits(Condition):
	def __init__(self,numcreds):
		Condition.__init__(self)
		self.creds=numcreds
	def __call__(self):
		import VS
		un=VS.getPlayer()
		if not un.isNull():			
			cc=un.getCredits()
			ret= (cc>=self.creds)
			print "Have at least "+str(self.creds)+" credits? "+str(cc)+" >= it? "+str(ret)
			return ret
		return False

class InSystemCondition(Condition):
	def __init__(self,system,shipname=None):
		Condition.__init__(self)
		self.system=None
		if system:
			if len(system):
				self.system=system.lower().replace(' ','_').split('/')
		self.dockedshipname=None
		if shipname:
			self.dockedshipname=shipname.replace(' ','_').lower()
	
	def __call__(self):
		import VS
		if self.system:
			sys=VS.getSystemFile().split('/')
			print str(sys)+'==?=='+str(self.system)
			for i in range(-1,-min(len(self.system),len(sys))-1,-1):
				if sys[i].lower()!=self.system[i]:
					print str(sys[i])+'!='+str(self.system[i])
					print '*** insystem return false: not in system!!'
					return False
		if self.dockedshipname:
			if type(self.dockedshipname)==str:
				print '*** Test if docked to: '+ self.dockedshipname
				iter = VS.getUnitList()
				while iter.notDone():
					if VS.getPlayer().isDocked(iter.current()) or iter.current().isDocked(VS.getPlayer()):
						#Not sure why both have to be checked, it seems to second gives a more consistantly correct response
						#find unit with name and check
						print '*** Compare '+iter.current().getName().replace(' ','_').lower()+" == "+self.dockedshipname
						print '    Compare '+iter.current().getFullname().replace(' ','_').lower()+" == "+self.dockedshipname
						if iter.current().getName().replace(' ','_').lower() == self.dockedshipname or iter.current().getFullname().replace(' ','_').lower() == self.dockedshipname:
							print '*** inSystem return true'
							return True
					else:
						print iter.current().getName()+' not docked to unit'
					iter.advance()
		else:
			print '*** inSystem return true, no self.dockedshipname'
			return True
		print '*** insystem return false!!'
		return False


class HasUndocked(Condition):
	def __init__(self):
		Condition.__init__(self)
		self.count=-1
	
	def __call__(self):
		import fixers
		print '*** HasUndocked check false'
		if self.count==-1:
			self.count=fixers.fixerloaded
			return False
		else:
			return fixers.fixerloaded!=self.count


class CargoSpaceCondition(Condition):
	def __init__(self,type,num=1):
		Condition.__init__(self)
		self.type=type
		self.num=num
	
	def __call__(self):
		import VS
		you=VS.getPlayer()
		mpart=VS.GetMasterPartList()
		carg=mpart.GetCargo(self.type)
		carg.SetContent(self.type)
		carg.SetQuantity(self.num)
		numcarg=you.addCargo(carg)
		you.removeCargo(self.type,numcarg,True)
		if numcarg<self.num:
			print '*** CargoSpace return false::IGNORED'
			#return False
		print '*** CargoSpace return true'
		return True
	

class AtMostActiveMissionsCondition(Condition):
	def __init__(self,num=0):
		Condition.__init__(self)
		self.num=num
	
	def __call__(self):
		import VS
		print '*** U half active mishuns <= ?'
		print '*** '+str(VS.numActiveMissions()-1)+' <= '+str(self.num)
		isactive=((VS.numActiveMissions()-1)<=self.num)
		print '*** '+str(isactive)
		return isactive
	

class AtLeastActiveMissionsCondition(Condition):
	def __init__(self,num=1):
		Condition.__init__(self)
		self.num=num
	
	def __call__(self):
		import VS
		print '*** U half active mishuns >= ?'
		print '*** '+str(VS.numActiveMissions()-1)+' >= '+str(self.num)
		isactive=((VS.numActiveMissions()-1)>=self.num)
		print '*** '+str(isactive)
		return isactive
	

class OrCondition(Condition):
	def __init__(self,conds,cond2=None):
		Condition.__init__(self)
		if cond2:
			self.conds=[conds,cond2]
		else:
			self.conds=conds
	
	def __call__(self):
		for c in self.conds:
			if c():
				return True
		return False
	

class AndCondition(Condition):
	def __init__(self,conds,cond2=None):
		Condition.__init__(self)
		if cond2:
			self.conds=[conds,cond2]
		else:
			self.conds=conds
	
	def __call__(self):
		for c in self.conds:
			if not c():
				return False
		return True
	

class InvertCondition(Condition):
	def __init__(self,cond):
		Condition.__init__(self)
		self.cond=cond
	
	def __call__(self):
		if self.cond():
			return False
		return True
	

InverseCondition=InvertCondition
NotCondition=InvertCondition


def tohex(r,g,b):
	def bytehex(num):
		def bytehex2(num):
			if num<10:
				return chr(num+ord('0'))
			else:
				return chr(num+ord('a')-10)
		return bytehex2(num/16)+bytehex2(num%16)
	return '#'+bytehex(int(r*255))+bytehex(int(g*255))+bytehex(int(b*255))

def getcolor(strs):
	h=(hash(strs)/2147483647.+1)/2
	if h<.1666666:
		return tohex(0,h/.1666666,1)
	elif h<.3333333:
		return tohex(0,1,1-((h-.1666666)/.1666666))
	if h<.5:
		return tohex((h-.3333333)/.1666666,1,0)
	elif h<.6666666:
		return tohex(1,1-((h-.5)/.1666666),0)
	elif h<.8333333:
		return tohex(1,0,(h-.6666666)/.1666666)
	else:
		return tohex(1-((h-.8333333)/.1666666),0,1)

def textline(strs):
	if type(strs) is list or type(strs) is tuple:
		if len(strs)>1:
			sound=None
			ret1=True
			if len(strs)>2:
				sound=strs[2]
			elif strs[1][-4:]=='.wav':
				sound=strs[1]
				ret1=False
			if sound and sound!='':
				import VS
				VS.StopAllSounds()
				print "playing sound "+str(sound)
				VS.playSound (sound, (0.,0.,0.), (0.,0.,0.))
			if ret1:
				return getcolor(str(strs[0]))+str(strs[0])+": #000000"+str(strs[1])
		return strs[0]
	return "#00ff00"+str(strs)

#depends on Base
def displayText(room,textlist,enqueue=False):
	import Base
	func=Base.MessageToRoom
	if enqueue:
		func=Base.EnqueueMessageToRoom
	if type(textlist) is str:
		if textlist!='':
			print '*** Base.message('+textlist+')'
			func(room,textline(textlist))
	else:
		if textlist and len(textlist):
			print '*** Base.message('+str(textlist[0])+')'
			#Base.MessageToRoom(room,str(textlist[0]))
			stri=''
			if enqueue:
				for x in textlist:
					func(room,textline(x))
			else:
				for x in textlist:
					stri+=textline(x)+"\n"
				func(room,stri);
			#	print '*** Base.enqueuEmessage('+str(x)+')'
			#	Base.EnqueueMessageToRoom(room,str(x))

class Script:
	def __init__(self,nextscript=None):
		self.nextscript=nextscript
	def __call__(self,room,subnodes):
		print '**************** CALL SCRIPT'
		if self.nextscript:
			print '***************** CALL NEXT SCRIPT'+str(self.nextscript)
			self.nextscript(room,subnodes)
		return True

# Should use this with GoToSubnodeIfTrue.
class RemoveCargo(Script):
	def __init__(self,name,num,missionflag,nextscript=None):
		Script.__init__(self,nextscript)
		self.cargname=name
		self.cargnum=num
		self.missionflag=missionflag
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		you=VS.getPlayer()
		removenum=you.removeCargo(self.cargname,self.cargnum,True)
		if self.missionflag:
			has=you.hasCargo(self.cargname)
			if (has):
				mpart=VS.GetMasterPartList()
				newcarg=mpart.GetCargo(self.cargname)
				has=you.removeCargo(self.cargname,has,1)
				newcarg.SetMissionFlag(0)
				newcarg.SetContent(self.cargname)
				newcarg.SetQuantity(has)
				you.addCargo(newcarg) #It seems that removing and then adding it again is the only way...
		print '*********** Remove cargo '+self.cargname+'('+str(self.cargnum)+')'
		if removenum<self.cargnum:
			print '        ...strict failed to remove cargo'
			return False #since we force add all cargo, we can fail if not all is removed
		if removenum<1:#self.cargnum less strict
			print '        ...really failed :-('
			return False
		return True
	

# Should use this with GoToSubnodeIfTrue.
class AddCargo(Script):
	def __init__(self,name,num,missionflag,nextscript=None):
		Script.__init__(self,nextscript)
		self.cargname=name
		self.cargnum=num
		self.missionflag=missionflag
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		if True or CargoSpaceCondition(self.cargname,self.cargnum)():
			import VS
			you=VS.getPlayer()
			mpart=VS.GetMasterPartList()
			carg=mpart.GetCargo(self.cargname)
			carg.SetQuantity(self.cargnum)
			if carg.GetContent()=='':
				carg.SetMass(0.01)
				carg.SetVolume(1)
				carg.SetPrice(0)
			carg.SetContent(self.cargname)
			carg.SetMissionFlag(self.missionflag)
			numsofar=you.addCargo(carg)
			print "Successfully added "+str(numsofar)
			numadded=0
			if (numsofar<self.cargnum):
				rang=range (you.numCargo())
				rang.reverse()
				for i in rang:
					karg=you.GetCargoIndex(i)
					if (not karg.GetMissionFlag()):
						if (karg.GetCategory().find("upgrades")==-1):
							content=karg.GetContent()
							print "testing "+ content
							diff=self.cargnum-numsofar-numadded
							quant=karg.GetQuantity()
							if (quant>0):
								if (quant>diff):
									diff=quant
								p=karg.GetPrice()
								diff=you.removeCargo(content,diff,True)
								numadded+=diff
								you.addCredits(p*diff)
								print "Took away "+str(diff)+" of "+content
								if (numadded+numsofar>=self.cargnum):
									break;
				carg.SetQuantity(self.cargnum-numsofar)
				print "attempting to add "+str(self.cargnum-numsofar)+" of "+carg.GetContent()
				num=you.addCargo(carg)
				print "added "+str(num)+" cargo after removing some"
				if (num+numsofar<self.cargnum):
					print "force add 1 cargo"
					carg.SetQuantity(self.cargnum-num-numsofar)
					you.forceAddCargo(carg)
							
			print '*********** Added cargo '+self.cargname+'('+str(self.cargnum)+')'
			return True
		return False
	

class SetSaveVariable(Script):
	def __init__(self,varname,varvalue,nextscript=None):
		Script.__init__(self,nextscript)
		self.name=str(varname)
		self.value=int(varvalue)
	
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		print "*** Setting \'%s : %d\'"%(self.name,self.value)
		setSaveValue(VS.getCurrentPlayer(),self.name,self.value)
		return True


class IncSaveVariable(Script):
	def __init__(self,varname,nextscript=None):
		Script.__init__(self,nextscript)
		self.name=str(varname)
	
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		print "*** Incrementing \'%s \'"%self.name
		incSaveValue(VS.getCurrentPlayer(),self.name)
		return True
	
class AddTechnology(Script):
	def __init__(self,technology,nextscript=None):
		Script.__init__(self,nextscript)
		self.tech=technology
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import universe
		universe.addTechLevel(self.tech)

class AdjustRelation(Script):
	def __init__(self,us,them,change,nextscript=None):
		Script.__init__(self,nextscript)
		self.us=us
		self.them=them
		self.change=change
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		VS.AdjustRelation(self.us,self.them,self.change,1.0)
		return True
class ClearFactionRecord(Script):
	def __init__(self,fac,newrelation,nextscript=None):
		Script.__init__(self,nextscript)
		self.faction=fac
		self.newval=newrelation
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		rel=VS.GetRelation(self.faction,"privateer")
		VS.AdjustRelation(self.faction,"privateer",self.newval-rel,1.0)
		rel=VS.GetRelation("privateer",self.faction)
		VS.AdjustRelation("privateer",self.faction,self.newval-rel,1.0)
	
class ClearRecord(Script):
	def __init__(self,nextscript=None):
		Script.__init__(self,nextscript)
	def FixRelation(self,fac,room,subnodes):
		ClearFactionRecord(fac,1.0)(room,subnodes)
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		self.FixRelation("pirates",room,subnodes)
		self.FixRelation("confed",room,subnodes)
		self.FixRelation("militia",room,subnodes)
		self.FixRelation("merchant",room,subnodes)
		self.FixRelation("hunter",room,subnodes)
class PushRelation(Script):
	def __init__(self,faction,nextscript=None):
		Script.__init__(self,nextscript)
		self.faction=faction
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import Director
		import VS
		cp=VS.getCurrentPlayer()
		key=self.faction+"_relation_stack"
		Director.pushSaveData(cp,key,VS.GetRelation(self.faction,"privateer"))
class PopRelation(Script):
	def __init__(self,faction,nextscript=None):
		Script.__init__(self,nextscript)
		self.faction=faction
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import Director
		import VS
		cp=VS.getCurrentPlayer()
		key=self.faction+"_relation_stack"
		length=Director.getSaveDataLength(cp,key)
		ClearFactionRecord(self.faction,Director.getSaveData(cp,key,length-1))(room,subnodes)
		Director.eraseSaveData(cp,key,length-1);

class LaunchWingmen(Script):
	def __init__(self,faction,shiptype,num,nextscript=None):
		Script.__init__(self,nextscript)
		self.faction=faction
		self.shiptype=shiptype
		self.num=num
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		you=VS.getPlayer()
		import launch
		wing=launch.launch_wave_around_unit("Wingmen",
						self.faction,
						self.shiptype,
						"default",
						self.num,
						500,
						1000,
						you)
		wing.setFgDirective('A')
		wing.setFlightgroupLeader(you)

class ChangeSystemOwner(Script):
	def __init__(self,system,faction,nextscript=None):
		Script.__init__(self,nextscript)
		self.faction=faction
		self.system=system
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		VS.SetGalaxyFaction(self.system,self.faction);

class AddCredits(Script):
	def __init__(self,numcreds,nextscript=None):
		Script.__init__(self,nextscript)
		self.creds=numcreds
		self.added=False
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		un=VS.getPlayer()
		if not un.isNull():
			if not self.added:
				un.addCredits(self.creds)
				self.added=True
		return True


class RemoveCredits(Script):
	def __init__(self,numcreds,nextscript=None):
		Script.__init__(self,nextscript)
		self.creds=numcreds
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		un=VS.getPlayer()
		if not un.isNull():
			un.addCredits(-self.creds)
		return True
    
class SetCredits(Script):
	def __init__(self,numcreds,nextscript=None):
		Script.__init__(self,nextscript)
		self.creds=numcreds
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import VS
		un=VS.getPlayer()
		if not un.isNull():
			un.addCredits(self.creds-un.getCredits())
		return True
    
class PushCredits(Script):
	def __init__(self,nextscript=None):
		Script.__init__(self,nextscript)
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import Director
		import VS
		cp=VS.getCurrentPlayer()
		un=VS.getPlayerX(cp)
		if not un.isNull():
			creds=un.getCredits()
    		key="credits_stack"
    		Director.pushSaveData(cp,key,creds)
		return True
		
class PopCredits(Script):
	def __init__(self,nextscript=None):
		Script.__init__(self,nextscript)
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import Director
		import VS
		cp=VS.getCurrentPlayer()
		un=VS.getPlayerX(cp)
		if not un.isNull():
			key="credits_stack"
			length=Director.getSaveDataLength(cp,key)
			un.addCredits(Director.getSaveData(cp,key,length-1))
			Director.eraseSaveData(cp,key,length-1);
		return True

class PushNews(Script):
	def __init__(self,story,nextscript=None):
		Script.__init__(self,nextscript)
		self.story=story
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import Director
		import VS
		cp=VS.getCurrentPlayer()
		Director.pushSaveString(cp,"dynamic_news",'#'+self.story)
    
#LoadMission(varname,missionname,missionargs,SetSaveVariable(varname,2,script)) # jay
class LoadMission(Script):
	def __init__(self,name,missionname,missionargs,nextscript=None):
		Script.__init__(self,nextscript)
		self.mname=missionname
		self.args=missionargs
		self.name=name
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		import mission_lib
		import VS
		mission_lib.AddNewMission(self.name,self.args,self.mname)
		mission_lib.SetLastMission(self.name)
		print '*** Loading the mission!'
		print '*** '+str(self.mname)+'('+str(self.args)+')'
		#VS.LoadMission('internal_mission_lib.mission')
		mission_lib.LoadLastMission()
		return True
	

class AddSprite(Script):
	def __init__(self,name,sprite,pos,nextscript=None):
		Script.__init__(self,nextscript)
		self.name=name
		self.sprite=sprite
		if self.sprite.find('/')==-1:
				self.sprite=('bases/fixers/'+self.sprite)
		self.pos=pos
#		print '************ Init add sprite '+ repr(self.name)+', '+repr(self.sprite)+', '+repr(self.pos)
	def __call__(self,room,subnodes):
		print '***************** ADD THE SPRITE'
		Script.__call__(self,room,subnodes)
		import Base
		print '*** AddSprite: Base.Texture'+str((room,self.name,self.sprite,self.pos[0],self.pos[1]))
		Base.Texture(room,self.name,self.sprite,self.pos[0],self.pos[1])
		return True
	
class AddPythonSprite(AddSprite):
	def __init__(self,name,sprite,center_position,widthheight,text,python,nextscript=None):
		AddSprite.__init__(self,name,sprite,center_position,nextscript)
		self.widthheight=widthheight
		self.text=text
		self.python=python
	def __call__(self,room,subnodes):
		AddSprite.__call__(self,room,subnodes)
		import Base
		Base.Python(room,self.name,self.pos[0]-(self.widthheight[0]/2.), self.pos[1]-(self.widthheight[1]/2.),
			self.widthheight[0], self.widthheight[1], self.text, self.python, True)
		return True

def AddRemovingSprite(name,sprite,center_position,widthheight,text,nextscript=None):
	return AddPythonSprite(name,sprite,center_position,
		widthheight,text,"#\nimport Base\nBase.EraseLink(Base.GetCurRoom(), "+repr(name)+")\nBase.EraseObj(Base.GetCurRoom(), "+repr(name)+")\n",nextscript)

def AddConversationStoppingSprite(name,sprite,center_position,widthheight,text,nextscript=None):
	return AddPythonSprite(name,sprite,center_position,
		widthheight,text,"#\nimport Base\nBase.EraseLink(Base.GetCurRoom(), "+repr(name)+")\nBase.EraseObj(Base.GetCurRoom(), "+repr(name)+")\nimport VS\nVS.StopAllSounds()\nBase.Message('')\n",nextscript)
def doTalkingHeads():
	try:
		import VS
		talkp=VS.vsConfig("graphics","talking_heads","true")
		talk= (talkp=="true" or talkp=="1")			
	except:
		talk=True
		print "recovered:"
		import sys
		print str(sys.exc_info()[0])+str(sys.exc_info()[1])			
	return talk

class Cutscene(AddPythonSprite):
	def __init__(self,name,sprite,center_position,widthheight,text,BaseMessage,music,origlist=None,nextscript=None):
		scripts="#\nimport Base\nBase.EraseLink(Base.GetCurRoom(), '"+name+"')\nBase.EraseObj(Base.GetCurRoom(), '"+name+"')\nBase.EraseObj(Base.GetCurRoom(), '"+name+"_black')\nBase.Message('')\n"
		if (origlist):
			scripts+="import VS\nlist=VS.musicAddList("+repr(origlist)+")\nVS.musicPlayList(list)"
		AddPythonSprite.__init__(self,name,sprite,center_position,widthheight,text,scripts,nextscript)
		BaseMessage.append('                                        <Click to exit cutscene>')
		self.BaseMessage=BaseMessage
		self.music=music
		self.origSong=origlist
		self.enqueue=False
	def MakeEnqueue(self):
		self.enqueue=True
		return self
	def __call__(self,room,subnodes):
		import Base
		import VS
		Base.Texture(0, self.name+"_black", "black.spr", 0, 0);
		AddPythonSprite.__call__(self,0,subnodes)
		displayText(0,self.BaseMessage,self.enqueue)
		if self.origSong:
			slist=VS.musicAddList(self.music)
			VS.musicPlayList(slist)
		else:
			VS.musicPlaySong(self.music)
		return True
	
class GoToSubnodeIfTrue(Script):
	def __init__(self,script,iftrue=0,iffalse=-1):
		Script.__init__(self,script)
		self.iftrue=iftrue
		self.iffalse=iffalse
	def __call__(self,room,subnodes):
		ret=False
		if self.nextscript:
			ret=self.nextscript(room,subnodes)
		if ret:
			print '*** True! '+str(self.iftrue)
			return self.iftrue
		else:
			print '*** False! '+str(self.iffalse)
			return self.iffalse
	

class TrueSubnode(Script):
	def __init__(self,nextscript=None):
		Script.__init__(self,nextscript)
	def __call__(self,room,subnodes):
		Script.__call__(self,room,subnodes)
		for i in range(len(subnodes)):
			if subnodes[i].checkPreconditions():
				return i
		return -1



class GoToSubnode(Script):
	def __init__(self,const,nextscript=None):
		Script.__init__(self,nextscript)
		self.const=const
	def __call__(self,room,subnodes):
		print '************* Goto before script call'
		Script.__call__(self,room,subnodes)
		print '************* Goto after script call'
		return self.const

YES_SPRITE='yes.spr'
NO_SPRITE='no.spr'

class Campaign:
	def __init__(self,savegamename,rootnode=None):
		self.name=savegamename
		self.root=rootnode
		self.current=rootnode
		self.savegame=[]
	
	def Init(self,rootnode):
		self.root=rootnode
		self.current=rootnode
		# Note: Init() will not evaluate the first node because it probably is not in a base.
		# The root note therefore sould probably be a CampaignClickNode
	
	#depends on Base... should remove dependencies?
	def setCurrentNode(self,room,newnodenum):
		print '*** set tehc urr3nt n0d3 to '+str(newnodenum)
		import VS
		import Director
		if newnodenum>=0:
			if newnodenum>=len(self.current.subnodes):
				print 'Error: cannot go to node '+str(newnodenum)
				print 'Failed node has text:'
				print str(self.current.text)
				return
			self.current=self.current.subnodes[newnodenum]
			self.savegame.append(newnodenum)
			Director.pushSaveData(VS.getCurrentPlayer(),self.name,float(newnodenum))
		elif newnodenum==-2:
			if not self.current.contingency:
				print 'Error: cannot go to contingency node!'
				print 'Failed node has text:'
				print str(self.current.text)
				return
			print '*** Going to contingency!!!'
			self.current=self.current.contingency
			self.savegame.append(-2)
			Director.pushSaveData(VS.getCurrentPlayer(),self.name,float(-2))
		self.current.evaluate(room)
	
	def readPositionFromSavegame(self):
		import VS
		import Director
		self.savegame=[]
		self.current=self.root
		plr=VS.getCurrentPlayer()
		length=Director.getSaveDataLength(plr,self.name)
		for i in range(length):
			newnodenum=int(Director.getSaveData(plr,self.name,i))
			if newnodenum>=0:
				if newnodenum>=len(self.current.subnodes):
					print 'Error: save game index out of bounds: '+str(newnodenum)
					return
				print self.current
				self.current=self.current.subnodes[newnodenum]
			elif newnodenum==-2:
				if not self.current.contingency:
					print 'Error: save game moves to invalid contengency node!'
					return
				print self.current
				self.current=self.current.contingency
			self.savegame.append(newnodenum)
		print '*** read position from save game: for '+self.name+': '+str(self.savegame)
		print self.current
	
	#depends on Base... should remove dependencies?
	def getCurrentNode(self,room):
		print '*** getting current node'
		import VS
		import Director
		plr=VS.getCurrentPlayer()
		if Director.getSaveDataLength(plr,self.name)!=len(self.savegame):
			self.readPositionFromSavegame()
		else:
			print '*** read stuff from savegame'
			for i in range(len(self.savegame)):
				if int(Director.getSaveData(plr,self.name,i))!=self.savegame[i]:
					self.readPositionFromSavegame()
					break
		print '*** :-) ***'
		print self.savegame
		while True:
			if self.current.checkPreconditions():
				if room>=0:
					self.current.evaluate(room)
					print '*** cur evalutaed'
				return self.current
			if not self.current.contingency:
				print '*** no contingency!'
				return None
			print '*** cur contingency!!'
			self.setCurrentNode(room,-2)
		print '*** Your Python is broken. Please fix it now!!!!'
		return None
	

class CampaignNode:
	def __init__(self):
		pass
	def IsCampaignChoiceNode(self):
		return False
	def Init(self,campaign,preconditions,text,spritelink,script,contingency,subnodes):
		self.campaign=campaign
		self.preconditions=preconditions
		self.text=text
		self.talkinghead=None
		self.spritelink=spritelink
		self.script=script
		self.subnodes=[]
		if self.spritelink:
			if len(self.spritelink)>2:
				self.talkinghead=self.spritelink[2]
			if self.spritelink[0].find('/')==-1:
				self.spritelink=('bases/fixers/'+self.spritelink[0],self.spritelink[1])
		for i in subnodes:
			self.subnodes.append(i)
		self.contingency=contingency
		return self
	def checkPreconditions(self):
		if self.preconditions:
			for cond in self.preconditions:
				if not cond():
					return False
		return True
	#depends on Base
	def getFixer(self,room):
		if self.spritelink and self.checkPreconditions():
			import fixers
			print '*** create fixer'+ str(self.spritelink)
			tmpscript="#\nimport campaign_lib\n"
			if self.talkinghead and doTalkingHeads():
				tmpscript+="campaign_lib.AddConversationStoppingSprite('Talking',"+repr(self.talkinghead)+",(.582,-.2716),(3.104,2.4832),'Return_To_Bar').__call__("+str(room)+",None)\n"
			return fixers.Fixer(self.spritelink[1].split(' ')[-1].lower(),self.spritelink[1],[],
				self.spritelink[0],tmpscript+"campaign_lib.clickFixer("+str(room)+")\n")
		print '*** no sprite. You lose.'
		return None
	#depends on Base
	def gotoChoice(self,room,num):
		self.campaign.setCurrentNode(room,num)
	#depends on Base
	def clickFixer(self,room):
		CampaignNode.evaluate(self,room)
	#depends on Base... should remove dependencies?
	def evaluate(self,room):
		if self.checkPreconditions():
			displayText(room,self.text)
			print self.subnodes
			num=self.script(room,self.subnodes)
			if num>=0 and num<len(self.subnodes):
				self.gotoChoice(room,num)
	

class CampaignClickNode(CampaignNode):
	def __init__(self):
		CampaignNode.__init__(self)
	def Init(self,campaign,preconditions,text,spritelink,script,contingency,subnodes):
		CampaignNode.Init(self,campaign,preconditions,text,spritelink,script,contingency,subnodes)
		return self
	#depends on Base... should remove dependencies?
	def evaluate(self,room):
		pass
	

class CampaignChoiceNode(CampaignNode):
	def __init__(self):
		CampaignNode.__init__(self)
	def IsCampaignChoiceNode(self):
		return True
	def Init(self,campaign,preconditions,text,spritelink,contingency,choices):
		tmp=[]
		tmpchoices=[]
		for i in choices:
			tmp.append(i[1])
			if i[0][0].find('/')==-1:
				tmpchoices.append(('bases/fixers/'+i[0][0],i[0][1]))
			else:
				tmpchoices.append(i[0])
		CampaignNode.Init(self,campaign,preconditions,text,spritelink,None,contingency,tmp)
		self.choices=tmpchoices
		return self
	def gotoChoice(self,room,num):
		self.campaign.setCurrentNode(room,num)
	def clickFixer(self,room):
		displayText(room,self.text)
	#depends on Base... should remove dependencies?
	def evaluate(self,room):
		print '***'
		print '***'
		print self.text
		displayText(room,self.text)
		import fixers
		arr=[]
		print '*** create buttons +'+str(self.choices)
		for x in range(len(self.choices)):
			arr.append(fixers.Choice(self.choices[x][0],"#\nimport campaign_lib\ncampaign_lib.clickChoice("+str(room)+","+str(x)+")\n",self.choices[x][1]))
		fixers.DestroyActiveButtons()
		fixers.CreateChoiceButtons(room,arr)
		print '***'
		print '***'
	
def CampaignEndNode(campaign):
	return CampaignNode().Init(campaign,[],[],None,GoToSubnode(0),None,[CampaignNode().Init(campaign,[InSystemCondition("NeverNeverLand/neverhere")],[],None,GoToSubnode(-1),None,[])])

#class CampaignEndNode(CampaignNode):
#	def __init__(self):
#		CampaignNode.__init__(self)
#	def Init(self,campaign):
#		CampaignNode.Init(self,campaign,[],[],None,GoToSubnode(0),None,[CampaignNode(campaign,).Init()])
#		print 'End Node init'
#		return self
#	def checkPreconditions(self):
#		print 'end check precondtions'
#		return True
#	def getFixer(self,room):
#		print 'end get fixer'
#		return None
#	def gotoChoice(self,room,num):
#		print 'end node goto'
#	def clickFixer(self,room):
#		print 'end node click'
#	def evaluate(self,room):
#		print 'end node eval'
	

def IfThenElse (A,B,C):
	if (A):
		return B
	return C

def AskToAcceptMission(campaign,sprite,conditiontoappear,conditiontobegin,scriptonclick,speech,RejectNode,FlyMission,MissionRefusal=None,SeedClickNode=None):
	if (not SeedClickNode):
		SeedClickNode=CampaignClickNode()
	if (not MissionRefusal):
		MissionRefusal=CampaignClickNode()
	MissionFirstRefusal=CampaignChoiceNode()
	ret=SeedClickNode.Init(campaign,
		conditiontoappear,
		[],
		sprite,
		TrueSubnode(scriptonclick),
		None,
		[CampaignChoiceNode().Init(campaign,
			conditiontobegin,
			speech["intro"],#if its not there python error at tree-compile, not runtime
			sprite,
			None,
			[((NO_SPRITE,"Refuse_Mission"),CampaignNode().Init(campaign,
				[],
				speech["reject1"],
				sprite,
				GoToSubnode(0),
				None,
				[CampaignClickNode().Init(campaign,
					conditiontobegin,
					[],
					sprite,
					GoToSubnode(0),
					None,
					[MissionFirstRefusal.Init(campaign,conditiontobegin,
					speech["reconsider"],
					sprite,
					None,
					[((NO_SPRITE,"Refuse_Mission"),CampaignNode().Init(campaign,
						[],
						speech["reject2"],
						sprite,
						TrueSubnode(),
						None,
						[MissionRefusal.Init(campaign,
							conditiontobegin,
							[],
							sprite,
							TrueSubnode(),
							None,
							[IfThenElse(RejectNode,RejectNode,MissionFirstRefusal)])])),
					((YES_SPRITE,"Accept_Mission"),FlyMission)])])])),
			 ((YES_SPRITE,"Accept_Mission"),FlyMission)])])
	return ret
	

def MakeVariableMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,scriptbegin,varname,speech,RejectNode,FailureNode,SuccessNode,SeedClickNode=None):
	if (not SeedClickNode):
		SeedClickNode=CampaignClickNode()
	MissionRefusal=CampaignClickNode()
	FlyMission=CampaignNode()
	FlyMissionContingency=CampaignNode()
	ret=AskToAcceptMission(campaign,
		sprite,
		conditiontobegin,
		conditiontobegin,
		scriptonclick,
		speech,
		RejectNode,
		FlyMission,
		MissionRefusal,
		SeedClickNode)
	FlyMission.Init(campaign,
			[],
			speech["accept"],
			sprite,
			IfThenElse(scriptbegin,GoToSubnodeIfTrue(scriptbegin,iftrue=1,iffalse=0),GoToSubnode(1)),
			None,
			[MissionRefusal,
			CampaignNode().Init(campaign,
				[],
				[],
				None,
				TrueSubnode(SetSaveVariable(varname,2)),
				None,
				[FlyMissionContingency.Init(campaign,
					[],
					[],
					None,
					TrueSubnode(),
					None,
					[CampaignClickNode().Init(campaign,
						conditiontobegin+[SaveVariableCondition(varname,-1)],
						speech["failure"],
						sprite,
						GoToSubnode(0),
						None,
						[FailureNode]),
					 CampaignNode().Init(campaign,
						conditiontoend+[SaveVariableCondition(varname,1)],
						[],
						None,
						GoToSubnode(0),
						None,
						[SuccessNode]),
					 CampaignClickNode().Init(campaign,
						conditiontobegin+[AndCondition(InvertCondition(OrCondition([SaveVariableCondition(varname,1)])),InvertCondition(SaveVariableCondition(varname,-1)))],
						speech["reminder"],
						sprite,
						TrueSubnode(scriptbegin),
						FlyMissionContingency,#stuck in a click node, not in ND
						[])])])])
	return ret

def MakeNoFailureCargoMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,script,cargoNameQuantity,varname,speech,RejectNode,FailureNode,SuccessNode,SeedClickNode=None):
	if (not SeedClickNode):
		SeedClickNode=CampaignClickNode()
	cargoMissionFlag=True
	if len(cargoNameQuantity)>2:
		cargoMissionFlag=cargoNameQuantity[2]
	MissionRefusal=CampaignClickNode()
	FlyMission=CampaignNode()
	FlyMissionContingency=CampaignNode()
	ret=AskToAcceptMission(campaign,
		sprite,
		conditiontobegin+[CargoSpaceCondition(cargoNameQuantity[0],cargoNameQuantity[1])],
		conditiontobegin,
		scriptonclick,
		speech,
		RejectNode,
		FlyMission,
		MissionRefusal,
		SeedClickNode)
	FlyMission.Init(campaign,
			[],
			speech["accept"],
			sprite,
			GoToSubnodeIfTrue(AddCargo(cargoNameQuantity[0],cargoNameQuantity[1],cargoMissionFlag,SetSaveVariable(varname,2,script)),iftrue=1,iffalse=0),
			None,
			[MissionRefusal,
			FlyMissionContingency.Init(campaign,
				[],
				[],
				None,                                         #(fac,        0, numcargos, diff, creds, launchcap, 0, category, str(path), ''))
				TrueSubnode(), # jay
				None,
				[CampaignClickNode().Init(campaign,
					conditiontobegin,
					speech["reminder"],
					sprite,
					TrueSubnode(script),
					FlyMissionContingency,#stuck in a click node, not in ND
					[]),#got advice, go back to click node
				 CampaignNode().Init(campaign,
					conditiontoend,
					[],
					None,
					GoToSubnodeIfTrue(RemoveCargo(cargoNameQuantity[0],cargoNameQuantity[1],cargoMissionFlag,SetSaveVariable(varname,1)),iftrue=1,iffalse=0),
					None,
					[FailureNode,
					 SuccessNode])])])	
	return ret

def MakeCargoMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,script,cargoNameQuantity,varname,speech,RejectNode,FailureNode,SuccessNode,SeedClickNode=None):
	return MakeNoFailureCargoMission(campaign,
		sprite,
		conditiontobegin,
		conditiontoend,
		scriptonclick,
		script,
		cargoNameQuantity,
		varname,
		speech,
		RejectNode,
		CampaignClickNode().Init(campaign,
					conditiontobegin,
					speech["failure"],
					sprite,
					GoToSubnode(0,SetSaveVariable(varname,-1)),
					None,
					[FailureNode]),
		SuccessNode,
		SeedClickNode)

def MakeNoFailureMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,script,missionname,missionargs,varname,speech,rejectnode,failurenode,succeednode,node=None):
	if not node:
		node=CampaignClickNode()
	getthemission=CampaignNode()
	reject2node=CampaignClickNode()
	ret=AskToAcceptMission(campaign,
		sprite,
		conditiontobegin,
		conditiontobegin,
		scriptonclick,
		speech,
		rejectnode,
		getthemission,
		reject2node,
		node)
	contingency=CampaignNode()
	getthemission.Init(campaign,
		conditiontobegin,
		speech["accept"],
		sprite,
		TrueSubnode(LoadMission(varname,missionname,missionargs,SetSaveVariable(varname,2,script))),
		contingency,
		[contingency.Init(campaign,
			[],
			[],
			None,
			TrueSubnode(),
			None,
			[CampaignClickNode().Init(campaign,
				conditiontobegin+[NotCondition(SaveVariableCondition(varname,-1)),NotCondition(SaveVariableCondition(varname,1)),AtMostActiveMissionsCondition()],
				[],
				sprite,
				TrueSubnode(),
				contingency,
				[getthemission,contingency]),
			 CampaignClickNode().Init(campaign,
				conditiontobegin+[NotCondition(OrCondition(SaveVariableCondition(varname,-1),SaveVariableCondition(varname,1))),AtLeastActiveMissionsCondition()],
				speech["reminder"],
				sprite,
				TrueSubnode(script),
				contingency,
				[]),
			 CampaignNode().Init(campaign,
				conditiontobegin+[SaveVariableCondition(varname,-1)],
				[],
				None,
				TrueSubnode(),
				None,
				[failurenode]),
			 CampaignNode().Init(campaign,
				conditiontoend+[SaveVariableCondition(varname,1)],
				[],
				None,
				TrueSubnode(),
				None,
				[succeednode])])])
	return node
def MakeMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,script,missionname,missionargs,varname,speech,rejectnode,failurenode,succeednode,node=None):
	return MakeNoFailureMission(campaign,sprite,conditiontobegin,conditiontoend,scriptonclick,script,missionname,missionargs,varname,speech,rejectnode,
		CampaignClickNode().Init(campaign,
					conditiontobegin,
					speech["failure"],
					sprite,
					GoToSubnode(0),
					None,
					[failurenode]),succeednode,node)

def getCampaignList():
	import campaigns
	return campaigns.getCampaigns()

def getActiveCampaignNodes(room):
	campaigns=getCampaignList()
	clist=[]
	print "there are "+str(len(campaigns))+" campagins"
	for campaign in campaigns:
		curnode=campaign.getCurrentNode(room)
		if curnode:
			print '*** found actuive node in campaign '+campaign.name
			clist.append(curnode)
			print 'checking contingency: '+str(curnode.checkPreconditions())
			#return clist # The bar shouldn't have more than one campaign at a time.
		else:
			print '*** no actuve node for '+campaign.name
	if (len(clist)):
		print 'Nodes '+str(len(clist))
	else:
		print '*** No node'

	for index in range(len(clist)):
		if (clist[index].spritelink):
			if (index!=0):
				tmp = clist[index]
				del clist[index]
				clist = [tmp]+clist;
			break
		if (clist[index].text and len(clist[index].text) and index!=0):
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			print "COOL Fix"
			tmp = clist[index]
			del clist[index]
			clist = [tmp]+clist;# doesn't change list length
	return clist

#depends on Base
def getFixersToDisplay(room):
	print '*** Get teh fixer to display!!!'
	cnodelist=getActiveCampaignNodes(room)
	fixerlist=[]
	for cnode in cnodelist:
		print '*** display it. '
		newfixer=cnode.getFixer(room)
		if newfixer:
			fixerlist.append(newfixer)
	return fixerlist

#depends on Base
def clickFixer(room):
	print '*** Clicked teh fixeer!!!'
	cnodelist=getActiveCampaignNodes(room)
	# Should only evaluate first one?
	for c in cnodelist:
		c.clickFixer(room)

#depends on Base
def clickChoice(room,choicenum):
	import fixers
	print '*** Clicked teh choice!!!'
	cnodelist=getActiveCampaignNodes(-1)
	# Should only evaluate first one?
	import VS
	VS.StopAllSounds()
	for c in cnodelist:
		print '*** clicked on choice +'+str(choicenum)+': '+cnodelist[0].campaign.name
		if (c.IsCampaignChoiceNode()):
			c.gotoChoice(room,choicenum)
			fixers.DestroyActiveButtons()
			break

