#!/usr/bin/env python

from . import track_fish
# from tracker.old_tcp_client import FishClient
from .fish_tank import Tank
from . import fishlog
from .time_counter import TimeCounter
import argparse
import os
import time
from . import plotter
from time import sleep
import Main
import threading
from pathlib import Path
from datetime import datetime

try:
    from tools import SQL_DB
except ImportError:
    from .tools import SQL_DB


FEED_EVERY = 3          # feed every 3 sec


# TODO:
# - create seperate log file for each fish
# - insert fish client send and test with feeder
# -


class Controller:
    def __init__(self, feed, _exception_class, _GUI_obj=None, _log_name=['test'], _camera=0):
        global total_feed
        global time_counter
        total_feed = 0
        time_counter = 0

        self.thread_plotter = None
        self.feed = feed

        self.time_count = TimeCounter()
        self.GUI_obj = _GUI_obj
        self.chb_Var = _GUI_obj.chb_Var
        self.time_last_feed = int(round(time.time()))

        self.Exception_log = _exception_class

        width = track_fish.init_tracking(self.Exception_log, int(_camera))

        # init logger
        #   full_script_path = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '/')
        #   full_root_script_path = full_script_path[:full_script_path.find('tracker')]
        #   log_folder = '{}data/log/'.format(full_root_script_path)

        # full_script_path = os.path.dirname(os.path.realpath(__file__))
        # trainerNEW_end_place = full_script_path.find(r"fish-trainerNEW") + len("fish-trainerNEW/")
        # full_root_script_path = full_script_path[:trainerNEW_end_place]
        # log_folder = os.path.join(full_root_script_path, r"data\log")
        # print("full_script_path:{}\nfull_root_script_path:{}\nlog_folder:{}".
        #       format(full_script_path, full_root_script_path, log_folder))
        self.log_folder = Main.log_folder()
        self.file_name = Main.log_file_name(_log_name)
        print("file_name:{}".format(self.file_name))

        self.logger = []

        #init tank
        self.tank = []
        f_id = 0
        #print ('Tank(1, 1):' + str(Tank(1, 1)))

        for size in width:
            self.tank.append(Tank(f_id, size))
            self.logger.append(fishlog.FishLog(self.GUI_obj, self.log_folder,
                                               "{}.({})".format(_log_name[f_id], str(f_id)), self.Exception_log))
            f_id = f_id + 1


    def __del__(self):  #Destroy
        print('Controller closed')

    def time(self):
        time_str = self.time_count.get_time_diff()
        if time_str:
            #print (time_str)
            self.GUI_obj.update_time(time_str)

    def check_exit_flag(self):
        _int_tmp = self.GUI_obj.exit_flag
        return _int_tmp

    def close_app(self):
        Main.destroy_Fish_training_GUI___Client()

    def check_training(self):
        _int_tmp = self.GUI_obj.stop_training
        return _int_tmp

    def end_training(self, fish_id):        # called in track_fish.py - cb.end_training(id_out)
        global total_feed
        fish_db = SQL_DB.Database(self.GUI_obj.db_file_full_path())
        log_filename = self.logger[fish_id].filename
        self.logger[fish_id].fo.close()
        sleep(0.2)  # 200mS wait
        t_data = ReadFile(log_filename)
        t_dt_str = t_data.traning_start_str
        time_str = t_dt_str[:t_dt_str.rindex(" ") + 6]

        fish_db.create_fish_record(t_data.fish_no)
        fish_db.create_training_record([t_data.train_day,
                                        t_data.fish_no,
                                        time_str,
                                        total_feed,
                                        log_filename,
                                        str(t_data.total_training_time),
                                        ""])
        self.GUI_obj.db_tree_view_data_refresh()

        thread_plotter = threading.Thread(target=plotter.run,
                                          args=(t_data, self.log_folder, log_filename, ),
                                          kwargs=dict(show=True, overwrite=True), )
        thread_plotter.daemon = False
        thread_plotter.start()
        thread_plotter.join()
        # self.thread_plotter = thread_plotter

        # plotter.run(self.log_folder, log_filename, show=True, overwrite=True)
        # sleep(5)

    def do(self, x, y, fish_id, _version):
        global total_feed

        time_now = int(round(time.time()))

        self.logger[fish_id].add_tracked_point(x, y)
        if time_now - self.time_last_feed > FEED_EVERY:     # feed every..
            feed_side = self.tank[fish_id].decide(x, y, _version)
        else:
            feed_side = None

        if feed_side is 'center':
            #feed_side = 'left'     # only send 'left' (socket)
            pass
        if feed_side is 'out_center':
            feed_side = None

        if feed_side is not None:
            total_feed += 1
            str_to_print = '{}\t,{}\t - \tTotal:{}'.format(fish_id, feed_side, total_feed)
            self.time_last_feed = time_now

            if self.GUI_obj is not None:
                self.Exception_log.feed_event(str_to_print)
            # fish_client = FishClient()
            if self.chb_Var.get() == '1':
                self.feed.new_feeder_run(0, feed_side)
                # fish_client.send(fish_id + 11, feed_side)
            else:
                pass
                # print("FEED NOW")
                # fish_client.send(fish_id + 1, feed_side)
            # fish_client.kill()

            #fish_client.send(fish_id, feed_side)
            self.logger[fish_id].add_feed(feed_side)

    def time_count(self):
        global time_counter
        print(time_counter)

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start

class ReadFile:
    def __init__(self, _file_name):
        file_ex = ""
        try:
            self.fish_no = -1
            self.date = -1
            self.ttl_time = -1

            self.data_x = []
            self.data_y = []
            self.max_x = 0
            self.max_y = 0

            self.traning_start_str = ""

            my_file = Path(_file_name)
            file_ex = my_file.is_file()
            if file_ex:
                file_h = open(_file_name, 'r')
                text_lines = file_h.read().split('\n')

                self.fish_no,\
                self.t_date,\
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

                    if data[0] is True:
                        self.add(data[1])

                # print(" self.max_x:",  self.max_x, "  self.max_y:",  self.max_y)
                if num > 10:
                    ttl_training_time = training_end - training_start
                    # print("training_start:{}".format(training_start))
                    self.traning_start_str = str(training_start)
                    self.total_training_time = ttl_training_time
                else:
                    print("File is empty")

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
        pass


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

        # print("_file_name:{}, _file_name.find(test):{}".format(_file_name, _file_name.find("test")))
        if not _file_name.find("test") == -1:
            traning_day = ""
            fish_no = "test"

        return fish_no, traning_date, traning_day

    @staticmethod
    def extract_x_y(_str):
        data_ok = False
        [x, y] = [0, 0]
        track_place = _str.find("track")
        # feed_line = _str.find("feed")

        if track_place is not -1:
            data_ok = True
            x_pos_start = track_place+len("track") + 1
            x_pos_end = _str.find(' ', x_pos_start)
            y_pos_start = x_pos_end + 1
            try:
                [x, y] = _str[x_pos_start:x_pos_end], _str[y_pos_start:]
                [x, y] = [float(x), float(y)]
            except ValueError:
                data_ok = False
                pass

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

# ap = argparse.ArgumentParser()
# ap.add_argument("-log", "--log", required=True, help="path to log folder")
# args = vars(ap.parse_args())
if __name__ == '__main__':
    controller = Controller()
    track_fish.track_loop(controller)

