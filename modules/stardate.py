def getFacCal(fac,stdt):									#FIXME: make docked faction dependent
	"""takes a stardate string and returns a list of ints with
	[year,month,date,hour,minute,second]"""
	zeroyear = getZeroYear("faction")
	styear = stdt[:stdt.find('.')-3]
	styeardec = float(stdt[len(styear):])		#FIXME: only goes up to 1 stardate accuracy
	return makeFacDate(int(zeroyear+int(styear)),styeardec,fac)

def makeFacDate(year,frac,fac):
	return [year] + getMDDHMS(frac,getDateSystem(fac),year,fac)

def daysinMonth(monthsystem,month):
	for mon in monthsystem:
		if mon[0] == month:
			return mon[1]
	return 1

def daysinYear(monthsystem):
	count = 0
	for mon in monthsystem:
		count+=mon[1]
	return count

def addMonthDays(monthsys,leap):
	for i in range(len(monthsys)):
		for lmon in leap:
			if monthsys[i][0] == lmon[0]:
				monthsys[i] = (monthsys[i][0],monthsys[i][1] + lmon[1])
	return monthsys

def getMDDHMS(frac,system,year,fac):
	monthsystem = addMonthDays(system[0],getLeap(year,fac))
	numdays = getStarToDay(monthsystem) * frac
	remdays = numdays
	countdays = 0
	mon = monthsystem[0][0]
	for i in range(len(monthsystem)):
		countdays+=monthsystem[i][1]
		if countdays >= numdays:
			mon = monthsystem[i][0]
			break
		else:
			remdays = numdays - countdays + 1	#FIXME: not sure exactly why the 1 is required, I think
										#it is so that a fractional day would be counted as
										#the 1st, 3.5 days into the month the 4th day etc
	days = int(remdays)
	remainder = remdays - days

	htemp = remainder * system[1][0]
	hours = int(htemp)
	mintemp = (htemp - hours) * system[1][1]
	minutes = int(mintemp)
	sectemp = (mintemp - minutes) * system[1][2]
	seconds = int(sectemp)
	return [mon,days,hours,minutes,seconds]


def getDateSystem(faction):
	"""returns a particlar races standard date system (not including leap years)"""
	if facDateSystems().has_key(faction):
		return facDateSystems()[faction]
	else:
		return facDateSystems()["standard"]


def getStarToDay(monthsystem):
	"""returns a particlar races stardate to day ration"""
	return daysinYear(monthsystem) / 1000.0	#FIXME: make faction dependent

def getZeroYear(faction):
	return 2003	#FIXME: make faction dependent

def getLeap(year,faction):
	if faction == "confed":
		if year%100 == 0:
			return list()
		elif year%4 == 0:
			return [("February",1)]
		else:
			return list()
	else:
		if year%100 == 0:
			return list()
		elif year%4 == 0:
			return [("February",1)]
		else:
			return list()

def facDateSystems():
	"""returns the date systems for all the factions with special ones"""
	return {

	"standard" :
	([("January",31),("February",28),("March",31),("April",30),("May",31),("June",30),("July",31),("August",31),("September",30),("October",31),("November",30),("December",31)],(24,60,60),["year","month","week","day","hour","minute","second"])

	}
