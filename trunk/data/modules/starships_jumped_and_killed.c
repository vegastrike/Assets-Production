module starships_jumped_and_killed {
  //here is what the my_list var is supposed to represent
  //struct my_list {
  //olist_t olist;
  //int begin_num_ships
  //int iterator;
  //int sys_iterator;
  //int new_num_ships;
  //};
  //init sets up a new()ed _olist with variables that it will use to track the starships...starship list must also be newed
  void init (object my_list, object starship_list) {
    _olist.push_back (my_list,starship_list);
    int size =_olist.size(starship_list)
    _olist.push_back (my_list,size);
    _olist.push_back (my_list,0);
    _olist.push_back (my_list,0);
    _olist.push_back (my_list,size);
  };
  //frees the list and all its contents
  void destroy (object my_list) {
    object starship_list = _olist.at (my_list,0);
    int iter =0;
    while (iter<_olist.size (starship_list)) {
      object cont = _olist.at (starship_list,iter);
      _unit.deleteContainer (cont);
      iter=iter+1;
    }
    _olist.delete (starship_list);
    _olist.delete (my_list);
  };

  int scan_for (int sys_iterator,object starship_list,int iterator) {
    //
  }
  bool UnitIsNull (object starship_list,int iterator) {
    object sshipcont=_olist.at(starship_list,iterator);
    object sship=_unit.getUnitFromContainer(sshipcont);
    if (_std.isNull(sship)) {
	  _olist.erase(starship_list,iterator);
      return true;
    } else {
      return false;
    }
  }

  void loop (object my_list) {
    object starship_list = _olist.at (my_list,0);//pointer
    int begin_num_ships = _olist.at (my_list,1);//constant
    int iterator = _olist.at (my_list,2);
    int sys_iterator = _olist.at (my_list,3);
    int new_num_ships = _olist.at (my_list,4);
    _olist.pop_back (my_list);
    _olist.pop_back (my_list);
    _olist.pop_back (my_list);
    //don't pop begin_num_ships...taht doesn't change
    if (iterator<_olist.size(starship_list)) {
      
      if (UnitIsNull (starship_list,iterator)) {
	new_num_ships=new_num_ships-1;
      }else {
	sys_iterator = scan_for (sys_iterator,starship_list,iterator);
	//if it's negative one then we couldn't find it... if it's 0 we could
	if (sys_iterator==0||sys_iterator==-1) {//if we've been through all the starships
	  sys_iterator=0;
	  iterator=iterator+1;
	}
      }
    }else {
      iterator=0;
    }
    //don't push begin_num_ships...that wasn't popped
    _olist.push_back (my_list,iterator);
    _olist.push_back (my_list,sys_iterator);
    _olist.push_back (my_list,new_num_ships);

  };
}
