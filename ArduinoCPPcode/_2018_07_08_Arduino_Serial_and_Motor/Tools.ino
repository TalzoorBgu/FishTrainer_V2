boolean isNumeric(char* str, short int _size) {
  unsigned int stringLength = _size;
  char new_str[8];

  if (stringLength == 0) {
    return false;
  }

  boolean seenDecimal = false;

  if (!isDigit(str[0])) {
    boolean CheckWOMinus;

    TrancFirst(str, new_str);
    CheckWOMinus = isNumeric(new_str, _size-1);
    
    if (CheckWOMinus) return true;
    else return false;
  }
  else {
    unsigned int i;
    for (i = 0; i < stringLength; i++) {

      if (isDigit(str[i])) {
        continue;
      }

      if (str[i] == '.') {
        if (seenDecimal) {
          return false;
        }
        seenDecimal = true;
        continue;
      }
      return false;
    }
    return true;
  }
  Serial.print(F("freeMemoryH()="));
  Serial.println(freeMemory());
}


void TrancFirst(char* _first_str, char* _sec_str) {
  int _strlen;
  int i = 0;
  _strlen = strlen(_first_str);
  for (i = 1; i < _strlen; i++) {
    _sec_str[i - 1] = _first_str[i];
  }
  _sec_str[_strlen-1] = '\0';
}

