import quest
import VS
import Base
import Director

activelinks=[]
activeobjs=[]
def checkSaveValue (playernum,questname, value):
    return quest.checkSaveValue(playernum,questname,value)
def setSaveValue (playernum,name,value):
	quest.removeQuest(playernum,name,value);

class Choice:
	def __init__(self,pics,actions,name):
		self.pics=pics
		self.name=name
		self.actions=actions
	def Draw(self,room,x,y,wid,hei):
		Base.Texture(room,self.name,self.pics,x+(wid/2),y+(wid/2))
		Base.Python(room,self.name,x,y,wid,hei,self.name,self.actions,True)
		activelinks.append((room,self.name))
		activeobjs.append((room,self.name))
class Fixer:
	def __init__(self,name,text,precondition,image,choices):
		self.name = name
		self.text = text
		self.precondition = precondition
		self.image = image
		self.choices = choices
	def abletodraw(self):
		for cond in self.precondition:
			var= cond[0]
			value = cond[1]
			if not checkSaveValue(VS.getCurrentPlayer(),var,value):
				return False
			
		return True
	def drawobjs(self,room,x,y,wid,hei):
		Base.Texture(room,self.name,self.image,x+(wid/2),y+(hei/2))
		Base.Python(room,self.name,x,y,wid,hei,self.text,self.choices,True)

fixers={"enigma_sector/niven":[
#	Fixer("patrick","Talk to Patrick",[("quest_drone",0)],"bases/fixers/pirate.spr","bases/fixers/patrick.py"),
#	Fixer("isoguy","Talk to Communist",[],"bases/fixers/iso.spr","bases/fixers/patrick.py"),
#	Fixer("drone","Talk to Evil Dude",[("31337ness",.05),("quest_drone",1)],"bases/fixers/cloak.spr","bases/fixers/patrick.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",0)],"bases/fixers/militia.spr","bases/fixers/explore_enigma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",0),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_notready.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",1),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_beta.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_beta.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",1),("gemini_sector/gamma_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_gamma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_gamma.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",1),("gemini_sector/delta_prime_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_delta_prime.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",2),("gemini_sector/delta_prime_navpoint",0)],"bases/fixers/militia.spr","bases/fixers/explore_delta_prime.py"),
	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",3),("gemini_sector/delta_navpoint",2),("gemini_sector/beta_navpoint",2),("gemini_sector/gamma_navpoint",2),("gemini_sector/delta_prime_navpoint",1)],"bases/fixers/militia.spr","bases/fixers/attack_drone0.py"),
#	Fixer("explore","Talk to the Explorer",[("enigma_sector/enigma_nav",2)],"bases/fixers/militia.spr","bases/fixers/explore_enigma3.py")
	],"enigma_sector/enigma":[
	Fixer("confed_drone","Talk to the Confed Officer",[("quest_drone",1)],"bases/fixers/confed.spr","bases/fixers/attack_drone1.py"),
	Fixer("confed_drone","Talk to the Confed Officer",[("quest_drone",-1)],"bases/fixers/confed.spr","bases/fixers/attack_drone1.py")
	],"enigma_sector/heinlein":[
	Fixer ("rowenna","Speak with Rowenna",[("decided_iso_evil",0)],"bases/fixers/iso.spr","bases/fixers/iso.py"),
	Fixer ("cloaked_man","Speak with hooded figure",[("decided_iso_good",0)],"bases/fixers/cloak.spr","bases/fixers/iso_antagonist.py")
	]}

def AppendFixer(name,fixer):
	fixers[name]=fixer

def DestroyActiveButtons ():
	for button in activelinks:
		Base.EraseLink(button[0],button[1])
	for button in activeobjs:
		Base.EraseObj(button[0],button[1])
def CreateChoiceButtons (room,buttonlist,vert=False,spacing=.025,wid=.2,hei=.2):
	x=0
	if (vert):
		x=-(wid/2)
		y=-((hei*len(buttonlist)*spacing)+spacing)/2
	else:
		y=-.75-(hei/2)
		x=-(wid*len(buttonlist)+(len(buttonlist)-1)*spacing)/2
	print x,y
	for button in buttonlist:
		button.Draw(room,x,y,wid,hei)
		if (vert):
			y-=(spacing+hei)
		else:
			x+=spacing+wid
		
def CreateFixers (room,locations):
	fixerlist = fixers.get (VS.getSystemFile())
	j=0
	if (fixerlist):
		for i in range (len(fixerlist)):
			if (j<len(locations) and fixerlist[i].abletodraw()):
				fixerlist[i].drawobjs (room,locations[j][0],locations[j][1],locations[j][2],locations[j][3])
				j+=1
