## Here are functions that retrieve and format the news from the dictionary
## returned by the dynamic_news_content.allNews() function
##
##	- type_event is a string of the event type (siege, fleetbattle)
##	- stage_event is a string of the event's stage
##	  ("start", "middle", "end")
##	- aggressor is a string of the aggressor faction
##	  (ie "confed","rlaan")
##	- defender "   "    "    "   "  defender faction
##	- success is an int, how much success the attacker is having
##	  (success = 1, loss = -1, draw = 0)
##	- scale_event is a float, the "importance" of the event
##	  (0.0 is highest, 1.0 is lowest)
##	- system is the system string where the event happened
##	  (ie "sol_sector/sol")
##	- keyword is not really important right now, but will allow us
##	  to call up specific news stories in the future..
##	  for example we may write a special story for a siege of
##	  planet earth....just use "all" for now

import string
import VS
import vsrandom
import dynamic_news_content


def makeDynamicNews	(stardate,type_event,stage_event,aggressor,defender,success
			,scale_event,system,keyword,aggressor_flightgroup,aggressor_type, defender_flightgroup, defender_type,randint):
	"""retrieves a relevant news item from the dynamic_news_content.allNews()
	list, and formats it"""

	if aggressor_flightgroup == "blue": #if the player was the attacker
		aggressor_flightgroup = "Huntington" #FIXME: make it the players callsign (or even fleetname)!
		if keyword == "all":
			keyword = "player"
		

	global allUsefullVariables
	allUsefullVariables =	{"type_event"	: type_event		#NOTE: atm none of the used in the content
				,"stage_event"	: stage_event		#can have punctuation in it :-(
				,"aggressor"	: aggressor		# -- as of 08/07/03 this is from aggressor down --
				,"defender"	: defender
				,"success"	: getSuccessStr(success)
				,"dockedat"	: getDockFaction()
				,"scale_event"	: scale_event
				,"system"	: system
				,"keyword"	: keyword
				,"stardate" : stardate
				,"aggressorFG"	: formatName(aggressor_flightgroup)
				,"aggressorFGtype": formatShipName(aggressor_type)
				,"defenderFG"	: formatName(defender_flightgroup)
				,"defenderFGtype": formatShipName(defender_type)
				}

	return formatNewsItem (getNewsItem(getDockFaction(),type_event,stage_event,getSuccessStr(success)
					 ,getPOV(getDockFaction(),defender,aggressor,getSuccessStr(success))
					 ,scale_event,keyword,randint),randint)

# ------------------------------------------------------------------------------
# String Formatting functions
# ------------------------------------------------------------------------------

def splitPunWord(word):
	"""splits a word into a list containing any prefix punctuation,
	the word, any suffix punctuation, and any trailing characters"""
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

def formatNewsItem(item,rint):
	import seedrandom
	randint = seedrandom.rands(rint)
	"""returns the formatted news item built from the relevant data"""
	lines = item.split("\n")
	for i in range (len(lines)):
		words = lines[i].split()
		for j in range (len(words)):
			if words[j].find("VAR_") != -1:
				word = splitPunWord(words[j])
				words[j] = word[0] + formatNameTags(word[1],dynamic_news_content.allFactionNames(),randint) + word[2] + word[3]
				randint = seedrandom.rands(randint)
				
		lines[i] = string.join(words)
	return string.join(lines,"\n")

def formatNameTags(word,names,randint):
	"""formats a news tag to be the string so desired
	valid tags include "system_sector", "aggressor_nick"
	and "defender_homeplanet" """
	try:
		[pre,var,tag] = string.split(word,"_")	
		global allUsefullVariables
		var_string = allUsefullVariables[var]
	except:
		print str(word)+" is not a valid dict name"
		return word
	if var == "system":
		if tag == "sector":
			return formatProperTitle(formatName(allUsefullVariables["system"][:allUsefullVariables["system"].index("_")]))
		if tag != "system":
			print "error "+tag+" not acceptible VAR_system_tag"
		return formatProperTitle(formatName(allUsefullVariables["system"][allUsefullVariables["system"].index("/")+1:]))
	elif var == "stardate":
		if tag == "value":
			return allUsefullVariables[var]
		else:
			print "stardate wrong"
			return allUsefulVariables[var]
	elif tag in ["FG","FGtype"] :
		return allUsefullVariables[var+tag]
	elif tag in names["alltags"] and validateDictKeys([var_string,tag],dynamic_news_content.allFactionNames()):
		tmp = names[var_string][tag]
		return tmp[randint%len(tmp)]
	else:
		print "Error. Invalid news tag, not found in dictionary."
		return word

def formatProperTitle(str):
	"""puts capital letters at the start of every word in string
	while preserving caps for all other letters!!! """
	words = str.split()
	for i in range (len(words)):
		if (len(words[i])):
			if words[i][0] in string.lowercase:
				words[i] = words[i][0].capitalize() + words[i][1:]
	return string.join(words)

def formatName(strin):
	"""removes any underscores or dots and replaces them with spaces"""
	return string.join(string.join(strin.split('.')).split('_'))

def formatShipName(strin):
	"""formats a standard ship name (ie firefly.blank) to
	something more natural (ie basic Firefly)"""
	lis = strin.split('.')
	if len(lis) > 1:
		extension = lis[len(lis)-1]
		if extension == "blank":
			ship = string.join(string.join(lis[:len(lis)-1]," ").split('_'),' ')
			return "basic " + formatProperTitle(ship)
		elif extension == "millspec":
			ship = string.join(string.join(lis[:len(lis)-1]," ").split('_'),' ')
			return "modified " + formatProperTitle(ship)
		else:
			ship = string.join(string.join(lis," ").split('_'),' ')
			return formatProperTitle(ship)
	else:
		return formatProperTitle(string.join(lis[0].split('_'),' '))
		

def makeVarList(ls):
	"""formats a list of variables to be stored in a save game
	for later reference"""
	return string.join([str(vsrandom.randrange(0,4194304))]+ls,',')


def makeStarDate(stri):
	"""formats a stardate string for appending to the news story"""
	import stardate
	global allUsefullVariables
	return "\\\\\\Story first broadcast: " + formatStarDate(stardate.getFacCal(allUsefullVariables["dockedat"],allUsefullVariables["stardate"]))

def formatStarDate(date):
	return str(date[1]) + " " + fillWithZeros(date[2],2) + " " + fillWithZeros(date[0],4) + ", " + fillWithZeros(date[3],2) + ":" + fillWithZeros(date[4],2) + ":" + fillWithZeros(date[5],2)

def fillWithZeros(inttofill,numnumbers):
	num = str(inttofill)
	while len(num) < numnumbers:
		num = "0" + num
	return num

# ------------------------------------------------------------------------------
# Dictionary and Validation functions
# ------------------------------------------------------------------------------

def validateDictKeys(listkeys,dict):
	"""checks to see if the keys given are available in the
	dictionary in the specified order"""

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
	"""validates that a news item with the specified variables
	(or a neutral one) exists) returns the faction for which
	it does exist (if any)"""
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
	"""validates that a keyword exists for a specified news list"""
	for i in range (len(newslist)):
		if newslist[i][1] == keyword:
			return 1

# ------------------------------------------------------------------------------
# Miscellaneous functions
# ------------------------------------------------------------------------------

def povCutOff():
	"""the "cutoff" value for neutral/good/bad in the getPOV function"""
	return 0.25

def getPOV(facmy,defender,aggressor,success):
	"""returns a rough string approximation of the relation between
	two functions"""
	relatdef = VS.GetRelation(facmy,defender)
	relatagg = VS.GetRelation(facmy,aggressor)
#	print "relatdef =",
#	print relatdef
#	print "relatagg =",
#	print relatagg

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
	"""returns the faction of the place the player is docked at"""
	i=0
	playa=VS.getPlayer()
	un=VS.getUnit(i)
	while(un):
		i+=1
		if (un.isDocked(playa) or playa.isDocked(un)):
			if not (un.isPlanet() or (un.getFactionName() == "neutral")):
				fac = un.getFactionName()
				print 'returning '+un.getName()+' s faction as '+fac+' from flightgroup '+un.getFlightgroupName()
				return fac
			break
		un=VS.getUnit(i)
	retfac = VS.GetGalaxyFaction(VS.getSystemFile())
	print "Returning " + retfac + " as the systems faction"
	return retfac
	


def getSuccessStr(success):
	"""returns a string either "success" or "loss" based on the arg success"""
	if success == 1:
		return "success"
	elif success == -1:
		return "loss"
	elif success == 0:
		return "draw"

def getNewsItem(faction_base,type_event,stage_event,success,pov,scale,keyword,randint):
	"""finds a suitable news string from
	the dynamic_news_content.allNews() dictionary"""
	faction = validateNewsItem(faction_base,type_event,stage_event,success,pov,keyword)
	if faction == "barf":
		print "Error: A suitable news story does not exist, returning a warning string."
		return getClosestScaleNews([(scale,"all","ERROR!\\Invalid news variables:\\(" + string.join([faction_base,type_event,stage_event,success,pov,str(scale),keyword],',') + ")\\A suitable news story for this event could not be found.\\@hellcatv: don't worry, flightgroup info is available, it just doesn't get passed down this far (it's stored in the global instead) but you know it's there so don't worry ;-)\\This is a placeholder error message.\\\\Contact the help-desk for any queries:\\dandandaman@users.sourceforge.net ;-)\\\\\\ -- The Vegastrike Community:\\Struggling with lack of hands to go around since 1998")],scale,randint)
	elif faction == "barfbarfbarfbarfbarfbarfbarfbarf":
		print "Error: News variables correct.  Content not available."
		return getClosestScaleNews([(scale,"all","ERROR!\\No content available:\\(" + string.join([faction_base,type_event,stage_event,success,pov,str(scale),keyword],',') + ")\\A suitable news story for this event could not be found.  Content must not be completed for this section.\\@hellcatv: don't worry, flightgroup info is available, it just doesn't get passed down this far (it's stored in the global instead) but you know it's there so don't worry ;-)\\This is a placeholder error message.\\\\Contact the help-desk for any queries:\\dandandaman@users.sourceforge.net ;-)\\\\\\ -- The Vegastrike Community:\\Struggling with lack of hands to go around since 1998")],scale,randint)
		
	listnews = filterForKeyword(dynamic_news_content.allNews()[faction][type_event][stage_event][success][pov],keyword)
	return getClosestScaleNews(listnews,scale,randint)

def filterForKeyword(listnews,keyword):
	"""filters a list of news items to return a list of only those
	matching the specified keyword"""
	kwlist = list()
	for item in listnews:
		if item[1] == keyword:
			kwlist.append(item)
	return kwlist

def getClosestScaleNews(listof,scale,randint):
	"""returns the closest scaled news item from a list of news items"""
	valtable = []
	for i in range (len(listof)):
		valtable.append(listof[i] + (abs(scale - listof[i][0]),))
	finallist = [valtable[0]]
	for i in range (1,len(valtable)):
		if finallist[0][3] > valtable[i][3]:
			finallist = [valtable[i]]
		elif finallist[len(finallist) - 1][3] == valtable[i][3]:
			finallist.append(valtable[i])
	if (len(finallist)==0):
		return "br0ken"
	else:
		return finallist[randint%len(finallist)][2]

def minorNewsTypes():
	"""a list of all the minor news types that should be system dependent"""
	return ["battle","destroyed"]

def checkSystemRelevant(system):
	"""returns 1 if the system in question is within a 1 system radius of
	the players current system"""
	mysys = VS.getSystemFile()
	if mysys == system:
		return 1
	for i in range(VS.GetNumAdjacentSystems(mysys)):
		if (VS.GetAdjacentSystem(mysys,i)==system):
			return 1

def GetAllAdjacentSystems(mystr):
	syslist = list()
	for i in range(VS.GetNumAdjacentSystems(mystr)):
		syslist.append(VS.GetAdjacentSystem(mystr,i))
	return syslist

def checkVarListRelevant(newslist,randint):
	"""returns true only if the newslist is relevant
	(major or close to home)"""
	if (not (newslist[1] in minorNewsTypes())):
		return 1
	if (checkSystemRelevant(newslist[7])):
		return 1

def processNewsTuple(newsstring,randint):
	"""takes a news variable string and returns the news story taking
	or not taking into account the random int given/not given"""

	ls = newsstring.split(',')
#	while (len(ls)<13):
#		ls.append ('unknown')
	print 'lsing '+ str(ls)
	ns = makeDynamicNews(ls[0],ls[1],ls[2],ls[3],ls[4],string.atoi(ls[5]),string.atof(ls[6]),ls[7],ls[8],ls[9],ls[10],ls[11],ls[12],randint)
	print ns
	return ns + makeStarDate(ls[0])
#Added flightgroups as the last few arguments


def manageDynamicNews(player,newsstring):
	""" manages the dynamic news item passed to it"""
#	print "against its ferrocious struggling I am"
#	print "pushing " + newsstring + " through the generator"
	varlist = newsstring.split(',')
	varlist.reverse()
	randint = int(varlist.pop())
	varlist.reverse()
	if checkVarListRelevant(varlist,randint):
#		print "news is relevant"
		varstring = string.join(varlist,",")
		import Director
		Director.pushSaveString(player,"news",processNewsTuple(varstring,randint))
	else:
#		print "news " + newsstring + " ignored...not relevant"
		print ".",

