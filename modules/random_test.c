module random_test {

  import random;

  void test(){
    int i=random.randomint(0-3,6);
    
    if(i>6){
      _io.printf("ERRROR\n");
    }
    _io.printf("random_test: %d\n",i);
  };
}
