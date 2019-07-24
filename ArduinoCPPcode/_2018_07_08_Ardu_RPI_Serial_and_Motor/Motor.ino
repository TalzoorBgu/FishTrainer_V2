




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

void SelectMotor(unsigned int motor){
  stepper.updatePins(stp_Pin[motor], dir_Pin[motor]);
  Serial.print(F("\tMotor selected. "));   
}
