module vec3 {

  object new(float x,float y,float z){
    object v3=_olist.new();

    _olist.push_back(v3,x);
    _olist.push_back(v3,y);
    _olist.push_back(v3,z);

    return v3;
  };
}
