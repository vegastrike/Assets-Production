import fixers
from fixers import Conversation, Node, RootNode, SubNode

# A list of tuples ("CampaignName","#\npython.code(to,load,the.conversation)")

campaigns=[
	("TestFixer","#\nimport quest_intro2\nconversation = quest_intro2.getCargoCon()"),
	("IntroFixer","#\nimport quest_intro\nconversation = quest_intro.getJenekConversation()"),
	]

def loadAll(cockpit):
	for x in campaigns:
		overwritearg=0
		if len(x)>2:
			overwritearg=x[2]
		fixers.queueFixer(cockpit,x[0],x[1],overwritearg)


