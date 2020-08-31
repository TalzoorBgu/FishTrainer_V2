#! /usr/bin/env python3

import sys
from sys import platform as sys_pf
# import fcntl
import platform
import configparser
from datetime import datetime
import os
from pathlib import Path
import tools.log as fish_log
from tools.fish import ArduinoFunctions
from datetime import timedelta
import _thread

# from tendo import singleton

try:
    import Tkinter as tk
    from Tkinter.font import Font
except ImportError:
    import tkinter as tk
    from tkinter.font import Font

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

try:
    import tools.ClientGUI_V2_support as ClientGUI_V2_support
except ImportError:
    from .tools import ClientGUI_V2_support as ClientGUI_V2_support
#
# pid_file = 'lock_file.pid'
# fp = open(pid_file, 'w')
# try:
#     fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
# except IOError:
#     # another instance is running
#     print("another instance is running")
#     sys.exit(0)

# ##########

# try:
#     single_check = singleton.SingleInstance()    # will sys.exit(-1) if other instance is running
#     print("Lock file:{}".format(single_check.lockfile))
# except singleton.SingleInstanceException:
#     print("Bye.")
#     sys.exit(-1)

Config = configparser.ConfigParser()
script_dir = os.path.dirname(os.path.realpath(__file__))  # script dir

# Global vars
exit_flag = False


class ConfigSectionMap:
    def __init__(self, _exception=None):
        self.exception = _exception
        self.file_name_short = 'GUI_config.txt'

        data_folder = Path(script_dir)
        file_to_open = data_folder / self.file_name_short
        self.file_name_long = file_to_open

    def get(self, section):
        dict1 = {}

        try:
            with open(self.file_name_long) as f:
                try:
                    Config.read_file(f)
                except configparser.DuplicateOptionError:
                    self.exception.error("Config file error! 'DuplicateOptionError'")
                    exit(1)

                if Config.has_section(section):
                    options = Config.options(section)
                    for option in options:
                        try:
                            dict1[option] = Config.get(section, option)
                        except:
                            print("exception on %s!" % option)
                            dict1[option] = None
                else:  # there is no such option
                    # print("Config file error!")
                    self.exception.error("Config file error! ({})".format(section))
                    dict1 = {}
        except FileNotFoundError:
            self.exception.error("Config file error! (FileNotFoundError), ({})".format(section))
        return dict1


class MainGUI:
    # '__init__from_page' function created with 'page' app - .tcl files
    # and pasted here.
    def __init__from_page(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("880x748+321+67")
        top.title("Fish training GUI V2 - Client")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.frmTraining = tk.Frame(top)
        self.frmTraining.place(relx=0.25, rely=0.388, relheight=0.175
                               , relwidth=0.743)
        self.frmTraining.configure(relief='groove')
        self.frmTraining.configure(borderwidth="2")
        self.frmTraining.configure(relief="groove")
        self.frmTraining.configure(background="#d9d9d9")
        self.frmTraining.configure(highlightbackground="#d9d9d9")
        self.frmTraining.configure(highlightcolor="black")
        self.frmTraining.configure(width=654)

        self.btnRunTraining = tk.Button(self.frmTraining)
        self.btnRunTraining.place(relx=0.856, rely=0.076, height=50, width=80)
        self.btnRunTraining.configure(activebackground="#d9d9d9")
        self.btnRunTraining.configure(activeforeground="#000000")
        self.btnRunTraining.configure(background="#d9d9d9")
        self.btnRunTraining.configure(command=ClientGUI_V2_support.onRunTraining)
        self.btnRunTraining.configure(foreground="#000000")
        self.btnRunTraining.configure(highlightbackground="#d9d9d9")
        self.btnRunTraining.configure(highlightcolor="black")
        self.btnRunTraining.configure(pady="0")
        self.btnRunTraining.configure(text='''Run training''')
        self.btnRunTraining.configure(wraplength="50")

        self.Label2 = tk.Label(self.frmTraining)
        self.Label2.place(relx=0.428, rely=0.076, height=24, width=85)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Training day''')

        self.radF1 = tk.Radiobutton(self.frmTraining)
        self.radF1.place(relx=0.505, rely=0.229, relheight=0.168, relwidth=0.089)

        self.radF1.configure(activebackground="#d9d9d9")
        self.radF1.configure(activeforeground="#000000")
        self.radF1.configure(background="#d9d9d9")
        self.radF1.configure(command=ClientGUI_V2_support.R1Sel)
        self.radF1.configure(foreground="#000000")
        self.radF1.configure(highlightbackground="#d9d9d9")
        self.radF1.configure(highlightcolor="black")
        self.radF1.configure(justify='left')
        self.radF1.configure(text='''Feed''')
        self.radF1.configure(value="F")
        self.radF1.configure(variable=ClientGUI_V2_support.FeedVar1)

        self.radN1 = tk.Radiobutton(self.frmTraining)
        self.radN1.place(relx=0.505, rely=0.382, relheight=0.168, relwidth=0.118)

        self.radN1.configure(activebackground="#d9d9d9")
        self.radN1.configure(activeforeground="#000000")
        self.radN1.configure(background="#d9d9d9")
        self.radN1.configure(command=ClientGUI_V2_support.R1Sel)
        self.radN1.configure(foreground="#000000")
        self.radN1.configure(highlightbackground="#d9d9d9")
        self.radN1.configure(highlightcolor="black")
        self.radN1.configure(justify='left')
        self.radN1.configure(text='''No feed''')
        self.radN1.configure(value="NF")
        self.radN1.configure(variable=ClientGUI_V2_support.FeedVar1)

        self.Label1 = tk.Label(self.frmTraining)
        self.Label1.place(relx=0.336, rely=0.076, height=24, width=57)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Fish no.''')

        self.btnStopTraining = tk.Button(self.frmTraining)
        self.btnStopTraining.place(relx=0.856, rely=0.534, height=50, width=80)
        self.btnStopTraining.configure(activebackground="#d9d9d9")
        self.btnStopTraining.configure(activeforeground="#000000")
        self.btnStopTraining.configure(background="#d9d9d9")
        self.btnStopTraining.configure(command=ClientGUI_V2_support.onStopTraining)
        self.btnStopTraining.configure(foreground="#000000")
        self.btnStopTraining.configure(highlightbackground="#d9d9d9")
        self.btnStopTraining.configure(highlightcolor="black")
        self.btnStopTraining.configure(pady="0")
        self.btnStopTraining.configure(text='''Stop training''')
        self.btnStopTraining.configure(wraplength="50")

        self.txtFishNo1 = tk.Text(self.frmTraining)
        self.txtFishNo1.place(relx=0.352, rely=0.229, relheight=0.244
                              , relwidth=0.092)
        self.txtFishNo1.configure(background="white")
        self.txtFishNo1.configure(font="TkTextFont")
        self.txtFishNo1.configure(foreground="black")
        self.txtFishNo1.configure(highlightbackground="#d9d9d9")
        self.txtFishNo1.configure(highlightcolor="black")
        self.txtFishNo1.configure(insertbackground="black")
        self.txtFishNo1.configure(selectbackground="#c4c4c4")
        self.txtFishNo1.configure(selectforeground="black")
        self.txtFishNo1.configure(undo="1")
        self.txtFishNo1.configure(width=60)
        self.txtFishNo1.configure(wrap="word")

        self.txtTrainingDay1 = tk.Text(self.frmTraining)
        self.txtTrainingDay1.place(relx=0.443, rely=0.229, relheight=0.244
                                   , relwidth=0.064)
        self.txtTrainingDay1.configure(background="white")
        self.txtTrainingDay1.configure(font="TkTextFont")
        self.txtTrainingDay1.configure(foreground="black")
        self.txtTrainingDay1.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay1.configure(highlightcolor="black")
        self.txtTrainingDay1.configure(insertbackground="black")
        self.txtTrainingDay1.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay1.configure(selectforeground="black")
        self.txtTrainingDay1.configure(undo="1")
        self.txtTrainingDay1.configure(width=42)
        self.txtTrainingDay1.configure(wrap="word")

        self.txtFishNo2 = tk.Text(self.frmTraining)
        self.txtFishNo2.place(relx=0.352, rely=0.534, relheight=0.244
                              , relwidth=0.092)
        self.txtFishNo2.configure(background="white")
        self.txtFishNo2.configure(font="TkTextFont")
        self.txtFishNo2.configure(foreground="black")
        self.txtFishNo2.configure(highlightbackground="#d9d9d9")
        self.txtFishNo2.configure(highlightcolor="black")
        self.txtFishNo2.configure(insertbackground="black")
        self.txtFishNo2.configure(selectbackground="#c4c4c4")
        self.txtFishNo2.configure(selectforeground="black")
        self.txtFishNo2.configure(undo="1")
        self.txtFishNo2.configure(width=60)
        self.txtFishNo2.configure(wrap="word")

        self.txtTrainingDay2 = tk.Text(self.frmTraining)
        self.txtTrainingDay2.place(relx=0.443, rely=0.534, relheight=0.244
                                   , relwidth=0.064)
        self.txtTrainingDay2.configure(background="white")
        self.txtTrainingDay2.configure(font="TkTextFont")
        self.txtTrainingDay2.configure(foreground="black")
        self.txtTrainingDay2.configure(highlightbackground="#d9d9d9")
        self.txtTrainingDay2.configure(highlightcolor="black")
        self.txtTrainingDay2.configure(insertbackground="black")
        self.txtTrainingDay2.configure(selectbackground="#c4c4c4")
        self.txtTrainingDay2.configure(selectforeground="black")
        self.txtTrainingDay2.configure(undo="1")
        self.txtTrainingDay2.configure(width=42)
        self.txtTrainingDay2.configure(wrap="word")

        self.radF2 = tk.Radiobutton(self.frmTraining)
        self.radF2.place(relx=0.505, rely=0.534, relheight=0.168, relwidth=0.089)

        self.radF2.configure(activebackground="#d9d9d9")
        self.radF2.configure(activeforeground="#000000")
        self.radF2.configure(background="#d9d9d9")
        self.radF2.configure(command=ClientGUI_V2_support.R2Sel)
        self.radF2.configure(foreground="#000000")
        self.radF2.configure(highlightbackground="#d9d9d9")
        self.radF2.configure(highlightcolor="black")
        self.radF2.configure(justify='left')
        self.radF2.configure(text='''Feed''')
        self.radF2.configure(value="F")
        self.radF2.configure(variable=ClientGUI_V2_support.FeedVar2)

        self.radN2 = tk.Radiobutton(self.frmTraining)
        self.radN2.place(relx=0.505, rely=0.687, relheight=0.168, relwidth=0.118)

        self.radN2.configure(activebackground="#d9d9d9")
        self.radN2.configure(activeforeground="#000000")
        self.radN2.configure(background="#d9d9d9")
        self.radN2.configure(command=ClientGUI_V2_support.R2Sel)
        self.radN2.configure(foreground="#000000")
        self.radN2.configure(highlightbackground="#d9d9d9")
        self.radN2.configure(highlightcolor="black")
        self.radN2.configure(justify='left')
        self.radN2.configure(text='''No feed''')
        self.radN2.configure(value="NF")
        self.radN2.configure(variable=ClientGUI_V2_support.FeedVar2)

        self.radCam1 = tk.Radiobutton(self.frmTraining)
        self.radCam1.place(relx=0.015, rely=0.076, relheight=0.168
                           , relwidth=0.133)
        self.radCam1.configure(activebackground="#d9d9d9")
        self.radCam1.configure(activeforeground="#000000")
        self.radCam1.configure(background="#d9d9d9")
        self.radCam1.configure(foreground="#000000")
        self.radCam1.configure(highlightbackground="#d9d9d9")
        self.radCam1.configure(highlightcolor="black")
        self.radCam1.configure(justify='left')
        self.radCam1.configure(text='''Camera 1''')
        self.radCam1.configure(value="0")
        self.radCam1.configure(variable=ClientGUI_V2_support.CamVar1)

        self.fra38_rad41 = tk.Radiobutton(self.frmTraining)
        self.fra38_rad41.place(relx=0.0, rely=0.0, relheight=0.008
                               , relwidth=0.002)
        self.fra38_rad41.configure(activebackground="#d9d9d9")
        self.fra38_rad41.configure(activeforeground="#000000")
        self.fra38_rad41.configure(background="#d9d9d9")
        self.fra38_rad41.configure(command=ClientGUI_V2_support.R1Sel)
        self.fra38_rad41.configure(foreground="#000000")
        self.fra38_rad41.configure(highlightbackground="#d9d9d9")
        self.fra38_rad41.configure(highlightcolor="black")
        self.fra38_rad41.configure(justify='left')
        self.fra38_rad41.configure(text='''Feed''')
        self.fra38_rad41.configure(value="F")
        self.fra38_rad41.configure(variable=ClientGUI_V2_support.FeedVar1)

        self.fra38_rad42 = tk.Radiobutton(self.frmTraining)
        self.fra38_rad42.place(relx=0.0, rely=0.0, relheight=0.008
                               , relwidth=0.002)
        self.fra38_rad42.configure(activebackground="#d9d9d9")
        self.fra38_rad42.configure(activeforeground="#000000")
        self.fra38_rad42.configure(background="#d9d9d9")
        self.fra38_rad42.configure(command=ClientGUI_V2_support.R1Sel)
        self.fra38_rad42.configure(foreground="#000000")
        self.fra38_rad42.configure(highlightbackground="#d9d9d9")
        self.fra38_rad42.configure(highlightcolor="black")
        self.fra38_rad42.configure(justify='left')
        self.fra38_rad42.configure(text='''Feed''')
        self.fra38_rad42.configure(value="F")
        self.fra38_rad42.configure(variable=ClientGUI_V2_support.FeedVar1)

        self.radCam2 = tk.Radiobutton(self.frmTraining)
        self.radCam2.place(relx=0.015, rely=0.229, relheight=0.168
                           , relwidth=0.133)
        self.radCam2.configure(activebackground="#d9d9d9")
        self.radCam2.configure(activeforeground="#000000")
        self.radCam2.configure(background="#d9d9d9")
        self.radCam2.configure(foreground="#000000")
        self.radCam2.configure(highlightbackground="#d9d9d9")
        self.radCam2.configure(highlightcolor="black")
        self.radCam2.configure(justify='left')
        self.radCam2.configure(text='''Camera 2''')
        self.radCam2.configure(value="1")
        self.radCam2.configure(variable=ClientGUI_V2_support.CamVar1)

        self.btnTankConf = tk.Button(self.frmTraining)
        self.btnTankConf.place(relx=0.015, rely=0.458, height=62, width=93)
        self.btnTankConf.configure(activebackground="#d9d9d9")
        self.btnTankConf.configure(activeforeground="#000000")
        self.btnTankConf.configure(background="#d9d9d9")
        self.btnTankConf.configure(command=ClientGUI_V2_support.onTankConfig)
        self.btnTankConf.configure(foreground="#000000")
        self.btnTankConf.configure(highlightbackground="#d9d9d9")
        self.btnTankConf.configure(highlightcolor="black")
        self.btnTankConf.configure(pady="0")
        self.btnTankConf.configure(text='''Tank conf.''')

        self.radF1_2 = tk.Radiobutton(self.frmTraining)
        self.radF1_2.place(relx=0.183, rely=0.458, relheight=0.168
                           , relwidth=0.122)
        self.radF1_2.configure(activebackground="#d9d9d9")
        self.radF1_2.configure(activeforeground="#000000")
        self.radF1_2.configure(background="#d9d9d9")
        self.radF1_2.configure(command=ClientGUI_V2_support.R3Sel)
        self.radF1_2.configure(foreground="#000000")
        self.radF1_2.configure(highlightbackground="#d9d9d9")
        self.radF1_2.configure(highlightcolor="black")
        self.radF1_2.configure(justify='left')
        self.radF1_2.configure(text='''Center''')
        self.radF1_2.configure(value="C")
        self.radF1_2.configure(variable=ClientGUI_V2_support.TrainingVar)

        self.radF1_1 = tk.Radiobutton(self.frmTraining)
        self.radF1_1.place(relx=0.183, rely=0.305, relheight=0.168
                           , relwidth=0.107)
        self.radF1_1.configure(activebackground="#d9d9d9")
        self.radF1_1.configure(activeforeground="#000000")
        self.radF1_1.configure(background="#d9d9d9")
        self.radF1_1.configure(command=ClientGUI_V2_support.R3Sel)
        self.radF1_1.configure(foreground="#000000")
        self.radF1_1.configure(highlightbackground="#d9d9d9")
        self.radF1_1.configure(highlightcolor="black")
        self.radF1_1.configure(justify='left')
        self.radF1_1.configure(text='''Edge''')
        self.radF1_1.configure(value="E")
        self.radF1_1.configure(variable=ClientGUI_V2_support.TrainingVar)

        self.Label5 = tk.Label(self.frmTraining)
        self.Label5.place(relx=0.183, rely=0.076, height=24, width=90)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(text='''Training type''')

        self.Label6 = tk.Label(self.frmTraining)
        self.Label6.place(relx=0.321, rely=0.229, height=24, width=19)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(text='''1''')

        self.Label10 = tk.Label(self.frmTraining)
        self.Label10.place(relx=0.321, rely=0.534, height=24, width=19)
        self.Label10.configure(activebackground="#f9f9f9")
        self.Label10.configure(activeforeground="black")
        self.Label10.configure(background="#d9d9d9")
        self.Label10.configure(foreground="#000000")
        self.Label10.configure(highlightbackground="#d9d9d9")
        self.Label10.configure(highlightcolor="black")
        self.Label10.configure(text='''2''')

        self.TSeparator1 = ttk.Separator(self.frmTraining)
        self.TSeparator1.place(relx=0.168, rely=0.076, relheight=0.763)
        self.TSeparator1.configure(orient="vertical")

        self.TSeparator2 = ttk.Separator(self.frmTraining)
        self.TSeparator2.place(relx=0.321, rely=0.076, relheight=0.763)
        self.TSeparator2.configure(orient="vertical")

        self.Label15 = tk.Label(self.frmTraining)
        self.Label15.place(relx=0.657, rely=0.076, height=24, width=93)
        self.Label15.configure(activebackground="#f9f9f9")
        self.Label15.configure(activeforeground="black")
        self.Label15.configure(background="#d9d9d9")
        self.Label15.configure(foreground="#000000")
        self.Label15.configure(highlightbackground="#d9d9d9")
        self.Label15.configure(highlightcolor="black")
        self.Label15.configure(text='''Training time:''')

        self.chbtn_StopTraining = tk.Checkbutton(self.frmTraining)
        self.chbtn_StopTraining.place(relx=0.657, rely=0.229, relheight=0.168
                                      , relwidth=0.136)
        self.chbtn_StopTraining.configure(activebackground="#d9d9d9")
        self.chbtn_StopTraining.configure(activeforeground="#000000")
        self.chbtn_StopTraining.configure(background="#d9d9d9")
        self.chbtn_StopTraining.configure(command=ClientGUI_V2_support.OnChkStopTraining)
        self.chbtn_StopTraining.configure(foreground="#000000")
        self.chbtn_StopTraining.configure(highlightbackground="#d9d9d9")
        self.chbtn_StopTraining.configure(highlightcolor="black")
        self.chbtn_StopTraining.configure(justify='left')
        self.chbtn_StopTraining.configure(text='''Stop after''')
        self.chbtn_StopTraining.configure(variable=ClientGUI_V2_support.chVar_stop_tr)

        self.TSeparator4 = ttk.Separator(self.frmTraining)
        self.TSeparator4.place(relx=0.642, rely=0.076, relheight=0.763)
        self.TSeparator4.configure(orient="vertical")

        self.TSeparator5 = ttk.Separator(self.frmTraining)
        self.TSeparator5.place(relx=0.841, rely=0.076, relheight=0.763)
        self.TSeparator5.configure(orient="vertical")

        self.txtTrainingStop = tk.Entry(self.frmTraining)
        self.txtTrainingStop.place(relx=0.657, rely=0.611, height=27
                                   , relwidth=0.171)
        self.txtTrainingStop.configure(background="white")
        self.txtTrainingStop.configure(font="TkFixedFont")
        self.txtTrainingStop.configure(foreground="#000000")
        self.txtTrainingStop.configure(highlightbackground="#d9d9d9")
        self.txtTrainingStop.configure(highlightcolor="black")
        self.txtTrainingStop.configure(insertbackground="black")
        self.txtTrainingStop.configure(justify='center')
        self.txtTrainingStop.configure(selectbackground="#c4c4c4")
        self.txtTrainingStop.configure(selectforeground="black")
        self.txtTrainingStop.configure(textvariable=ClientGUI_V2_support.txtTrainingStop)

        self.Label17 = tk.Label(self.frmTraining)
        self.Label17.place(relx=0.65, rely=0.458, height=24, width=118)
        self.Label17.configure(activebackground="#f9f9f9")
        self.Label17.configure(activeforeground="black")
        self.Label17.configure(background="#d9d9d9")
        self.Label17.configure(font="self.myFont_small")
        self.Label17.configure(foreground="#000000")
        self.Label17.configure(highlightbackground="#d9d9d9")
        self.Label17.configure(highlightcolor="black")
        self.Label17.configure(text='''format- 00:00:00''')

        self.btnExit = tk.Button(top)
        self.btnExit.place(relx=0.784, rely=0.936, height=40, width=177)
        self.btnExit.configure(activebackground="#d9d9d9")
        self.btnExit.configure(activeforeground="#000000")
        self.btnExit.configure(background="#d9d9d9")
        self.btnExit.configure(command=ClientGUI_V2_support.onExit)
        self.btnExit.configure(foreground="#000000")
        self.btnExit.configure(highlightbackground="#d9d9d9")
        self.btnExit.configure(highlightcolor="black")
        self.btnExit.configure(pady="0")
        self.btnExit.configure(text='''Exit''')

        self.frmStat = tk.Frame(top)
        self.frmStat.place(relx=0.011, rely=0.013, relheight=0.361
                           , relwidth=0.983)
        self.frmStat.configure(relief='groove')
        self.frmStat.configure(borderwidth="2")
        self.frmStat.configure(relief="groove")
        self.frmStat.configure(background="#d9d9d9")
        self.frmStat.configure(highlightbackground="#d9d9d9")
        self.frmStat.configure(highlightcolor="black")
        self.frmStat.configure(width=864)

        self.Label3 = tk.Label(self.frmStat)
        self.Label3.place(relx=0.006, rely=0.019, height=24, width=94)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Fish statistics''')

        self.btnStatClear = tk.Button(self.frmStat)
        self.btnStatClear.place(relx=0.006, rely=0.833, height=30, width=62)
        self.btnStatClear.configure(activebackground="#d9d9d9")
        self.btnStatClear.configure(activeforeground="#000000")
        self.btnStatClear.configure(background="#d9d9d9")
        self.btnStatClear.configure(command=ClientGUI_V2_support.onStatClear)
        self.btnStatClear.configure(foreground="#000000")
        self.btnStatClear.configure(highlightbackground="#d9d9d9")
        self.btnStatClear.configure(highlightcolor="black")
        self.btnStatClear.configure(pady="0")
        self.btnStatClear.configure(text='''Clear''')

        self.btnDB_refresh = tk.Button(self.frmStat)
        self.btnDB_refresh.place(relx=0.543, rely=0.815, height=38, width=141)
        self.btnDB_refresh.configure(activebackground="#d9d9d9")
        self.btnDB_refresh.configure(activeforeground="#000000")
        self.btnDB_refresh.configure(background="#d9d9d9")
        self.btnDB_refresh.configure(command=ClientGUI_V2_support.OnRefresh)
        self.btnDB_refresh.configure(foreground="#000000")
        self.btnDB_refresh.configure(highlightbackground="#d9d9d9")
        self.btnDB_refresh.configure(highlightcolor="black")
        self.btnDB_refresh.configure(pady="0")
        self.btnDB_refresh.configure(text='''Refresh''')

        self.Label9 = tk.Label(self.frmStat)
        self.Label9.place(relx=0.15, rely=0.037, height=24, width=89)
        self.Label9.configure(activebackground="#f9f9f9")
        self.Label9.configure(activeforeground="black")
        self.Label9.configure(background="#d9d9d9")
        self.Label9.configure(foreground="#000000")
        self.Label9.configure(highlightbackground="#d9d9d9")
        self.Label9.configure(highlightcolor="black")
        self.Label9.configure(text='''Main folder:''')

        self.Label11 = tk.Label(self.frmStat)
        self.Label11.place(relx=0.116, rely=0.889, height=24, width=77)
        self.Label11.configure(activebackground="#f9f9f9")
        self.Label11.configure(activeforeground="black")
        self.Label11.configure(background="#d9d9d9")
        self.Label11.configure(foreground="#000000")
        self.Label11.configure(highlightbackground="#d9d9d9")
        self.Label11.configure(highlightcolor="black")
        self.Label11.configure(text='''Days back''')

        self.txtStatDaysBack = tk.Text(self.frmStat)
        self.txtStatDaysBack.place(relx=0.208, rely=0.889, relheight=0.089
                                   , relwidth=0.076)
        self.txtStatDaysBack.configure(background="white")
        self.txtStatDaysBack.configure(font="TkTextFont")
        self.txtStatDaysBack.configure(foreground="black")
        self.txtStatDaysBack.configure(highlightbackground="#d9d9d9")
        self.txtStatDaysBack.configure(highlightcolor="black")
        self.txtStatDaysBack.configure(insertbackground="black")
        self.txtStatDaysBack.configure(selectbackground="#c4c4c4")
        self.txtStatDaysBack.configure(selectforeground="black")
        self.txtStatDaysBack.configure(undo="1")
        self.txtStatDaysBack.configure(width=66)
        self.txtStatDaysBack.configure(wrap="word")

        self.txtMainFolder = tk.Text(self.frmStat)
        self.txtMainFolder.place(relx=0.254, rely=0.037, relheight=0.089
                                 , relwidth=0.731)
        self.txtMainFolder.configure(background="white")
        self.txtMainFolder.configure(font="TkTextFont")
        self.txtMainFolder.configure(foreground="black")
        self.txtMainFolder.configure(highlightbackground="#d9d9d9")
        self.txtMainFolder.configure(highlightcolor="black")
        self.txtMainFolder.configure(insertbackground="black")
        self.txtMainFolder.configure(selectbackground="#c4c4c4")
        self.txtMainFolder.configure(selectforeground="black")
        self.txtMainFolder.configure(undo="1")
        self.txtMainFolder.configure(width=632)
        self.txtMainFolder.configure(wrap="word")

        self.Frame1 = tk.Frame(self.frmStat)
        self.Frame1.place(relx=0.012, rely=0.148, relheight=0.648
                          , relwidth=0.711)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=615)

        self.style.configure('Treeview.Heading', font="TkDefaultFont")
        self.DB = ScrolledTreeView(self.Frame1)
        self.DB.place(relx=0.016, rely=0.057, relheight=0.874, relwidth=0.976)
        self.DB.configure(columns="Col1")
        # build_treeview_support starting.
        self.DB.heading("#0", text="Tree")
        self.DB.heading("#0", anchor="center")
        self.DB.column("#0", width="293")
        self.DB.column("#0", minwidth="20")
        self.DB.column("#0", stretch="1")
        self.DB.column("#0", anchor="w")
        self.DB.heading("Col1", text="Col1")
        self.DB.heading("Col1", anchor="center")
        self.DB.column("Col1", width="293")
        self.DB.column("Col1", minwidth="20")
        self.DB.column("Col1", stretch="1")
        self.DB.column("Col1", anchor="w")

        self.Label13 = tk.Label(self.frmStat)
        self.Label13.place(relx=0.74, rely=0.167, height=24, width=76)
        self.Label13.configure(activebackground="#f9f9f9")
        self.Label13.configure(activeforeground="black")
        self.Label13.configure(background="#d9d9d9")
        self.Label13.configure(foreground="#000000")
        self.Label13.configure(highlightbackground="#d9d9d9")
        self.Label13.configure(highlightcolor="black")
        self.Label13.configure(text='''Log folder''')

        self.Label16 = tk.Label(self.frmStat)
        self.Label16.place(relx=0.74, rely=0.426, height=24, width=95)
        self.Label16.configure(activebackground="#f9f9f9")
        self.Label16.configure(activeforeground="black")
        self.Label16.configure(background="#d9d9d9")
        self.Label16.configure(foreground="#000000")
        self.Label16.configure(highlightbackground="#d9d9d9")
        self.Label16.configure(highlightcolor="black")
        self.Label16.configure(text='''Database file''')

        self.txtLogFolder = tk.Text(self.frmStat)
        self.txtLogFolder.place(relx=0.74, rely=0.259, relheight=0.093
                                , relwidth=0.249)
        self.txtLogFolder.configure(background="white")
        self.txtLogFolder.configure(font="TkTextFont")
        self.txtLogFolder.configure(foreground="black")
        self.txtLogFolder.configure(highlightbackground="#d9d9d9")
        self.txtLogFolder.configure(highlightcolor="black")
        self.txtLogFolder.configure(insertbackground="black")
        self.txtLogFolder.configure(selectbackground="#c4c4c4")
        self.txtLogFolder.configure(selectforeground="black")
        self.txtLogFolder.configure(width=218)
        self.txtLogFolder.configure(wrap="word")

        self.txtDBfile = tk.Text(self.frmStat)
        self.txtDBfile.place(relx=0.74, rely=0.5, relheight=0.093
                             , relwidth=0.249)
        self.txtDBfile.configure(background="white")
        self.txtDBfile.configure(font="TkTextFont")
        self.txtDBfile.configure(foreground="black")
        self.txtDBfile.configure(highlightbackground="#d9d9d9")
        self.txtDBfile.configure(highlightcolor="black")
        self.txtDBfile.configure(insertbackground="black")
        self.txtDBfile.configure(selectbackground="#c4c4c4")
        self.txtDBfile.configure(selectforeground="black")
        self.txtDBfile.configure(width=218)
        self.txtDBfile.configure(wrap="word")

        self.Label12 = tk.Label(self.frmStat)
        self.Label12.place(relx=0.104, rely=0.815, height=24, width=41)
        self.Label12.configure(activebackground="#f9f9f9")
        self.Label12.configure(activeforeground="black")
        self.Label12.configure(background="#d9d9d9")
        self.Label12.configure(foreground="#000000")
        self.Label12.configure(highlightbackground="#d9d9d9")
        self.Label12.configure(highlightcolor="black")
        self.Label12.configure(text='''Filter''')

        self.btnOpenLogFolder = tk.Button(self.frmStat)
        self.btnOpenLogFolder.place(relx=0.913, rely=0.352, height=32, width=52)
        self.btnOpenLogFolder.configure(activebackground="#d9d9d9")
        self.btnOpenLogFolder.configure(activeforeground="#000000")
        self.btnOpenLogFolder.configure(background="#d9d9d9")
        self.btnOpenLogFolder.configure(command=ClientGUI_V2_support.onOpenFolder)
        self.btnOpenLogFolder.configure(foreground="#000000")
        self.btnOpenLogFolder.configure(highlightbackground="#d9d9d9")
        self.btnOpenLogFolder.configure(highlightcolor="black")
        self.btnOpenLogFolder.configure(relief="raised")
        self.btnOpenLogFolder.configure(text='''Open''')

        self.btnShowDBfile = tk.Button(self.frmStat)
        self.btnShowDBfile.place(relx=0.913, rely=0.593, height=32, width=52)
        self.btnShowDBfile.configure(activebackground="#d9d9d9")
        self.btnShowDBfile.configure(activeforeground="#000000")
        self.btnShowDBfile.configure(background="#d9d9d9")
        self.btnShowDBfile.configure(command=ClientGUI_V2_support.onShowDBFile)
        self.btnShowDBfile.configure(foreground="#000000")
        self.btnShowDBfile.configure(highlightbackground="#d9d9d9")
        self.btnShowDBfile.configure(highlightcolor="black")
        self.btnShowDBfile.configure(relief="raised")
        self.btnShowDBfile.configure(text='''Show''')

        self.TSeparator3 = ttk.Separator(self.frmStat)
        self.TSeparator3.place(relx=0.728, rely=0.148, relheight=0.778)
        self.TSeparator3.configure(orient="vertical")

        self.txtConfigFile = tk.Text(self.frmStat)
        self.txtConfigFile.place(relx=0.74, rely=0.741, relheight=0.093
                                 , relwidth=0.249)
        self.txtConfigFile.configure(background="white")
        self.txtConfigFile.configure(font="TkTextFont")
        self.txtConfigFile.configure(foreground="black")
        self.txtConfigFile.configure(highlightbackground="#d9d9d9")
        self.txtConfigFile.configure(highlightcolor="black")
        self.txtConfigFile.configure(insertbackground="black")
        self.txtConfigFile.configure(selectbackground="#c4c4c4")
        self.txtConfigFile.configure(selectforeground="black")
        self.txtConfigFile.configure(width=218)
        self.txtConfigFile.configure(wrap="word")

        self.btnShowConfig = tk.Button(self.frmStat)
        self.btnShowConfig.place(relx=0.913, rely=0.833, height=32, width=52)
        self.btnShowConfig.configure(activebackground="#d9d9d9")
        self.btnShowConfig.configure(activeforeground="#000000")
        self.btnShowConfig.configure(background="#d9d9d9")
        self.btnShowConfig.configure(foreground="#000000")
        self.btnShowConfig.configure(highlightbackground="#d9d9d9")
        self.btnShowConfig.configure(highlightcolor="black")
        self.btnShowConfig.configure(text='''Show''')
        self.btnShowConfig.configure(command=ClientGUI_V2_support.onShowConfigFile)


        self.Label18 = tk.Label(self.frmStat)
        self.Label18.place(relx=0.74, rely=0.648, height=24, width=72)
        self.Label18.configure(background="#d9d9d9")
        self.Label18.configure(foreground="#000000")
        self.Label18.configure(text='''Config file''')

        self.frmCom = tk.Frame(top)
        self.frmCom.place(relx=0.011, rely=0.388, relheight=0.175
                          , relwidth=0.232)
        self.frmCom.configure(relief='groove')
        self.frmCom.configure(borderwidth="2")
        self.frmCom.configure(relief="groove")
        self.frmCom.configure(background="#d9d9d9")
        self.frmCom.configure(highlightbackground="#d9d9d9")
        self.frmCom.configure(highlightcolor="black")
        self.frmCom.configure(width=204)

        self.Label4 = tk.Label(self.frmCom)
        self.Label4.place(relx=0.025, rely=0.038, height=24, width=73)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Motor test''')

        self.btnMotor1L = tk.Button(self.frmCom)
        self.btnMotor1L.place(relx=0.588, rely=0.153, height=48, width=37)
        self.btnMotor1L.configure(activebackground="#d9d9d9")
        self.btnMotor1L.configure(activeforeground="#000000")
        self.btnMotor1L.configure(background="#d9d9d9")
        self.btnMotor1L.configure(command=ClientGUI_V2_support.on1L)
        self.btnMotor1L.configure(foreground="#000000")
        self.btnMotor1L.configure(highlightbackground="#d9d9d9")
        self.btnMotor1L.configure(highlightcolor="black")
        self.btnMotor1L.configure(pady="0")
        self.btnMotor1L.configure(text='''(1)L''')

        self.btnMotor1R = tk.Button(self.frmCom)
        self.btnMotor1R.place(relx=0.588, rely=0.534, height=48, width=37)
        self.btnMotor1R.configure(activebackground="#d9d9d9")
        self.btnMotor1R.configure(activeforeground="#000000")
        self.btnMotor1R.configure(background="#d9d9d9")
        self.btnMotor1R.configure(command=ClientGUI_V2_support.on1R)
        self.btnMotor1R.configure(foreground="#000000")
        self.btnMotor1R.configure(highlightbackground="#d9d9d9")
        self.btnMotor1R.configure(highlightcolor="black")
        self.btnMotor1R.configure(pady="0")
        self.btnMotor1R.configure(text='''(1)R''')

        self.btnMotor2R = tk.Button(self.frmCom)
        self.btnMotor2R.place(relx=0.784, rely=0.534, height=48, width=37)
        self.btnMotor2R.configure(activebackground="#d9d9d9")
        self.btnMotor2R.configure(activeforeground="#000000")
        self.btnMotor2R.configure(background="#d9d9d9")
        self.btnMotor2R.configure(command=ClientGUI_V2_support.on2R)
        self.btnMotor2R.configure(foreground="#000000")
        self.btnMotor2R.configure(highlightbackground="#d9d9d9")
        self.btnMotor2R.configure(highlightcolor="black")
        self.btnMotor2R.configure(pady="0")
        self.btnMotor2R.configure(text='''(2)R''')

        self.btnMotor2L = tk.Button(self.frmCom)
        self.btnMotor2L.place(relx=0.784, rely=0.153, height=48, width=37)
        self.btnMotor2L.configure(activebackground="#d9d9d9")
        self.btnMotor2L.configure(activeforeground="#000000")
        self.btnMotor2L.configure(background="#d9d9d9")
        self.btnMotor2L.configure(command=ClientGUI_V2_support.on2L)
        self.btnMotor2L.configure(foreground="#000000")
        self.btnMotor2L.configure(highlightbackground="#d9d9d9")
        self.btnMotor2L.configure(highlightcolor="black")
        self.btnMotor2L.configure(pady="0")
        self.btnMotor2L.configure(text='''(2)L''')

        self.Label7 = tk.Label(self.frmCom)
        self.Label7.place(relx=0.049, rely=0.229, height=21, width=99)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(text='''Steps number''')

        self.txtStepNum = tk.Entry(self.frmCom)
        self.txtStepNum.place(relx=0.049, rely=0.382, height=27, relwidth=0.392)
        self.txtStepNum.configure(background="white")
        self.txtStepNum.configure(font="TkFixedFont")
        self.txtStepNum.configure(foreground="#000000")
        self.txtStepNum.configure(highlightbackground="#d9d9d9")
        self.txtStepNum.configure(highlightcolor="black")
        self.txtStepNum.configure(insertbackground="black")
        self.txtStepNum.configure(selectbackground="#c4c4c4")
        self.txtStepNum.configure(selectforeground="black")

        self.btnSetZero = tk.Button(self.frmCom)
        self.btnSetZero.place(relx=0.049, rely=0.611, height=38, width=107)
        self.btnSetZero.configure(activebackground="#d9d9d9")
        self.btnSetZero.configure(activeforeground="#000000")
        self.btnSetZero.configure(background="#d9d9d9")
        self.btnSetZero.configure(command=ClientGUI_V2_support.onSetZero)
        self.btnSetZero.configure(foreground="#000000")
        self.btnSetZero.configure(highlightbackground="#d9d9d9")
        self.btnSetZero.configure(highlightcolor="black")
        self.btnSetZero.configure(pady="0")
        self.btnSetZero.configure(text='''Set ZERO pos.''')

        self.frmLog = tk.Frame(top)
        self.frmLog.place(relx=0.011, rely=0.575, relheight=0.354
                          , relwidth=0.983)
        self.frmLog.configure(relief='groove')
        self.frmLog.configure(borderwidth="2")
        self.frmLog.configure(relief="groove")
        self.frmLog.configure(background="#d9d9d9")
        self.frmLog.configure(highlightbackground="#d9d9d9")
        self.frmLog.configure(highlightcolor="black")
        self.frmLog.configure(width=865)

        self.Label8 = tk.Label(self.frmLog)
        self.Label8.place(relx=0.006, rely=0.019, height=24, width=33)
        self.Label8.configure(activebackground="#f9f9f9")
        self.Label8.configure(activeforeground="black")
        self.Label8.configure(background="#d9d9d9")
        self.Label8.configure(foreground="#000000")
        self.Label8.configure(highlightbackground="#d9d9d9")
        self.Label8.configure(highlightcolor="black")
        self.Label8.configure(text='''Log''')

        self.txtMainLog = tk.Text(self.frmLog)
        self.txtMainLog.place(relx=0.006, rely=0.113, relheight=0.777
                              , relwidth=0.985)
        self.txtMainLog.configure(background="white")
        self.txtMainLog.configure(font="TkTextFont")
        self.txtMainLog.configure(foreground="black")
        self.txtMainLog.configure(highlightbackground="#d9d9d9")
        self.txtMainLog.configure(highlightcolor="black")
        self.txtMainLog.configure(insertbackground="black")
        self.txtMainLog.configure(selectbackground="#c4c4c4")
        self.txtMainLog.configure(selectforeground="black")
        self.txtMainLog.configure(undo="1")
        self.txtMainLog.configure(width=852)
        self.txtMainLog.configure(wrap="word")

        self.frmLogClear = tk.Button(self.frmLog)
        self.frmLogClear.place(relx=0.012, rely=0.906, height=22, width=70)
        self.frmLogClear.configure(activebackground="#d9d9d9")
        self.frmLogClear.configure(activeforeground="#000000")
        self.frmLogClear.configure(background="#d9d9d9")
        self.frmLogClear.configure(command=ClientGUI_V2_support.onLogClear)
        self.frmLogClear.configure(foreground="#000000")
        self.frmLogClear.configure(highlightbackground="#d9d9d9")
        self.frmLogClear.configure(highlightcolor="black")
        self.frmLogClear.configure(pady="0")
        self.frmLogClear.configure(text='''Clear''')

        self.Label14 = tk.Label(self.frmLog)
        self.Label14.place(relx=0.532, rely=0.019, height=24, width=91)
        self.Label14.configure(activebackground="#f9f9f9")
        self.Label14.configure(activeforeground="black")
        self.Label14.configure(background="#d9d9d9")
        self.Label14.configure(foreground="#000000")
        self.Label14.configure(highlightbackground="#d9d9d9")
        self.Label14.configure(highlightcolor="black")
        self.Label14.configure(text='''Time runing:''')

        self.lblTimeCount = tk.Label(self.frmLog)
        self.lblTimeCount.place(relx=0.647, rely=0.019, height=24, width=211)
        self.lblTimeCount.configure(activebackground="#f9f9f9")
        self.lblTimeCount.configure(activeforeground="black")
        self.lblTimeCount.configure(background="#d9d9d9")
        self.lblTimeCount.configure(font="TkTextFont")
        self.lblTimeCount.configure(foreground="#0000fe")
        self.lblTimeCount.configure(highlightbackground="#d9d9d9")
        self.lblTimeCount.configure(highlightcolor="black")
        self.lblTimeCount.configure(justify='left')
        self.lblTimeCount.configure(text='''00:00''')

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

    def __init__(self, top=None):

        self.stop_training = True
        self.exit_flag = False

        self.top = top
        self.__init__from_page(top)
        self.Font_init()
        self.buttons_disable()

        self.exception_obj = fish_log.RaiseException(self)
        self.exception_obj.info(" --- Program started --- ", bold=True)
        self.exception_obj.info(" --- Loading --- ")

        self.arduino_obj = ArduinoFunctions(self.exception_obj)
        self.log_folder = log_folder()

        self.vars_init()
        self.fillValue()

        self.exception_obj.info("config file - ..\{}".format(self.config_file_name))


    def Font_init(self):
        self.myFont_reg = Font(family="TkTextFont", size=14)
        self.myFont_bold = Font(family="TkTextFont", size=14, weight="bold")
        self.myFont_big_bold = Font(family="TkTextFont", size=18, weight="bold")
        self.myFont_big14 = Font(family="TkTextFont", size=14)
        self.myFont_big16 = Font(family="TkTextFont", size=16)
        self.myFont_big18 = Font(family="TkTextFont", size=18)
        self.myFont_Small = Font(family="TkTextFont", size=12)
        self.myFont_Ssmall = Font(family="TkTextFont", size=10)
        self.myFont_Sssmall = Font(family="TkTextFont", size=8)

        self.txtMainLog.tag_configure("bold", font=self.myFont_bold)
        self.txtMainLog.configure(font=self.myFont_reg)

        self.radF1.configure(font=self.myFont_Sssmall)
        self.radN1.configure(font=self.myFont_Sssmall)
        self.radF2.configure(font=self.myFont_Sssmall)
        self.radN2.configure(font=self.myFont_Sssmall)

        self.txtFishNo1.configure(font=self.myFont_big18)
        self.txtTrainingDay1.configure(font=self.myFont_big18)
        self.txtFishNo2.configure(font=self.myFont_big18)
        self.txtTrainingDay2.configure(font=self.myFont_big18)

        self.lblTimeCount.configure(font=self.myFont_big_bold)

    # noinspection PyAttributeOutsideInit
    def vars_init(self):
        self.LogFolderName = ""
        self.Stat_days = ""
        self.Stat_arg = ""
        self.ServerIP = ""
        self.Args = ""
        self.max_training_time = ""

    def str_pins_split(self, _str):
        p1_place = int(_str.find("("))
        p2_place = int(_str.find(")"))
        new_str = _str[p1_place + 1:p2_place]
        new_str = new_str.split(",")
        results = list(map(int, new_str))

        return results

    def treeview_sort_column(self, tv, col, reverse):
        col_text = tv.heading(col)["text"]
        col_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        if col_text == "Last training":
            col_list.sort(reverse=reverse)
        else:
            col_list.sort(key=lambda x: x[0], reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(col_list):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def tree_view_create(self):
        try:
            self.DB.pack()
            self.DB.pack_forget()
            #
            self.style.configure('Treeview', font=self.myFont_big14)
            self.style.configure('Treeview.Heading', font="TkDefaultFont")
            self.DB = ScrolledTreeView(self.Frame1)
            self.DB.place(relx=0.012, rely=0.057, relheight=0.874, relwidth=0.98)

            # build_treeview_support starting.
            col_names = ['Fish no.', 'Last training', 'Training day', 'Total feed', 'Avg feed p. records']
            col_width = [70, 170, 90, 95, 135]
            columns_list = []
            for i in range(len(col_names)):
                columns_list.append("Col{}".format(i))
            self.DB.configure(columns=columns_list, show='headings')

            for no, col_name in enumerate(col_names):
                # print("no:{} val:{}".format(no, col_name))
                col_idx = "#{}".format(no + 1)
                self.DB.heading(col_idx, text=col_name)
                self.DB.heading(col_idx, anchor="center")
                self.DB.heading(col_idx, command=lambda _col=col_idx: self.treeview_sort_column(self.DB, _col, False))
                self.DB.column(col_idx, width=col_width[no])
                self.DB.column(col_idx, minwidth="20")
                self.DB.column(col_idx, stretch="1")
                self.DB.column(col_idx, anchor="center")
                self.DB.bind("<Double-1>", self.OnTreeDoubleClick)
        except RuntimeError:
            print("Error (tree_view_create) - Window closed")

    def OnTreeDoubleClick(self, event):
        item = self.DB.selection()
        item_val = self.DB.item(item, "values")
        if item_val is not "":
            fish_no = item_val[0]
            try:
                training_no = int(item_val[2])
            except ValueError:
                training_no = 0
            # print("you clicked on", val)
            self.txtFishNo1.delete('1.0', tk.END)
            self.txtFishNo1.insert('0.0', fish_no)
            self.txtTrainingDay1.delete('1.0', tk.END)
            self.txtTrainingDay1.insert('0.0', training_no + 1)

    def db_file_full_path(self):
        full_path = Path("{}/data/{}".format(script_dir, self.DB_fish_file))
        return full_path

    def config_file_full_path(self):
        full_path = Path("{}/{}".format(script_dir, self.config_file_name))
        return full_path

    @staticmethod
    def db_file_exists(_file_name):
        my_file = Path(_file_name)
        file_ex = my_file.is_file()
        return file_ex

    def db_fill(self):
        try:
            str_db_path = self.db_file_full_path()
            if self.db_file_exists(str_db_path) is False:
                self.exception_obj.error("\t ----- DB file ({}) "
                                         "not exist !! Creating new one -----".format(str_db_path)
                                         , bold=True)
                folder_to_create = str_db_path.parents[0]
                folder_to_create.mkdir(parents=True, exist_ok=True)

            fish_db = fish_log.Database(str_db_path)
            fish_list = fish_db.db_fish_view()
            # print("fish_list:{}".format(fish_list))
            for i, each_fish in enumerate(fish_list):
                fish_rec = fish_db.extract_fish_records(each_fish)
                ttl_feeds = fish_db.calc_total_and_avg_feed(fish_rec)
                last_training = fish_db.find_last_training(fish_rec)
                training_day = fish_db.find_training_day(fish_rec)
                data_insert = [each_fish, last_training, training_day, ttl_feeds[0], "{:.1f}".format(ttl_feeds[1])]
                self.DB.insert("", tk.END, values=data_insert)
        except RuntimeError:
            print("Error (db_fill) - Window closed")
        finally:
            fish_db.__exit__()

    def fillValue(self):
        ConfigVals = ConfigSectionMap(self.exception_obj)
        self.config_file_name = ConfigVals.file_name_short
        self.config_file_name_long = ConfigVals.file_name_long
        self.chb_Var = ClientGUI_V2_support.chb_Var

        fish_statistics_dict = ConfigVals.get("Fish Statistics")
        communication_dist = ConfigVals.get("Communication")
        fish_dict = ConfigVals.get("Fish")
        arduino_dict = ConfigVals.get("Arduino")
        motor_dict = ConfigVals.get("Motor")
        camera_dict = ConfigVals.get("Camera")

        try:
            if camera_dict == {}:
                pass
            else:
                self.rad_camera = camera_dict['camera default']

            if motor_dict == {}:
                pass
            else:
                pins_1a = motor_dict['pins1a']
                pins_1b = motor_dict['pins1b']
                pin_step_1a_list = self.str_pins_split(pins_1a)
                pin_step_1b_list = self.str_pins_split(pins_1b)
                pins_2a = motor_dict['pins2a']
                pins_2b = motor_dict['pins2b']
                pin_step_2a_list = self.str_pins_split(pins_2a)
                pin_step_2b_list = self.str_pins_split(pins_2b)

            if fish_statistics_dict == {}:
                pass
            else:
                self.DB_fish_file = fish_statistics_dict['db file']
                self.LogFolderName = log_folder()
                self.Stat_days = fish_statistics_dict['days back']
                self.Stat_arg = fish_statistics_dict['arg']

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
                str_max_training_time = fish_dict['max training time']
                str_max_training_time_split = str(str_max_training_time).split(':')

                # convert max_training_time to timedelta object
                self.max_training_time = timedelta(hours=int(str_max_training_time_split[0])
                                                   , minutes=int(str_max_training_time_split[1])
                                                   , seconds=int(str_max_training_time_split[2]))

            if arduino_dict == {}:
                pass
            else:
                set_stepper_pins = arduino_dict['send stepper pins']
                if set_stepper_pins == 'True':

                    arduino_obj = self.arduino_obj

                    if arduino_obj.connection == 'OK':
                        (p1a_st, p1a_dir, p1a_en) = pin_step_1a_list
                        (p1b_st, p1b_dir, p1b_en) = pin_step_1b_list
                        (p2a_st, p2a_dir, p2a_en) = pin_step_2a_list
                        (p2b_st, p2b_dir, p2b_en) = pin_step_2b_list

                        arduino_obj.send_command(arduino_obj.command_str.init_seq_motor(1, p2a_st, p2a_dir, p2a_en))
                        arduino_obj.send_command(arduino_obj.command_str.init_seq_motor(2, p2b_st, p2b_dir, p2b_en))
                        arduino_obj.send_command(arduino_obj.command_str.init_seq_motor(3, p1a_st, p1a_dir, p1a_en))
                        arduino_obj.send_command(arduino_obj.command_str.init_seq_motor(4, p1b_st, p1b_dir, p1b_en))
                        arduino_obj.send_command(arduino_obj.command_str.define_default_vel_acc(10, 20, 10))
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.exception_obj.error("{}({}) - somthing is wrong with config file.".
                                     format(exc_type.__name__, exc_obj))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.exception_obj.error("line({})-{}({})".
                                     format(exc_tb.tb_lineno, exc_type.__name__, exc_obj))

        str_main_folder = str(main_folder())
        log_folder_only = str(log_folder()).replace(str_main_folder, "")
        self.txtLogFolder.insert('0.0', log_folder_only)
        self.txtMainFolder.insert('0.0', str_main_folder)
        str_db_file = str(self.db_file_full_path())
        db_file_only = str_db_file.replace(str_main_folder, "")
        self.txtDBfile.insert('0.0', db_file_only)
        str_config_file = str(self.config_file_name_long)
        config_file_only = str_config_file.replace(str_main_folder, "")
        self.txtConfigFile.insert('0.0', config_file_only)

        self.txtStatDaysBack.insert('0.0', self.Stat_days)
        self.txtTrainingStop.configure(state='disabled')
        ClientGUI_V2_support.txtTrainingStop.trace("w",
                                                   lambda name,
                                                          index,
                                                          mode,
                                                          txtTrainingStop=ClientGUI_V2_support.txtTrainingStop:
                                                   entryUpdateEndHour(self.txtTrainingStop))

        ClientGUI_V2_support.chb_Var.set('1')  # NEW feeder
        ClientGUI_V2_support.FeedVar1.set('F')
        ClientGUI_V2_support.FeedVar2.set('F')
        # ClientGUI_V2_support.CamVar1.set('1')
        ClientGUI_V2_support.TrainingVar.set('C')
        ClientGUI_V2_support.chVar_stop_tr.set('0')

        if self.rad_camera is not None:
            print("self.rad_camera:{},type:{}".format(self.rad_camera, type(self.rad_camera)))
            if self.rad_camera == '1':
                self.radCam1.configure(value='1')
                self.radCam2.configure(value='0')
                ClientGUI_V2_support.CamVar1.set('0')
            else:
                self.radCam1.configure(value='0')
                self.radCam2.configure(value='1')
                ClientGUI_V2_support.CamVar1.set('1')

        self.db_tree_view_data_refresh()

    def all_children(self, wid, finList):
        _list = wid.winfo_children()
        for item in _list:
            finList.append(item)
            self.all_children(item, finList)
        return finList

    def buttons_disable(self, disable=True):
        childlist = []
        childlist = self.all_children(self.top, childlist)
        for item in childlist:
            if "button" in str(item):
                if disable:
                    item.config(state="disabled")
                else:
                    item.config(state="normal")

    def db_tree_view_data_refresh(self):
        self.tree_view_create()
        self.db_fill()

    def print_and_update_main_log(self, str_to_print, _bold, new_line=True):
        global Fish_trainingGUI, top
        try:
            str_temp = '{}'.format(str_to_print)
            print(str_temp)
            if new_line: str_temp = '{}\n'.format(str_temp)
            if _bold:
                self.txtMainLog.insert(tk.END, str_temp, "bold")
            else:
                self.txtMainLog.insert(tk.END, str_temp)
            self.txtMainLog.see(tk.END)
        except RuntimeError:
            print("Error (print_and_update_main_log) - Window closed.")

    def update_time(self, _time_timed_str, training_stop_timed_str=None):
        # print("type:{}".format(type(time_str)))
        _str_time_array = str(_time_timed_str).split(':')
        _str_time_array = list(map(int, _str_time_array))

        _str_hr = _str_time_array[0]
        _str_min = _str_time_array[1]
        _str_sec = _str_time_array[2]
        # time_str = '{}:{}:{}'.format(_str_hr, _str_min, _str_sec)
        time_timed_str = str(_time_timed_str)
        if training_stop_timed_str is not None:
            time_timed_str = "{} / {}".format(str(_time_timed_str), training_stop_timed_str)
        self.lblTimeCount.configure(text=time_timed_str)

        stop_training = self.check_if_auto_training_stop(_time_timed_str, training_stop_timed_str,
                                                         self.max_training_time)

        if _str_min > 1:
            self.lblTimeCount.configure(fg='#5eaf24')

        return stop_training

        def __call__(self):
            print("RUN Command")

    def check_if_auto_training_stop(self, _time_timed_str, _training_stop_timed_str, _max_training_time):
        stop_training = False
        try:
            if _max_training_time is not None:
                if _time_timed_str >= _max_training_time:
                    self.print_and_update_main_log('\t\tMAXIMUM TRAINING TIME - QUITING', True)       # bold=True
                    stop_training = True
            if _training_stop_timed_str is not None:
                if _time_timed_str >= _training_stop_timed_str:
                    stop_training = True

        except TypeError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.exception_obj.error("line({})-{}({})".
                                     format(exc_tb.tb_lineno, exc_type.__name__, exc_obj))

        return stop_training

    def stop_training_func(self):
        ClientGUI_V2_support.onStopTraining()

    def exit_press(self):
        ClientGUI_V2_support.onExit()

    def time_stamp(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                      | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                      + tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''

    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


def entryUpdateEndHour(entry):
    try:
        text = entry.get()
        if len(text) in (2, 5):
            entry.insert(tk.END, ':')
            entry.icursor(len(text) + 1)
        elif len(text) not in (3, 6):
            if not text[-1].isdigit():
                entry.delete(0, tk.END)
                entry.insert(0, text[:-1])
        if len(text) > 8:
            entry.delete(0, tk.END)
            entry.insert(0, text[:8])
    except IndexError:
        pass


def gui_init():
    ClientGUI_V2_support.set_Tk_var()
    Fish_trainingGUI = MainGUI(root)
    Excp = Fish_trainingGUI.exception_obj
    arduino_obj = Fish_trainingGUI.arduino_obj
    ClientGUI_V2_support.init(root, Fish_trainingGUI, Excp, arduino_obj)
    Excp.info("Loading DONE", bold=True)
    Fish_trainingGUI.buttons_disable(False)

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, Fish_trainingGUI, root

    sys.stdout = fish_log.Logger_stdout()  # start main stdout logger - logfile.log
    root = tk.Tk()
    # root.winfo_children()
    _thread.start_new_thread(gui_init, ())

    try:
        root.mainloop()
    finally:
        ClientGUI_V2_support.onExit()


def destroy_Fish_training_GUI___Client():
    global Fish_trainingGUI
    ClientGUI_V2_support.destroy_window()
    Fish_traningGUI = None


def make_two_digit_num(int_to_check):
    str_temp = '{}'.format(int_to_check)
    if int_to_check < 10:
        str_temp = '0{}'.format(int_to_check)
    return str_temp


def main_folder():
    path = Path(os.path.dirname(__file__))
    return path


def log_folder():
    main_folder_path = main_folder()
    full_path = Path("{}/data/log".format(main_folder_path))
    return full_path


def log_file_name(_file_name):
    full_path = log_folder()
    file_name = Path("{}/{}".format(full_path, _file_name))

    return file_name


if __name__ == '__main__':
    t_stamp = datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')
    print("{}Started".format(t_stamp))
    print("Python version: {}".format(sys.version))
    Fish_trainingGUI = None
    vp_start_gui()
