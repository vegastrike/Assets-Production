module vec3 {

  object new(float x,float y,float z){
    object v3=_olist.new();

    _olist.push_back(v3,x);
    _olist.push_back(v3,y);
    _olist.push_back(v3,z);

    return v3;
  };

  object random_around_area(object pos,float r1,float r2){
    float x=_olist.at(pos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2)+(random.random(r1,r2)*random.randomsign());

    return new(x,y,z);
  };

  object random_around_player(float r1,float r2){
    object player_unit=_unit.getPlayer();
    object ppos=_unit.getPosition(player_unit);

    return random_around_area(ppos,r1,r2);
  };
}
