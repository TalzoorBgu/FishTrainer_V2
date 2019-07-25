void DEBUG_BLINK(byte num_of_blinking, boolean use_delay) {
  if (use_delay) {
    for (int i = 1; i < (num_of_blinking * 2); i++) {
      digitalWrite(LED_Yellow_LOW, LOW);
      analogWrite(LED_Yellow_A, 100 * ((i - 1) % 2));
      digitalWrite(LED_Red_LOW, LOW);
      analogWrite(LED_Red_A, 100 * (i % 2));
      delay(100);
    }
  } else {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      if (ledState == LOW) {
        ledState = HIGH;
      } else {
        ledState = LOW;
      }
      //      for (int i = 1; i < (num_of_blinking * 2); i++) {
      digitalWrite(LED_Yellow_LOW, LOW);
      analogWrite(LED_Yellow_A, 100 * ledState);
      digitalWrite(LED_Red_LOW, LOW);
      analogWrite(LED_Red_A, 100 * ledState);
      //      }
    }
  }
}
