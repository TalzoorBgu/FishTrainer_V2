
from datetime import datetime


class RaiseException():

    def __init__(self, _object):
        self.object = _object

    def error(self, str_msg):
        self.object.print_and_update_main_log("{} Error! {}".format(self.time_stamp(), str_msg))

    def time_stamp(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M.%S --> ')


