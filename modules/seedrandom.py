_seed=0
RAND_MAX = 0x7fffffff
def getallchar ():
    rez = ""
    for i in range(256):
        rez += "%c"% i
    return rez
allchar = getallchar()
aye = allchar.find('a')
AAYE= allchar.find('A')
Uhun= allchar.find('0')
totalnormchar=26+26+10
def getNumFromChar(c):
	global allchar,aye,AAYE, Uhun
	charnum=allchar.find(c)
	if (charnum-aye<26):
		charnum = charnum-aye
	else:
		if (charnum-AAYE<26):
			charnum = charnum-AAYE+26
		else:
			if (charnum-Uhun<10):
				charnum = charnum-Uhun+26+26
	return charnum
def seedstring (stru):
	num=0
	l=len (stru)
	for i in range(l):
		global totalnormchar,RAND_MAX
		num+=getNumFromChar(stru[l-i-1])
		num*=totalnormchar;
		num = num % RAND_MAX
		try:
			num = int(num)
		except:
			print 'warning'
	return num
def interleave (slist):
	touch=True
	index=0
	rez=''
	while (touch):
		touch=False
		for s in slist:
			if len(s)>index:
				touch=True
				rez+=s[index]
		index+=1
	return rez
_seed=0	
def rands(intseed):
	global RAND_MAX
	intseed = ( intseed * 1103515245 + 12345)
	intseed = intseed %RAND_MAX
	try:
		intseed=int(intseed)
	except:
		return intseed
	return intseed
def rand():
	global _seed
	_seed = rands (_seed)
	return _seed
def seed (seednum):
	global _seed
	_seed = seednum
