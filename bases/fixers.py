import quest
import VS
import Base
import Director

activelinks=[]
activeobjs=[]
def checkSaveValue (playernum,questname, value):
    mylen=Director.getSaveDataLength(playernum,questname)
    print mylen
    if (mylen>0):
        myfloat=Director.getSaveData(playernum,questname,0)
        print myfloat
    else:
	myfloat=0
    if (myfloat==value):
        return 1
    return 0
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
	Fixer("patrick","Buy a Centerion",[("quest_drone",0)],"bases/fixers/pirate.spr","bases/fixers/patrick.py"),
	Fixer("patrick","Buy a Centerion",[],"bases/fixers/iso.spr","bases/fixers/patrick.py"),
	Fixer("patrick","Buy a Centerion",[("31337ness",.05),("quest_drone",1)],"bases/fixers/cloak.spr","bases/fixers/patrick.py"),
	Fixer("patrick","Buy a Centerion",[],"bases/fixers/militia.spr","bases/fixers/patrick.py")
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
