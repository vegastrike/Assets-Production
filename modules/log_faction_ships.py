import math
import faction_ships
stattable={}
def lg (num):
    return math.log(1+num)/math.log(2)
for i in faction_ships.stattableexp:
    tuple = faction_ships.stattableexp[i]
    stattable[i]=(tuple[0],tuple[1],lg(tuple[2]),lg(tuple[3]),lg(tuple[4]))
    stattable[i+'.blank']=(tuple[0],tuple[1]*.5,lg(tuple[2])*.5,lg(tuple[3])*.5,lg(tuple[4])*.5)
print stattable
