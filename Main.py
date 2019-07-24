#! /usr/bin/env python

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

try:
    from tools import exception_class
except ImportError:
    from .tools import exception_class

try:
    from tools import ClientGUI_support
except ImportError:
    from .tools import ClientGUI_support

import configparser
from datetime import datetime
import os

from pathlib import Path


Config = configparser.ConfigParser()

#Global vars
exit_var = False


def print_path():
    pass


class ConfigSectionMap:
    def __init__(self, _exception=None):
        self.exception = _exception

    def get(self, section):
        dict1 = {}

        script_dir = os.path.dirname(os.path.realpath(__file__))  # script dir
        file_name = 'GUI_config.txt'

        data_folder = Path(script_dir)
        file_to_open = data_folder / file_name

        try:
            with open(file_to_open) as f:
                Config.read_file(f)

                if Config.has_section(section):
                    options = Config.options(section)
                    for option in options:
                        try:
                            dict1[option] = Config.get(section, option)
                            if dict1[option] == -1:
                                DebugPrint("skip: %s" % option)
                        except:
                            print("exception on %s!" % option)
                            dict1[option] = None
                else:   # there is no such option
                    # print("Config file error!")
                    self.exception.error("Config file error! ({})".format(section))
                    dict1 = {}
        except FileNotFoundError:
            self.exception.error("Config file error! (FileNotFoundError), ({})".format(section))
        return dict1


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, Fish_traningGUI, root
    root = Tk()
    ClientGUI_support.set_Tk_var()
    Fish_traning_GUI = Fish_traning_GUI___Client(root)
    Excp = exception_class.RaiseException(Fish_traning_GUI)

    if ClientGUI_support.feed_object.Arduino.connection == 'NO':
        Excp.error("No Arduino conn. check serial port (USB)")

    ClientGUI_support.init(root, Fish_traning_GUI)
    root.mainloop()

Fish_traningGUI = None
def create_Fish_traning_GUI___Client(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global Fish_traningGUI, w_win, rt
    rt = root
    Fish_traningGUI = Toplevel (root)
    ClientGUI_support.set_Tk_var()
    top = Fish_traning_GUI___Client (w)
    ClientGUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Fish_traning_GUI___Client():
    global Fish_traningGUI
    Fish_traningGUI.destroy()
    Fish_traningGUI = None


class Fish_traning_GUI___Client:
    def __init__(self, top = None, excp = None):

        self.stop_traning = False
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font9 = "-family {Abadi MT Condensed Extra Bold} -size 10 "  \
            "-weight bold -slant roman -underline 0 -overstrike 0"

        top.geometry("891x800+57+75")
        top.title("Fish traning GUI - Client")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.frmTraining = Frame(top)
        self.frmTraining.place(relx=0.01, rely=0.47, relheight=0.16
                               , relwidth=0.97)
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(borderwidth="2")
        self.frmTraining.configure(relief=GROOVE)
        self.frmTraining.configure(background="#d9d9d9")
        self.frmTraining.configure(highlightbackground="#d9d9d9")
        self.frmTraining.configure(highlightcolor="black")
        self.frmTraining.configure(width=864)

        self.btnRunTraining = Button(self.frmTraining)
        self.btnRunTraining.place(relx=0.78, rely=0.5, height=50, width=90)
        self.btnRunTraining.configure(activebackground="#d9d9d9")
        self.btnRunTraining.configure(activeforeground="#000000")
        self.btnRunTraining.configure(background="#d9d9d9")
        self.btnRunTraining.configure(command=ClientGUI_support.onRunTraining)
        self.btnRunTraining.configure(disabledforeground="#a3a3a3")
        self.btnRunTraining.configure(foreground="#000000")
        self.btnRunTraining.configure(highlightbackground="#d9d9d9")
        self.btnRunTraining.configure(highlightcolor="black")
        self.btnRunTraining.configure(pady="0")
        self.btnRunTraining.configure(text='''Run traning''')

        self.Label2 = Label(self.frmTraining)
        self.Label2.place(relx=0.12, rely=0.06, height=24, width=85)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Training day''')

        self.radF1 = Radiobutton(self.frmTraining)
        self.radF1.place(relx=0.23, rely=0.19, relheight=0.19, relwidth=0.06)
        self.radF1.configure(activebackground="#d9d9d9")
        self.radF1.configure(activeforeground="#000000")
        self.radF1.configure(background="#d9d9d9")
        self.radF1.configure(command=ClientGUI_support.R1Sel)
        self.radF1.configure(disabledforeground="#a3a3a3")
        self.radF1.configure(foreground="#000000")
        self.radF1.configure(highlightbackground="#d9d9d9")
        self.radF1.configure(highlightcolor="black")
        self.radF1.configure(justify=LEFT)
        self.radF1.configure(text='''Feed''')
        self.radF1.configure(value="F")
        self.radF1.configure(variable=ClientGUI_support.FeedVar1)

        self.radN1 = Radiobutton(self.frmTraining)
        self.radN1.place(relx=0.23, rely=0.34, relheight=0.19, relwidth=0.08)
        self.radN1.configure(activebackground="#d9d9d9")
        self.radN1.configure(activeforeground="#000000")
        self.radN1.configure(background="#d9d9d9")
        self.radN1.configure(command=ClientGUI_support.R1Sel)
        self.radN1.configure(disabledforeground="#a3a3a3")
        self.radN1.configure(foreground="#000000")
        self.radN1.configure(highlightbackground="#d9d9d9")
        self.radN1.configure(highlightcolor="black")
        self.radN1.configure(justify=LEFT)
        self.radN1.configure(text='''No feed''')
        self.radN1.configure(value="NF")
        self.radN1.configure(variable=ClientGUI_support.FeedVar1)

        self.Label1 = Label(self.frmTraining)
        self.Label1.place(relx=0.01, rely=0.06, height=24, width=57)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Fish no.''')

        self.txtArgs = Text(self.frmTraining)
        self.txtArgs.place(relx=0.52, rely=0.67, relheight=0.24, relwidth=0.25)
        self.txtArgs.configure(background="white")
        self.txtArgs.configure(font=font9)
        self.txtArgs.configure(foreground="black")
        self.txtArgs.configure(highlightbackground="#d9d9d9")
        self.txtArgs.configure(highlightcolor="black")
        self.txtArgs.configure(insertbackground="black")
        self.txtArgs.configure(selectbackground="#c4c4c4")
        self.txtArgs.configure(selectforeground="black")
        self.txtArgs.configure(undo="1")
        self.txtArgs.configure(width=218)
        self.txtArgs.configure(wrap=WORD)

        self.Label10 = Label(self.frmTraining)
        self.Label10.place(relx=0.52, rely=0.43, height=21, width=65)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(disabledforeground="#a3a3a3")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''Arguments''')

        self.btnStopTraning = Button(self.frmTraining)
        self.btnStopTraning.place(relx=0.89, rely=0.5, height=50, width=90)
        self.btnStopTraning.configure(activebackground="#d9d9d9")
        self.btnStopTraning.configure(activeforeground="#000000")
        self.btnStopTraning.configure(background="#d9d9d9")
        self.btnStopTraning.configure(command=ClientGUI_support.onStopTraining)
        self.btnStopTraning.configure(disabledforeground="#a3a3a3")
        self.btnStopTraning.configure(foreground="#000000")
        self.btnStopTraning.configure(highlightbackground="#d9d9d9")
        self.btnStopTraning.configure(highlightcolor="black")
        self.btnStopTraning.configure(pady="0")
        self.btnStopTraning.configure(text='''Stop traning''')

        self.txtFishNo1 = Text(self.frmTraining)
        self.txtFishNo1.place(relx=0.02, rely=0.23, relheight=0.24, relwidth=0.1)

        self.txtFishNo1.configure(background="white")
        self.txtFishNo1.configure(font=font9)
        self.txtFishNo1.configure(foreground="black")
        self.txtFishNo1.configure(highlightbackground="#d9d9d9")
        self.txtFishNo1.configure(highlightcolor="black")
        self.txtFishNo1.configure(insertbackground="black")
        self.txtFishNo1.configure(selectbackground="#c4c4c4")
        self.txtFishNo1.configure(selectforeground="black")
        self.txtFishNo1.configure(undo="1")
        self.txtFishNo1.configure(width=90)
        self.txtFishNo1.configure(wrap=WORD)

        self.txtTrainingDay1 = Text(self.frmTraining)
        self.txtTrainingDay1.place(relx=0.14, rely=0.24, relheight=0.24
                                   , relwidth=0.09)
        self.txtTrainingDay1.configure(background="white")
        self.txtTrainingDay1.configure(font=font9)
        self.txtTrainingDay1.configure(foreground="black")
        self.txtTrainingDay1.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay1.configure(highlightcolor="black")
        self.txtTrainingDay1.configure(insertbackground="black")
        self.txtTrainingDay1.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay1.configure(selectforeground="black")
        self.txtTrainingDay1.configure(undo="1")
        self.txtTrainingDay1.configure(width=82)
        self.txtTrainingDay1.configure(wrap=WORD)

        self.txtFishNo2 = Text(self.frmTraining)
        self.txtFishNo2.place(relx=0.02, rely=0.55, relheight=0.24, relwidth=0.1)

        self.txtFishNo2.configure(background="white")
        self.txtFishNo2.configure(font=font9)
        self.txtFishNo2.configure(foreground="black")
        self.txtFishNo2.configure(highlightbackground="#d9d9d9")
        self.txtFishNo2.configure(highlightcolor="black")
        self.txtFishNo2.configure(insertbackground="black")
        self.txtFishNo2.configure(selectbackground="#c4c4c4")
        self.txtFishNo2.configure(selectforeground="black")
        self.txtFishNo2.configure(undo="1")
        self.txtFishNo2.configure(width=90)
        self.txtFishNo2.configure(wrap=WORD)

        self.txtTrainingDay2 = Text(self.frmTraining)
        self.txtTrainingDay2.place(relx=0.14, rely=0.55, relheight=0.24
                                   , relwidth=0.09)
        self.txtTrainingDay2.configure(background="white")
        self.txtTrainingDay2.configure(font=font9)
        self.txtTrainingDay2.configure(foreground="black")
        self.txtTrainingDay2.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay2.configure(highlightcolor="black")
        self.txtTrainingDay2.configure(insertbackground="black")
        self.txtTrainingDay2.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay2.configure(selectforeground="black")
        self.txtTrainingDay2.configure(undo="1")
        self.txtTrainingDay2.configure(width=82)
        self.txtTrainingDay2.configure(wrap=WORD)

        self.radF2 = Radiobutton(self.frmTraining)
        self.radF2.place(relx=0.23, rely=0.5, relheight=0.19, relwidth=0.06)
        self.radF2.configure(activebackground="#d9d9d9")
        self.radF2.configure(activeforeground="#000000")
        self.radF2.configure(background="#d9d9d9")
        self.radF2.configure(command=ClientGUI_support.R2Sel)
        self.radF2.configure(disabledforeground="#a3a3a3")
        self.radF2.configure(foreground="#000000")
        self.radF2.configure(highlightbackground="#d9d9d9")
        self.radF2.configure(highlightcolor="black")
        self.radF2.configure(justify=LEFT)
        self.radF2.configure(text='''Feed''')
        self.radF2.configure(value="F")
        self.radF2.configure(variable=ClientGUI_support.FeedVar2)

        self.radN2 = Radiobutton(self.frmTraining)
        self.radN2.place(relx=0.23, rely=0.65, relheight=0.19, relwidth=0.08)
        self.radN2.configure(activebackground="#d9d9d9")
        self.radN2.configure(activeforeground="#000000")
        self.radN2.configure(background="#d9d9d9")
        self.radN2.configure(command=ClientGUI_support.R2Sel)
        self.radN2.configure(disabledforeground="#a3a3a3")
        self.radN2.configure(foreground="#000000")
        self.radN2.configure(highlightbackground="#d9d9d9")
        self.radN2.configure(highlightcolor="black")
        self.radN2.configure(justify=LEFT)
        self.radN2.configure(text='''No feed''')
        self.radN2.configure(value="NF")
        self.radN2.configure(variable=ClientGUI_support.FeedVar2)

        self.radCam1 = Radiobutton(self.frmTraining)
        self.radCam1.place(relx=0.32, rely=0.19, relheight=0.19, relwidth=0.09)
        self.radCam1.configure(activebackground="#d9d9d9")
        self.radCam1.configure(activeforeground="#000000")
        self.radCam1.configure(background="#d9d9d9")
        self.radCam1.configure(command=ClientGUI_support.R1Sel)
        self.radCam1.configure(disabledforeground="#a3a3a3")
        self.radCam1.configure(foreground="#000000")
        self.radCam1.configure(highlightbackground="#d9d9d9")
        self.radCam1.configure(highlightcolor="black")
        self.radCam1.configure(justify=LEFT)
        self.radCam1.configure(text='''Camera 1''')
        self.radCam1.configure(value="0")
        self.radCam1.configure(variable=ClientGUI_support.CamVar1)

        self.fra38_rad41 = Radiobutton(self.frmTraining)
        self.fra38_rad41.place(relx=0.0, rely=0.0, relheight=0.01, relwidth=0.0)
        self.fra38_rad41.configure(activebackground="#d9d9d9")
        self.fra38_rad41.configure(activeforeground="#000000")
        self.fra38_rad41.configure(background="#d9d9d9")
        self.fra38_rad41.configure(command=ClientGUI_support.R1Sel)
        self.fra38_rad41.configure(disabledforeground="#a3a3a3")
        self.fra38_rad41.configure(foreground="#000000")
        self.fra38_rad41.configure(highlightbackground="#d9d9d9")
        self.fra38_rad41.configure(highlightcolor="black")
        self.fra38_rad41.configure(justify=LEFT)
        self.fra38_rad41.configure(text='''Feed''')
        self.fra38_rad41.configure(value="F")
        self.fra38_rad41.configure(variable=ClientGUI_support.FeedVar1)

        self.fra38_rad42 = Radiobutton(self.frmTraining)
        self.fra38_rad42.place(relx=0.0, rely=0.0, relheight=0.01, relwidth=0.0)
        self.fra38_rad42.configure(activebackground="#d9d9d9")
        self.fra38_rad42.configure(activeforeground="#000000")
        self.fra38_rad42.configure(background="#d9d9d9")
        self.fra38_rad42.configure(command=ClientGUI_support.R1Sel)
        self.fra38_rad42.configure(disabledforeground="#a3a3a3")
        self.fra38_rad42.configure(foreground="#000000")
        self.fra38_rad42.configure(highlightbackground="#d9d9d9")
        self.fra38_rad42.configure(highlightcolor="black")
        self.fra38_rad42.configure(justify=LEFT)
        self.fra38_rad42.configure(text='''Feed''')
        self.fra38_rad42.configure(value="F")
        self.fra38_rad42.configure(variable=ClientGUI_support.FeedVar1)

        self.radCam2 = Radiobutton(self.frmTraining)
        self.radCam2.place(relx=0.32, rely=0.34, relheight=0.19, relwidth=0.09)
        self.radCam2.configure(activebackground="#d9d9d9")
        self.radCam2.configure(activeforeground="#000000")
        self.radCam2.configure(background="#d9d9d9")
        self.radCam2.configure(command=ClientGUI_support.R1Sel)
        self.radCam2.configure(disabledforeground="#a3a3a3")
        self.radCam2.configure(foreground="#000000")
        self.radCam2.configure(highlightbackground="#d9d9d9")
        self.radCam2.configure(highlightcolor="black")
        self.radCam2.configure(justify=LEFT)
        self.radCam2.configure(text='''Camera 2''')
        self.radCam2.configure(value="1")
        self.radCam2.configure(variable=ClientGUI_support.CamVar1)

        self.btnTankConf = Button(self.frmTraining)
        self.btnTankConf.place(relx=0.42, rely=0.08, height=112, width=73)
        self.btnTankConf.configure(activebackground="#d9d9d9")
        self.btnTankConf.configure(activeforeground="#000000")
        self.btnTankConf.configure(background="#d9d9d9")
        self.btnTankConf.configure(command=ClientGUI_support.onTankConfig)
        self.btnTankConf.configure(disabledforeground="#a3a3a3")
        self.btnTankConf.configure(foreground="#000000")
        self.btnTankConf.configure(highlightbackground="#d9d9d9")
        self.btnTankConf.configure(highlightcolor="black")
        self.btnTankConf.configure(pady="0")
        self.btnTankConf.configure(text='''Tank conf.''')

        self.radF1_2 = Radiobutton(self.frmTraining)
        self.radF1_2.place(relx=0.9, rely=0.15, relheight=0.17, relwidth=0.08)
        self.radF1_2.configure(activebackground="#d9d9d9")
        self.radF1_2.configure(activeforeground="#000000")
        self.radF1_2.configure(background="#d9d9d9")
        self.radF1_2.configure(command=ClientGUI_support.R3Sel)
        self.radF1_2.configure(disabledforeground="#a3a3a3")
        self.radF1_2.configure(foreground="#000000")
        self.radF1_2.configure(highlightbackground="#d9d9d9")
        self.radF1_2.configure(highlightcolor="black")
        self.radF1_2.configure(justify=LEFT)
        self.radF1_2.configure(text='''Center''')
        self.radF1_2.configure(value="C")
        self.radF1_2.configure(variable=ClientGUI_support.TraningVar)
        self.radF1_2.configure(width=70)

        self.radF1_1 = Radiobutton(self.frmTraining)
        self.radF1_1.place(relx=0.82, rely=0.15, relheight=0.17, relwidth=0.08)
        self.radF1_1.configure(activebackground="#d9d9d9")
        self.radF1_1.configure(activeforeground="#000000")
        self.radF1_1.configure(background="#d9d9d9")
        self.radF1_1.configure(command=ClientGUI_support.R3Sel)
        self.radF1_1.configure(disabledforeground="#a3a3a3")
        self.radF1_1.configure(foreground="#000000")
        self.radF1_1.configure(highlightbackground="#d9d9d9")
        self.radF1_1.configure(highlightcolor="black")
        self.radF1_1.configure(justify=LEFT)
        self.radF1_1.configure(text='''Edge''')
        self.radF1_1.configure(value="E")
        self.radF1_1.configure(variable=ClientGUI_support.TraningVar)

        self.btnExit = Button(top)
        self.btnExit.place(relx=0.78, rely=0.94, height=40, width=177)
        self.btnExit.configure(activebackground="#d9d9d9")
        self.btnExit.configure(activeforeground="#000000")
        self.btnExit.configure(background="#d9d9d9")
        self.btnExit.configure(command=ClientGUI_support.onExit)
        self.btnExit.configure(disabledforeground="#a3a3a3")
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        self.btnExit.configure(pady="0")
        self.btnExit.configure(text='''Exit''')

        self.frmStat = Frame(top)
        self.frmStat.place(relx=0.02, rely=0.01, relheight=0.33, relwidth=0.97)
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(borderwidth="2")
        self.frmStat.configure(relief=GROOVE)
        self.frmStat.configure(background="#d9d9d9")
        self.frmStat.configure(highlightbackground="#d9d9d9")
        self.frmStat.configure(highlightcolor="black")
        self.frmStat.configure(width=864)

        self.Label3 = Label(self.frmStat)
        self.Label3.place(relx=0.01, rely=0.03, height=21, width=75)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Fish statistics''')

        self.btnStatClear = Button(self.frmStat)
        self.btnStatClear.place(relx=0.01, rely=0.84, height=30, width=62)
        self.btnStatClear.configure(activebackground="#d9d9d9")
        self.btnStatClear.configure(activeforeground="#000000")
        self.btnStatClear.configure(background="#d9d9d9")
        self.btnStatClear.configure(command=ClientGUI_support.onStatClear)
        self.btnStatClear.configure(disabledforeground="#a3a3a3")
        self.btnStatClear.configure(foreground="#000000")
        self.btnStatClear.configure(highlightbackground="#d9d9d9")
        self.btnStatClear.configure(highlightcolor="black")
        self.btnStatClear.configure(pady="0")
        self.btnStatClear.configure(text='''Clear''')

        self.btnStatRun = Button(self.frmStat)
        self.btnStatRun.place(relx=0.81, rely=0.81, height=38, width=141)
        self.btnStatRun.configure(activebackground="#d9d9d9")
        self.btnStatRun.configure(activeforeground="#000000")
        self.btnStatRun.configure(background="#d9d9d9")
        self.btnStatRun.configure(command=ClientGUI_support.onStatRun)
        self.btnStatRun.configure(disabledforeground="#a3a3a3")
        self.btnStatRun.configure(foreground="#000000")
        self.btnStatRun.configure(highlightbackground="#d9d9d9")
        self.btnStatRun.configure(highlightcolor="black")
        self.btnStatRun.configure(pady="0")
        self.btnStatRun.configure(text='''Run''')

        self.Label9 = Label(self.frmStat)
        self.Label9.place(relx=0.36, rely=0.03, height=24, width=89)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(disabledforeground="#a3a3a3")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''Log folder''')

        self.txtStatLog = Text(self.frmStat)
        self.txtStatLog.place(relx=0.01, rely=0.15, relheight=0.63
                              , relwidth=0.97)
        self.txtStatLog.configure(background="white")
        self.txtStatLog.configure(font="TkTextFont")
        self.txtStatLog.configure(foreground="black")
        self.txtStatLog.configure(highlightbackground="#d9d9d9")
        self.txtStatLog.configure(highlightcolor="black")
        self.txtStatLog.configure(insertbackground="black")
        self.txtStatLog.configure(selectbackground="#c4c4c4")
        self.txtStatLog.configure(selectforeground="black")
        self.txtStatLog.configure(undo="1")
        self.txtStatLog.configure(width=842)
        self.txtStatLog.configure(wrap=WORD)

        self.Label11 = Label(self.frmStat)
        self.Label11.place(relx=0.09, rely=0.81, height=21, width=59)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(activeforeground="black")
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(disabledforeground="#a3a3a3")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#d9d9d9")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(text='''Days back''')

        self.txtStatDaysBack = Text(self.frmStat)
        self.txtStatDaysBack.place(relx=0.19, rely=0.81, relheight=0.09
                                   , relwidth=0.08)
        self.txtStatDaysBack.configure(background="white")
        self.txtStatDaysBack.configure(font=font9)
        self.txtStatDaysBack.configure(foreground="black")
        self.txtStatDaysBack.configure(highlightbackground="#d9d9d9")
        self.txtStatDaysBack.configure(highlightcolor="black")
        self.txtStatDaysBack.configure(insertbackground="black")
        self.txtStatDaysBack.configure(selectbackground="#c4c4c4")
        self.txtStatDaysBack.configure(selectforeground="black")
        self.txtStatDaysBack.configure(undo="1")
        self.txtStatDaysBack.configure(width=66)
        self.txtStatDaysBack.configure(wrap=WORD)

        self.Label12 = Label(self.frmStat)
        self.Label12.place(relx=0.28, rely=0.81, height=21, width=28)
        self.Label12.configure(activebackground="#f9f9f9")
        self.Label12.configure(activeforeground="black")
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(disabledforeground="#a3a3a3")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(highlightbackground="#d9d9d9")
        self.Label12.configure(highlightcolor="black")
        self.Label12.configure(text='''Arg.''')

        self.txtStatArgs = Text(self.frmStat)
        self.txtStatArgs.place(relx=0.33, rely=0.81, relheight=0.09
                               , relwidth=0.09)
        self.txtStatArgs.configure(background="white")
        self.txtStatArgs.configure(font=font9)
        self.txtStatArgs.configure(foreground="black")
        self.txtStatArgs.configure(highlightbackground="#d9d9d9")
        self.txtStatArgs.configure(highlightcolor="black")
        self.txtStatArgs.configure(insertbackground="black")
        self.txtStatArgs.configure(selectbackground="#c4c4c4")
        self.txtStatArgs.configure(selectforeground="black")
        self.txtStatArgs.configure(undo="1")
        self.txtStatArgs.configure(width=74)
        self.txtStatArgs.configure(wrap=WORD)

        self.Label13 = Label(self.frmStat)
        self.Label13.place(relx=0.09, rely=0.9, height=21, width=50)
        self.Label13.configure(activebackground="#f9f9f9")
        self.Label13.configure(activeforeground="black")
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(disabledforeground="#a3a3a3")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(highlightbackground="#d9d9d9")
        self.Label13.configure(highlightcolor="black")
        self.Label13.configure(text='''Run arg.''')

        self.txtStatRunArgs = Text(self.frmStat)
        self.txtStatRunArgs.place(relx=0.19, rely=0.9, relheight=0.09
                                  , relwidth=0.6)
        self.txtStatRunArgs.configure(background="white")
        self.txtStatRunArgs.configure(font=font9)
        self.txtStatRunArgs.configure(foreground="black")
        self.txtStatRunArgs.configure(highlightbackground="#d9d9d9")
        self.txtStatRunArgs.configure(highlightcolor="black")
        self.txtStatRunArgs.configure(insertbackground="black")
        self.txtStatRunArgs.configure(selectbackground="#c4c4c4")
        self.txtStatRunArgs.configure(selectforeground="black")
        self.txtStatRunArgs.configure(undo="1")
        self.txtStatRunArgs.configure(width=378)
        self.txtStatRunArgs.configure(wrap=WORD)

        self.txtLogFolder = Text(self.frmStat)
        self.txtLogFolder.place(relx=0.46, rely=0.03, relheight=0.09
                                , relwidth=0.51)
        self.txtLogFolder.configure(background="white")
        self.txtLogFolder.configure(font=font9)
        self.txtLogFolder.configure(foreground="black")
        self.txtLogFolder.configure(highlightbackground="#d9d9d9")
        self.txtLogFolder.configure(highlightcolor="black")
        self.txtLogFolder.configure(insertbackground="black")
        self.txtLogFolder.configure(selectbackground="#c4c4c4")
        self.txtLogFolder.configure(selectforeground="black")
        self.txtLogFolder.configure(undo="1")
        self.txtLogFolder.configure(width=442)
        self.txtLogFolder.configure(wrap=WORD)

        self.frmCom = Frame(top)
        self.frmCom.place(relx=0.01, rely=0.35, relheight=0.11, relwidth=0.97)
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(borderwidth="2")
        self.frmCom.configure(relief=GROOVE)
        self.frmCom.configure(background="#d9d9d9")
        self.frmCom.configure(highlightbackground="#d9d9d9")
        self.frmCom.configure(highlightcolor="black")
        self.frmCom.configure(width=864)

        self.Label4 = Label(self.frmCom)
        self.Label4.place(relx=0.01, rely=0.09, height=21, width=93)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Communication''')

        self.txtServerIP = Entry(self.frmCom)
        self.txtServerIP.place(relx=0.02, rely=0.62, height=20, relwidth=0.19)
        self.txtServerIP.configure(background="white")
        self.txtServerIP.configure(disabledforeground="#a3a3a3")
        self.txtServerIP.configure(font="TkFixedFont")
        self.txtServerIP.configure(foreground="#000000")
        self.txtServerIP.configure(highlightbackground="#d9d9d9")
        self.txtServerIP.configure(highlightcolor="black")
        self.txtServerIP.configure(insertbackground="black")
        self.txtServerIP.configure(selectbackground="#c4c4c4")
        self.txtServerIP.configure(selectforeground="black")

        self.Label5 = Label(self.frmCom)
        self.Label5.place(relx=0.02, rely=0.35, height=21, width=54)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Server IP:''')

        self.btnComSend = Button(self.frmCom)
        self.btnComSend.place(relx=0.21, rely=0.18, height=62, width=103)
        self.btnComSend.configure(activebackground="#d9d9d9")
        self.btnComSend.configure(activeforeground="#000000")
        self.btnComSend.configure(background="#d9d9d9")
        self.btnComSend.configure(command=ClientGUI_support.onSendtest)
        self.btnComSend.configure(disabledforeground="#a3a3a3")
        self.btnComSend.configure(foreground="#000000")
        self.btnComSend.configure(highlightbackground="#d9d9d9")
        self.btnComSend.configure(highlightcolor="black")
        self.btnComSend.configure(pady="0")
        self.btnComSend.configure(text='''Send test''')

        self.Label6 = Label(self.frmCom)
        self.Label6.place(relx=0.63, rely=0.22, height=21, width=61)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''Motor test''')

        self.btnMotor1L = Button(self.frmCom)
        self.btnMotor1L.place(relx=0.73, rely=0.11, height=38, width=57)
        self.btnMotor1L.configure(activebackground="#d9d9d9")
        self.btnMotor1L.configure(activeforeground="#000000")
        self.btnMotor1L.configure(background="#d9d9d9")
        self.btnMotor1L.configure(command=ClientGUI_support.on1L)
        self.btnMotor1L.configure(disabledforeground="#a3a3a3")
        self.btnMotor1L.configure(foreground="#000000")
        self.btnMotor1L.configure(highlightbackground="#d9d9d9")
        self.btnMotor1L.configure(highlightcolor="black")
        self.btnMotor1L.configure(pady="0")
        self.btnMotor1L.configure(text='''(1) Left''')

        self.btnMotor1R = Button(self.frmCom)
        self.btnMotor1R.place(relx=0.73, rely=0.55, height=38, width=57)
        self.btnMotor1R.configure(activebackground="#d9d9d9")
        self.btnMotor1R.configure(activeforeground="#000000")
        self.btnMotor1R.configure(background="#d9d9d9")
        self.btnMotor1R.configure(command=ClientGUI_support.on1R)
        self.btnMotor1R.configure(disabledforeground="#a3a3a3")
        self.btnMotor1R.configure(foreground="#000000")
        self.btnMotor1R.configure(highlightbackground="#d9d9d9")
        self.btnMotor1R.configure(highlightcolor="black")
        self.btnMotor1R.configure(pady="0")
        self.btnMotor1R.configure(text='''(1) Right''')

        self.btnMotor2R = Button(self.frmCom)
        self.btnMotor2R.place(relx=0.8, rely=0.55, height=38, width=57)
        self.btnMotor2R.configure(activebackground="#d9d9d9")
        self.btnMotor2R.configure(activeforeground="#000000")
        self.btnMotor2R.configure(background="#d9d9d9")
        self.btnMotor2R.configure(command=ClientGUI_support.on2R)
        self.btnMotor2R.configure(disabledforeground="#a3a3a3")
        self.btnMotor2R.configure(foreground="#000000")
        self.btnMotor2R.configure(highlightbackground="#d9d9d9")
        self.btnMotor2R.configure(highlightcolor="black")
        self.btnMotor2R.configure(pady="0")
        self.btnMotor2R.configure(text='''(2) Right''')

        self.btnMotor2L = Button(self.frmCom)
        self.btnMotor2L.place(relx=0.8, rely=0.11, height=38, width=57)
        self.btnMotor2L.configure(activebackground="#d9d9d9")
        self.btnMotor2L.configure(activeforeground="#000000")
        self.btnMotor2L.configure(background="#d9d9d9")
        self.btnMotor2L.configure(command=ClientGUI_support.on2L)
        self.btnMotor2L.configure(disabledforeground="#a3a3a3")
        self.btnMotor2L.configure(foreground="#000000")
        self.btnMotor2L.configure(highlightbackground="#d9d9d9")
        self.btnMotor2L.configure(highlightcolor="black")
        self.btnMotor2L.configure(pady="0")
        self.btnMotor2L.configure(text='''(2) Left''')

        self.Label7 = Label(self.frmCom)
        self.Label7.place(relx=0.64, rely=0.44, height=21, width=79)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Steps number''')

        self.txtStepNum = Entry(self.frmCom)
        self.txtStepNum.place(relx=0.63, rely=0.66, height=27, relwidth=0.09)
        self.txtStepNum.configure(background="white")
        self.txtStepNum.configure(disabledforeground="#a3a3a3")
        self.txtStepNum.configure(font="TkFixedFont")
        self.txtStepNum.configure(foreground="#000000")
        self.txtStepNum.configure(highlightbackground="#d9d9d9")
        self.txtStepNum.configure(highlightcolor="black")
        self.txtStepNum.configure(insertbackground="black")
        self.txtStepNum.configure(selectbackground="#c4c4c4")
        self.txtStepNum.configure(selectforeground="black")

        self.txtVelocity = Entry(self.frmCom)
        self.txtVelocity.place(relx=0.51, rely=0.33, height=27, relwidth=0.09)
        self.txtVelocity.configure(background="white")
        self.txtVelocity.configure(disabledforeground="#a3a3a3")
        self.txtVelocity.configure(font="TkFixedFont")
        self.txtVelocity.configure(foreground="#000000")
        self.txtVelocity.configure(highlightbackground="#d9d9d9")
        self.txtVelocity.configure(highlightcolor="black")
        self.txtVelocity.configure(insertbackground="black")
        self.txtVelocity.configure(selectbackground="#c4c4c4")
        self.txtVelocity.configure(selectforeground="black")

        self.txtAccl = Entry(self.frmCom)
        self.txtAccl.place(relx=0.51, rely=0.66, height=27, relwidth=0.09)
        self.txtAccl.configure(background="white")
        self.txtAccl.configure(disabledforeground="#a3a3a3")
        self.txtAccl.configure(font="TkFixedFont")
        self.txtAccl.configure(foreground="#000000")
        self.txtAccl.configure(highlightbackground="#d9d9d9")
        self.txtAccl.configure(highlightcolor="black")
        self.txtAccl.configure(insertbackground="black")
        self.txtAccl.configure(selectbackground="#c4c4c4")
        self.txtAccl.configure(selectforeground="black")

        self.chb_NewMotor = Checkbutton(self.frmCom)
        self.chb_NewMotor.place(relx=0.89, rely=0.11, relheight=0.38
                                , relwidth=0.08)
        self.chb_NewMotor.configure(activebackground="#d9d9d9")
        self.chb_NewMotor.configure(activeforeground="#000000")
        self.chb_NewMotor.configure(background="#d9d9d9")
        self.chb_NewMotor.configure(disabledforeground="#a3a3a3")
        self.chb_NewMotor.configure(foreground="#000000")
        self.chb_NewMotor.configure(highlightbackground="#d9d9d9")
        self.chb_NewMotor.configure(highlightcolor="black")
        self.chb_NewMotor.configure(justify=LEFT)
        self.chb_NewMotor.configure(text='''Red Feeder''')
        self.chb_NewMotor.configure(variable=ClientGUI_support.chb_Var)
        self.chb_NewMotor.configure(wraplength="35")

        self.btnSetZero = Button(self.frmCom)
        self.btnSetZero.place(relx=0.89, rely=0.55, height=38, width=87)
        self.btnSetZero.configure(activebackground="#d9d9d9")
        self.btnSetZero.configure(activeforeground="#000000")
        self.btnSetZero.configure(background="#d9d9d9")
        self.btnSetZero.configure(command=ClientGUI_support.onSetZero)
        self.btnSetZero.configure(disabledforeground="#a3a3a3")
        self.btnSetZero.configure(foreground="#000000")
        self.btnSetZero.configure(highlightbackground="#d9d9d9")
        self.btnSetZero.configure(highlightcolor="black")
        self.btnSetZero.configure(pady="0")
        self.btnSetZero.configure(text='''Set ZERO pos.''')

        self.Label7_3 = Label(self.frmCom)
        self.Label7_3.place(relx=0.46, rely=0.38, height=21, width=39)
        self.Label7_3.configure(activebackground="#f9f9f9")
        self.Label7_3.configure(activeforeground="black")
        self.Label7_3.configure(background="#d9d9d9")
        self.Label7_3.configure(disabledforeground="#a3a3a3")
        self.Label7_3.configure(foreground="#000000")
        self.Label7_3.configure(highlightbackground="#d9d9d9")
        self.Label7_3.configure(highlightcolor="black")
        self.Label7_3.configure(text='''Vel''')

        self.Label7_4 = Label(self.frmCom)
        self.Label7_4.place(relx=0.46, rely=0.66, height=21, width=39)
        self.Label7_4.configure(activebackground="#f9f9f9")
        self.Label7_4.configure(activeforeground="black")
        self.Label7_4.configure(background="#d9d9d9")
        self.Label7_4.configure(disabledforeground="#a3a3a3")
        self.Label7_4.configure(foreground="#000000")
        self.Label7_4.configure(highlightbackground="#d9d9d9")
        self.Label7_4.configure(highlightcolor="black")
        self.Label7_4.configure(text='''Accl''')

        self.frmLog = Frame(top)
        self.frmLog.place(relx=0.02, rely=0.64, relheight=0.29, relwidth=0.97)
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(borderwidth="2")
        self.frmLog.configure(relief=GROOVE)
        self.frmLog.configure(background="#d9d9d9")
        self.frmLog.configure(highlightbackground="#d9d9d9")
        self.frmLog.configure(highlightcolor="black")
        self.frmLog.configure(width=861)

        self.Label8 = Label(self.frmLog)
        self.Label8.place(relx=0.01, rely=0.03, height=21, width=26)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(activeforeground="black")
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(disabledforeground="#a3a3a3")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#d9d9d9")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(text='''Log''')

        self.txtMainLog = Text(self.frmLog)
        self.txtMainLog.place(relx=0.01, rely=0.14, relheight=0.75
                              , relwidth=0.98)
        self.txtMainLog.configure(background="white")
        self.txtMainLog.configure(font="TkTextFont")
        self.txtMainLog.configure(foreground="black")
        self.txtMainLog.configure(highlightbackground="#d9d9d9")
        self.txtMainLog.configure(highlightcolor="black")
        self.txtMainLog.configure(insertbackground="black")
        self.txtMainLog.configure(selectbackground="#c4c4c4")
        self.txtMainLog.configure(selectforeground="black")
        self.txtMainLog.configure(undo="1")
        self.txtMainLog.configure(width=842)
        self.txtMainLog.configure(wrap=WORD)

        self.frmLogClear = Button(self.frmLog)
        self.frmLogClear.place(relx=0.01, rely=0.89, height=22, width=70)
        self.frmLogClear.configure(activebackground="#d9d9d9")
        self.frmLogClear.configure(activeforeground="#000000")
        self.frmLogClear.configure(background="#d9d9d9")
        self.frmLogClear.configure(command=ClientGUI_support.onLogClear)
        self.frmLogClear.configure(disabledforeground="#a3a3a3")
        self.frmLogClear.configure(foreground="#000000")
        self.frmLogClear.configure(highlightbackground="#d9d9d9")
        self.frmLogClear.configure(highlightcolor="black")
        self.frmLogClear.configure(pady="0")
        self.frmLogClear.configure(text='''Clear''')

        self.Label14 = Label(self.frmLog)
        self.Label14.place(relx=0.13, rely=0.03, height=21, width=74)
        self.Label14.configure(activebackground="#f9f9f9")
        self.Label14.configure(activeforeground="black")
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(disabledforeground="#a3a3a3")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(highlightbackground="#d9d9d9")
        self.Label14.configure(highlightcolor="black")
        self.Label14.configure(text='''Time runing:''')

        self.Label15 = Label(self.frmLog)
        self.Label15.place(relx=0.24, rely=0.03, height=24, width=121)
        self.Label15.configure(activebackground="#f9f9f9")
        self.Label15.configure(activeforeground="black")
        self.Label15.configure(background="#d9d9d9")
        self.Label15.configure(disabledforeground="#a3a3a3")
        self.Label15.configure(font=font9)
        self.Label15.configure(foreground="#0000fe")
        self.Label15.configure(highlightbackground="#d9d9d9")
        self.Label15.configure(highlightcolor="black")
        self.Label15.configure(text='''00:00''')

        self.menubar = Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.Exception = exception_class.RaiseException(self)

        self.vars_init()
        self.fillValue()
        self.print_and_update_main_log("{} ---Started---".format(self.time_stamp()))


    def vars_init(self):
        self.LogFolderName = ""
        self.Stat_days = ""
        self.Stat_arg = ""
        self.ServerIP = ""
        self.Args = ""

    def fillValue(self):
        ConfigVals = ConfigSectionMap(self.Exception)
        self.chb_Var = ClientGUI_support.chb_Var

        fish_statistics_dict = ConfigVals.get("Fish Statistics")
        communication_dist = ConfigVals.get("Communication")
        fish_dict = ConfigVals.get("Fish")

        if fish_statistics_dict=={}:
            pass
        else:
            self.LogFolderName = fish_statistics_dict['log folder']
            self.Stat_days = fish_statistics_dict['days back']
            self.Stat_arg = fish_statistics_dict['arg']
        #self.Red_Feeder = ConfigSectionMap("Motor")['redFeeder']

        if communication_dist == {}:
            pass
        else:
            self.ServerIP = communication_dist['server ip']

        if fish_dict == {}:
            pass
        else:
            Arg1 = fish_dict['argument1']
            Arg2 = fish_dict['argument2']
            self.Args = '{} {}'.format(Arg1, Arg2)

        #print self.Args

        self.txtLogFolder.insert('0.0', self.LogFolderName)
        self.txtServerIP.insert('0', self.ServerIP)
        self.txtArgs.insert('0.0', self.Args)
        self.txtStatDaysBack.insert('0.0', self.Stat_days)
        self.txtStatArgs.insert('0.0', self.Stat_arg)
        temp_run_arg = "{} {} {} {}".format('fish_stat.py', self.LogFolderName, self.Stat_days, self.Stat_arg)
        self.txtStatRunArgs.insert('0.0', temp_run_arg)
        ClientGUI_support.chb_Var.set('1') # NEW feeder
        ClientGUI_support.FeedVar1.set('F')
        ClientGUI_support.FeedVar2.set('F')
        ClientGUI_support.CamVar1.set('0')
        ClientGUI_support.TraningVar.set('E')
        # self.chb_NewMotor.setvar(ClientGUI_support.chb_Var, '1')
        #check = True
        #print('self.chb_NewMotor:{}'.format(self.chb_NewMotor.getboolean(check)))

    def print_and_update_main_log(self, str_to_print, new_line=True):
        global Fish_traningGUI, top
        str_temp = '{}'.format(str_to_print)
        print (str_temp)
        if new_line: str_temp = '{}\n'.format(str_temp)
        self.txtMainLog.insert(END, str_temp)
        self.txtMainLog.see(END)

    def update_time(self, time_str):
        _str_time_array = str(time_str).split(':')
        _str_time_array = list(map(int, _str_time_array))

        _str_hr = _str_time_array[0]
        _str_min = _str_time_array[1]
        _str_sec = _str_time_array[2]
        # time_str = '{}:{}:{}'.format(_str_hr, _str_min, _str_sec)

        if _str_min < 20:
            self.Label15.configure(text=time_str)
        else:  # >20 --> make it green
            self.Label15.configure(text=time_str, fg='#5eaf24')


        def __call__(self):
            print("RUN Command")

    def time_stamp(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


def make_two_digit_num(int_to_check):
    str_temp = '{}'.format(int_to_check)
    if int_to_check < 10:
        str_temp = '0{}'.format(int_to_check)
    return str_temp



if __name__ == '__main__':
    vp_start_gui()
