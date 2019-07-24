#include <EEPROMex.h>

const int maxAllowedWrites = 80;
const int memBase          = 350;

void issuedAdresses() {
  int i = 0;
  Serial.println(F("-----------------------------------"));
  Serial.println(F("Following Addresses have been issued"));
  Serial.println(F("-----------------------------------"));

  Serial.println(F("addresses \t\t size \t\t value"));
  for (i = 1; i < 7; i++) {
    Serial.print(addrInt[i]); Serial.print(F(" \t\t ")); Serial.print(sizeof(int)); Serial.print(F(" (int)")); Serial.print(F(" \t\t ")); Serial.println(Stepper_Pins[i]);
  }
  Serial.print(addrInt[i]); Serial.print(F(" \t\t ")); Serial.print(sizeof(int)); Serial.print(F(" (int)")); Serial.print(F(" \t\t ")); Serial.println(max_velocity);
  Serial.print(addrInt[i]); Serial.print(F(" \t\t ")); Serial.print(sizeof(int)); Serial.print(F(" (int)")); Serial.print(F(" \t\t ")); Serial.println(max_accel);
  Serial.print(addrInt[i]); Serial.print(F(" \t\t ")); Serial.print(sizeof(int)); Serial.print(F(" (int)")); Serial.print(F(" \t\t ")); Serial.println(MinPulseW);

  delay(40);
}

int EEReadInt(int addr) {
  int output;
  output = EEPROM.readInt(addr);

  return output;
}

void EEWriteInt(int addr, int val) {
  EEPROM.writeInt(addr, val);
  delay(10);
}

void EEPROMexInit() {
  int i = 0;

  EEPROM.setMemPool(memBase, EEPROMSizeUno);
  EEPROM.setMaxAllowedWrites(maxAllowedWrites);

  addrInt[1]       = EEPROM.getAddress(sizeof(int));
  addrInt[2]       = EEPROM.getAddress(sizeof(int));
  addrInt[3]       = EEPROM.getAddress(sizeof(int));
  addrInt[4]       = EEPROM.getAddress(sizeof(int));
  addrInt[5]       = EEPROM.getAddress(sizeof(int));
  addrInt[6]       = EEPROM.getAddress(sizeof(int));
  addrInt[7]       = EEPROM.getAddress(sizeof(int)); //max vel
  addrInt[8]       = EEPROM.getAddress(sizeof(int)); //max accel
  addrInt[9]       = EEPROM.getAddress(sizeof(int)); //min pulse width

  delay(100);

  for (i = 1; i < 7; i++) {                     //Read all pin
    int _out = EEReadInt(addrInt[i]);
    Stepper_Pins[i] = _out;
    delay(50);
//    Serial.print("_out:"); Serial.print(_out);
  }

  max_velocity =  EEReadInt(addrInt[7]);        //Read velocity and accelration
  max_accel =     EEReadInt(addrInt[8]);
  MinPulseW =     EEReadInt(addrInt[9]);

  issuedAdresses();
}

void EEPinWrite(unsigned int _motor, unsigned int _stp_pin, unsigned int _dir_pin, unsigned int _en_pin) {
  char _buffer[20];
  Serial.print(F("WRITING--> addr("));
  itoa(1 + 3 * (_motor - 1), _buffer, 10);
  Serial.print(_buffer); Serial.print(F(","));
  itoa(2 + 3 * (_motor - 1), _buffer, 10);
  Serial.print(_buffer); Serial.print(F(","));
  itoa(3 + 3 * (_motor - 1), _buffer, 10);
  Serial.print(_buffer); Serial.print(F(")="));
  Serial.print(addrInt[1 + 3 * (_motor - 1)]); Serial.print(F(","));
  Serial.print(addrInt[2 + 3 * (_motor - 1)]); Serial.print(F(","));
  Serial.print(addrInt[3 + 3 * (_motor - 1)]); Serial.print(F("\t"));
  Serial.print(F("pins="));
  Serial.print(_stp_pin); Serial.print(F(","));
  Serial.print(_dir_pin); Serial.print(F(","));
  Serial.print(_en_pin); Serial.print(F("\t"));
  EEWriteInt(addrInt[1 + 3 * (_motor - 1)], _stp_pin);
  EEWriteInt(addrInt[2 + 3 * (_motor - 1)], _dir_pin);
  EEWriteInt(addrInt[3 + 3 * (_motor - 1)], _en_pin);
  Serial.println(F(" OK"));
}

void EEVelAccelPulseWrite(unsigned int _max_vel, unsigned int _max_accel, unsigned int _minPulsew) {
  Serial.print(F("WRITING--> Max_velo("));
  Serial.print(_max_vel); Serial.print(F("), Max_accel("));
  Serial.print(_max_accel); Serial.print(F("), _MinPulW("));
  Serial.print(_minPulsew); Serial.print(F(")"));
  EEWriteInt(addrInt[7], _max_vel);
  EEWriteInt(addrInt[8], _max_accel);
  EEWriteInt(addrInt[9], _minPulsew);
  Serial.println(F(" OK"));
}
