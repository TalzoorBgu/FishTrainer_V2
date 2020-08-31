#include <SoftwareSerial.h>
#include "src/AccelStepper/AccelStepper.h"
#include "src/MemoryFree/MemoryFree.h"

#define STR_SIZE      40
#define NUM_OF_PROGS  1
#define NUM_OF_PARAM  4
#define STEPS  26
#define DEBUG 1
#define baud_rate 115200

#ifdef DEBUG
#define LED_Yellow_LOW 2
#define LED_Yellow_A 3
#define LED_Red_LOW 4
#define LED_Red_A 5
#endif

//PROTOTYPES
void DEBUG_BLINK(byte num_of_blinking, boolean use_delay = false);
void Prog_show(int _prog_num, int _size, int _show_step = 0);
void do_step(unsigned int action, int steps_or_pos, int dir = 0, boolean wait_for_ready = false);
void MotorPins(unsigned int motor, unsigned int _stp_pin,
               unsigned int _dir_pin, unsigned int _en_pin, boolean EEwrite = true);
void Set_accel_vel_pulse(unsigned int _max_v, unsigned int _max_a, unsigned int _minPulseW, boolean _EEWrite = false);
void PROG_params_INIT(int _prog_num = -1);


boolean program_mode = false;
int PROG_params[NUM_OF_PROGS][STEPS][NUM_OF_PARAM] = {};   //10 available programs
byte PROG_num = 0;
byte PROG_step = 0;

byte stp_Pin[3] = {0};
byte dir_Pin[3] = {0};
byte En_pin[3] = {0};
byte max_velocity;
byte max_accel;
byte MinPulseW;
char serial_inData[STR_SIZE];

unsigned long previousMillis = 0;
const long interval = 50;
byte ledState = LOW;

AccelStepper stepper(AccelStepper::DRIVER, stp_Pin[1], dir_Pin[1]);

const int Shake_loc = 10;
int full_cycle = 1600;

boolean no_shake = false;

boolean start_seq = false; //to start step by step
boolean print_serial = true;

int step_no = 0;

int  addrInt[10] = {0};
byte Stepper_Pins[6] = {0};

void setup()
{

  Serial.begin(baud_rate);
  //  RPISerial.begin(9600);
  delay(10);
  Serial.print("Fish Training system V2.1");
  Serial.println(F("\tConnected to PC"));

  EEPROMexInit();
  delay(10);

  StepperInit();

  PROG_params_INIT();

  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  Serial.print(F("freeMemory()="));
  Serial.println(freeMemory());
}

void loop() // run over and over
{
  boolean running_motor;
  char _str[STR_SIZE];
  //  DEBUG_BLINK(2);
  stepper.run();
  //if (!stepper.isRunning()) stepper.disableOutputs();

  // If data is available on Raspberry Pi, print it to PC


  if (Serial.available()) {
    strcpy(_str, serialEvent(0));
    //    Serial.print(F("IN:"));
    Serial.print(_str);
    //delay(100);
    //    RPISerial.print(_str);

    int params[NUM_OF_PARAM] = {};
    unsigned int sizeOfp = sizeof(params) / sizeof(params[0]);

    translate_str(_str, strlen(_str), params, sizeOfp);


    /*Serial.print(F(" --> params: ")); Serial.print(params[0]);
      Serial.print(F(",")); Serial.print(params[1]);
      Serial.print(F(",")); Serial.print(params[2]);
      Serial.print(F(",")); Serial.println(params[3]);
    */

    if (program_mode and !(params[0] == 51)) {
      Prog_write(PROG_num, PROG_step, params, NUM_OF_PARAM);
      PROG_step++;
    }
    else if (params[0] == 50)     {
      program_mode = true;
      PROG_num = params[1];
      PROG_params_INIT(PROG_num);
      Serial.println();
      //Prog_write(PROG_num, params, NUM_OF_PARAM);
    }
    else if (params[0] == 51)     {
      program_mode = false;
      PROG_step = 0;
      Serial.println();
    }
    else if (params[0] == 52)     Prog_show(params[1], NUM_OF_PARAM);
    else if (params[0] == 58)     Prog_run(params[1], NUM_OF_PARAM);
    else if (params[0] == 990)    SelectMotor(params[1]);
    else if (params[0] == 991)    MotorPins(1, params[1], params[2], params[3]);
    else if (params[0] == 992)    MotorPins(2, params[1], params[2], params[3]);
    else if (params[0] == 980)    MotorDisable(params[1]);
    else if (params[0] == 981)    MotorEnable(params[1]);
    else if (params[0] == 99)     Set_accel_vel_pulse(params[1], params[2], params[3], true);
    else if (params[0] == 98)     Set_accel_vel_pulse(params[1], params[2], params[3], false);
    else                          do_step(params[0], params[1], params[2], true);
  }

}

void do_step(unsigned int action, int steps_or_pos, int dir, boolean wait_for_ready) {

  switch (action) {
    case 1:
      if (dir == 10) steps_or_pos = steps_or_pos * (-1);
      stepper.move(steps_or_pos);
      break;
    case 10:
      stepper.moveTo(steps_or_pos);
      break;
    case 20:
      //Serial.print(F("\tDelay"));
      delay(steps_or_pos);
      break;
  }
  stepper.enableOutputs();

  if (wait_for_ready) {
    stepper.run();
    while (stepper.isRunning()) {
      stepper.run();
    }
  }

}
