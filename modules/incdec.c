module incdec {
  int value;
  void init (){
    value=0;
  };
  void inc(){
    value=value+1;
    _io.printf ("Incrementing %d\n",value);
  };
  void dec () {
    value=value-1;
    _io.printf ("Decrementing %d\n",value);
  };

}
