import string
import VS
import vsrandom
import dynamic_news_content

# Here are functions that retrieve and format the news from the dictionary
# returned by the dynamic_news_content.allNews() function
#
#	- type_event is a string of the event type (siege, fleetbattle)
#	- stage_event is a string of the event's stage ("start", "middle", "end")
#	- aggressor is a string of the aggressor faction (ie "confed","rlaan")
#	- defender "   "    "    "   "  defender faction
#	- success is an int, how much success the attacker is having (success = 1, loss = -1, draw = 0)
#	- scale_event is a float, the "importance" of the event (0.0 is highest, 1.0 is lowest)
#	- system is the system string where the event happened (ie "sol_sector/sol")
#	- keyword is not really important right now, but will allow us to call up specific news stories in the future.. #	  for example we may write a special story for a siege of planet earth....just use "all" for now



def makeDynamicNews	(type_event,stage_event,aggressor,defender,success
			,scale_event,system,keyword):
# retrieves a relevant news item from the dynamic_news_content.allNews()
# list, and formats it
	global allUsefullVariables
	allUsefullVariables =	{"type_event"	: type_event
				,"stage_event"	: stage_event
				,"aggressor"	: aggressor
				,"defender"	: defender
				,"success"	: getSuccessStr(success)
#				,"dockedat"	: getDockFaction()
				,"scale_event"	: scale_event
				,"system"	: system
				,"keyword"	: keyword
				}

	return formatNewsItem (getNewsItem(getDockFaction(),type_event,stage_event,getSuccessStr(success)
					 ,getPOV(getDockFaction(),defender,aggressor,getSuccessStr(success))
					 ,scale_event,keyword))

# ------------------------------------------------------------------------------
# String Formatting functions
# ------------------------------------------------------------------------------

def splitPunWord(word):
# splits a word into a list containing any prefix punctuation,
# the word, any suffix punctuation, and any trailing characters
	pre_pun = word[:word.find("VAR_")]
	word_2 = word[len(pre_pun):]
	excess_pun = ""
	for i in range(len(word_2)):
		if word_2[i] in string.punctuation and word_2[i] != "_":
			excess_pun+=word_2[i]
	if len(excess_pun) > 0:
		middle = word_2[:word_2.find(excess_pun[0])]
		end_pun = word_2[word_2.find(excess_pun[0]):word_2.find(excess_pun[len(excess_pun)-1])+1]
		end_alpha = word_2[word_2.find(excess_pun[len(excess_pun)-1])+1:]
		return [pre_pun,middle,end_pun,end_alpha]
	else:
		return [pre_pun,word_2,"",""]

def formatNewsItem(item):
# returns the formatted news item built from the relevant data
	lines = item.split("\n")
	for i in range (len(lines)):
		words = lines[i].split()
		for j in range (len(words)):
			if words[j].find("VAR_") != -1:
				word = splitPunWord(words[j])
				words[j] = word[0] + formatNameTags(word[1],dynamic_news_content.allFactionNames()) + word[2] + word[3]
		lines[i] = string.join(words)
	return string.join(lines,"\n")

def formatNameTags(word,names):
# formats a news tag to be the string so desired
# valid tags include "system_sector", "aggressor_nick", "defender_homeplanet"
	[pre,var,tag] = string.split(word,"_")	
	global allUsefullVariables
	var_string = allUsefullVariables[var]
	if var == "system":
		if tag == "system":
			return formatProperTitle(allUsefullVariables["system"][allUsefullVariables["system"].index("/")+1:])
		if tag == "sector":
			return formatProperTitle(allUsefullVariables["system"][:allUsefullVariables["system"].index("_")])
	if tag in names["alltags"]:
		return names[var_string][tag]
	else:
		print "Error. Invalid news tag."
		return word

def formatProperTitle(str):
# puts capital letters at the start of every word in string
# while preserving caps for all other letters!!!
	words = str.split()
	for i in range (len(words)):
		if words[i][0] in string.lowercase:
			words[i] = words[i][0].capitalize() + words[i][1:]
	return string.join(words)

def makeVarList(ls):
# formats a list of variables to be stored in a save game for later reference
	return string.join(ls,',')


# ------------------------------------------------------------------------------
# Dictionary and Validation functions
# ------------------------------------------------------------------------------

def validateDictKeys(listkeys,dict):
# checks to see if the keys given are available in the dictionary in the specified order

	dicto = dict
	listo = listkeys
	count_true = 0
	for i in range (len(listkeys)):
		if type(dicto) == type(dict):
			if dicto.has_key(listkeys[i]):
				dicto = dicto[listkeys[i]]
				count_true = count_true + 1
	if count_true == len(listkeys):
		return 1
	else:
		return 0

def validateNewsItem(faction_base,type_event,stage_event,success,pov,keyword):
# validates that a news item with the specified variables (or a neutral one) exists)
# returns the faction for which it does exist (if any)
	neutral_list = 0
	neutral_keyword = 0
	specific_list = 0
	specific_keyword = 0
	if validateDictKeys(["neutral",type_event,stage_event,success,pov],dynamic_news_content.allNews()):
		neutral_list = 1
		if validateNewsKeyword(dynamic_news_content.allNews()["neutral"][type_event][stage_event][success][pov],keyword):
			neutral_keyword = 1

	if validateDictKeys([faction_base,type_event,stage_event,success,pov],dynamic_news_content.allNews()):
		specific_list = 1
		if validateNewsKeyword(dynamic_news_content.allNews()[faction_base][type_event][stage_event][success][pov],keyword):
			specific_keyword = 1
	if (not neutral_list) and (not specific_list):
		print "Error.  Specified news variables do not match news dictionary. Returning barf."
		return "barf"
	if (not neutral_keyword) and (not specific_keyword):
		print "Error.  Specified news keyword do not exist. Returning lots of barf."
		return "barfbarfbarfbarfbarfbarfbarfbarf"
	else:
		if specific_keyword:
			return faction_base
		else:
			return "neutral"

def validateNewsKeyword(newslist,keyword):
# validates that a keyword exists for a specified news list
	for i in range (len(newslist)):
		if newslist[i][1] == keyword:
			return 1

# ------------------------------------------------------------------------------
# Miscellaneous functions
# ------------------------------------------------------------------------------

def povCutOff():
# the "cutoff" value for neutral/good/bad in the getPOV function
	return 0.15

def getPOV(facmy,defender,aggressor,success):
# returns a rough string approximation of the relation between two functions
	relatdef = VS.GetRelation(facmy,defender)
	relatagg = VS.GetRelation(facmy,aggressor)

	if (relatdef <= -povCutOff() and relatagg <= -povCutOff()) or (relatdef >= povCutOff() and relatagg >= povCutOff()):
		return "neutral"
	elif relatdef > relatagg:
		if success == "success":
			return "bad"
		elif success == "loss":
			return "good"
		elif success == "draw":
			return "good"
	elif relatdef < relatagg:
		if success == "success":
			return "good"
		elif success == "loss":
			return "bad"
		elif success == "draw":
			return "bad"
	else:
		print "Error, one or more values out of range"
		return "neutral"

def getDockFaction():
# returns the faction of the place the player is docked at
#	return "aera" # FIXME -- make the stub functions actually return a useful value!
	i=0
	playa=VS.getPlayer()
	un=VS.getUnit(i)
	while(un):
		i+=1
		if (un.isDocked(playa)):
			break
		un=VS.getUnit(i)
	if un.isPlanet() or (un.getFactionName() == "neutral"):
		global allUsefullVariables
		return VS.GetGalaxyFaction(allUsefullVariables["system"])
	else:
		return un.getFactionName()

def getSuccessStr(success):
# returns a string either "success" or "loss" based on the arg success
	if success == 1:
		return "success"
	elif success == -1:
		return "loss"
	elif success == 0:
		return "draw"

def getNewsItem(faction_base,type_event,stage_event,success,pov,scale,keyword):
# finds a suitable news string from the dynamic_news_content.allNews() dictionary
	listnews = dynamic_news_content.allNews()[validateNewsItem(faction_base,type_event,stage_event,success,pov,keyword)][type_event][stage_event][success][pov]
	return getClosestScaleNews(listnews,scale)

def getClosestScaleNews(listof,scale):
# returns the closest scaled news item from a list of news items
	valtable = []
	for i in range (len(listof)):
		valtable.append(listof[i] + (abs(scale - listof[i][0]),))
	finallist = [valtable[0]]
	for i in range (1,len(valtable)):
		if finallist[0][3] > valtable[i][3]:
			finallist = [valtable[i]]
		elif finallist[len(finallist) - 1][3] == valtable[i][3]:
			finallist.append(valtable[i])
	return finallist[vsrandom.randrange(0,len(finallist), step=1)][2]



def processNewsTuple(newsstring):
	ls = newsstring.split(',')
	ns = makeDynamicNews(ls[0],ls[1],ls[2],ls[3],string.atoi(ls[4]),string.atof(ls[5]),ls[6],ls[7])
	print ns
	return ns
#	return newsstring #FIXME


def pushDynamicNews(player,newsstring):
	print 'pushing' + newsstring + ' to news savevar'
	import Director
	Director.pushSaveString(player,"news",processNewsTuple(newsstring))
