




void Set_accel_vel_pulse(unsigned int _max_v, unsigned int _max_a, unsigned int _minPulseW, boolean _EEWrite) {
  stepper.setMaxSpeed(_max_v * 100);
  stepper.setAcceleration(_max_a * 100);
  stepper.setMinPulseWidth(_minPulseW);

  //Serial.println(F("Setting ok"));

  if (_EEWrite) EEVelAccelPulseWrite(_max_v, _max_a, _minPulseW);
}

void MotorPins(unsigned int motor, unsigned int _stp_pin, unsigned int _dir_pin, unsigned int _en_pin, boolean EEwrite) {  //not
  int i = 0;
  stp_Pin[motor]  = _stp_pin;
  dir_Pin[motor]  = _dir_pin;
  En_pin[motor]   = _en_pin;
  //if (motor == 1) {
  
  stepper.updatePins(stp_Pin[motor], dir_Pin[motor]);
  stepper.setEnablePin(En_pin[motor]);
  //}
  /*else if (motor == 2) {
    stepper2.updatePins(stp_Pin[motor], dir_Pin[motor]);
    stepper2.setEnablePin(En_pin[motor]);
    }*/
  if (EEwrite)
  {
//    Serial.print("Writing motor pins:"); Serial.print(stp_Pin[motor]); Serial.print(dir_Pin[motor]); Serial.print(En_pin[motor]);
    EEPinWrite(motor, stp_Pin[motor], dir_Pin[motor], En_pin[motor]);
  }
}

void SelectMotor(unsigned int _motor){
  stepper.updatePins(stp_Pin[_motor], dir_Pin[_motor]);
  Serial.print(F("\tMotor selected. "));
}

void MotorDisable(unsigned int _motor){
   SelectMotor(_motor);
   stepper.disableOutputs();
   Serial.print(F("\tMotor disabled. "));
}

void MotorEnable(unsigned int _motor){
   SelectMotor(_motor);
   stepper.enableOutputs();
   Serial.print(F("\tMotor enabled. "));
}

void StepperInit(){
  Serial.print(F("Stepper_Pin[i]=("));
  for (i = 1; i < 6; i++) {
    Serial.print(Stepper_Pins[i]);
    Serial.print(F(","));
  }
  Serial.print(Stepper_Pins[6]);
  Serial.println(")");

  for (i = 1; i < 3; i++) {
    stp_Pin[i] = Stepper_Pins[1 + (3 * (i - 1))];
    dir_Pin[i] = Stepper_Pins[2 + (3 * (i - 1))];
    En_pin[i] = Stepper_Pins[3 + (3 * (i - 1))];
    delay(2);
  }

  for (i = 1; i < 3; i++) {
    Serial.print(F("motor_")); Serial.print(i); Serial.print(F("="));
    Serial.print(stp_Pin[i]); Serial.print(F(","));
    Serial.print(dir_Pin[i]); Serial.print(F(","));
    Serial.print(En_pin[i]); Serial.print(F("\t"));
    MotorPins(i, stp_Pin[i], dir_Pin[i], En_pin[i], false);
  } Serial.println(F(" PINS: step, dir, en"));

  Serial.print(F("Max_v:")); Serial.print(max_velocity);
  Serial.print(F(", Max_a:")); Serial.print(max_accel);
  Serial.print(F(", MinPulseW:")); Serial.print(MinPulseW);
  Serial.println(F(""));
  Set_accel_vel_pulse(max_velocity, max_accel, MinPulseW, false);

  pinMode(En_pin[1], OUTPUT);
  digitalWrite(En_pin[1], LOW);

  stepper.setEnablePin(En_pin[1]);
  stepper.updatePins(stp_Pin[1], dir_Pin[1]);
  }
