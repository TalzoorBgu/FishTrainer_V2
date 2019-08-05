
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# import matplotlib.pylab


import numpy
from pathlib import Path
import os
import sys
import webbrowser
import argparse
import subprocess
import threading


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
        print("img full_name:{}".format(full_name))

        self.ax.figure.savefig(full_name, dpi=600)
        if self.open_png:
            open_img_thread = threading.Thread(target=openImage, args=(full_name, ))
            open_img_thread.start()
            open_img_thread.join()
            print("OpenImg thread finished")
            # openImage(full_name)


def run(_read_file_class, _log_folder, _file_to_plot, **kwargs):
    read_file_class = _read_file_class
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

    file_data = read_file_class.file_data()
    if len(file_data[0]) < 10 and len(file_data[1]) < 10:
        print("Not enough data!")
    else:
        # print("file_data:{}".format(file_data))

        properties = [read_file_class.fish_no,
                      read_file_class.train_day,
                      read_file_class.traning_start_str,
                      read_file_class.total_training_time, [read_file_class.max_x, read_file_class.max_y]]

        plot_fig = PlotTraj(properties, show_at_end, overwrite)
        plot_fig.plot_it(file_data)
        plot_fig.save(log_img_folder)
        print("Plotter finished")

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
