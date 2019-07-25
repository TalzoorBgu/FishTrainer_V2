from __future__ import print_function
import time ## Import 'time' library. Allows us to use 'sleep'
import sys
from . import arduino as arduino_class

time_to_sleep=0
#pin_enbl = 36
#pin_left  = 38 #change to 15
#pin_right = 37 #

class tracker_Feeder:
    def __init__(self):
        global time_to_sleep
        time_to_sleep=0.25/1000.0 #(0.005) - 5ms
        print('feeder init -- ', end='')

        self.Arduino = arduino_class.Arduino_Functions()
        if not self.Arduino.connection == 'OK':
            print('No Arduino answer. Check Serial conn.')
            # raise ConnectionError('No Arduino answer. Check Serial conn.')

        self.check_arduino_conn()

        if self.ardu_conn == True:
            pass
            self.Arduino.send_default_program()

    def check_arduino_conn(self):
        self.ardu_conn = self.Arduino.check_arduino_connection()
        # print('ardu_conn:{}'.format(self.ardu_conn))
        return self.ardu_conn

    def new_feeder_run(self, _feeder, _side):
        res = ''
        print("inside new_feeder_run, side={}".format(_side))
        if _side == 'left' or _side == 1:
            _motor = 1
        else:
            _motor = 2

        if self.ardu_conn == True:
            res = self.Arduino.prog_run(0, _motor)  #back to motor 1 or 2
        else:
            pass
        return res


    def move_steps(self, _step_no, _side):
        res = ''
        if _side == 'left' or _side == 1:
            _motor = 1
        else:
            _motor = 2

        if self.ardu_conn == True:
            res = self.Arduino.motor_move(_step_no, _motor)
        else:
            pass
        return res



    def set_zero(self, _int_on):
        if _int_on == 1:
            self.Arduino.disable_pins(1)
        else:
            self.Arduino.disable_pins(0)

    ##Define a function named Blink()



    def velocity_calc(self, max_velocity, total_steps, percentage, c_step):
        action_range = total_steps*(percentage/100.0)

        if (c_step <= action_range):
            accl_pr = self.accl('up', c_step, percentage, total_steps)
            velocity = (accl_pr/100.0)*max_velocity
        elif (c_step >= total_steps - action_range):
            accl_pr = self.accl('down', c_step, percentage, total_steps)
            velocity = (accl_pr/100.0)*max_velocity
        else:
            velocity = max_velocity
        return velocity

    def accl(self, direction, i, percentage, total_steps):
        func = 100
        try:
            if direction == 'up':
                func = math.exp((20.0 * 100.0 * i) / (2.0 * percentage * total_steps))
            if direction == 'down':
                func = math.exp((20.0 * 100.0 * (total_steps - i) ) / (2.0 * percentage * total_steps))
            accl = func
            if accl > 100.0: accl = 100
        except ZeroDivisionError as error:
            print ("Error: ZeroDivisionError")
            accl = func
        return accl

    def destruct():
        GPIO.cleanup()
        return


# spin(16,int(sys.argv[1])) # uncomment for fast testing
