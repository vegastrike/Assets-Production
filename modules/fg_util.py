import Director
import VS
import vsrandom
ccp=VS.getCurrentPlayer()
#Aera Plants
#Rlaan Rocks
#Hum0n Cities
#Uln adVerbs
#klkk Adjectives
def MaxNumFlightgroupsInSystem ():
	return 10
def MaxNumBasesInSystem():
	return 10
def MinNumBasesInSystem():
	return 0
def MakeFactionKey (faction):
	return 'FF:'+str(VS.GetFactionIndex(faction))
def MakeFGKey (fgname,faction):
	return 'FG:'+str(fgname)+'|'+str(VS.GetFactionIndex(faction))
def MakeStarSystemFGKey (starsystem):
	return 'SS:'+str(starsystem)
def ShipListOffset ():
	return 3
def PerShipDataSize ():
	return 3
def AllFactions ():
	facs =[]
	for i in range (VS.GetNumFactions()):
		facs+= [VS.GetFactionName(i)]
	return facs
basenamelist={}
flightgroupnamelist={}
genericalphabet=['Alpha','Beta','Gamma','Delta','Epsilon','Zeta','Phi','Omega']
def ReadBaseNameList(faction):
	bnl=[]
	print 'reading base names '+str(faction)
	filename = 'universe/fgnames/'+faction+'.txt'
	try:
		f = open (filename,'r')
		bnl = f.readlines()
		f.close()
	except:
		try:
			f = open ('../'+filename,'r')
			bnl = f.readlines()
			f.close()
		except:
			try:
				f = open ('../universe/names.txt','r')
				bnl = f.readlines()
				f.close()
			except:
				try:
					f = open ('universe/names.txt','r')
					bnl = f.readlines()
					f.close()
				except:
					global genericalphabet
					bnl=genericalphabet
	for i in range(len(bnl)):
		bnl[i]=bnl[i].rstrip()
	import vsrandom
	vsrandom.shuffle(bnl)
	return bnl
def GetRandomFGNames (numflightgroups, faction):
	global flightgroupnamelist
	if (not (faction in flightgroupnamelist)):
		flightgroupnamelist[faction]=ReadBaseNameList(faction)
	additional=[]
	if (numflightgroups>len(flightgroupnamelist[faction])):
		for i in range (numflightgroups-len(flightgroupnamelist)):
			additional.append(str(i))
	return additional+flightgroupnamelist[faction]
basecounter=0
def GetRandomBaseName (n,faction):
	global basecounter
	retval=[]
	global basenamelist
	try:
		import seedrandom
		if (not (faction in basenamelist)):
			basenamelist[faction]=ReadBaseNameList(faction+'_base')
		for i in range (n):
			retval+=[basenamelist[faction][basecounter%len(basenamelist[faction])]]
			basecounter+=1
	except:
		print 'uhoh base lsit wrong'
		retval=[]
		for i in range (n):
			retval+=[str(n)]
			n+=1
	return retval
origfgoffset=0
def TweakFGNames (origfgnames):
	global origfgoffset
	tweaker=str(origfgoffset)
	tweaktuple = ('prime','double_prime','triple_prime','quad_prime','quint_prime')
	if (origfgoffset<len(tweaktuple)):
		tweaker = tweaktuple[origfgoffset]
	rez=[]
	for i in origfgnames:
		rez.append (i+'_'+tweaker)
	origfgoffset+=1
	return rez
		
def WriteStringList(cp,key,tup):
	siz = Director.getSaveStringLength (cp,key)
	s_size=siz;
	lentup= len(tup)
	if (lentup<siz):
		siz=lentup
	for i in range(siz):
		Director.putSaveString(cp,key,i,tup[i])
	for i in range (s_size,lentup):
		Director.pushSaveString(cp,key,tup[i])
	for i in range (lentup,s_size):
		Director.eraseSaveString(cp,key,lentup)
def ReadStringList (cp,key):
	siz = Director.getSaveStringLength (cp,key)
	tup =[]
	for i in range (siz):
		tup += [Director.getSaveString(cp,key,i)]
	return tup
def AllFlightgroups (faction):
	key = MakeFactionKey (faction)
	return ReadStringList(ccp,key)
def NumAllFlightgroups (faction):
	key = MakeFactionKey(faction)
	return Director.getSaveStringLength(ccp,key)
def RandomFlightgroup (faction):
	key = MakeFactionKey(faction)
	i = Director.getSaveStringLength(ccp,MakeFactionKey(faction))
	if (i==0):
		return ''
	import vsrandom
	return Director.getSaveString(ccp,key,vsrandom.randrange(0,i))
def ListToPipe (tup):
	fina=''
	if (len(tup)):
		fina=tup[0]
	for i in range (1,len(tup)):
		fina+='|'+tup[i]
	return fina

def _MakeFGString (starsystem,typenumlist):
	totalships = 0
	ret = []
	damage=0
	strlist=[]
	for tt in typenumlist:
		totalships+=int(tt[1])
		strlist+=[str(tt[0]),str(tt[1]),str(tt[1])]
	return [str(totalships),str(starsystem),str(damage)]+strlist

def _AddShipToKnownFG(key,tn):
	leg = Director.getSaveStringLength (ccp,key)
	#try:
	numtotships =int(Director.getSaveString(ccp,key,0))
	numtotships+=int(tn[1])
	Director.putSaveString(ccp,key,0,str(numtotships))
	#except:
	#	print 'error adding ship to flightgroup'
	for i in range (ShipListOffset()+1,leg,PerShipDataSize()):
		if (Director.getSaveString(ccp,key,i-1)==str(tn[0])):
			numships=0
			numactiveships=0
			try:
				numships+= int(tn[1])
				numactiveships+= int(tn[1])
				numships+= int (Director.getSaveString(ccp,key,i))
				numactiveships+= int (Director.getSaveString(ccp,key,i+1))
			except:
				pass
			Director.putSaveString(ccp,key,i,str(numships))
			Director.putSaveString(ccp,key,i+1,str(numactiveships))
			return
	Director.pushSaveString(ccp,key,str(tn[0]))
	Director.pushSaveString(ccp,key,str(tn[1]))
	Director.pushSaveString(ccp,key,str(tn[1]))#add to number active ships

def _AddFGToSystem (fgname,faction,starsystem):
	key = MakeStarSystemFGKey (starsystem)
	leg = Director.getSaveStringLength (ccp,key)
	index = VS.GetFactionIndex (faction)
	if (leg>index):
		st=Director.getSaveString (ccp,key,index)
		if (len(st)>0):
			st+='|'
		Director.putSaveString(ccp,key,index,st+fgname)
	else:
		for i in range (leg,index):
			Director.pushSaveString(ccp,key,'')
		Director.pushSaveString(ccp,key,fgname)


def _RemoveFGFromSystem (fgname,faction,starsystem):
	key = MakeStarSystemFGKey( starsystem)
	leg = Director.getSaveStringLength(ccp,key)
	index = VS.GetFactionIndex(faction)
	if (leg>index):
		tup = Director.getSaveString (ccp,key,index).split('|')
		try:
			del tup[tup.index(fgname)]
			Director.putSaveString(ccp,key,index,ListToPipe(tup))			
		except:
			print 'fg '+fgname+' not found in '+starsystem
	else:
		print 'no ships of faction '+faction+' in '+starsystem

def _AddFGToFactionList(fgname,faction):
	key = MakeFactionKey(faction)
	Director.pushSaveString (ccp,key,fgname)
		
def _RemoveFGFromFactionList (fgname,faction):
	key = MakeFactionKey(faction)
	lun=Director.getSaveStringLength(ccp,key)
	for i in range (lun):
		if (Director.getSaveString(ccp,key,i)==fgname):
			Director.eraseSaveString(ccp,key,i)
			return 1
	return 0

def CheckFG (fgname,faction):
	key = MakeFGKey (fgname,faction)
	leg = Director.getSaveStringLength (ccp,key)
	totalships=0
	try:
		for i in range (ShipListOffset()+1,leg,PerShipDataSize()):
			shipshere=Director.getSaveString(ccp,key,i)
			totalships+=int(shipshere)
			temp=Director.getSaveString(ccp,key,i+1)
			if (temp!=shipshere):
				print 'correcting flightgroup '+fgname+' to have right landed ships'
			Director.putSaveString(ccp,key,i+1,shipshere)#set num actives to zero
		if (totalships!=int(Director.getSaveString(ccp,key,0))):
			print 'mismatch on flightgroup '+fgname+' faction '+faction
			return 0
	except:
		print 'nonint readingo n flightgroup '+fgname+'faction '+faction
		return 0
	return 1
def PurgeZeroShips (faction):
	key=MakeFactionKey(faction)
	len=Director.getSaveStringLength (ccp,key)
	i=0
	while i<len:
		curfg=Director.getSaveString(ccp,key,i)
		CheckFG (curfg,faction)
		numships=NumShipsInFG(curfg,faction)
		if (numships==0):
			DeleteFG(curfg,faction)
			i-=1
			len-=1
		i+=1
		
def NumShipsInFG (fgname,faction):
	key = MakeFGKey (fgname,faction)
	len = Director.getSaveStringLength (ccp,key)
	if (len==0):
		return 0
	else:
		try:
			return int(Director.getSaveString(ccp,key,0))
		except:
			print 'fatal: flightgroup without size'
			return 0

def GetDamageInFGPool (fgname,faction):
	key = MakeFGKey (fgname,faction)
	len = Director.getSaveStringLength (ccp,key)
	if (len<3):
		return 0
	else:
		try:
			return int(Director.getSaveString(ccp,key,2))
		except:
			print 'nonfatal: flightgroup without size'
			return 0

def SetDamageInFGPool (fgname,faction,num):
	key = MakeFGKey (fgname,faction)
	len = Director.getSaveStringLength (ccp,key)
	if (len>2):
		Director.putSaveString(ccp,key,2,str(num))				   


def DeleteFG(fgname,faction):
	key = MakeFGKey (fgname,faction)
	len = Director.getSaveStringLength (ccp,key)
	if (len>=ShipListOffset()):
		starsystem=Director.getSaveString(ccp,key,1)
		_RemoveFGFromSystem(fgname,faction,starsystem)
		_RemoveFGFromFactionList(fgname,faction)
		WriteStringList (ccp,MakeFGKey(fgname,faction),[] )
def DeleteAllFG (faction):
	for fgname in ReadStringList (ccp,MakeFactionKey (faction)):
		DeleteFG (fgname,faction)
def FGSystem (fgname,faction):
	key = MakeFGKey(fgname,faction)
	len = Director.getSaveStringLength(ccp,key)
	if (len>1):
		return Director.getSaveString(ccp,key,1)
	else:
		#print fgname+' for '+faction+' already died, in no system'
		return 'nil'
def TransferFG (fgname,faction,tosys):
	key = MakeFGKey(fgname,faction)
	len = Director.getSaveStringLength(ccp,key)
	if (len>1):
		starsystem=Director.getSaveString(ccp,key,1)
		_RemoveFGFromSystem(fgname,faction,starsystem)
		_AddFGToSystem(fgname,faction,tosys)
		Director.putSaveString(ccp,key,1,tosys)

def AddShipsToFG (fgname,faction,typenumbertuple,starsystem):
	key = MakeFGKey(fgname,faction)	
	len = Director.getSaveStringLength (ccp,key)
	if (len<ShipListOffset()):
		WriteStringList(ccp,key,_MakeFGString( starsystem,typenumbertuple) )
		_AddFGToSystem (fgname,faction,starsystem)
		_AddFGToFactionList (fgname,faction)
	else:
		for tn in typenumbertuple:
			_AddShipToKnownFG(key,tn)
	
def RemoveShipFromFG (fgname,faction,type,numkill=1,landed=0):
	key = MakeFGKey (fgname,faction)
	leg = Director.getSaveStringLength (ccp,key)
	for i in range (ShipListOffset()+1,leg,PerShipDataSize()):
		if (Director.getSaveString(ccp,key,i-1)==str(type)):
			numships=0
			numlandedships=0
			try:
				numships = int (Director.getSaveString (ccp,key,i))
				numlandedships=int (Director.getSaveString (ccp,key,i+1))
			except:
				print "unable to get savestring "+i+" from FG "+fgname +" "+faction+ " "+type
			if (numships>numkill):
				numships-=numkill
				if (numships<numlandedships):
					landed=1
					#print 'trying to remove launched ship '+type+' but all are landed'
				Director.putSaveString (ccp,key,i,str(numships))
				if (landed and numlandedships>0):
					Director.putSaveString(ccp,key,i+1,str(numlandedships-numkill))
			else:
				numkill=numships
				numships=0
				for j in range (i-1,i+PerShipDataSize()-1):
					Director.eraseSaveString(ccp,key,i-1)
			if (numships>=0):
				try:
					totalnumships = int(Director.getSaveString(ccp,key,0))
					totalnumships -=numkill
					if (totalnumships>=0):
						Director.putSaveString(ccp,key,0,str(totalnumships))
						if(totalnumships==0):
							DeleteFG(fgname,faction)
					else:
						print 'error...removing too many ships'
				except:
					print 'error, flight record '+fgname+' corrupt'
			return numkill
	print 'cannot find ship to delete in '+faction+' fg ' + fgname
	return 0
def BaseFGInSystemName (system):
	return 'Base_'+system
def AllFGsInSystem(faction,system):
	key = MakeStarSystemFGKey (system)
	leg = Director.getSaveStringLength (ccp,key)
#	if 1:#(not (Director.dontdoprint)):
#		print faction
	facnum = VS.GetFactionIndex (faction)
	ret=[]
	if (leg>facnum):
		st=Director.getSaveString(ccp,key,facnum)
		if (len(st)>0):
			ret = st.split('|')
	return ret

def FGsInSystem(faction,system):
	ret = AllFGsInSystem(faction,system)
	basefg = BaseFGInSystemName(system)
	if (basefg in ret):
		del ret[ret.index(basefg)]
	return ret

def BaseFGInSystem(faction,system):
	ret = AllFGsInSystem(faction,system)
	basefg = BaseFGInSystemName(system)
	if (basefg in ret):
		return 1
	return 0
def BaseFG(faction,system):
	if (BaseFGInSystem(faction,system)):
		return LandedShipsInFG (BaseFGInSystemName(system),faction)		
	return []
def NumFactionFGsInSystem(faction,system):
	key = MakeStarSystemFGKey (system)
	leg = Director.getSaveStringLength (ccp,key)
	facnum = VS.GetFactionIndex (faction)
	st=''
	if (leg>facnum):
		st=Director.getSaveString(ccp,key,facnum)
	if (st):
		return st.count('|')+1
	return 0

def CountFactionShipsInSystem(faction,system):
	count=0
	st=''
	for fgs in FGsInSystem (faction,system):
		st+=fgs+' '
		ships=ReadStringList (ccp,MakeFGKey (fgs,faction))
		for num in range(ShipListOffset()+2,len(ships),PerShipDataSize()):
			try:
				count+= int(ships[num])
			except:
				print 'number ships '+ships[num] + ' not read'
	print 'OFFICIALCOUNT '+st
	return count
def _prob_round(curnum):
	import vsrandom
	ret = int(curnum)
	diff = curnum-int(curnum)
	if (diff>0):
		if (vsrandom.uniform (0,1)<diff):
			ret+=1
	else:
		if (vsrandom.uniform (0,1)<-diff):
			ret-=1
	return ret

def LandedShipsInFG(fgname,faction):
	return ShipsInFG(fgname,faction,2)
def ShipsInFG(fgname,faction,offset=1):
	ships = ReadStringList (ccp,MakeFGKey(fgname,faction))
	rez=[]
	for num in range (ShipListOffset(),len(ships),PerShipDataSize()):
		rez+=[(ships[num],int(ships[num+offset]))]
	return rez
def RandomShipIn (fg,fac):
	key = MakeFGKey(fg,fac)
	len = Director.getSaveStringLength(ccp,key)-ShipListOffset()
	len = int(len/PerShipDataSize())
	if (len>0):
		return Director.getSaveString(ccp,key,ShipListOffset()+PerShipDataSize()*vsrandom.randrange(0,len))
	return ''

def minIndex (vals,indices):
	for i in indices:
		ok=1
		for j in indices:
			if vals[j]<vals[i]:
				ok=0
		if ok:
			return i
	return 0

def launchBaseOrbit(type,faction,loc,orbitradius,orbitspeed,unit):
	import Vector
	import dynamic_universe
	R = Vector.Vector(vsrandom.uniform(.5*orbitradius,orbitradius),
					  vsrandom.uniform(.5*orbitradius,orbitradius),
					  vsrandom.uniform(.5*orbitradius,orbitradius))
	RMag = Vector.Mag(R)
	T = Vector.Vector(vsrandom.uniform(.5*orbitradius,orbitradius),
					  vsrandom.uniform(.75*orbitradius,.85*orbitradius),
					  vsrandom.uniform(.5*orbitradius,orbitradius))
	S = Vector.Cross (T,R)
	
	S = Vector.Scale(S,
					 vsrandom.uniform (.4*orbitradius,orbitradius)
					 /Vector.Mag(S))
	SMag = Vector.Mag(S)	
	bas=VS.launch("Base",type,faction,"unit","default",1,1,Vector.Add(loc,R),'')
	nam=GetRandomBaseName (1,faction);
	R = Vector.Scale (R,(RMag+2.0*bas.rSize())/RMag)
	S = Vector.Scale (S,(SMag+2.0*bas.rSize())/SMag)	
	bas.orbit (unit,orbitspeed,R,S,(0.0,0.0,0.0))
	
	dynamic_universe.TrackLaunchedShip (BaseFGInSystemName(VS.getSystemFile()),
										faction,
										type,
										bas)
def launchSingleBase (type,faction,sig):
	radpct = VS.getPlanetRadiusPercent()
	radpct = sig.rSize()*(1+radpct)
	speed = vsrandom.uniform (0,50)
	launchBaseOrbit (type,faction,(0,0,0),radpct,speed,sig)
def launchBaseStuck (type,faction):
	un=VS.getPlayer()
	maxspeed=100.1
	if (un):
		maxspeed=un.maxAfterburnerSpeed()+30.1
	un.setNull();
	launchBaseOrbit (type,faction,un.Position(),maxspeed*180,0,un)
def launchBase (type,num,faction,system,sig_units,numfighters):
	import seedrandom
	print 'launching base '+ type
	seedrandom.seed(seedrandom.seedstring(seedrandom.interleave(['type',
																 'faction',
																 'system'])))
	if (len(sig_units)):
		for i in range (num):
			one=seedrandom.rand()
			two=seedrandom.rand()
			three=seedrandom.rand()
			indices = [one%len(sig_units),
					   two%len(sig_units),
					   three%len(sig_units)];
			which = minIndex(numfighters,indices)
			if (sig_units[which].isJumppoint()):
				numfighters[which]+=20
			else:
				numfighters[which]+=1
			launchSingleBase (type,faction,sig_units[which])
	else:
		for i in range(num):
			launchBaseStuck(type,faction)
def zeros (le):
	shipcount=[];
	for i in range(le): shipcount+=[0];
	return shipcount
def launchBases(sys):
	import universe
	print 'launching bases for '+sys
	fac = VS.GetGalaxyFaction(sys)
	fgs = BaseFG (fac,sys)
	sig_units = universe.significantUnits()
	shipcount=zeros(len(sig_units))	
	for fg in fgs:
		launchBase(fg[0],fg[1],fac,sys,sig_units,shipcount)
def GetShipsInFG(fgname,faction):
	import vsrandom
	ships = ReadStringList (ccp,MakeFGKey(fgname,faction))
	if (len(ships)<=ShipListOffset()):
		return []
	try:
		count=int(ships[0])
	except:
		print 'bad flightgroup record '+ships
	launchnum = vsrandom.randrange(1,6)
	if (launchnum>count):
		launchnum=count
	ret = []
	for num in range(ShipListOffset(),len(ships),PerShipDataSize()):
		curnum=int(ships[num+2])
		cnum = _prob_round(curnum*float(launchnum)/count)
		if (cnum>0):
			ret+=[(ships[num],cnum)]
	return ret

def LaunchLandShip(fgname,faction,typ,numlaunched=1):
	key = MakeFGKey (fgname,faction)
	ships=ReadStringList (ccp,key)
	for num in range (ShipListOffset(),len(ships),PerShipDataSize()):
		if (typ == ships[num]):
			try:
				ntobegin=int(ships[num+1])
				nactive=int(ships[num+2])
				nactive-=numlaunched
				if (nactive<0):
					nactive=0
					print 'error more ships launched than in FG '+fgname
				if (nactive>ntobegin):
					nactive=ntobegin
					print 'error ships '+typ+'landed that never launched'
				Director.putSaveString(ccp,key,num+2,str(nactive))
			except:
				print 'error in FG data (str->int)'
def LaunchShip (fgname,faction,typ,num=1):
	LaunchLandShip (fgname,faction,typ,num)
def LandShip (fgname,faction,typ,num=1):
	LaunchLandShip(fgname,faction,typ,-num)
def AllShips (faction,offset=1):
	ret=[]
	for i in AllFlightgroups (faction):
		ret+=ShipsInFG (i,faction,offset)
	return ret
def CheckAllShips(faction):
	for i in AllFlightgroups(faction):
		sys = FGSystem(i,faction)
		fgsin=AllFGsInSystem(faction,sys)
		if (not i in fgsin):
			print 'error '+str(fgsin) + i+' not in system '+ sys
def SortedAllShips (faction,offset=1):
	ret={}
	for i in AllFlightgroups (faction):
		for j in ShipsInFG(i,faction,offset):
			if j[0] in ret:
				ret[j[0]]+=j[1]
			else:
				ret[j[0]]=j[1]
	return ret
def getFgLeaderType(fgname,faction):
#	print "wah " +str(ShipsInFG(fgname,faction))
	l = ShipsInFG(fgname,faction)
	if (len(l)):
		if (len(l[0])):
			return l[0][0];
	import faction_ships
	return faction_ships.getRandomFighter(faction)
