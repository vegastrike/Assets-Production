class difficulty:
  creds
  playeriterator
  credsToMax
  cred_ratio
  def usingDifficulty ():
    return (VS.getDifficulty()!=1.0)
  
  def getPlayerDifficulty (playa):
    ret=0.0
    if (playa):
      temp =  VS.getSaveData (playa,"31337ness") #???
      if (len(temp)>0):
	ret = _olist.at (temp,0)
      
    
    return ret
  
  def init(creditsToMaximizeDifficulty):
    credsToMax = creditsToMaximizeDifficulty
    whichplayer=0
    player=_unit.getPlayerX(0)
    i=0
    playeriterator=0
    creds=_olist.new()
    diff = _std.getDifficulty()
    while (!_std.isNull(player)):
      temp = _unit.getSaveData (player,"31337ness")
      mycred = _unit.getCredits (player)
      _olist.push_back(creds,mycred)
      if (_olist.size(temp)==0):
	//	_io.printf ("pushing_bakc new diff %f",diff)
	_olist.push_back(temp,diff)
       else:
	saveddiff = _olist.at (temp,0)
	//	_io.printf ("getting diff %f",saveddiff)
	if (saveddiff>diff):
	  diff = saveddiff
	
      
      i=i+1
      player=_unit.getPlayerX(i)
    
    _std.setDifficulty(diff)    
  
  def loop ():
    player = _unit.getPlayerX(playeriterator)
    if (!_std.isNull(player)):
      oldcreds = _olist.at(creds,playeriterator)
      newcreds = _unit.getCredits (player)
      if (newcreds!=oldcreds):
	if (newcreds>oldcreds):
	  difficulty
	  save = _unit.getSaveData (player,"31337ness")
	  if (_olist.size(save)>0):
	    difficulty = _olist.at (save,0)
	  else:
	    difficulty = _std.getDifficulty()
	  

	  difficulty=difficulty+((newcreds-oldcreds)/credsToMax)
	  if (difficulty>0.99999):
	    difficulty=0.99999
	  
	  if (_olist.size(save)>0):
	    _olist.set(save,0,difficulty)
	  else:
	    _io.printf ("WARNING ERROR DETECTED IN CREDITS MODULE. PLEASE REPORT")
	    _olist.push_back (save,difficulty)
	  
	  _std.setDifficulty(difficulty)
	
	_olist.set(creds,playeriterator,newcreds)
           
      playeriterator=playeriterator+1
    else:
      playeriterator=0
    
  


