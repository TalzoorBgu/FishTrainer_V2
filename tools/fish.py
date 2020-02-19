#!/usr/bin/env python
import argparse
import datetime
import glob
import os
import random
import sys
import threading
import time
from pathlib import Path
from time import sleep
import cv2
import serial

import Main
import tools.log
from tools.log import FishLog, ReadFile

FULL_CYCLE = 2 * 200
HALF_CYCLE = FULL_CYCLE / 2
bool_send_default_program = False


class Tank:
    def __init__(self, fid, width):  # pin_num - set in config file on pi
        self.fid = fid
        self.width = width
        self.side = None

    def decide(self, x, y, _ver='edge'):
        tmp_return = None
        if _ver is 'edge':
            if x < self.width / 4 and not self.side == 'left':
                self.side = 'left'
                tmp_return = 'left'

            elif x > self.width * 3 / 4 and not self.side == 'right':
                self.side = 'right'
                tmp_return = 'right'

        elif _ver is 'center':
            if (x > self.width * 3 / 8 and x < self.width * 5 / 8) and (
                    y > self.width * 3 / 8 and y < self.width * 5 / 8):
                if self.side is 'out_center':
                    self.side = 'center'
                    tmp_return = 'center'
            else:
                self.side = 'out_center'
                tmp_return = 'out_center'

        return tmp_return


class ScenePlanner:
    def __init__(self, _exception_class):
        self.refPt = []
        self.fish = []
        self.cropping = False
        self.exception_obj = _exception_class

    def draw_current(self, _img, _camera):
        try:
            file_path = get_file_name(_camera)

            fish_draw = []
            with open(file_path) as f:
                lines = f.read().splitlines()
            for line in lines:
                fish_draw.append(eval(line))
            for fishy in fish_draw:
                cv2.rectangle(_img, (fishy['left'], fishy['upper']), (fishy['right'], fishy['lower']),
                              (255, 255, 255), 1)
        except IOError:
            print('file dosent exsit - cannot draw')

    def click_and_crop(self, event, x, y, flags, param):
        global image, fish, refPt

        # grab references to the global variables
        global refPt, cropping

        camera = param
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False

            # arrange points left-right up-down
            ordered = [(min(refPt[0][0], refPt[1][0]), min(refPt[0][1], refPt[1][1]))]
            ordered.append((max(refPt[0][0], refPt[1][0]), max(refPt[0][1], refPt[1][1])))

            fish.append({'camera:': camera, 'upper': ordered[0][1], 'lower': ordered[1][1], 'left': ordered[0][0],
                         'right': ordered[1][0]})

            # draw a rectangle around the region of interest
            cv2.rectangle(image, ordered[0], ordered[1],
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
            cv2.imshow("image", image)

    def SP_Main(self, _camera=0):
        global image, fish, refPt
        refPt = []
        fish = []
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--image", help="Path to the image")
        ap.add_argument("-v", "--video", help="path to the (optional) video file")
        args = vars(ap.parse_args())

        # load the image, clone it, and setup the mouse callback function
        # if a video path was not supplied, grab the reference
        # to the webcam
        if not args.get("video", False):
            video_capture = cv2.VideoCapture(int(_camera))

        # otherwise, grab a reference to the video file
        else:
            video_capture = cv2.VideoCapture(args["video"])

        try:
            ret, image = video_capture.read()

            if image is None:  # check for empty frames
                self.exception_obj.error("No Image, camera failed to properly initialize!")

            # draw current configuration
            self.draw_current(image, _camera)

            # image = cv2.imread(args["image"])
            clone = image.copy()
            cv2.namedWindow("image")
            cv2.setMouseCallback("image", self.click_and_crop, _camera)

            # keep looping until the 'c' key is pressed
            loop_out = False
            while not loop_out:

                # Write Text
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                fontColor = (255, 255, 255)
                lineType = 2

                cv2.putText(image, 'please mark your tanks', (50, 50), font, fontScale, fontColor, lineType)
                cv2.putText(image, 'press "c" to finish and "r" to reset', (50, 100), font, fontScale, fontColor,
                            lineType)
                ''
                # display the image and wait for a keypress
                cv2.imshow("image", image)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                # 'r'=99            'c'=99
                # 'R'=82            'C'=67
                # 'heb(r)' = 248    'heb(c)=225

                # print key
                if (key == ord('r') or key == ord('R') or key == 248):
                    image = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif (key == ord('c') or key == ord('C') or key == 225):
                    loop_out = True

            # if there are two reference points, then crop the region of interest
            # from the image and display it

            if len(refPt) == 2:
                file_path = get_file_name(_camera)

                thefile = open(file_path, 'w+')

                print("file_path:{}".format(file_path))

                for fishy in fish:
                    print(fishy)
                    thefile.write("%s\n" % fishy)

                thefile.flush()
                thefile.close()
                print("tank_config.txt saved!")

        except (AttributeError, NameError) as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.exception_obj.error("{},{} line:{}".format(exc_type, fname, exc_tb.tb_lineno))

        finally:
            # close all open windows
            cv2.destroyAllWindows()
            cv2.waitKey(1)


class TrackerFeeder:
    def __init__(self):
        global time_to_sleep
        time_to_sleep = 0.25 / 1000.0  # (0.005) - 5ms
        print('feeder init -- ', end='')

        self.Arduino = ArduinoFunctions()
        if not self.Arduino.connection == 'OK':
            print('No Arduino answer. Check Serial conn.')

        self.check_arduino_conn()

        if self.ardu_conn is True:
            self.Arduino.send_default_program()

    def check_arduino_conn(self):
        self.ardu_conn = self.Arduino.check_arduino_connection()
        return self.ardu_conn

    def new_feeder_run(self, _feeder, _side):
        res = ''
        print("side={}".format(_side))
        if _side == 'left' or _side == 1 or _side == 'center':
            _motor = 2
        else:
            _motor = 1

        if self.ardu_conn is True:
            res = self.Arduino.prog_run(0, _motor)  # back to motor 1 or 2
        else:
            pass
        return res

    def move_steps(self, _step_no, _side):
        res = ''
        if _side == 'left' or _side == 1:
            _motor = 1
        else:
            _motor = 2

        if self.ardu_conn is True:
            res = self.Arduino.motor_move(_step_no, _motor)
        else:
            pass
        return res

    # def set_zero(self, _int_on=0):
    #     self.Arduino.disable_pins(_int_on)



class SendCommand:
    def __init__(self, _full_cycle=FULL_CYCLE):
        self.full_cycle = _full_cycle

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
        steps = float(_steps) / 360.0 * FULL_CYCLE
        steps = int(steps)
        str_to_send = 'move,{},{}'.format(steps, _dir)
        return str_to_send

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
        if _num == 'left' or _num == 1:
            _motor = 1
        else:
            _motor = 2
        _str_to_send = 'dis_pins,{}'.format(_motor)
        return _str_to_send

    def en_pins(self, _num):
        if _num == 'left' or _num == 1:
            _motor = 1
        else:
            _motor = 2
        _str_to_send = 'en_pins,{}'.format(_motor)
        return _str_to_send


class MySerial:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)

    def write(self, cmd):
        try:
            if not cmd == '':
                print('(Comp_OUT):#{}#'.format(cmd))
                self.serial.write(cmd.encode())
                sleep(20.0 / 1000.0)  # 20mS
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Serial write error")
        finally:
            sys.stdout.flush()
        return 'done'

    def read(self):
        ch_r = ''
        try:
            nb_chars = self.serial.in_waiting
            if nb_chars > 0:
                time.sleep(20.0 / 1000.0)
                nb_chars = self.serial.in_waiting
                ch_r = self.serial.read(nb_chars).decode()
                real_string = False  # flag to check if all char=0
                for ch_sep in ch_r:
                    # print('b:{}'.format(ord(ch_sep)), end='')
                    if not ord(ch_sep) == 0: real_string = True
                if not real_string: ch_r = ''
                if len(ch_r) > 0 and ord(ch_r[-1]) == 224:
                    print('Serial ready')
                else:
                    pass
        except KeyboardInterrupt:
            raise KeyboardInterrupt

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Serial read error: {}, file:{}, line:{}".format(exc_type, fname, exc_tb.tb_lineno))
            print(exc_obj)

        finally:
            sys.stdout.flush()

        return ch_r


class ArduinoFunctions:
    def __init__(self):
        self.command_str = SendCommand(FULL_CYCLE)
        serial_ports_list = serial_ports()
        print("serial_ports_list:{}".format(serial_ports_list))
        try:
            self.connection = 'NO'
            for port in reversed(serial_ports_list):  # usually COM7
                print("Checking port:{}".format(port))
                self.serial_con = MySerial(port, 9600)
                #     dump first lines
                time.sleep(3)  # sec
                str_in = self.receive_data()
                # print("str_in:@@{}@@".format(str_in))
                if str_in.find("Connected to PC") is not -1:
                    self.connection = 'OK'
                if self.connection is 'OK':
                    break
                time.sleep(5 / 1000)  # ms
        except:
            self.connection = 'NO'
        finally:
            print("Arduino conn:{}".format(self.connection))

    def __enter__(self):
        return self

    def send_command(self, _command):
        res = self.serial_con.write(_command)
        sleep(20 / 1000)  # ms
        res = self.receive_data()

        return res

    def check_arduino_connection(self):
        # ser = MySerial("/dev/ttyS0", 9600)
        _bool_flag = False
        _str_to_send = 'First_Conn_Check'
        try:
            self.serial_con.write(_str_to_send)

            result = ''
            millis = int(round(time.time() * 1000))
            time_now = millis
            while (result == '' and time_now - millis < 2000):  # wait for respond before sending next command
                time_now = int(round(time.time() * 1000))
                result = self.serial_con.read()

            if result == _str_to_send: _bool_flag = True
            if _bool_flag == False and result != '': print('res:#{}#'.format(result))
        except:
            pass
        # self.serial_con.serial.close()
        return _bool_flag

    def main(self):
        global bool_send_default_program
        print('--- Arduino Main loop ---')
        try:
            i = 0
            millis = int(round(time.time() * 1000))
            interval = 500  # mS
            old_time = millis

            while True:     # runs in
                millis = int(round(time.time() * 1000))
                tim_now = millis

                i += 1
                time.sleep(5/1000)
                result = self.serial_con.read()

                if not result == '':
                    if len(result) == 1:
                        if not ord(result) == 240 \
                                or not ord(result) == 0:
                            result = ''  # don't print invalid chars
                    if tim_now > (old_time + interval):
                        print('(Ard_IN):', end=' ')
                        old_time = tim_now
                    print('{}'.format(result), end=' ')

                if bool_send_default_program:
                    self.send_default_program()
                    bool_send_default_program = False

        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            e = sys.exc_info()
            print("main error: {},{}".format(e[0], e[1]))

    def send_default_program(self):
        PROG_arry = [['prog_start', 0, 0, 0],
                     ['moveto', 0, 0, 0],
                     ['def_v_a', 60, 40, 20],
                     ['moveto', 30, 0, 0],
                     ['def_v_a', 600, 300, 20],
                     ['delay', 400, 'L', 0],

                     ['move', 180 + 30, 'L', 0],
                     ['delay', 450, 'L', 0],
                     ['def_v_a', 60, 60, 40],
                     ['move', 80, 'R', 0],
                     ['delay', 300, 'L', 0],
                     ['move', 80, 'L', 0],
                     ['delay', 200, 'L', 0],

                     ['def_v_a', 25, 1, 20],

                     ['move', 30, 'L', 0],
                     ['move', 25, 'L', 0],
                     ['delay', 60, 'L', 0],
                     ['move', 25, 'R', 0],

                     ['def_v_a', 40, 20, 30],
                     ['moveto', 0, 0, 0],

                     ['def_v_a', 100, 80, 30],
                     ['prog_end', 0, 0, 0]
                     ]

        for step in PROG_arry:
            _str_to_send = ''

            if step[0] == 'move':
                _str_to_send = self.command_str.move(step[1], step[2])
            if step[0] == 'moveto':
                _str_to_send = self.command_str.moveto(step[1])
            if step[0] == 'delay':
                _str_to_send = self.command_str.delay(step[1])
            if step[0] == 'def_v_a':
                _str_to_send = self.command_str.define_vel_acc(step[1], step[2], step[3])
            if step[0] == 'prog_start':
                _str_to_send = self.command_str.program_start(step[1])
            if step[0] == 'prog_end':
                _str_to_send = self.command_str.program_end(step[1])

            self.serial_con.write(_str_to_send)

            result = ''
            while result == '':  # wait for respond before sending next command
                result = self.serial_con.read()
            if "p_end" in result:
                print('Program write --> OK')

    def disable_pins(self, _int_on, _all=-1):   # -1=all, num=motors
        if _all is -1:
            motor = [0, 1]
        else:
            motor = [0]

        for m in motor:
            if _int_on == 1:
                _str_to_send = self.command_str.disable_pins(m)
            else:
                _str_to_send = self.command_str.en_pins(m)
            res = self.send_command(_str_to_send)

        return res

    def motor_move(self, _step_no, _motor):
        _str_to_send = self.command_str.select_motor(_motor)
        result = self.send_command(_str_to_send)
        if "s_motor" in result:
            print('s_motor:{} --> OK'.format(_motor))
        sleep(20.0 / 1000.0)  # 20ms

        _str_to_send = self.command_str.move(_step_no, 'R')
        result = self.send_command(_str_to_send)

        return result

    def prog_run(self, _prog, _motor):
        # ser = MySerial("/dev/ttyS0", 9600)
        # command = SendCommand(FULL_CYCLE)

        res = ''

        _str_to_send = self.command_str.select_motor(_motor)
        result = self.send_command(_str_to_send)

        if "s_motor" in result:
            print('s_motor:{} --> OK'.format(_motor))
        sleep(20.0 / 1000.0)  # 20ms

        _str_to_send = self.command_str.run_prog(_prog)
        result = self.send_command(_str_to_send)

        if "run_prog" in result:
            print('run_prog --> OK'.format(_motor))
            res = 'Program runing on motor {}'.format(_motor)

        return res

    def receive_data(self):
        str_in = ""

        ser_inwait = self.serial_con.serial.inWaiting()
        while self.serial_con.serial.inWaiting():
            # str_in = str_in + self.serial_con.serial.readline().decode()
            str_in = str_in + self.serial_con.serial.read().decode()
            sleep(1 / 1000)  # 1ms

        if not str_in == "":
            print("(Ardu_in): {}".format(str_in))
        return str_in

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.serial_con.close()


def get_file_name(_camera):
    full_script_path = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '/')
    file_path = Path('{}tank_config_cam_{}.txt'.format(full_script_path, _camera))

    return file_path


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


FEED_EVERY = 3  # feed every 3 sec


class Tracking:
    def __init__(self, _exception_class, _max_training_time, _camera=0, video=None):
        self.video_capture = None
        file_path = get_file_name(_camera)

        self.height = []
        self.fgbg = []
        self.fish = []
        self.width = []
        self.file = []

        self.exception_obj = _exception_class
        self.controller_obj = None
        self.max_training_time = _max_training_time

        try:
            print("file_path:{}".format(file_path))
            with open(file_path) as file:
                lines = file.read().splitlines()

            for line in lines:
                self.fish.append(eval(line))

            # if a video path was not supplied, grab the reference to the webcam
            if video is None:
                self.video_capture = cv2.VideoCapture(int(_camera))
            # otherwise, grab a reference to the video file
            else:
                self.video_capture = cv2.VideoCapture(video)

            id = 0
            for fishy in self.fish:
                self.fgbg.append(cv2.bgsegm.createBackgroundSubtractorMOG())
                self.width.append(fishy['right'] - fishy['left'])
                self.height.append(fishy['lower'] - fishy['upper'])
                tmp_str = 'self.width: {0}, self.height: {1}'.format(self.width[id], self.height[id])
                print(tmp_str)
                id = id + 1



        except FileNotFoundError:
            self.exception_obj.error("No cam config file!, Press 'Tank conf.' first.")
        finally:
            print("self.file:{}".format(self.file))
            if not self.file == []:
                self.file.close()

    def set_controller_obj(self, _controller):
        self.controller_obj = _controller

    def track_loop(self, _version='edge'):  # cb is an object that has a do() function in the calling script
        self.stop_training = False

        if self.video_capture is None:
            self.exception_obj.error("Having problem to get image from camera")
            return 0

        self.exception_obj.info("Training started. version:{}, max training time:{}".
                                format(_version, self.max_training_time), bold=True)

        for i, fishy in enumerate(self.fish):
            img_name = "image" + str(i)
            mask_name = "mask" + str(i)
            cv2.namedWindow(img_name)
            cv2.namedWindow(mask_name)
            cv2.startWindowThread()

        self.stop_training = self.controller_obj.check_training()
        exit_flag = self.controller_obj.check_exit_flag()

        while self.stop_training is False:
            sys.stdout.flush()
            self.controller_obj.time()

            # Capture frame-by-frame
            ret, frame = self.video_capture.read()
            if frame is None:
                # print('No Image')
                self.exception_obj.error('No Image! check that camera closed on other apps')
                break  # check for empty frames

            for i, fishy in enumerate(self.fish):
                img_name = "image" + str(i)
                mask_name = "mask" + str(i)
                frame_cut = frame[fishy['upper']:fishy['lower'], fishy['left']:fishy['right']]
                fgmask = self.fgbg[i].apply(frame_cut)
                fgmask = cv2.erode(fgmask, None, iterations=2)
                mask = cv2.dilate(fgmask, None, iterations=2)

                tank_width = abs(fishy['upper'] - fishy['lower'])
                tank_height = abs(fishy['left'] - fishy['right'])
                # print("tank_dim:{}/{}".format(tank_width, tank_height))

                self.draw_lines(cv2, tank_width, tank_height, frame_cut, _version)

                cv2.imshow(img_name, frame_cut)
                cv2.imshow(mask_name, fgmask)
                cv2.waitKey(1)
                # find contours in the mask and initialize the current
                # (x, y) center of the ball
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                max_rad = 0
                for cntr in cnts:
                    ((x, y), radius) = cv2.minEnclosingCircle(cntr)
                    if radius > max_rad:
                        largest_cntr = cntr
                        max_rad = radius
                # check if largest_cntr is set
                if len(cnts) > 0:
                    ((x, y), radius) = cv2.minEnclosingCircle(largest_cntr)
                    cv2.circle(frame_cut, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # show radius for debbuging
                    cv2.imshow("image" + str(i), frame_cut)
                    cv2.waitKey(1)

                    if self.controller_obj is not None:
                        self.controller_obj.do(x, y, i, _version)

                self.stop_training = self.controller_obj.check_training()
                exit_flag = self.controller_obj.check_exit_flag()

            # TBD - inclear where to put
            # if cv2.waitKey(1) & 0xFF == ord('q'): break #Exit when Q is pressed

        # exit while loop:
        print("Loop exit")
        if exit_flag:
            pass

        self.exception_obj.info("Training stopped")

        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        self.video_capture.release()
        id_out = 0
        for fishy in self.fish:
            # print("OUT:fish_id:{}".format(id_out))
            self.controller_obj.end_training(id_out)
            id_out += 1
            # sleep(1.5)
        print("thread_track_fish Finished")

    def draw_lines(self, _cv_obj, _tank_width, _tank_height, _frame, _ver):
        if _ver is 'edge':
            low_boundry = 1.0 / 4.0
            hige_boundry = 3.0 / 4.0
        elif _ver is 'center':
            low_boundry = 3.0 / 8.0
            hige_boundry = 5.0 / 8.0

        down = int(_tank_width * low_boundry)
        up = int(_tank_width * hige_boundry)
        right = int(_tank_height * low_boundry)
        left = int(_tank_height * hige_boundry)

        # print("_ver:{}, _tank_height:{}, left_up:{}, left_down:{}".
        #      format(_ver, _tank_height, left_up, left_down))
        # print("low_boundry:{}".format(low_boundry))

        if _ver is 'edge':
            _cv_obj.line(_frame, (left, 0), (left, _tank_width), (255, 255, 255), 1)
            _cv_obj.line(_frame, (right, 0), (right, _tank_width), (255, 255, 255), 1)
        elif _ver is 'center':
            _cv_obj.rectangle(_frame, (left, down), (right, up), (255, 255, 255), 1)


class Controller:
    def __init__(self, _tracking_obj, _feed, _exception_class, _log_folder, _log_name=['test'], _GUI_obj=None,
                 _camera=0, _training_stop_timed=None):
        global time_counter

        time_counter = 0

        self.training_stop_timed = _training_stop_timed
        self.total_feed = []
        self.thread_plotter = None
        self.feed = _feed

        self.time_count = TimeCounter()
        self.GUI_obj = _GUI_obj
        self.chb_Var = _GUI_obj.chb_Var
        self.time_last_feed = int(round(time.time()))

        self.exception_log = _exception_class
        self.tracking_obj = _tracking_obj

        self.logger = []
        self.tank = []
        self.log_folder = _log_folder
        # fish_id = 0
        # print("self.tracking_obj.width:{}".format(self.tracking_obj.width))
        print("_log_name:{}".format(_log_name))
        for i, size in enumerate(self.tracking_obj.width):
            self.total_feed.append(0)
            # print("i:{}".format(i))
            self.tank.append(Tank(i, size))
            log_str = "{}.({})".format(_log_name[i], str(i))
            # print("log_str:{}".format(log_str))
            self.logger.append(FishLog(self.log_folder,
                                       log_str,
                                       self.exception_log)
                               )
        self.feed.Arduino.disable_pins(False, _camera)               # make motors available (training sys by cam)

    def __del__(self):  # Destroy
        self.feed.Arduino.disable_pins(True, _camera)                # shut motors off
        print('Controller closed')

    def time(self):
        time_str = self.time_count.get_time_diff()
        if time_str:
            stop_training = self.GUI_obj.update_time(time_str, self.training_stop_timed)
            if stop_training: self.GUI_obj.stop_training_func()

    def check_exit_flag(self):
        _int_tmp = self.GUI_obj.exit_flag
        return _int_tmp

    def close_app(self):
        Main.destroy_Fish_training_GUI___Client()

    def check_training(self):
        _int_tmp = self.GUI_obj.stop_training
        return _int_tmp

    def end_training(self, fish_id):  # called in tracking.py - cb.end_training(id_out)
        try:
            fish_db = tools.log.Database(self.GUI_obj.db_file_full_path())

            log_filename = self.logger[fish_id].filename
            self.logger[fish_id].file_obj.close()
            sleep(200/1000)  # 200mS wait
            t_data = ReadFile(log_filename)
            if not t_data.file_empty:  # continue only when there is data
                t_dt_str = t_data.training_start_str
                time_str = t_dt_str[:t_dt_str.rindex(" ") + 6]
                total_feed = self.total_feed[fish_id]
                print("Creating DB record")
                fish_db.create_training_record([t_data.train_day,
                                                t_data.fish_no,
                                                time_str,
                                                total_feed,
                                                log_filename,
                                                str(t_data.total_training_time),
                                                ""])
                self.GUI_obj.db_tree_view_data_refresh()

                thread_plotter = threading.Thread(target=tools.log.run,
                                                  args=(t_data, self.log_folder, log_filename,),
                                                  kwargs=dict(show=True, overwrite=True), )
                thread_plotter.daemon = False
                thread_plotter.start()
                thread_plotter.join()
            else:
                self.exception_log.error("No data. DB record not created")
        finally:
            fish_db.__exit__()
            self.feed.Arduino.disable_pins(True)

    def do(self, x, y, fish_id, _version):
        time_now = int(round(time.time()))

        self.logger[fish_id].add_tracked_point(x, y)
        if time_now - self.time_last_feed > FEED_EVERY:  # feed every..
            feed_side = self.tank[fish_id].decide(x, y, _version)
        else:
            feed_side = None

        if feed_side is 'center':
            # feed_side = 'left'     # only send 'left' (socket)
            pass
        if feed_side is 'out_center':
            feed_side = None

        if feed_side is not None:
            self.total_feed[fish_id] += 1
            str_to_print = '{}\t,{}\t - \tTotal:{}'.format(fish_id, feed_side, self.total_feed[fish_id])
            self.time_last_feed = time_now

            if self.GUI_obj is not None:
                self.exception_log.feed_event(str_to_print)
            if self.chb_Var.get() == '1':
                self.feed.new_feeder_run(0, feed_side)
            else:
                pass

            self.logger[fish_id].add_feed(feed_side)

    def time_count(self):
        global time_counter
        print(time_counter)


class TimeCounter:

    def __init__(self):
        self.start_time = datetime.datetime.now()
        # debug ------
        str_year = self.start_time.year
        str_month = self.start_time.month
        str_day = self.start_time.day
        str_hr = self.start_time.hour
        str_min = self.start_time.minute
        print("date:{}/{}/{} {}:{}".format(str_year, str_month, str_day, str_hr, str_min))
        # debug ------
        # self.start_time = datetime.datetime(str_year, str_month, str_day, str_hr-1, str_min+1)
        [self.t_hr, self.t_min, self.t_sec] = \
            self.start_time.hour, \
            self.start_time.minute, \
            self.start_time.second

        self.old_t_hr = self.t_hr
        self.old_t_min = self.t_min
        self.old_t_sec = self.t_sec

        str_time_start = datetime.datetime.now()

    def get_time_str(self):
        # global str_time_start, str_time, old_str_time

        old_t_sec = self.t_sec
        [self.t_hr, self.t_min, self.t_sec] = datetime.now().hour, datetime.now().minute, datetime.now().second
        str_to_return = 0
        if not old_t_sec == self.t_sec:
            str_to_return = "{0}:{1}.{2}".format(self.t_hr, self.t_min, self.t_sec)

        return str_to_return

    def get_time_diff(self):
        now_time = datetime.datetime.now()

        old_t_sec = self.t_sec
        [self.t_hr, self.t_min, self.t_sec] = now_time.hour, now_time.minute, now_time.second
        str_to_return = 0
        if not old_t_sec == self.t_sec:
            hr_diff = self.t_hr - self.old_t_hr
            min_diff = self.t_min - self.old_t_min
            sec_diff = self.t_sec - self.old_t_sec

            str_to_return = datetime.timedelta(hours=hr_diff, minutes=min_diff, seconds=sec_diff)

        return str_to_return

    def make_two_digit_num(int_to_check):
        str_temp = '{}'.format(int_to_check)
        if int_to_check < 10: str_temp = '0{}'.format(int_to_check)
        return str_temp
