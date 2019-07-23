import sqlite3


class SQL_Data:
    def __init__(self ,_file_name):
        self.connection = sqlite3.connect("myTable.db")
        self.crsr = self.connection.cursor()

    def table_create(self):
        # SQL command to create a table in the database
        sql_command = """CREATE TABLE fish_data (  
                staff_number INTEGER PRIMARY KEY,  
                fname VARCHAR(20),  
                lname VARCHAR(30),  
                gender CHAR(1),  
                joining DATE);"""

        # execute the statement
        self.crsr.execute(sql_command)
        self.connection.commit()

    def get_data(self):
        pass

    def write_data(self):
        # SQL command to insert the data in the table
        sql_command = """INSERT INTO fish_data VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
        self.crsr.execute(sql_command)

        # another SQL command to insert the data in the table
        sql_command = """INSERT INTO fish_data VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
        self.crsr.execute(sql_command)

        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        self.connection.commit()

    def __del__(self):
        self.connection.close()
#


if __name__ == '__main__':
    sql_inst = SQL_Data()
    sql_inst.write_data()
