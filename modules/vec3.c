module vec3 {

  import random;

  void print(object v3){
    float x=_olist.at(v3,0);
    float y=_olist.at(v3,1);
    float z=_olist.at(v3,2);
    
    _io.printf("[ %f , %f , %f ]",x,y,z);
  };

  object string(object v3){
    float x=_olist.at(v3,0);
    float y=_olist.at(v3,1);
    float z=_olist.at(v3,2);
    
    object my_out=_string.new();
    _io.sprintf(my_out,"[ %f , %f , %f ]",x,y,z);
    return my_out;
  };


  object new(float x,float y,float z){
    object v3=_olist.new();

    _olist.push_back(v3,x);
    _olist.push_back(v3,y);
    _olist.push_back(v3,z);

    return v3;
  };
  void set(object v3,float x,float y,float z){
    _olist.set(v3,0,x);
    _olist.set(v3,1,y);
    _olist.set(v3,2,z);
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

    object ret=random_around_area(ppos,r1,r2);

    _olist.delete(ppos);
    return ret;
  };

  object ahead_of_player(float r1,float r2){
    object player_unit=_unit.getPlayer();
    object ppos=_unit.getPosition(player_unit);

    object vel=_unit.getVelocity(player_unit);

    float distance=random.random(r1,r2);

    _io.printf("ppos="); print(ppos);
    _io.printf("\nvel="); print(vel);
    _io.printf("\ndistance=%f\n",distance);

    scale(vel,distance);

    _io.printf("vel2="); print(vel);

    add(ppos,vel);
    
    _io.printf("\nppos="); print(ppos);

    _olist.delete(vel);

    return ppos;
  };

  void scale(object vec,float factor){
    float x=_olist.at(vec,0);
    float y=_olist.at(vec,1);
    float z=_olist.at(vec,2);

    x=x*factor;
    y=y*factor;
    z=z*factor;

    set(vec,x,y,z);
  };

  object clone(object vec){
    float x=_olist.at(vec,0);
    float y=_olist.at(vec,1);
    float z=_olist.at(vec,2);

    object ret=new(x,y,z);

    return ret;
  };

  void add(object vec1,object vec2){
    float x=_olist.at(vec1,0);
    float y=_olist.at(vec1,1);
    float z=_olist.at(vec1,2);

    float a=_olist.at(vec2,0);
    float b=_olist.at(vec2,1);
    float c=_olist.at(vec2,2);

    x=x+a;
    y=y+b;
    z=z+c;

    set(vec1,x,y,z);

  };



}
