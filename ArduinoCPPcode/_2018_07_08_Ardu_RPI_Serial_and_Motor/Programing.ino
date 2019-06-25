void PROG_params_INIT(int _prog_num) {
  int i, i1;
  if (!(_prog_num == -1)) {
    for (i1 = 0; i1 < STEPS; i1++) {
      PROG_params[_prog_num][i1][0] = -1;
    }
  } else {
    for (i = 0; i < NUM_OF_PROGS; i++) {
      for (i1 = 0; i1 < STEPS; i1++) {
        PROG_params[i][i1][0] = -1;
      }
    }
  }
}

void Prog_write(int _prog_num, int _prog_step, int _params[], int _param_size) {
  int i = 0;
  for (i = 0; i < _param_size; i++) {
    PROG_params[_prog_num][_prog_step][i] = _params[i];
  }
  Prog_show(_prog_num, _param_size, _prog_step);
}

void Prog_show(int _prog_num, int _param_size, int _show_step) {
  int i1, i2 = 0;
  int _step_count = 0;
  char _tmp_str[100];

  strcpy (_tmp_str, "");

  if (!_show_step == 0) {
    Prog_str(_prog_num, _show_step, _tmp_str);
    //Serial.print(_tmp_str);
    //Serial.println();

  } else {
    RPISerial.print("\n");
    for (i2; i2 < STEPS; i2++) {
      //Serial.print("i2:"); Serial.print(i2);
      if (PROG_params[_prog_num][i2][0] == -1) break;
      Prog_str(_prog_num, i2, _tmp_str);
      strcat(_tmp_str, "\n");
      //Serial.print(_tmp_str);
      //RPISerial.print(_tmp_str);
    }
  }
}

void Prog_run(int _prog_num, int _param_size) {
  int i1, i2 = 0;
  char _tmp_str[100];
  //Serial.print("freeMemory()=");
  //Serial.println(freeMemory());
  Serial.println(F("--- PROG RUN ---"));
  for (i2 = 0; i2 < STEPS; i2++) {
    if (PROG_params[_prog_num][i2][0] == -1) break;
    Prog_str(_prog_num, i2, _tmp_str);
    //Serial.print(_tmp_str);
    if (PROG_params[_prog_num][i2][0] == 98) {
      Set_accel_vel_pulse(PROG_params[_prog_num][i2][1], PROG_params[_prog_num][i2][2], PROG_params[_prog_num][i2][3], false);
    }
    else {
      do_step(PROG_params[_prog_num][i2][0], PROG_params[_prog_num][i2][1], PROG_params[_prog_num][i2][2], true);
    }
    //Serial.println();
  }
  RPISerial.print(F("PROG_DONE"));

}

void Prog_str (int _prog_num, int _step, char* _tmp_str) {
  char _buf[100];
  int i;

  strcpy(_tmp_str, "");
  strcat(_tmp_str, "\tPROG_params["); strcat(_tmp_str, itoa(_prog_num, _buf, 10)); strcat(_tmp_str, "]");
  strcat(_tmp_str, "["); strcat(_tmp_str, itoa(_step, _buf, 10)); strcat(_tmp_str, "]=");
  for (i = 0; i < NUM_OF_PARAM; i++) {
    strcat(_tmp_str, itoa(PROG_params[_prog_num][_step][i], _buf, 10)); strcat(_tmp_str, ",");
  }
  _tmp_str[strlen(_tmp_str) - 1] = '\0'; //delete last ","
}
