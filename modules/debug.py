import traceback
import sys

debugnum=0

class VSException(Exception):
	pass


def _info(msg): # == /dev/null
	pass

def prettyfile(fil):
	lasttwo=str(fil).split('/')[-2:]
	if len(lasttwo)<2: return fil
	return lasttwo[0][0]+'/'+lasttwo[1]

def _debug(msg): # Simple line number
	laststack = traceback.extract_stack()[-2]
	print ' +++ '+prettyfile(laststack[0])+':'+str(laststack[1])+': '+str(msg)


def _warn(msg): # Traceback without killing the script
	global debugnum
	debugnum+=1
	print " *** Python Warning "+str(debugnum)+"!"
	sys.stderr.write('Warning Traceback '+str(debugnum)+':\n')
	for frame in traceback.extract_stack()[:-1]:
		sys.stderr.write('  File "'+prettyfile(frame[0])+'", line '+str(frame[1]))
		sys.stderr.write(', in '+str(frame[2])+'\n    '+str(frame[3])+'\n')
	sys.stderr.write('Message: '+str(msg)+'\n\n')

def _fatal(msg): # Kill the script!
	global debugnum
	debugnum+=1
	print "Python VSException "+str(debugnum)+"!"
	raise VSException(msg)

fatal = _fatal # Really bad error... Kill the script.  Same as a call to raise()

warn = _warn   # Anything that shouldn't happen, but shouldn't cause a crash either.
error = _warn  # Different name for the same thing.

# Less important messages that happen a lot.
debug = _debug # Useful messages for hunting down bugs, or loading status.
info = _info   # I don't think this is useful, but why not?

# For release, we can disable unimportant messages:
debug = _info


