module printf {

  void printf_test(){
    float i=1.3;

    while(i<10.0){
      _io.PrintFloats( :s1="floats: "; i );
      _io.printf("Hello world i=%f\n", 1.0 );
      i=i+1.0;
    }
  };

}
