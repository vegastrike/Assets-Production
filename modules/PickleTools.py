from types import *

# '\\' is always forbidden
def addSlashes(m,forbidden="#!|\\?\"\'\r\n",extended_forbidden=1):
	def bytehex(num):
		def bytehex2(num):
			num = int(num)%256
			if num<10:
				return chr(num+ord('0'))
			else:
				return chr(num+ord('a')-10)
		return bytehex2(num/16)+bytehex2(num%16)		

	rv = ""
	for i in range(len(m)):
		quote =    (extended_forbidden and ord(m[i])>=128) \
		        or (m[i] in forbidden) \
		        or (m[i] == '\\')
		if quote:
			rv += "\\"+bytehex(ord(m[i]))
		else:
			rv += m[i]
	return rv

def stripSlashes(m):
	def hexbyte(s):
		def hexbyte2(c):
			if ( ord(c)>=ord('0') and ord(c)<=ord('9') ):
				return ord(c) - ord('0')
			else:
				return 10 + ord(c) - ord('a')
		return ( hexbyte2(s[0])*16+hexbyte2(s[1]) ) % 256
	rv = "";
	i = 0
	l = len(m)
	while (i<l):
		if (m[i]=='\\') and (i+2<l):
			rv += chr( hexbyte(m[i+1:i+3]) )
			i += 3
		else:
			rv += m[i]
			i += 1
	return rv

def encodeMap(m):
	if type(m) is DictionaryType:
		rv = ""
		for item in m.iteritems():
			if len(rv)>0:
				rv += "|"
			#recursive, in case there are nested maps
			rv += addSlashes(str(item[0])) + "#" + encodeMap(item[1])
	else:
		rv = addSlashes(str(m))
	return addSlashes(rv)

def decodeMap(m):
	m = stripSlashes(m)
	ilist = m.split('|')
	if len(ilist)==1:
		ipair = ilist[0].split('#')
		if len(ipair)==1:
			return stripSlashes(ipair[0])
		elif len(ipair)>=2:
			return { stripSlashes(ipair[0]) : decodeMap(ipair[1]) } 
		else:
			return ''
	else:
		rv = {}
		for ipair in ilist:
			ipair = ipair.split('#')
			if len(ipair)>=2:
				rv[stripSlashes(ipair[0])] = decodeMap(ipair[1])
		return rv
