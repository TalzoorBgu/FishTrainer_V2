// Only Serial event function
char* serialEvent(int Which_serial) { //0 for Serial, 1 for SoftSerial
  
  char inChar;
  byte index = 0;

  while (Which_serial ? RPISerial.available() : Serial.available()) {
    if (index < STR_SIZE - 1) // One less than the size of the array
    {
      inChar = (Which_serial ? (char)RPISerial.read() : (char)Serial.read()); // Read a character
      serial_inData[index] = inChar; // Store it
      index++; // Increment where to write next
      serial_inData[index] = '\0'; // Null terminate the string
    }
    delay(2); //1mS
  }
//  Serial.print("inData:"); Serial.print(inData);
  Serial.flush();
  return serial_inData;
}
