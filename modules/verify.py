from campaign_lib import *
import campaigns
campaigns.loadAll(0)
global traverser
traverser=[]
def isType(a,typ):
    return a.__init__.im_func==typ.__init__.im_func
class MyCondition:
	def __init__(self,var=[]):
		self.system=("","")
		self.vars=var
	def pre(self,precond):

		#FIXME
		return True
	def script(self,scriptname):
		if (scriptname==None):
			print "None script"
			return True
		return scriptname.__init__.im_func==TrueSubnode.__init__.im_func
	def post(self,postcond):
		#FIXME
		return True
def EndNode(node):
	return CampaignEndNode(node.campaign).subnodes[0]
def IsEnd(node):
	precond=CampaignEndNode(node.campaign).subnodes[0].preconditions[0]
	try:
		if (len(node.preconditions)!=1):
			return False
	except:
		print node
		print dir(node)
		print node.preconditions
	if (node.preconditions[0].__init__.im_func!=precond.__init__.im_func):
		return False
	return node.preconditions[0].system==precond.system and  node.preconditions[0].dockedshipname==precond.dockedshipname
		
class Traverser:
	def __init__(self,campaign):
		self.node=campaign.root
		self.system=[]
		self.visitednodes=[self.node]
	def dup(self):
		tmp=Traverser(self.node.campaign)
		tmp.system=self.system
		tmp.node=self.node
		tmp.visitednodes=self.visitednodes
		return tmp
	def warn(self,strin):
		print strin
	def cont(self,newnode):
		if newnode in self.visitednodes:
			self.node=EndNode(self.node)
		else:
			self.node=newnode
			self.visitednodes.append(newnode)
	def Update(self,var):
		if (IsEnd(self.node)):
			return None
		cond=MyCondition(var)
		if not cond.pre(self.node.preconditions):
			return None
		if cond.script(self.node.script):
			#true subnode
			for sn in self.node.subnodes:
				if (cond.post(sn.preconditions)):
					tmp=self.dup()
					tmp.cont(sn)
					traverser.append(tmp)
			if (self.node.contingency):
				self.cont(self.node.contingency)
			else:
				self.cont(EndNode(self.node))
		elif self.node.contingency:
			for sn in self.node.subnodes:
				tmp=self.dup()
				tmp.cont(sn)
				traverser.append(tmp)
			self.warn("Contingency in non trueSubnode")
			self.cont(self.node.contingency)
		elif (len(self.node.subnodes)):
			if (len(self.node.subnodes)>1):
				for sn in self.node.subnodes[1:]:
					tmp=self.dup()
					tmp.cont(sn)
					traverser.append(tmp)
			self.cont(self.node.subnodes[0])
		else:
			return None#cannot make progres
		return cond.vars;
def IsFinished():
	global traverser
	for i in range(len(traverser)-1,-1,-1):

		if IsEnd(traverser[i].node):
			del traverser[i]

	return len(traverser)>0
for iter in campaigns.campaigns:
	traverser.append(Traverser(iter))
print len(traverser)
while len(traverser):
	IsFinished()
	progress=False
	variables=[]
	for i in range(len(traverser)):
		var=traverser[i].Update(variables)
		if (type(var)==type([])):
			variables=var
			progress=True
	if not progress and len(traverser):
		print "Deadlock "
		break
