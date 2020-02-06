import sys

def methodtype(a,b,c):
    return a.__get__(b, c)
