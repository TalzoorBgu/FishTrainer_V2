#!/usr/bin/python
import datetime
# from time import gmtime, strftime
import os
from datetime import datetime
# from Main import Fish_training_GUI___Client

def time_stamp():
    return datetime.today().strftime('%Y-%m-%d %H%M%S')

class FishLog:
    def __init__(self, _GUI_obj, log_folder, fish_name, _exception_log):
        '''file name- fish_name+date+time, open new file, init counters to 0'''

        self.GUI_obj = _GUI_obj
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
        print ('start logging data')
        # Open a file

        self.filename='{}/{}{}{}'.format(log_folder, time_stamp(), '_'+fish_name, ".txt") # time+name
        print ('log file:{}'.format(self.filename))

        self.fo = open(self.filename, 'w+')
        
    def add_tracked_point(self,x,y):
        self.fo.write(str(self.line_number)+' ') #
        self.fo.write(str(self.track_count)+' ') #
        self.fo.write(str(datetime.now().time())+' ') #
        self.fo.write('track'+' ') #

        self.fo.write("{0:.2f} ".format(round(x, 2))) #self.fo.write(str(x)+' ') #
        self.fo.write("{0:.2f}".format(round(y, 2))) #self.fo.write(str(y)+' ') #

        self.fo.write('\n') #
        self.line_number = self.line_number+1
        self.track_count = self.track_count+1
        
    def add_feed(self,side):
        self.fo.write(str(self.line_number)+' ') #
        self.fo.write(str(self.feed_count[side])+' ') #
        self.fo.write(str(datetime.now().time())+' ') #
        self.fo.write('feed'+' ') #
        self.fo.write(side+' ') #
        self.fo.write('\n') #
        self.line_number=self.line_number+1
        self.feed_count[side]=self.feed_count[side]+1
        

