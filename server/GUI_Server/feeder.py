from __future__ import print_function
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import sys
import arduino

time_to_sleep=0
#pin_enbl = 36
#pin_left  = 38 #change to 15
#pin_right = 37 #

class Feeder:
    def __init__(self, pins):
        global time_to_sleep
        time_to_sleep=0.25/1000.0 #(0.005) - 5ms
        print('feeder init -- ', end='')
        GPIO.setmode(GPIO.BCM) ## Use board pin numbering
        for pin in pins:
            # print ('pin:{} '.format(pin), end='')
            print ('')
            if not int(pin) == 0:
                print("pin:{}".format(pin))
                GPIO.setup(int(pin), GPIO.OUT)
        self.check_arduino_conn()
        if self.ardu_conn == True:
            arduino.send_default_program()


    def check_arduino_conn(self):
        self.ardu_conn = arduino.check_arduino_connection()
        print('ardu_conn:{}'.format(self.ardu_conn))
        return self.ardu_conn

    def new_feeder_run(self, _feeder, _side):
        if _side == 'left':
            _motor = 1
        else:
            _motor = 2
        res = arduino.prog_run(0, _motor)  #back to motor 1 or 2
        return res

    def set_zero(self, _int_on):
        if _int_on == 1:
            arduino.disable_pins(1)
        else:
            arduino.disable_pins(0)

    ##Define a function named Blink()
    def spin(self, pin_num, steps, en_pin):
        print ('pin {}-->'.format(str(pin_num)),end='') ## Print current loop
        print ('steps:{}, en:{}'.format(steps, en_pin))
        GPIO.output(en_pin, True) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## slp shutdwon Wait
        for i in range(steps): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
            GPIO.output(pin_num,True)## Switch on pin
            time.sleep(time_to_sleep)## Wait
            GPIO.output(pin_num,False)## Switch off pin
            time.sleep(time_to_sleep)## Wait
        time.sleep(time_to_sleep)
        GPIO.output(en_pin, False) #pull slp pin to HIGH
        time.sleep(time_to_sleep)## sleep back Wait
        print ("Done",end='') ## When loop is complete, print "Done"
        return 'Done'

    def raw_spin(self, pin_num, pin_dir, en_pin, steps, direction, velocity, accl):
        print("raw_spin")
        print ("accl:{0}".format(accl))
        GPIO.output(en_pin, True) #pull slp pin to HIGH
        GPIO.output(pin_dir, direction == 'L')    #HIGH for 'L', LOW for else
        print ('steps:{0}, {1}%:{2}'.format(steps, accl, int((accl/100.0)*steps)))
        i2 = 0
        for i in range(steps): #53.3 for big pill # 133 for pill device# 1600 for archimeds ### one step is 1.8 degrees
            velocity_val = self.velocity_calc(velocity, steps, accl, i)
            if velocity_val < 1: velocity_val = 1
            wait_val = 1.0/(500000.0*velocity_val)
            # print('VEL:{}'.format(wait_val))
            #print ('{0},{1:.2f}-{2:.5f}\t\t'.format(i, velocity_val, 1.0/(velocity_val)), end='')
            #if i/10 == 0: print (".", end='')
            GPIO.output(pin_num, True)## Switch on pin
            time.sleep(wait_val)## Wait
            GPIO.output(pin_num, False)## Switch off pin
            time.sleep(wait_val)## Wait
            i2 += 1
        print('i2:{}'.format(i2))
        print ("")
        GPIO.output(en_pin, False) #pull slp pin to HIGH
        GPIO.output(pin_dir, False)
        print("Done")
        return 'Done'

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
