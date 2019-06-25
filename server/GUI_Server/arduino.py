# main
from __future__ import print_function
import serial
import time
import curses
import thread
import sys
from time import sleep
from datetime import datetime

FULL_CYCLE = 2 * 400
HALF_CYCLE = FULL_CYCLE / 2

bool_send_default_program = False

class SendCommand:
    #def __init__(self,
    #             stp_pin1,
    #             dir_pin1,
    #             en_pin1,
    #             stp_pin2,
    #             dir_pin2,
    #             en_pin2,
    #             _full_cycle):
    def __init__(self, _full_cycle=FULL_CYCLE):
        self.full_cycle = _full_cycle
        # _str = self.init_seq_motor_1(stp_pin1, dir_pin1, en_pin1)
        # ser.write(_str)
        # _str = self.init_seq_motor_2(stp_pin2, dir_pin2, en_pin2)
        # ser.write(_str)

    def init_seq_motor_1(self, _pin1, _pin2, _pin3):
        _str_to_send = 'in_s_motor_1,{},{},{}'.format(_pin1, _pin2, _pin3)
        return _str_to_send

    def init_seq_motor_2(self, _pin1, _pin2, _pin3):
        _str_to_send = 'in_s_motor_2,{},{},{}'.format(_pin1, _pin2, _pin3)
        return _str_to_send

    def select_motor(self, _motor):
        _str_to_send = 's_motor,{}'.format(_motor)
        return _str_to_send

    def move(self, _steps, _dir):
        _steps = float(_steps) / 360.0 * FULL_CYCLE
        _steps = int(_steps)
        _str_to_send = 'move,{},{}'.format(_steps, _dir)
        return _str_to_send

    def moveto(self, _pos):
        _pos = float(_pos) / 360.0 * FULL_CYCLE
        _pos = int(_pos)
        _str_to_send = 'moveto,{}'.format(_pos)
        return _str_to_send

    def delay(self, _delay):
        _str_to_send = 'delay,{}'.format(_delay)
        return _str_to_send

    def program_start(self, _num):
        _str_to_send = 'p_start,{}'.format(_num)
        return _str_to_send

    def program_end(self, _num):
        _str_to_send = 'p_end,{}'.format(_num)
        return _str_to_send

    def define_vel_acc(self, _vel, _acc, _pulse_w):
        _str_to_send = 'def_v_a,{},{},{}'.format(_vel, _acc, _pulse_w)
        return _str_to_send

    def define_default_vel_acc(self, _vel, _acc, _pulse_w):
        _str_to_send = 'def_dflt_v_a,{},{},{}'.format(_vel, _acc, _pulse_w)
        return _str_to_send

    def show_prog(self, _num):
        _str_to_send = 'show_prog,{}'.format(_num)
        return _str_to_send

    def run_prog(self, _num):
        _str_to_send = 'run_prog,{}'.format(_num)
        return _str_to_send

    def disable_pins(self, _num):
        _str_to_send = 'dis_pins,{}'.format(_num)
        return _str_to_send

    def en_pins(self, _num):
        _str_to_send = 'en_pins,{}'.format(_num)
        return _str_to_send



class MySerial:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)

    def write(self, cmd):
        try:
            if not cmd == '':
                print('(RPi_OUT):#{}#'.format(cmd))
                self.serial.write(cmd.encode())
                sleep(20.0/1000.0)      # 10mS
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Serial write error")
        finally:
            sys.stdout.flush()
        return 'done'

    def read(self):
        ch_r_d = ''
        ch_r = ''
        try:
            nb_chars = self.serial.in_waiting
            if nb_chars > 0:
                time.sleep(80.0/1000.0)
                nb_chars = self.serial.in_waiting
                ch_r = self.serial.read(nb_chars)
                real_string = False  # flag to check if all char=0
                for ch_sep in ch_r:
                    # print('b:{}'.format(ord(ch_sep)), end='')
                    if not ord(ch_sep) == 0: real_string = True
                if not real_string: ch_r = ''
                if len(ch_r) > 0 and ord(ch_r[-1]) == 224:
                    print('Serial ready')
                else:
                    ch_r = ch_r.decode()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            e = sys.exc_info()
            print("Serial read error: {},{}".format(e[0], e[1]))
            pass
        finally:
            sys.stdout.flush()

        return ch_r





def check_arduino_connection():
    ser = MySerial("/dev/ttyS0", 9600)

    _bool_flag = False
    _str_to_send = 'First_Conn_Check'
    ser.write(_str_to_send)

    result = ''
    millis = int(round(time.time() * 1000))
    time_now = millis
    while (result == '' and time_now - millis < 2000):  # wait for respond before sending next command
        time_now = int(round(time.time() * 1000))
        result = ser.read()

    if result == _str_to_send: _bool_flag = True
    if _bool_flag==False and result != '': print('res:{}'.format(result))

    ser.serial.close()
    return _bool_flag

def main():
    global bool_send_default_program
    ser = MySerial("/dev/ttyS0", 9600)
    # command = SendCommand(0, 0, 0, 1, 1, 1, FULL_CYCLE)
    command = SendCommand(FULL_CYCLE)
    print('--- Main loop ---')
    try:
        i = 0
        millis = int(round(time.time() * 1000))
        interval = 500  # mS
        old_time = millis

        while True:
            millis = int(round(time.time() * 1000))
            tim_now = millis

            i += 1
            time.sleep(0.005)
            result = ser.read()

            if not result == '':
                if len(result) == 1:
                    if not ord(result) == 240 \
                            or not ord(result) == 0:
                        result = ''  # don't print invalid chars
                if tim_now > (old_time + interval):
                    print('(RPi_IN):', end=' ')
                    old_time = tim_now
                print('{}'.format(result), end=' ')

            if bool_send_default_program:
                send_default_program()
                bool_send_default_program = False

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        e = sys.exc_info()
        print("main error: {},{}".format(e[0], e[1]))

def input_thread():
    global bool_send_default_program
    while True:
        key_pressed = read_key()
        print("Key pressed-{}".format(key_pressed))

        if key_pressed.lower() == "q":
            thread.interrupt_main()
            break
        else:
            res = ''
            if key_pressed.lower() == "i":
                res = command.init_seq_motor_1(6, 8, 7)
            if key_pressed.lower() == "o":
                res = command.init_seq_motor_2(10, 11, 12)
            if key_pressed.lower() == "a":
                res = command.move(100, 'R')
            if key_pressed.lower() == "b":
                res = command.move(200, 'L')
            if key_pressed.lower() == "0":
                res = command.moveto(0)
            if key_pressed.lower() == "1":
                res = command.moveto(90)
            if key_pressed.lower() == "2":
                res = command.moveto(180)
            if key_pressed.lower() == "3":
                res = command.moveto(-360)
            if key_pressed.lower() == "4":
                res = command.moveto(360*4)
            if key_pressed.lower() == "c":
                res = command.define_vel_acc(60, 400, 1)
            if key_pressed.lower() == "d":
                res = command.disable_pins(0)
            if key_pressed.lower() == "e":
                res = command.define_vel_acc(60, 400, 15)
            if key_pressed.lower() == "f":
                res = command.define_vel_acc(60, 400, 30)
            if key_pressed.lower() == "g":
                res = command.define_vel_acc(50, 120, 60)
            if key_pressed.lower() == "9":
                res = command.delay(300)
            if key_pressed.lower() == "8":
                res = command.delay(600)
            if key_pressed.lower() == "s":
                res = command.show_prog(0)
            if key_pressed.lower() == "[":
                res = command.program_start(0)
            if key_pressed.lower() == "]":
                res = command.program_end(0)
            if key_pressed.lower() == "l":
                res = command.show_prog(1)
            if key_pressed.lower() == "{":
                res = command.program_start(1)
            if key_pressed.lower() == "}":
                res = command.program_end(1)
            if key_pressed.lower() == "t":
                res = command.run_prog(0)
            if key_pressed.lower() == "y":
                res = command.run_prog(1)
            if key_pressed.lower() == "=":
                bool_send_default_program = True

            if not res == '': ser.write(res)



def read_key():
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~(termios.ICANON | termios.ECHO)  # c_lflags
    c = None
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
    return c


def send_default_program():
    ser = MySerial("/dev/ttyS0", 9600)
    # command = SendCommand(0, 0, 0, 1, 1, 1, FULL_CYCLE)
    command = SendCommand(FULL_CYCLE)
    PROG_arry = [['prog_start',     0,      0,      0],
                 ['moveto',         0,      0,      0],
                 ['def_v_a',        60,     40,    20],
                 ['moveto',         30,      0,      0],
                 ['def_v_a',        600,     300,    20],
                 ['delay',          400, 'L', 0],
                 #['move',           360*4,   0,      0],

                 ['move',           180+30, 'L', 0],
                 ['delay',          450,    'L', 0],
                 ['def_v_a',        60,     60,     40],
                 ['move',           80,     'R',    0],
                 ['delay',          300,     'L',    0],
                 ['move',           80,     'L',    0],
                 ['delay',          200,    'L',    0],

                 ['def_v_a',        25,     1,    20],

                 ['move',           30,     'L',    0],
                 ['move',           25,     'L',    0],
                 ['delay',          60, 'L', 0],
                 ['move',           25,     'R',    0],

                 ['def_v_a',        40,     20,     30],
                 ['moveto',         0,      0,      0],

                 ['def_v_a',        100,    80,     30],
                 ['prog_end',       0,      0,      0]
                 ]

    for step in PROG_arry:
        _str_to_send = ''

        if step[0] == 'move':
            _str_to_send = command.move(step[1], step[2])
        if step[0] == 'moveto':
            _str_to_send = command.moveto(step[1])
        if step[0] == 'delay':
            _str_to_send = command.delay(step[1])
        if step[0] == 'def_v_a':
            _str_to_send = command.define_vel_acc(step[1], step[2], step[3])
        if step[0] == 'prog_start':
            _str_to_send = command.program_start(step[1])
        if step[0] == 'prog_end':
            _str_to_send = command.program_end(step[1])

        ser.write(_str_to_send)

        result = ''
        while result == '':     # wait for respond before sending next command
            result = ser.read()
        if "p_end" in result:
            print('Program write --> OK')
        #print('res:#{}#, result==_str_var:{}'.format(result, result == _str_to_send))
        # time.sleep(10.0/1000.0)

    #ser.write(res)
def disable_pins(_int_on):
    ser = MySerial("/dev/ttyS0", 9600)
    command = SendCommand(FULL_CYCLE)

    if _int_on == 1:
        _str_to_send = command.disable_pins(0)
    else:
        _str_to_send = command.en_pins(0)

    ser.write(_str_to_send)

    result = ''
    while result == '':  # wait for respond before sending next command
        result = ser.read()


def prog_run(_prog, _motor):
    ser = MySerial("/dev/ttyS0", 9600)
    command = SendCommand(FULL_CYCLE)

    res = ''

    _str_to_send = command.select_motor(_motor)
    ser.write(_str_to_send)

    result = ''
    while result == '':  # wait for respond before sending next command
        result = ser.read()
    if "s_motor" in result:
        print('s_motor:{} --> OK'.format(_motor))
    sleep(100.0 / 1000.0)
    while result == '':  # wait for respond before sending next command
        result = ser.read()
    print(result)

    _str_to_send = command.run_prog(_prog)
    ser.write(_str_to_send)

    result = ''
    while result == '':  # wait for respond before sending next command
        result = ser.read()
    if "run_prog" in result:
        print('run_prog --> OK'.format(_motor))
        res = 'Program runing on motor {}'.format(_motor)

    return res

if __name__ == '__main__':
    try:
        print('---Start---')
        thread.start_new_thread(input_thread, ())  # ADDED
        flag_first_time = True
        if check_arduino_connection():
            pass
        else:
            raise EnvironmentError('No Arduino answer. Check Serial conn.')
        send_default_program()
        main()
        sys.stdout.flush()

    except KeyboardInterrupt:  # ADDED
        print("Quit")

    except:
        e = sys.exc_info()
        print("Main error: {},{}".format(e[0], e[1]))

    finally:
        ser.serial.close()
        print("Bye.")
        sys.stdout.flush()
        sys.exit(0)
        pass
