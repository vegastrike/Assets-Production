module starships_jumped_and_killed {
  //here is what the my_list var is supposed to represent
  //struct my_list {
  //olist_t olist;
  //int begin_num_ships
  //int iterator;
  //int sys_iterator;
  //};
  //init sets up a new()ed _olist with variables that it will use to track the starships...starship list must also be newed
  void init (object my_list, object starship_list) {
    _olist.push_back (my_list,starship_list);
    int size =_olist.size(starship_list)
    _olist.push_back (my_list,size);
    _olist.push_back (my_list,0);
    _olist.push_back (my_list,0);
    
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
  void loop (object my_list) {
    object starship_list = _olist.at (my_list,0);//pointer
    int begin_num_ships = _olist.at (my_list,1);//constant
    int iterator = _olist.at (my_list,2);
    int sys_iterator = _olist.at (my_list,3);
    _olist.pop_back (my_list);
    _olist.pop_back (my_list);
    //don't pop begin_num_ships...taht doesn't change
    if (iterator<_olist.size(starship_list)) {
      sys_iterator = scan_for (sys_iterator, _olist.at (starship_list,iterator));
      if (sys_iterator==0) {//if we've been through all the starships
	iterator=iterator+1;
      }
    }else {
      iterator=0;
    }
    //don't push begin_num_ships...that wasn't popped
    _olist.push_back (iterator);
    _olist.push_back (sys_iterator);

  };
}
