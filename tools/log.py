#!/usr/bin/python
import datetime
import os
import sqlite3
import subprocess
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path

import numpy

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

from matplotlib import pyplot as plt, gridspec as gridspec, patches


def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H%M%S')


class FishLog:
    def __init__(self, log_folder, fish_name, _exception_log):
        '''file name- fish_name+date+time, open new file, init counters to 0'''
        self.Exception_log = _exception_log
        # check if dir exist and create if not
        if not os.path.exists(log_folder):
            self.Exception_log.error("NO LOG FOLDER FOUND - rebuiling it. ")
            # self.GUI_obj.print_and_update_main_log("NO LOG FOLDER FOUND - rebuiling it. ")
            os.makedirs(log_folder)

        self.line_number = 0
        self.track_count = 0
        self.feed_count = {'left': 0, 'right': 0, 'center': 0}
        self.fish_name = fish_name
        print('start logging data')
        # Open a file

        self.filename = '{}/{}{}{}'.format(log_folder, time_stamp(), '_' + fish_name, ".txt")   # time+name
        print('log file:{}'.format(self.filename))
        self.fo = open(self.filename, 'w+')
        self.add_tracked_point(0, 0)        # for start training time

    def add_tracked_point(self, x, y):
        self.fo.write(str(self.line_number)+' ')
        self.fo.write(str(self.track_count)+' ')
        self.fo.write(str(datetime.now().time())+' ')
        self.fo.write('track' + ' ')

        self.fo.write("{0:.2f} ".format(round(x, 2)))
        self.fo.write("{0:.2f}".format(round(y, 2)))

        self.fo.write('\n')
        self.line_number = self.line_number+1
        self.track_count = self.track_count+1
        
    def add_feed(self,side):
        self.fo.write(str(self.line_number)+' ')
        self.fo.write(str(self.feed_count[side])+' ')
        self.fo.write(str(datetime.now().time())+' ')
        self.fo.write('feed' + ' ')
        self.fo.write(side + ' ')
        self.fo.write('\n')
        self.line_number = self.line_number + 1
        self.feed_count[side] = self.feed_count[side]+1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fo.close()


class ReadFile:
    def __init__(self, _file_name):
        file_ex = ""
        try:
            self.fish_no = -1
            self.date = -1
            self.ttl_time = -1

            self.data_x = []
            self.data_y = []
            self.feed_x = []
            self.feed_y = []
            self.max_x = 0
            self.max_y = 0

            self.training_start_str = ""
            self.file_empty = False

            my_file = Path(_file_name)
            file_ex = my_file.is_file()
            if file_ex:
                file_h = open(_file_name, 'r')
                text_lines = file_h.read().split('\n')

                self.fish_no, \
                self.t_date, \
                self.train_day = self.file_prop(_file_name)

                training_end = training_start = self.extract_time(text_lines[0], self.t_date)

                for num, word in enumerate(text_lines):
                    data = self.extract_x_y(word)
                    self.max_x = data[1][0] if data[1][0] > self.max_x else self.max_x
                    self.max_y = data[1][1] if data[1][1] > self.max_y else self.max_y

                    timeformat_time = self.extract_time(word, self.t_date)
                    if type(timeformat_time) == type(training_end):
                        bool_later = True if timeformat_time > training_end else False
                        if bool_later:
                            training_end = timeformat_time

                    if data[0] is "TRACK":
                        self.add(data[1])
                    elif data[0] is "FEED":
                        self.feed_add()

                # print(" self.max_x:",  self.max_x, "  self.max_y:",  self.max_y)
                if num > 10:
                    ttl_training_time = training_end - training_start
                    # print("training_start:{}".format(training_start))
                    self.training_start_str = str(training_start)
                    self.total_training_time = ttl_training_time
                else:
                    print("File is empty")
                    self.file_empty = True

            elif not file_ex:
                print("File does not exist!")

        except:
            print("Error")
            raise
        finally:
            if file_ex: file_h.close()
            print("File closed")

    def add(self, _data):
        self.data_x.append(_data[0])
        self.data_y.append(_data[1])
        # print("track data:{},{}".format(self.data_x[-1], self.data_y[-1]))

    def feed_add(self):
        self.feed_x.append(self.data_x[-1])
        self.feed_y.append(self.data_y[-1])
        # print("feed data:{},{}".format(self.feed_x[-1], self.feed_y[-1]))

    @staticmethod
    def file_prop(_file_name):
        log_place = _file_name.find("log")
        date_end_place = _file_name.find(" ", log_place)
        _F_place = _file_name.find("_F", log_place)
        DAY_place = _file_name.find("DAY")
        DAY_end_place = _file_name.find(".", DAY_place)

        traning_date = _file_name[log_place+4:date_end_place]
        traning_day = _file_name[DAY_place+3:DAY_end_place]
        fish_no = _file_name[_F_place+2:DAY_place]

        # if not _file_name.find("test") == -1:
        #     traning_day = ""
        #     fish_no = "test"

        return fish_no, traning_date, traning_day

    @staticmethod
    def extract_x_y(_str):
        data_ok = "NO"
        [x, y] = [0, 0]
        track_place = _str.find("track")
        feed_line = _str.find("feed")

        if track_place is not -1:
            data_ok = "TRACK"
            x_pos_start = track_place+len("track") + 1
            x_pos_end = _str.find(' ', x_pos_start)
            y_pos_start = x_pos_end + 1
            try:
                [x, y] = _str[x_pos_start:x_pos_end], _str[y_pos_start:]
                [x, y] = [float(x), float(y)]
            except ValueError:
                data_ok = False
                pass
        elif feed_line is not -1:
            data_ok = "FEED"
            # will take [x, y] from last tracking data

        return data_ok, [x, y]

    @staticmethod
    def extract_time(_str, _date):
        time_timeformat = ''
        try:
            if _str:
                time_start_place = find_nth_overlapping(_str, " ", 2)
                time_end_place = _str.find('.')
                time_str = _str[time_start_place+1:time_end_place]
                time_date_str = "{} {}".format(_date, time_str)
                t_format = '%Y-%m-%d %H:%M:%S'
                time_timeformat = datetime.strptime(time_date_str, t_format)
        except ValueError:
            time_timeformat = ''
            pass
        return time_timeformat

    def file_data(self):
        return [self.data_x, self.data_y]

    def file_feed_data(self):
        return [self.feed_x, self.feed_y]


def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start


class Logger_stdout(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.close()


class Database(object):
    def __init__(self, _db_file="db_file.db"):
        self.sql_create_training_table = """CREATE TABLE IF NOT EXISTS 'training' (
        'id' INTEGER PRIMARY KEY,
        'training_no' INTEGER,
        'fish_no' INTEGER,
        'date' DATE,
        'feed_count' INTEGER,
        'file_name' VARCHAR(400),
        'training_duration' VARCHAR(14),
        'file_note' VARCHAR(255)
        );"""

        self.database = _db_file
        self.db_conn = None
        self.connect()
        cur = self.db_conn.cursor()
        # cur.execute(self.sql_create_fish_table)
        cur.execute(self.sql_create_training_table)
        self.db_conn.commit()
        # print("self.db_conn:{}".format(self.db_conn))

    def connect(self):
        conn = sqlite3.connect(self.database)
        conn.commit()
        # conn.close()
        self.db_conn = conn

    def db_fish_view(self):
        cur = self.db_conn.cursor()
        # cur.execute(""" SELECT fish_no FROM fish """)
        cur.execute(""" SELECT fish_no FROM training """)
        rows = cur.fetchall()
        unique_fish_list = unique(rows)
        # for i, fish_no in enumerate(unique_fish_list):
        #     print("fish_{}:{}, ".format(i, fish_no[0]), end='')
        return self.clean_list(unique_fish_list)

    def extract_fish_records(self, _fish_no):
        sql_comm = """ SELECT training_no, date, feed_count FROM training where fish_no = (?) order by training_no """
        cur = self.db_conn.cursor()
        cur.execute(sql_comm, [_fish_no])
        rows = cur.fetchall()
        return rows

    def create_training_record(self, _training):
        sql_comm = """ INSERT INTO training(training_no, 
                                        fish_no, 
                                        date, 
                                        feed_count, 
                                        file_name, 
                                        training_duration, 
                                        file_note)
                  VALUES(?,?,?,?,?,?,?) """
        cur = self.db_conn.cursor()
        print("_training:{}".format(_training))
        cur.execute(sql_comm, _training)
        self.db_conn.commit()
        return cur.lastrowid

    @staticmethod
    def clean_list(_lst_in):
        list_to_clean = []
        for i, fish_no in enumerate(_lst_in):
            list_to_clean.append(fish_no[0])
        return list_to_clean

    @staticmethod
    def calc_total_and_avg_feed(_fish_records):
        ttl_feed = 0
        for each_rec in _fish_records:
            ttl_feed = ttl_feed + each_rec[2]
        avg_feed = ttl_feed / len(_fish_records)
        return ttl_feed, avg_feed

    @staticmethod
    def find_last_training(_fish_records):
        dates_list = []
        for each_rec in _fish_records:
            dates_list.append(each_rec[1])
        last_training = max(dates_list)
        return last_training

    @staticmethod
    def find_training_day(_fish_records):
        try:
            training_no = []
            for each_rec in _fish_records:
                training_no.append(each_rec[0])
            training_day = max(training_no)
        except TypeError:
            print("Error! Check DB records.")
        return training_day

    def __exit__(self):
        self.db_conn.close()


def add_rec():      # for debug purpose (test SQL DB record addition)
    fish_db = Database()
    fish_no = 701
    fish_db.create_fish_record(fish_no)

    training_no = 1
    t_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    feed_count = 71
    file_full_path = "C:\\path\\to\\file\\t5_name.txt"
    t_duration = str(timedelta(seconds=56, minutes=19, hours=0))
    file_note = "this is note8"
    fish_db.create_training_record(
        [training_no, fish_no, t_date, feed_count, file_full_path,
         t_duration, file_note])

# function to get unique values
def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


class RaiseException:

    def __init__(self, _object):
        self.object = _object

    def error(self, str_msg, **kwargs):
        _bold = False
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "bold":
                    _bold = value
        self.object.print_and_update_main_log("{} Error! {}".format(self.time_stamp(), str_msg), _bold)

    def info(self, str_msg, **kwargs):
        _bold = False
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "bold":
                    _bold = value
        self.object.print_and_update_main_log("{} Info: {}".format(self.time_stamp(), str_msg), _bold)

    def info_wo_tstamp(self, str_msg, **kwargs):
        _bold = False
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "bold":
                    _bold = value
        self.object.print_and_update_main_log("Info: {}".format(str_msg), _bold)

    def feed_event(self, str_msg, **kwargs):
        _bold = False
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "bold":
                    _bold = value
        self.object.print_and_update_main_log("Feed event: {}".format(str_msg), _bold)

    def time_stamp(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


class PlotTraj:

    def __init__(self, properties, _open_png, _overwrite, _xlabel='X', _ylabel='Y'):

        self.data = []
        self.line = []
        self.open_png = _open_png
        self.overwrite = _overwrite
        self.info = properties
        self.max_x = properties[4][0]
        self.max_y = properties[4][1]
        print("properties:", properties)

        pass

    def plot_it(self, _data, _feed_data):
        self.data = _data
        data_x = numpy.array(_data[0])
        data_y = numpy.array(_data[1])
        info = self.info

        fig = plt.figure()
        gs1 = gridspec.GridSpec(1, 1)

        self.ax = fig.add_subplot(gs1[0])

        _title = '$Fish-{}$ \nTraining day:{}\nDate:{}, Total time:{}'.\
            format(info[0], info[1], info[2], info[3])

        self.ax.set_aspect('equal', adjustable="box")

        plt.subplots_adjust(top=0.8)

        self.ax.set_title(_title)
        x_ticks = self.ax.xaxis.get_major_ticks()
        y_ticks = self.ax.yaxis.get_major_ticks()
        for tick in x_ticks:
            tick.label.set_fontsize(6)
        for tick in y_ticks:
            tick.label.set_fontsize(6)

        self.line, = self.ax.plot(data_x, data_y, linewidth=0.5, color='black')

        for i in range(len(_feed_data[0])):
            circle = patches.Circle((_feed_data[0][i], _feed_data[1][i]), 1, color='red')
            self.ax.add_patch(circle)

    def save(self, _folder_name=''):
        info = self.info
        folder_name = os.path.join(_folder_name, info[0])
        dir_ex = os.path.exists(folder_name)
        print("folder_name:{}, exists:{}".format(folder_name, dir_ex))

        if dir_ex:
            pass
        else:
            os.makedirs(folder_name)

        time_info = str(info[2]).replace(':', '')
        file_name_to_save = "{}.png".format(time_info)
        full_name = Path(os.path.join(folder_name, file_name_to_save))
        print("img full_name:{}".format(full_name))

        self.ax.figure.savefig(full_name, dpi=600)
        if self.open_png:
            open_img_thread = threading.Thread(target=openImage, args=(full_name, ))
            open_img_thread.start()
            open_img_thread.join()
            print("OpenImg thread finished")


def run(_read_file_class, _log_folder, _file_to_plot, **kwargs):
    read_file_class = _read_file_class
    log_img_folder = "{}-img".format(_log_folder)
    show_at_end = True
    overwrite = True

    if "show" in kwargs:
        show_at_end = kwargs["show"]
    if "overwrite" in kwargs:
        overwrite = kwargs["overwrite"]

    print("Checking file-{}".format(_file_to_plot))

    file_data = read_file_class.file_data()
    file_feed_data = read_file_class.file_feed_data()

    if len(file_data[0]) < 10 and len(file_data[1]) < 10:
        print("Not enough data!")
    else:

        properties = [read_file_class.fish_no,
                      read_file_class.train_day,
                      read_file_class.training_start_str,
                      read_file_class.total_training_time, [read_file_class.max_x, read_file_class.max_y]]

        plot_fig = PlotTraj(properties, show_at_end, overwrite)
        plot_fig.plot_it(file_data, file_feed_data)
        plot_fig.save(log_img_folder)
        print("Plotter finished")


def openImage(_img):
    imageViewerFromCommandLine = {'linux': 'xdg-open',
                                  'win32': 'explorer',
                                  'darwin': 'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, str(_img)])