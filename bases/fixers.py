import quest
import VS
import vsrandom
import Base
import Director
import mission_lib
import fixer_lib
import code
activelinks=[]
activeobjs=[]
def checkSaveValue (playernum,questname, value):
    return quest.checkSaveValue(playernum,questname,value)
def setSaveValue (playernum,name,value):
	quest.removeQuest(playernum,name,value);

def payCheck(playernum,savevalue,value,money):
    if checkSaveValue(playernum,savevalue,value):
        VS.getPlayerX(playernum).addCredits(money)
        setSaveValue(playernum,savevalue,value+1)

class Choice:
	_number=0
	def __init__(self,pics,actions,name):
		self.pics=pics
		self.name=name
		self.index=name.replace('/','_')+'/'+str(Choice._number)
		Choice._number+=1
		self.actions=actions
	def drawobjs(self,room,x,y,wid,hei):
		Base.Texture(room,self.index,self.pics,x+(wid/2.),y+(wid/2.))
		Base.Python(room,self.index,x,y,wid,hei,self.name,self.actions,1)
		global activelinks
		global activeobjs
		activelinks.append((room,self.index))
		print '*** add link: '+str((room,self.index))
		print activelinks
		activeobjs.append((room,self.index))
		print '*** add obj: '+str((room,self.index))
		print activeobjs
class Fixer:
	"""A class that draws nobody."""
	def __init__(self,name,text,precondition,image,choices):
		self.name = name
		self.text = text
		self.precondition = precondition
		self.choices = choices
		pos=image.rfind(".")
		if pos>=0:
			image=image[:pos]
		self.image = image
	def abletodraw(self):
		for cond in self.precondition:
			var= cond[0]
			value = cond[1]
			if not checkSaveValue(VS.getCurrentPlayer(),var,value):
				return 0
			
		return 1
	def drawobjs(self,room,x,y,wid,hei,imageappend=''):
		Base.Texture(room,self.name,self.image+imageappend+".spr",x+(wid/2.),y+(hei/2.))
		Base.Python(room,self.name,x,y,wid,hei,self.text,self.choices,1)
class CFixer(Fixer):
    """A class class for \'Campaign\' Fixers."""
    
    STANDARDIMPORT = "\nimport VS\n"
    
    def __init__(self, conversation):
        self.conversation = conversation
        self.name, self.text, self.image, self.choices = conversation.getFixerStrings()
        pos=self.image.rfind(".")
        if pos>=0:
            self.image=self.image[:pos]

    def abletodraw(self):
#        print "Fixer can draw? -- " + str(self.conversation.canDraw())
        return self.conversation.canDraw()

class NoFixer (Fixer):
	"""Class that displays nobody.  Should maybe draw a bartender guy to talk to."""
	def __init__(self):
		Fixer.__init__(self,'nobody','Bar',[],'','')

	def abletodraw(self):
		"""A NoFixer can't draw."""
		return 0

	def drawobjs(self,room,x,y,wid,hei,imageappend=''):
		"""Don't create the python script OR the texture, so trhe user won't notice :-)"""
		pass

def RandFixer (room,which):
	fixer=mission_lib.CreateRandomMission(which)
	if fixer==():
		return NoFixer()
	return Fixer(fixer[1].split(' ')[-1].lower(),fixer[1],[],fixer[0],"bases/fixers/generic%d.py"%which)

def getCampaignFixers (room):
	import campaign_lib
	return campaign_lib.getFixersToDisplay(room)

fixers={"enigma_sector/niven":[
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",0)],"bases/fixers/militia.spr","bases/fixers/explore_enigma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",0),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_notready.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",1),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_beta.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_beta.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",1),("gemini_sector/gamma_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_gamma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_gamma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",1),("gemini_sector/delta_prime_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_delta_prime.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",2),("gemini_sector/delta_prime_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_delta_prime.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",2),("gemini_sector/delta_prime_navpoint",1)],"bases/fixers/militia.spr","bases/fixers/attack_drone0.py"),
	],"enigma_sector/enigma":[
	Fixer("confed_drone","Talk to the Confed Officer",[("quest_drone",1)],"bases/fixers/confed.spr","bases/fixers/attack_drone1.py"),
	Fixer("confed_drone","Talk to the Confed Officer",[("quest_drone",-1)],"bases/fixers/confed.spr","bases/fixers/attack_drone1.py")
	],"enigma_sector/heinlein":[
	Fixer ("cloaked_man","Speak with hooded figure",[("decided_iso_good",0)],"bases/fixers/cloak.spr","bases/fixers/iso_antagonist.py"),
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission2",0)],"bases/fixers/iso.spr","bases/fixers/iso.py"),
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission2",-1)],"bases/fixers/iso.spr","bases/fixers/iso.py")
	],"enigma_sector/adams":[
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission3",0),("iso_mission2",1)],"bases/fixers/iso.spr","bases/fixers/iso.py"),
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission3",0),("iso_mission2",-1)],"bases/fixers/iso.spr","bases/fixers/iso.py"),
	Fixer ("cloaked_man","Speak with hooded figure",[("decided_iso_good",0),("iso_evil2",1)],"bases/fixers/cloak.spr","bases/fixers/iso_antagonist.py")
	],"enigma_sector/defiance":[
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission3",1)],"bases/fixers/iso.spr","bases/fixers/iso.py"),
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0),("iso_mission3",-1)],"bases/fixers/iso.spr","bases/fixers/iso.py")
	],"enigma_sector/blake":[
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	],"enigma_sector/rigel":[
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission2",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission3",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission4",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",1),("pirate_mission3",2),("pirate_mission4",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",1),("pirate_mission3",2),("pirate_mission4",1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	],"sol_sector/tingvallir":[
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission2",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission3",-1)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",1),("pirate_mission3",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py"),
	Fixer ("pirate","Talk with the Pirate",[("pirate_mission1",1),("pirate_mission2",1),("pirate_mission3",1),("pirate_mission4",0)],"bases/fixers/pirate.spr","bases/fixers/pirates.py")
	]}

def eraseCFixer(playernum, name):
    """Removes the Campaign Fixer from the queue."""
    index = getCFixerIndex(playernum, name)
    if index >= 0:
        Director.eraseSaveString(playernum, "CFixers", index)

def getCFixerIndex(playernum, name):
    mylen=Director.getSaveStringLength(int(playernum),"CFixers")
    index = -1
    for i in range(mylen):
        if name == Director.getSaveString(playernum,"CFixers",i).split('|')[0]:
            index = i
            break
    return index

def getCFixers(playernum):
    """Gets the queued campaign fixers."""
    mylen=Director.getSaveStringLength(playernum,"CFixers")
    fixerlist = list()
    if (mylen>0):
        for i in range(mylen):
            fixerlist.append(Director.getSaveString(playernum,"CFixers",i).split('|'))
#FIXME: add another possibility apart from script
    cfixers = list()
    for fxr in fixerlist:
        tempd = dict()
        exec fxr[1] in tempd
        cfixers.append(CFixer(tempd["conversation"]))
    return cfixers

def queueFixer(playernum, name, scripttext, overwrite=0):
    """Will place the referenced fixer in the fixer queue.  The queue is a
    save variable that is checked each time the bar is created for relevant
    fixers."""
    mylen=Director.getSaveStringLength(int(playernum),"CFixers")
    for i in range(mylen):
        if name == Director.getSaveString(playernum,"CFixers",i).split('|')[0]:
            if overwrite:
                Director.putSaveString(int(playernum),str("CFixers"),i,name + '|' + scripttext)
                return
            print "WARNING: Fixer already exists."
            return
#            raise RuntimeError("Campaign Fixer already exists with reference \'%s\'"%name)
    Director.pushSaveString(int(playernum),str("CFixers"),name + '|' + scripttext)

def AppendFixer(name,fixer):
	fixers[name]=fixer

def DestroyActiveButtons ():
	global activelinks
	global activeobjs
	for button in activelinks:
		Base.EraseLink(button[0],button[1])
		print '*** erase link: '+str(button)
		print activelinks
	for button in activeobjs:
		Base.EraseObj(button[0],button[1])
		print '*** erase obj: '+str(button)
		print activeobjs
	activeobjs=[]
	activelinks=[]
def CreateChoiceButtons (room,buttonlist,vert=0,spacing=.025,wid=.2,hei=.2):
	x=0
	if (vert):
		x=-(wid/2.)
		y=-((hei*len(buttonlist)*spacing)+spacing)/2.
	else:
		y=-.75-(hei/2.)
		x=-(wid*len(buttonlist)+(len(buttonlist)-1)*spacing)/2.
	print x,y
	for button in buttonlist:
		print '*** draw: '+str(button.index)
		button.drawobjs(room,x,y,wid,hei)
		if (vert):
			y-=(spacing+hei)
		else:
			x+=spacing+wid

global fixerloaded
fixerloaded=0
def CreateCampaignFixers (room,locations,j=0):
	fixerlist = getCampaignFixers(room)
	locfixers = fixers.get (VS.getSystemFile())
	if locfixers:
		fixerlist+=locfixers
	if (fixerlist):
		global fixerloaded
		fixerloaded+=1
		for i in range (len(fixerlist)):
			if (j<len(locations) and fixerlist[i] and fixerlist[i].abletodraw()):
				append=''
				if len(locations[j])>4:
					append=locations[j][4]
				fixerlist[i].drawobjs (room,locations[j][0],locations[j][1],locations[j][2],locations[j][3],append)
				j+=1
	return j

def CreateMissionFixers (room,locations,j=0):
	rndnum=vsrandom.random()
	if rndnum<.7 and j<len(locations):
		f=RandFixer(room,0)
		append=''
		if len(locations[j])>4:
			append=locations[j][4]
		f.drawobjs (room,locations[j][0],locations[j][1],locations[j][2],locations[j][3],append)
		j+=1
		img=f.image
		rndnum=vsrandom.random()
		if rndnum<.6 and j<len(locations):
			i=0
			while f.image==img and i<10:
				f=RandFixer(room,1)
				i+=1
			if i<10:
				append=''
				if len(locations[j])>4:
					append=locations[j][4]
				f.drawobjs (room,locations[j][0],locations[j][1],locations[j][2],locations[j][3],append)
				j+=1
	return j

def CreateFixers (room,locations):
	j=0
	j=CreateCampaignFixers(room,locations,j)
	j=CreateMissionFixers(room,locations,j)
	return j

class Conversation:

    ROOT_KEY = "Root"

    def __init__(self, name=str(), precons=list(), onclick=str(), nodes=dict()):
        self.name = str(name)
        self.preconditions = list(precons)
        self.onclick = str(onclick)
        self.nodes = dict(nodes)

    def getNode(self, nam=str()):
        """Returns the required Node, if it exists."""
        name = str(nam)
        if name == str():
            name = self.ROOT_KEY
        if self.nodes.has_key(name):
            return self.nodes[name]
        print "Error: Node with name \'%s\' does not exist."%name

    def addNode(self, node, name=str()):
        """Add a Node to the conversation.  Only one RootNode can exist in a
        conversation at any time."""
        if isinstance(node, RootNode):
            self.nodes[self.ROOT_KEY] = node
        elif isinstance(node, Node):
            if name==str():
                print "Error: Node must be added with a name argument."
            else:
                self.nodes[name] = node
        else:
            print "Error: Node is not of a valid type."

    def getFixerStrings(self):
        """Gets the required strings for the construction of the CFixer class."""
        spr, motext, onclick = self.getNode().getInitialInfo()
        return self.name, motext, spr, onclick

    def canDraw(self):
        """Checks if the required precondition has been satisfied."""
#        print "Checking if can draw"
#        print self.preconditions
#        print "len " + str(len(self.preconditions))
        for precon in self.preconditions:
            if not fixer_lib.evaluateCondition(precon):
#                print "uhoh"
                return 0
#        print "okay"
        return 1

    def getNewInfo(self, nam=str()):
        """Gets the new information, from the node with matching name, required
        to progress the conversation."""
        name = str(nam)
        if name == str():
            name = self.ROOT_KEY
        n = self.getNode(name).getSubNode()
        return n.text, n.choices

    def iterate(self, nam=str()):
        """Will execute the next stage of the conversation, ie create the relevant
        textual message and response buttons, given the conversation string, and
        the reference to the next possible nodes."""
        name = str(nam)
        if name == str():
            name = self.ROOT_KEY
        DestroyActiveButtons()
        text, choices = self.getNewInfo(name)
        if choices:
            choices = list(choices)
            for i in range(len(choices)):
                choices[i] = choices[i].split('|')
                choices[i] = Choice(choices[i][0], choices[i][1], choices[i][2])
            CreateChoiceButtons(Base.GetCurRoom(),choices)
        if text:
            Base.Message(text)

class SubNode:
    
    def __init__(self, text=str(), conditions=list(), choices=list(), sprite=str(), motext=str()):
        self.conditions = list(conditions)
        self.text = str(text)
        self.choices = list(choices)
        self.sprite = str(sprite)
        self.motext = str(motext)

    def addCondition(self, condition):
        """Adds the condition (a string) to the conditions list."""
        try:
            self.conditions.append(condition)
        except:
            print "Error: Condition could not be added."

    def addChoice(self, choice):
        """Adds the choice (a string) to the choices list."""
        try:
            self.choices.append(choice)
        except:
            print "Error: Choice could not be added."

class Node:

    def __init__(self, subnodes=list()):
        self.subnodes = list(subnodes)

    def addSubNode(self, subnod=None):
        """If a SubNode is given as an argument, is is added and returned.
        Else a new SubNode object is created, added and returned."""
        if subnod is None:
            subnode = SubNode()
        else:
            subnode = subnod
        self.subnodes.append(subnode)
        return subnode

    def getSubNode(self, index=-1):
        """Retrieves a SubNode either by the specified index, or the first in
        the list to have its conditions met.  If none satisfy the conditions,
        the last in the list is returned."""
        if index > -1:
            return self.subnodes[index]
        else:
            le = len(self.subnodes)
            for i in range(le):
                if fixer_lib.evaluateConditions(self.subnodes[i].conditions):
#                    print "Returning subnode with text=" + self.subnodes[i].text
                    return self.subnodes[i]
#                print "Rejecting subnode with text=" + self.subnodes[i].text
            return self.subnodes[le - 1]

class RootNode(Node):

    def getInitialInfo(self, index=-1):
        """Gets the required information to setup the initial fixer.  The data
        is retrieved using the getSubNode method using, if applicable, the
        provided index."""
        sub = self.getSubNode(index)
        return sub.sprite, sub.motext, sub.choices[0]
