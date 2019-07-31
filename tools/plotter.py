
import matplotlib.pylab
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy
from pathlib import Path
from datetime import datetime
import os
import sys
import webbrowser
import argparse
import subprocess



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
                    print("training_start:{}".format(training_start))
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


# def save_plot(_info, _ax, open_png, overwrite, _project_wd=''):
#
#     if not _project_wd:
#         runing_dw = os.getcwd()
#         fish_trainerNEW_end_place = runing_dw.find("fish-trainerNEW") + len("fish-trainerNEW")
#         project_wd = runing_dw[:fish_trainerNEW_end_place]
#
#     info = _info
#     folder_name = os.path.join(project_wd, "data/log-img", info[0])
#
#     time_info = str(info[2]).replace(':', '')
#     file_name_to_save = "{}.png".format(time_info)
#     full_name = os.path.join(folder_name, file_name_to_save)
#     print("full fig name:{}".format(full_name))
#
#     fig_already_exsits = os.path.isfile(full_name)
#
#     if (fig_already_exsits and overwrite) or (not fig_already_exsits):
#
#         dir_ex = os.path.exists(folder_name)
#         print("folder_name:{}, exists:{}".format(folder_name, dir_ex))
#
#         if dir_ex:
#             pass
#         else:
#             os.makedirs(folder_name)
#
#         _ax.figure.savefig(full_name, dpi=600)
#         if open_png:
#             webbrowser.open(full_name)
#     else:
#         print("figure already exists, skipping")


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

    def plot_it(self, _data):
        # self.plt = matplotlib.pylab
        self.data = _data
        hte = numpy.array(_data[0])
        hre = numpy.array(_data[1])
        info = self.info

        # print("x,y_max:", self.max_x, self.max_y)

        # fig = plt.figure(figsize=(5+ self.max_x/100, 5+ self.max_y/100))
        fig = plt.figure()
        gs1 = gridspec.GridSpec(1, 1)

        self.ax = fig.add_subplot(gs1[0])

        _title = '$Fish-{}$ \nTraining day:{}\nDate:{}, Total time:{}'.\
            format(info[0], info[1], info[2], info[3])

        # self.plt.title('$Fish-{}$ \nTraining day:{}\nDate:{}, Total time:{}'.
        #                format(info[0], info[1], info[2], info[3]))
        # plt.tight_layout()
        # gs1.tight_layout(fig)
        self.ax.set_aspect('equal', adjustable="box")

        plt.subplots_adjust(top=0.8)
        # self.ax = plt.gca()
        # self.ax.axis('equal')
        self.ax.set_title(_title)
        x_ticks = self.ax.xaxis.get_major_ticks()
        y_ticks = self.ax.yaxis.get_major_ticks()
        for tick in x_ticks:
            tick.label.set_fontsize(6)
        for tick in y_ticks:
            tick.label.set_fontsize(6)

        # self.ax.title.set_y(1.05)
        # self.ax.autoscale()

        # self.ax.set_ylim([0, 100])
        # self.ax.set_xlim([0, 700])

        # self.ax.annotate(_title,
        #              xy=(0, 0),
        #              xytext=(0.5, 1.04),
        #              xycoords='axes fraction',
        #              textcoords='axes fraction',
        #              fontsize=20,
        #              horizontalalignment='center')

        self.line, = self.ax.plot(hte, hre, linewidth=0.5, color='black')

        # plt.show()


        # job_server = pp.Server(ppservers=ppservers)

        # print ("Starting Parallel Python v2 with", job_server.get_ncpus(), "workers")
        # job = job_server.submit(save_plot, (self.info, self.ax, self.open_png, self.overwrite),
        #                         (), ("matplotlib", "os", "webbrowser", "matplotlib.pylab"))
        # job()
        # job_server.print_stats()

    def save(self, _folder_name=''):
        #NOT USED ANYMORE
        # if not project_wd:
        #     runing_dw = os.getcwd()
        #     fish_trainerNEW_end_place = runing_dw.find("fish-trainerNEW") + len("fish-trainerNEW")
        #     project_wd = runing_dw[:fish_trainerNEW_end_place]

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
        print("full_name:{}".format(full_name))

        self.ax.figure.savefig(full_name, dpi=600)
        if self.open_png:
            openImage(full_name)


def run(_log_folder, _file_to_plot, **kwargs):
    log_img_folder = "{}-img".format(_log_folder)
    show_at_end = True
    overwrite = True

    if "show" in kwargs:
        show_at_end = kwargs["show"]
    if "overwrite" in kwargs:
        overwrite = kwargs["overwrite"]

    #Check line:
    # _file_to_plot = r"C:\Users\Owner\PycharmProjects\fish-trainerNEW\data\log\2019-02-10 175510_F315DAY3.(0).txt"

    print("Checking file-{}".format(_file_to_plot))
    read_f = ReadFile(_file_to_plot)

    file_data = read_f.file_data()
    if len(file_data[0]) < 10 and len(file_data[1]) < 10:
        print("Not enough data!")
    else:
        # print("file_data:{}".format(file_data))
        properties = [read_f.fish_no,
                         read_f.train_day,
                         read_f.traning_start_str,
                         read_f.total_training_time, [read_f.max_x, read_f.max_y]]

        plot_fig = PlotTraj(properties, show_at_end, overwrite)
        plot_fig.plot_it(file_data)
        plot_fig.save(log_img_folder)

def folder_to_file_list():
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', help= 'paste path to log files')
    args = parser.parse_args()

    if args.path == 'auto':
        full_script_path = os.path.dirname(os.path.realpath(__file__))
        trainerNEW_end_place = ""   # full_script_path.find(r"fish-trainerNEW") + len("fish-trainerNEW/")
        full_root_script_path = full_script_path[:trainerNEW_end_place]
        folder = os.path.join(full_root_script_path, r"data/log")
    else:
        print("type:{}".format(type(args.path)))
        print("args.path:#{}#".format(args.path))
        folder = args.path

    my_dir = Path(folder)
    print("my_dir:{}".format(my_dir))
    dir_ex = my_dir.is_dir()

    files = []
    sorted_files = []

    if dir_ex:
        files = [f for f in os.listdir(folder) if
                 os.path.isfile(os.path.join(folder, f))]
        for item in files:
            if item.find("FDAY") is -1:
                sorted_files.append(item)
    else:
        print("dir dose'nt exist")

    return folder, sorted_files

def openImage(_img):
    imageViewerFromCommandLine = {'linux': 'xdg-open',
                                  'win32': 'explorer',
                                  'darwin': 'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, str(_img)])


if __name__ == '__main__':
    #1280x1024

    # for example
    # long one
    # file_to_check =   r"..\data\log\2019-02-10 175510_F315DAY3.(0).txt"
    # box one
    file_to_check = "../data/log/2019-01-11 073701_F573DAY1.(0).txt"       # for example

    run(file_to_check)
    exit(1)
    # folder, file_list = folder_to_file_list()
    # for file_item in file_list:
    #     file_name = os.path.join(folder, file_item)
    #
    #     run(file_name, show=False, overwrite=False)
    #     os.close()
