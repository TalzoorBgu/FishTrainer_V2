#! /usr/bin/env python
#
# Support module generated by PAGE version 4.10
# In conjunction with Tcl version 8.6
#    Feb 24, 2018 06:27:58 PM
#    Apr 23, 2018 08:54:50 PM


import sys
import subprocess
import threading
try:
    import scene_planner
except ImportError:
    from . import scene_planner
from .controller import Controller
from . import track_fish
# from tracker.old_tcp_client import FishClient
from time import sleep
from .track_feeder import tracker_Feeder

feed_object = tracker_Feeder()

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def set_Tk_var():
    global FeedVar1
    FeedVar1 = StringVar()
    global FeedVar2
    FeedVar2 = StringVar()
    global TraningVar
    TraningVar = StringVar()
    global chb_Var
    chb_Var = StringVar()
    global CamVar1
    CamVar1 = StringVar()

def R_Cam1Sel():
    global CamVar1
    print('ClientGUI_support.R_Cam1Sel')
    print("CamVar1.get():{}".format(CamVar1.get()))
    sys.stdout.flush()

def R1Sel():
    global FeedVar1
    print('ClientGUI_support.R1Sel')
    print("FeedVar1.get():{}".format(FeedVar1.get()))
    sys.stdout.flush()

def R2Sel():
    global FeedVar2
    print('ClientGUI_support.R2Sel')
    print("FeedVar2.get():{}".format(FeedVar2.get()))
    sys.stdout.flush()

def R3Sel():
    global TraningVar, Fish_trainingGUI
    print('ClientGUI_support.R3Sel')
    r_button_val = TraningVar.get()
    print("TraningVar.get():{}".format(r_button_val))
    motor_notification = ""

    if r_button_val is 'E':
        train_type = 'Edge'
    elif r_button_val is 'C':
        train_type = 'Center'
        motor_notification = "\tmotor B will be active"

    exception_class.info_wo_tstamp("\tSeleced traning type : {}".format(train_type))
    if motor_notification is not "":
        exception_class.info_wo_tstamp(motor_notification)

    sys.stdout.flush()

def onLogClear():
    sys.stdout.flush()
    Fish_trainingGUI.txtMainLog.delete('0.0', END)


def Feed():
    print('ClientGUI_support.Feed')
    sys.stdout.flush()

def on1L():
    # global chb_Var
    # global FeedVar
    print('ClientGUI_support.on1L')

    try:
        exception_class.info_wo_tstamp("\tTest motor - 1L")

        steps_no = Fish_trainingGUI.txtStepNum.get()
        motor = 1
        if steps_no == '':
            program = 0
            feed_object.new_feeder_run(program, motor)
        else:
            feed_object.move_steps(steps_no, motor)

        sys.stdout.flush()
    except TypeError:
        pass

def on1R():
    print('ClientGUI_support.on1R')
    try:
        exception_class.info_wo_tstamp("\tTest motor - 1R")

        steps_no = Fish_trainingGUI.txtStepNum.get()
        motor = 0
        if steps_no == '':
            program = 0
            feed_object.new_feeder_run(program, motor)
        else:
            feed_object.move_steps(steps_no, motor)

        sys.stdout.flush()
    except TypeError:
        pass

def on2L():
    print('ClientGUI_support.on2L')
    # velocity = Fish_traningGUI.txtVelocity.get()
    # acceleration = Fish_traningGUI.txtAccl.get()

    # fish_client = FishClient(Fish_traningGUI)
    # fish_client.send('test_2L', 0, Fish_traningGUI.txtStepNum.get(), velocity, acceleration)
    # fish_client.kill()

    sys.stdout.flush()

def on2R():
    print('ClientGUI_support.on2R')
    # velocity = Fish_traningGUI.txtVelocity.get()
    # acceleration = Fish_traningGUI.txtAccl.get()

    # fish_client = FishClient(Fish_traningGUI)
    # fish_client.send('test_2R', 0, Fish_traningGUI.txtStepNum.get(), velocity, acceleration)
    # fish_client.kill()
    sys.stdout.flush()

def onExit():
    global exit_flag, Fish_trainingGUI, thread_track_fish
    print('ClientGUI_support.onExit')
    sys.stdout.flush()

    # exit_var = True
    # Fish_traningGUI.stop_traning = True
    print("stop_training:{}".format(Fish_trainingGUI.stop_training))

    if Fish_trainingGUI.stop_training:
        destroy_window()
    else:
        Fish_trainingGUI.exit_flag = True
        onStopTraining()
        thread_track_fish.join()
        destroy_window()

    # destroy_window()

    # sleep(1)
    # sys.exit(1)

def onRunTraining():
    global TraningVar, thread_track_fish, controller
    sys.stdout.flush()

    Fish_trainingGUI.stop_training = False
    log_name = []
    fish_no = Fish_trainingGUI.txtFishNo1.get('0.0', 'end-1c')
    training_day = Fish_trainingGUI.txtTrainingDay1.get('0.0', 'end-1c')

    if fish_no is "" or training_day is "":
        log_name.append('test')
        exception_class.info_wo_tstamp("\t\t --- NO 'Fish no.' or 'Training day', file: test.txt ---", bold=True)
    else:
        log_name.append('F{}DAY{}'.format(fish_no, training_day))

    try:
        _tmp1 = type(controller)
        controller.__del__()
        # exception_class.info("Controller closed")
    except UnboundLocalError:
        print("there is not Controller instance")
    except NameError:
        print("name 'controller' is not defined")

    camera = CamVar1.get()

    controller = Controller(feed_object, exception_class, Fish_trainingGUI, log_name, camera)
    _tmp1 = type(controller)
    print("type:{}".format(_tmp1))

    training_type = "edge" if TraningVar.get() is 'E' else "center"
    track_loop_args = (controller, exception_class, training_type, )
    thread_track_fish = threading.Thread(target=track_fish.track_loop, args=track_loop_args)

    thread_track_fish.daemon = True
    thread_track_fish.start()

def onStopTraining():
    global Fish_trainingGUI
    sys.stdout.flush()

    # onExit()
    Fish_trainingGUI.stop_training = True
    #Fish_traningGUI.print_and_update_main_log("Stopped!")

def onSendtest():
    print('ClientGUI_support.onSendtest')
    sys.stdout.flush()
    # fish_client = FishClient()
    # fish_client.send('test', 0)
    # fish_client.kill()

def onStatClear():
    sys.stdout.flush()
    Fish_trainingGUI.txtStatLog.delete('0.0', END)


def onTankConfig():
    global CamVar1, exception_class

    print('ClientGUI_support.onTankConfig')
    sys.stdout.flush()
    relvant_camera = CamVar1.get()
    scene_planner.SP_Main(exception_class, relvant_camera)
    # thread_track_fish = threading.Thread(target=scene_planner.SP_Main, args=(CamVar1.get()))
    # thread_track_fish.start()


def onSetZero():
    print('ClientGUI_support.onSetZero')
    btn_txt = Fish_trainingGUI.btnSetZero['text']
    if btn_txt == "Set ZERO pos.":
        Fish_trainingGUI.btnSetZero.configure(text='END')
        feed_object.Arduino.disable_pins(True)
    else:
        Fish_trainingGUI.btnSetZero.configure(text='Set ZERO pos.')
        feed_object.Arduino.disable_pins(False)

    #
    # fish_client = FishClient()
    # fish_client.send(_str_to_send, 0)
    # fish_client.kill()

def onStatRun():
    global Fish_trainingGUI
    sys.stdout.flush()
    # _StatInfo = ThreadingProcess('fish_stat.py',
    #                              Fish_trainingGUI.LogFolderName,
    #                              Fish_trainingGUI.txtStatDaysBack.get('0.0', END),
    #                              Fish_trainingGUI.txtStatArgs.get('0.0', END)).run()
    # Fish_trainingGUI.txtStatLog.insert(END, _StatInfo)
    # Fish_trainingGUI.txtStatLog.see(END)
    # print ("HERE:{}".format(_StatInfo))

def init(top, gui, _exception_class,  *args, **kwargs):
    global Fish_trainingGUI, top_level, root, exception_class
    Fish_trainingGUI = gui
    top_level = top
    root = top
    exception_class = _exception_class
    # root.protocol("WM_DELETE_WINDOW", onStopTraining)
    # root.bind("<Destroy>", onStopTraining)

def destroy_window():
    global top_level, thread_track_fish, controller
    # Function which closes the window.
    # print("Quiting.")
    controller.__del__()

    top_level.destroy()
    top_level = None
    # sys.exit(0)

# class ThreadingProcess(object):
#
#     def __init__(self, file_name, arg0='', arg1='', arg2=''):
#         self.interval = 1
#         self.file_name = file_name
#         self.arg0 = arg0
#         self.arg1 = arg1
#         self.arg2 = arg2
#         print("ThreadingProcess:{}".format(file_name))
#
#
#     def runTrack(self, process):
#         try:
#
#             str_name = [sys.executable, self.file_name, self.arg0, self.arg1, self.arg2]
#             process = subprocess.Popen(str_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             output, error_output = process.communicate()
#             print(process.stdout.readline())
#         except:
#             print ('Err - Check (.py) call file')
#             if output=='': output=error_output
#
#         #return output
#
#     def run(self):
#         #print self.file_name
#         #while True:
#         #    print('Doing something imporant in the background')
#         #file = '/Users/talzoor/PycharmProjects/test/fish_stat.py'
#         try:
#             process = subprocess.Popen(['python', self.file_name, self.arg0, self.arg1, self.arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             output, error_output = process.communicate()
#
#         except:
#             print ('Err - Check (fish_stat.py) call file')
#
#         if output=='': output=error_output
#         return output


# class Counter(object):
#     def __init__(self, start=0):
#         self.lock = threading.Lock()
#         self.value = start
#
#     def increment(self):
#         logging.debug('Waiting for a lock')
#         self.lock.acquire()
#         try:
#             logging.debug('Acquired a lock')
#             self.value = self.value + 1
#         finally:
#             logging.debug('Released a lock')
#             self.lock.release()



if __name__ == '__main__':
    import ClientGUI
    ClientGUI.vp_start_gui()





