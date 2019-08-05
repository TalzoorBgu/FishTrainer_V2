import sqlite3
from datetime import datetime
from datetime import timedelta

class Database(object):
    def __init__(self, _db_file="db_file.db"):
        # # Converts DT.time to TEXT when inserting
        # sqlite3.register_adapter(datetime.time, self.adapt_timeobj)
        #
        # # Converts TEXT to DT.time when selecting
        # sqlite3.register_converter("timeobj", self.convert_timeobj)

        # self.sql_create_fish_table = """ CREATE TABLE IF NOT EXISTS 'fish' (
        # 'fish_no' INTEGER PRIMARY KEY
        # ); """

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

    def create_fish_record(self, _fish_no):
        pass
        # sql_comm = """ INSERT INTO fish(fish_no) VALUES (?) """
        # cur = self.db_conn.cursor()
        # fish_no_rec = [_fish_no]
        # try:
        #     cur.execute(sql_comm, fish_no_rec)
        #     self.db_conn.commit()
        # except sqlite3.IntegrityError:
        #     print("'fish_no' {} is not unique!".format(fish_no_rec[0]))
        # return cur.lastrowid

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
        training_no = []
        for each_rec in _fish_records:
            training_no.append(each_rec[0])
        training_day = max(training_no)
        return training_day

    def __exit__(self):
        self.db_conn.close()


def add_rec():
    fish_no = 701
    fish_db.create_fish_record(fish_no)

    training_no = 1
    # fish_no = 377
    # t_date = datetime.strptime('2023-11-30 21:32:18', '%Y-%m-%d %H:%M:%S')
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


if __name__ == '__main__':
    fish_db = Database()

    add_rec()

    fish_list = fish_db.db_fish_view()
    print("fish_list:{}".format(fish_list))
    for each_fish in fish_list:
        fish_rec = fish_db.extract_fish_records(each_fish)
        print("fish_no:{}".format(each_fish))
        ttl_feeds = fish_db.calc_total_and_avg_feed(fish_rec)
        last_training = fish_db.find_last_training(fish_rec)
        training_day = fish_db.find_training_day(fish_rec)
        for i, each_fish_rec in enumerate(fish_rec):
            print("\trec({}):{}".format(i, each_fish_rec))
        print("ttl_feeds:{}".format(ttl_feeds))
        print("last_training:{}".format(last_training))
        print("training_day:{}".format(training_day))
        print("\n")







