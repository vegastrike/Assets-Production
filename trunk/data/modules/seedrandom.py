_seed=0
RAND_MAX = 0x7fffffff
aye = ord('a')
AAYE= ord('A')
Uhun= ord('0')
totalnormchar=26+26+10
def getNumFromChar(c):
    global aye,AAYE, Uhun
    charnum=ord(c)
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
        num*=totalnormchar
        num = num % RAND_MAX
    return num
def interleave (slist):
    touch=1
    index=0
    rez=''
    while (touch):
        touch=0
        for s in slist:
            if len(s)>index:
                touch=1
                rez+=s[index]
        index+=1
    return rez
_seed=0
def rands(intseed):
    global RAND_MAX
    intseed = int(intseed) * 1103515245 + 12345
    intseed = intseed % RAND_MAX
    return intseed
def rand():
    global _seed
    _seed = rands (_seed)
    return _seed
def seed (seednum):
    global _seed
    _seed = seednum
