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
	for i in range (lentup,s_size)):
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
	for i in range (len(tup)-1)
		fina+='|'+tup[i]
	return fina

class dynamicuniverse:

	def _MakeFGString (self,starsystem,typenumlist):
		totalships = 0
		ret = []
		damage=0
		for tt in numtypelist:
			totalships+=int(tt[1])
			strlist+=[str(tt[0]),str(tt[1])]
		return [str(totalships),str(starsystem),str(damage)]+strlist

	def _AddShiptoKnownFG(self,key,tn):
		len = Director.getSaveStringLength (self.cp,key)
		try:
			numtotships =int(Director.getSaveString(self.cp,key,0))
			numtotships+=int(tn[1])
			Director.putSaveString(self.cp,key,0,str(numtotships))
		except:
			print 'error adding ship to flightgroup'
		for i in range (ShipListOffset+1,len,2):
			if (Director.getSaveString(self.cp,key,i-1)==str(tn[0])):
				numships=0
				try:
					numships+= int(tn[1])
					numships+= int (Director.getSaveString(self.cp,key,i))
				except:
					pass
				Director.putSaveString(self.cp,key,i,str(numships))
				return
		Director.pushSaveString(self.cp,key,str(tn[0]))
		Director.pushSaveString(self.cp,key,str(tn[1]))

	def _AddFGToSystem (self,fgname,faction,starsystem):
		key = MakeStarSystemFGKey (starsystem)
		len = Director.getSaveStringLength (self.cp,key)
		index = VS.getFactionIndex (faction)
		if (len>index):
			st=Director.getSaveString (self.cp,key,index)
			if (len(st)>0):
				st+='|'
			Director.putSaveString(self.cp,key,index,st+fgname)
		else:
			for i in range (len,index):
				Director.pushSaveString(self.cp,key,'')
			Director.pushSaveString(self.cp,key,fgname)

	def _RemoveFGFromSystem (self,fgname,faction,starsystem):
		key = MakeStarSystemFGKey( starsystem)
		len = Director.getSaveStringLength(self.cp,key)
		index = VS.getFactionIndex(faction)
		if (len>index):
			tup = Director.getSaveString (self.cp,key,index).split('|')
			try:
				del tup[tup.index(fgname)]
				Director.putSaveString(self.cp,key,index,ListToPipe(tup))			
			except:
				print 'fg '+fgname+' not found in '+starsystem
		else:
			print 'no ships of faction '+faction+' in '+starsystem

	def _AddFGToFactionList(self,fgname,faction):
		key = MakeFactionKey(faction)
		Director.pushSaveString (self.cp,key,fgname)
	def _RemoveFGFromFactionList (self,fgname,faction):
		key = MakeFactionKey(faction)
		Director.getSaveStringLength()
		#FIXME
	def DeleteFlightgroup(self,fgname,faction):
		key = MakeFGKey (fgname,faction)
		len = Director.getSaveStringLength (self.cp,key)
		if (len>=ShipListOffset()):
			starsystem=Director.getSaveString(self.cp,key,1)
			self._RemoveFGFromSystem(starsystem)
			self._RemoveFGFromFactionList(fgname,faction)
	def AddShipsToFG (self,fgname,faction,typenumbertuple,starsystem):
		key = MakeFGKey(fgname,faction)	
		len = Director.getSaveStringLength (self.cp,key)
		if (len<ShipListOffset()):
			WriteStringList(self.cp,key,self._MakeFGString( starsystem,typenumbertuple) )
			self._AddFGToSystem (fgname,faction,starsystem)
			self._AddFGToFactionList (fgname,faction)
		else:
			for tn in typenumbertuple:
				self._AddShipToKnownFG(key,tn)
		
	def RemoveShipFromFG (self,fgname,faction,type):
		key = MakeFGKey (fgname,faction)
		len = Director.getSaveStringLength (self.cp,key)
		for i in range (ShipListOffset+1,len,2):
			if (Director.getSaveString(self.cp,key,i-1)==str(type)):
				numships=0
				try:
					numships = int (Director.getSaveString (self.cp,key,i))
				except:
					pass
				if (numships>0):
					numships-=1
					Director.putSaveString (self.cp,key,i,str(numships))
				else:
					Director.eraseSaveString(self.cp,key,i)
					Director.eraseSaveString(self.cp,key,i-1)
		print 'cannot find ship to delete in '+faction+' fg ' + fgname
