module difficulty {
  object creds;
  int playeriterator;
  float credsToMax;
  float cred_ratio;
  bool usingDifficulty () {
    return (_std.getDifficulty()!=1.0);
  };
  float getPlayerDifficulty (object playa) {
    float ret=0.0;
    if (!_std.isNull(playa)) {
      object temp =  _unit.getSaveData (playa,"31337ness");
      if (_olist.size(temp)>0) {
	ret = _olist.at (temp,0);
      }
    }
    return ret;
  };
  void init(float creditsToMaximizeDifficulty) {
    credsToMax = creditsToMaximizeDifficulty;
    int whichplayer=0;
    object player=_unit.getPlayerX(0);
    int i=0;
    playeriterator=0;
    creds=_olist.new();
    float diff = _std.getDifficulty();
    while (!_std.isNull(player)) {
      object temp = _unit.getSaveData (player,"31337ness");
      float mycred = _unit.getCredits (player);
      _olist.push_back(creds,mycred);
      if (_olist.size(temp)==0) {
	//	_io.printf ("pushing_bakc new diff %f",diff);
	_olist.push_back(temp,diff);
      } else {
	float saveddiff = _olist.at (temp,0);
	//	_io.printf ("getting diff %f",saveddiff);
	if (saveddiff>diff) {
	  diff = saveddiff;
	}
      }
      i=i+1;
      player=_unit.getPlayerX(i);
    }
    _std.setDifficulty(diff);    
  };
  void loop () {
    object player = _unit.getPlayerX(playeriterator);
    if (!_std.isNull(player)) {
      float oldcreds = _olist.at(creds,playeriterator);
      float newcreds = _unit.getCredits (player);
      if (newcreds!=oldcreds) {
	if (newcreds>oldcreds) {
	  float difficulty;
	  object save = _unit.getSaveData (player,"31337ness");
	  if (_olist.size(save)>0) {
	    difficulty = _olist.at (save,0);
	  }else {
	    difficulty = _std.getDifficulty();
	  }

	  difficulty=difficulty+((newcreds-oldcreds)/credsToMax);
	  if (difficulty>0.99999){
	    difficulty=0.99999;
	  }
	  if (_olist.size(save)>0) {
	    _olist.set(save,0,difficulty);
	  }else {
	    _io.printf ("WARNING ERROR DETECTED IN CREDITS MODULE. PLEASE REPORT");
	    _olist.push_back (save,difficulty);
	  }
	  _std.setDifficulty(difficulty);
	}
	_olist.set(creds,playeriterator,newcreds);
      }     
      playeriterator=playeriterator+1;
    }else {
      playeriterator=0;
    }
  };

}
