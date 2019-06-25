void translate_str(char* _str, int _str_len, int arry[], int siz)
{
  // arry[0]:
  //        1 = move, 10 = moveto, 20 = delay, 50 = start program mode, 51 = end program
  char _tmp_str[4][14];
  char buf[_str_len + 1];
  int len;
  char *p = _str;
  char *split_str;
  int i;

  for (i = 0; i < (siz + 1); i++) {
    arry[i] = 0;
    strcpy(_tmp_str[i], "\0");
  }


  i = 0;
  split_str = strtok_r(p, ",", &p);

  while (split_str != NULL) { // delimiter is the semicolon
    strcpy(_tmp_str[i], split_str);
    int len_tmp_str = strlen(_tmp_str[i]);
    char last_char = _tmp_str[i][len_tmp_str - 1];

    if (last_char == '\n') _tmp_str[i][len_tmp_str - 1] = '\0';
    i++;
    split_str = strtok_r(p, ",", &p);
  }

  /*for (i = 0; i < 3; i++) {
    Serial.print(i); Serial.print("\t->"); Serial.print(_tmp_str[i]); Serial.println("<-");
    }*/

  if (!strcmp(_tmp_str[0], "move")) {
    //Serial.println("[move]");
    arry[0] = 1;
  } else if (!strcmp(_tmp_str[0], "moveto")) {
    //Serial.println("[moveto]");
    arry[0] = 10;
  } else if (!strcmp(_tmp_str[0], "delay")) {
    //Serial.println("[moveto]");
    arry[0] = 20;
  } else if (!strcmp(_tmp_str[0], "def_v_a")) {
    //Serial.println("[define_vel_acc]");
    arry[0] = 98;
  } else if (!strcmp(_tmp_str[0], "def_dflt_v_a")) {
    //Serial.println("[define_vel_acc]");
    arry[0] = 99;
  } else if (!strcmp(_tmp_str[0], "in_s_motor_1")) {
    arry[0] = 991;
  } else if (!strcmp(_tmp_str[0], "in_s_motor_2")) {
    arry[0] = 992;
  } else if (!strcmp(_tmp_str[0], "s_motor")) {
    arry[0] = 990;
  } else if (!strcmp(_tmp_str[0], "p_start")) {
    Serial.print(F("\tprograming start"));
    arry[0] = 50;
  } else if (!strcmp(_tmp_str[0], "p_end")) {
    Serial.print(F("\tprograming end"));
    arry[0] = 51;
  } else if (!strcmp(_tmp_str[0], "show_prog")) {
    arry[0] = 52;
  } else if (!strcmp(_tmp_str[0], "run_prog")) {
    arry[0] = 58;
  } else if (!strcmp(_tmp_str[0], "dis_pins")) {
    arry[0] = 980;
  } else if (!strcmp(_tmp_str[0], "en_pins")) {
    arry[0] = 981;
  }

  
  

  //Serial.print(F("_tmp_str[1]=")); Serial.println(_tmp_str[1]);
  //Serial.print(F("isNumeric(_tmp_str[1])=")); Serial.println(isNumeric(_tmp_str[1]));
  //Serial.print(F("atol(_tmp_str[1])=")); Serial.println(atol(_tmp_str[1]));
  short int _tmp_size;
  _tmp_size = strlen(_tmp_str[1]);

  if (isNumeric(_tmp_str[1], _tmp_size)) {
    arry[1] = atol(_tmp_str[1]);
  }

  _tmp_size = strlen(_tmp_str[2]);
  if (!strcmp(_tmp_str[2], "L")) arry[2] = 10;
  else if (!strcmp(_tmp_str[2], "R")) arry[2] = 11;
  else if (isNumeric(_tmp_str[2], _tmp_size)) arry[2] = atoi(_tmp_str[2]);


  _tmp_size = strlen(_tmp_str[3]);
  if (isNumeric(_tmp_str[3], _tmp_size)) {
    arry[3] = atoi(_tmp_str[3]);
  }

}
/*
void add_space_before(char* _str, int _str_size, int _final_str_size) {
  int i = _final_str_size;
  char _tmp_str[_final_str_size];
  //Serial.print(F("_str=#")); Serial.print(_str); Serial.println(F("#"));
  for (i; i >= 0; i--) {
    if (_str_size >= 0) {
      _tmp_str[i] = _str[_str_size];
      _str_size--;
    } else {
      _tmp_str[i] = ' ';
    }
    //Serial.print(F("i:")); Serial.print(i); Serial.print(F("=(")); Serial.print(_tmp_str[i]); Serial.print(F(")"));
  }
  _tmp_str[strlen(_tmp_str) - 1] = '\0';
  strcpy(_str, _tmp_str);
  Serial.print(F("new_str=#")); Serial.print(_str); Serial.println(F("#"));
  delay(200);

}*/

