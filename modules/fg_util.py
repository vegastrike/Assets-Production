import Director
import VS
def MakeFactionKey (faction):
	return 'FG:'+str(VS.getFactionIndex(faction))
def MakeFGKey (fgname,faction):
	return 'FG:'+str(fgname)+'|'+str(VS.getFactionIndex(faction))
def MakeStarSystemFGKey (starsystem):
	return 'FG:'+str(starsystem)
def ShipListOffset ():
	return 3

def GetRandomFGNames (numflightgroups):
	rez=[]
	for i in range (numflightgroups):
		rez.append(str(i))
	return rez
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
	siz = getSaveStringLength (cp,key)
	s_size=siz;
	lentup= len(tup)
	if (lentup<size):
		siz=lentup
	for i in range(siz):
		putSaveString(cp,key,i,tup[i])
	for i in range (s_size,lentup):
		pushSaveString(cp,key,tup[i])
	for i in range (lentup,s_size):
		eraseSaveString(cp,key,lentup)
def ReadStringList (cp,key):
	siz = getSaveStringLength (cp,key)
	tup =[]
	for i in range (siz):
		tup += [getSaveString(cp,key,i)]
	return tup

def ListToPipe (tup):
	fina=''
	if (len(tup)):
		fina=tup[0]
	for i in range (len(tup)-1):
		fina+='|'+tup[i]
	return fina

	def _MakeFGString (starsystem,typenumlist):
		totalships = 0
		ret = []
		damage=0
		for tt in numtypelist:
			totalships+=int(tt[1])
			strlist+=[str(tt[0]),str(tt[1])]
		return [str(totalships),str(starsystem),str(damage)]+strlist

	def _AddShiptoKnownFG(key,tn):
		leg = Director.getSaveStringLength (dynamic_universe.cp,key)
		try:
			numtotships =int(Director.getSaveString(dynamic_universe.cp,key,0))
			numtotships+=int(tn[1])
			Director.putSaveString(dynamic_universe.cp,key,0,str(numtotships))
		except:
			print 'error adding ship to flightgroup'
		for i in range (ShipListOffset+1,leg,2):
			if (Director.getSaveString(dynamic_universe.cp,key,i-1)==str(tn[0])):
				numships=0
				try:
					numships+= int(tn[1])
					numships+= int (Director.getSaveString(dynamic_universe.cp,key,i))
				except:
					pass
				Director.putSaveString(dynamic_universe.cp,key,i,str(numships))
				return
		Director.pushSaveString(dynamic_universe.cp,key,str(tn[0]))
		Director.pushSaveString(dynamic_universe.cp,key,str(tn[1]))

	def _AddFGToSystem (fgname,faction,starsystem):
		key = MakeStarSystemFGKey (starsystem)
		leg = Director.getSaveStringLength (dynamic_universe.cp,key)
		index = VS.getFactionIndex (faction)
		if (leg>index):
			st=Director.getSaveString (dynamic_universe.cp,key,index)
			if (len(st)>0):
				st+='|'
			Director.putSaveString(dynamic_universe.cp,key,index,st+fgname)
		else:
			for i in range (leg,index):
				Director.pushSaveString(dynamic_universe.cp,key,'')
			Director.pushSaveString(dynamic_universe.cp,key,fgname)

		
	def _RemoveFGFromSystem (fgname,faction,starsystem):
		key = MakeStarSystemFGKey( starsystem)
		leg = Director.getSaveStringLength(dynamic_universe.cp,key)
		index = VS.getFactionIndex(faction)
		if (leg>index):
			tup = Director.getSaveString (dynamic_universe.cp,key,index).split('|')
			try:
				del tup[tup.index(fgname)]
				Director.putSaveString(dynamic_universe.cp,key,index,ListToPipe(tup))			
			except:
				print 'fg '+fgname+' not found in '+starsystem
		else:
			print 'no ships of faction '+faction+' in '+starsystem

	def _AddFGToFactionList(fgname,faction):
		key = MakeFactionKey(faction)
		Director.pushSaveString (dynamic_universe.cp,key,fgname)
			

	def _RemoveFGFromFactionList (fgname,faction):
		key = MakeFactionKey(faction)
		lun=Director.getSaveStringLength(dynamic_universe.cp,key)
		for i in range (lun):
			if (Director.getSaveString(dynamic_universe.cp,key,i)==fgname):
				Director.eraseSaveString(dynamic_universe.cp,key,i)
				return 1
		return 0

	def CheckFG (fgname,faction):
		key = MakeFGKey (fgname,faction)
		leg = VS.getSaveStringLength (dynamic_universe.cp,key)
		totalships=0
		try:
			for i in range (ShipListOffset+1,leg,2):
				totalships+=int(VS.getSaveString(dynamic_universe.cp,key,i))
			if (totalships!=int(VS.getSaveString(dynamic_universe.cp,key,0))):
				print 'mismatch on flightgroup '+fgname+' faction '+faction
				return 0
		except:
			print 'nonint readingo n flightgroup '+fgname+'faction '+faction
			return 0
		return 1
	def PurgeZeroShips (faction):
		key=MakeFactionKey(faction)
		for i in range (VS.getSaveStringLength (dynamic_universe.cp,key)):
			curfg=VS.getSaveString(dynamic_universe.cp,key,i)
			CheckFG (curfg,faction)
			numships=NumShipsInFG(curfg,faction)
			if (numships==0):
				DeleteFG(curfg,faction)
			
	def NumShipsInFG (fgname,faction):
		key = MakeFGKey (fgname,faction)
		len = Director.getSaveStringLength (dynamic_universe.cp,key)
		if (len==0):
			return 0
		else:
			try:
				return int(Director.getSaveString(dynamic_universe.cp,key,0))
			except:
				print 'fatal: flightgroup without size'
	def DeleteFG(fgname,faction):
		key = MakeFGKey (fgname,faction)
		len = Director.getSaveStringLength (dynamic_universe.cp,key)
		if (len>=ShipListOffset()):
			starsystem=Director.getSaveString(dynamic_universe.cp,key,1)
			_RemoveFGFromSystem(starsystem)
			_RemoveFGFromFactionList(fgname,faction)
			WriteStringList (dynamic_universe.cp,MakeFGKey(fgname,faction),[] )
	def AddShipsToFG (fgname,faction,typenumbertuple,starsystem):
		key = MakeFGKey(fgname,faction)	
		len = Director.getSaveStringLength (dynamic_universe.cp,key)
		if (len<ShipListOffset()):
			WriteStringList(dynamic_universe.cp,key,_MakeFGString( starsystem,typenumbertuple) )
			_AddFGToSystem (fgname,faction,starsystem)
			_AddFGToFactionList (fgname,faction)
		else:
			for tn in typenumbertuple:
				_AddShipToKnownFG(key,tn)
		
	def RemoveShipFromFG (fgname,faction,type):
		key = MakeFGKey (fgname,faction)
		leg = Director.getSaveStringLength (dynamic_universe.cp,key)
		for i in range (ShipListOffset+1,leg,2):
			if (Director.getSaveString(dynamic_universe.cp,key,i-1)==str(type)):
				numships=0
				try:
					numships = int (Director.getSaveString (dynamic_universe.cp,key,i))
				except:
					pass
				if (numships>0):
					numships-=1
					Director.putSaveString (dynamic_universe.cp,key,i,str(numships))
				else:
					Director.eraseSaveString(dynamic_universe.cp,key,i)
					Director.eraseSaveString(dynamic_universe.cp,key,i-1)
		print 'cannot find ship to delete in '+faction+' fg ' + fgname
