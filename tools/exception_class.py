
from datetime import datetime


class RaiseException():

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

    def time_stamp(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


