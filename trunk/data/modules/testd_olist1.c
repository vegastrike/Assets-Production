module testd_olist1 {

  object list_of_lists;
  float nr_of_lists,max_nr_lists;

 void loop(){
    float counter;
    object new_list;

    counter=_std.Rnd()*20.0;

    _io.PrintFloats(:s1="creating a list with "; :s2=" numbers"; counter);

    new_list=fill_list(counter);

    _io.PrintFloats(:s1="before pushback in listoflists";);

    _olist.push_back(list_of_lists,new_list);

    _io.PrintFloats(:s1="before print_list";);

    print_list(list_of_lists);

    nr_of_lists=nr_of_lists+1.0;

    if(nr_of_lists>max_nr_lists){
      float i;
      object sublist;
      i=0.0;

      while(i<max_nr_lists){
	_io.PrintFloats(:s1="subList nr. "; i);
	sublist=_olist.at(list_of_lists,i);
	_olist.toxml(sublist);
	i=i+1.0;
      }
    }
  };

  void init_list(){
    _io.PrintFloats(:s1="initializing list of lists";);
    list_of_lists=_olist.new();
    nr_of_lists=0.0;
    max_nr_lists=10.0;
  };

  void print_list(object list){
    _io.PrintFloats(:s1="List of Lists:";);
    _olist.toxml(list);
  };

  object fill_list(float counter){
    object list;
    list=_olist.new();
    //_io.PrintFloats(:s1="after init";);

    float  i;
    i=0.0;
    while(i<counter){
      float tmp;
      tmp=_std.Rnd();
      _olist.push_back(list,tmp);
      i=i+1.0;
      //_io.PrintFloats(:s1="end of while";);
    }

    // _io.PrintFloats(:s1="after while";);
    _olist.toxml(list);

    return list;
  };


 

}
