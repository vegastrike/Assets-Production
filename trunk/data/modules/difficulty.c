module difficulty {
  object creds;
  object saved_data;
  int playeriterator;
  float credsToMax;
  float cached_cred_difficulty;
  float cred_ratio;
  float getCredDifficulty() {
    return getPlayerCredDifficulty (_unit.getPlayer());
  };
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
  float getPlayerCredDifficulty (object playa) {
    float ret=0.0;
    if (!_std.isNull(playa)) {
      object temp =  _unit.getSaveData (playa,"31337ness");
      if (_olist.size(temp)>1) {
	ret = _olist.at (temp,1);
      }
    }
    return ret;
  };
  void init(float creditsToMaximizeDifficulty, float cred_diff, float cred_diff_ratio) {
    credsToMax = creditsToMaximizeDifficulty;
    int whichplayer=0;
    object player=_unit.getPlayerX(0);
    int i=0;
    playeriterator=0;
    saved_data = _olist.new();
    creds=_olist.new();
    float diff = _std.getDifficulty();
    cred_ratio = cred_diff_ratio;
    cached_cred_difficulty = cred_diff;
    while (!_std.isNull(player)) {
      object temp = _unit.getSaveData (player,"31337ness");
      float mycred = _unit.getCredits (player);
      _olist.push_back(creds,mycred);
      if (_olist.size(temp)==0) {
	_olist.push_back(temp,diff);
	_olist.push_back(temp,cached_cred_difficulty);
      } else {
	float saveddiff = _olist.at (temp,0);
	if (saveddiff>diff) {
	  diff = saveddiff;
	}
	if (_olist.size(temp)>1) {
	  float savedcred = _olist.at(temp,1);
	  if (savedcred>cached_cred_difficulty) {
	    cached_cred_difficulty=savedcred;
	  }
	}else {
	  _olist.push_back (temp,cached_cred_difficulty);
	}
      }
      _olist.push_back(saved_data,temp);
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
	  object save = _olist.at (saved_data,playeriterator);
       	  float difficulty = _olist.at (save,0);

	  difficulty=difficulty+((newcreds-oldcreds)/credsToMax);
	  if (difficulty>0.99999){
	    difficulty=0.99999;
	  }
	  _olist.set(save,0,difficulty);
	  _std.setDifficulty(difficulty);
	  cached_cred_difficulty = cached_cred_difficulty+cred_ratio*(newcreds-oldcreds);
	  _olist.set (save,1,cached_cred_difficulty);
	}
	_olist.set(creds,playeriterator,newcreds);
      }
      
      playeriterator=playeriterator+1;
    }else {
      playeriterator=0;
    }
  };

}
