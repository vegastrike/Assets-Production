# A collection of functions useful for dealing with flightgroup tuples.
# Added as used.
# For more information on the types of veriables used,
# see the VS python doc in the manual.

# Cloaks or uncloaks (1 or 0) a flightgroup tuple (tup).
def TfgCloak(state,tup):
	num = len(tup)
	for i in range(num):
		tup[i].Cloak(state)
		num = num + 1

# Tells us if a tup is null
def TfgisNull(tup):
	num = 0
	for i in tup:
		if (i):
			num = num + 1
	if num == 0:
		return 1
	else:
		return 0

# Returns an integer value of the number of ships in the tup.  Not sure if it takes notice of null state.
def TfgHeadCount(tup):
	num = 0
	for i in tup:
		if (i):
			num = num + 1
	return num

# Sets a whole tupled flightgroup on a target.
def setTfgDirective(tup,tgt,dir):
	num = len(tup)
	for i in range(num):
		tup[i].SetTarget(tgt)
		tup[i].setFgDirective(dir)

# Jumps a whole fg tuple using the JumpTo command.
def TfgJumpTo(tup,system):
	num = len(tup)
	for i in range(num):
		tup[i].JumpTo(system)

