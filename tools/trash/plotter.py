
import matplotlib

from tools.log import run

matplotlib.use('Agg')
# import matplotlib.pylab


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
