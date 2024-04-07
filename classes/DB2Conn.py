import os.path
import sqlite3 as db
from sqlite3 import Error
'''
    this is a re-write of the DBConn class or DB Connection class. There are some things that DBConn is doing that
    don't lend itself to smooth operation. Most of that is the manner in which the connection is made in the 
    __init__ method of the class. I personnaly hate dealing with tuples, so I'm refactoring this class to 
    get rid of dealing with tuples.
'''
class DB2Conn:
    def __init__(self, database):
        '''
        The __init__ method takes one parameter: the database name. this value is set at the very beginning of
        the program as a global variable read from a file on disk (cdb). it is the active database for the program.
        :param database:
        '''
        self.database = database
        self.conn = db.connect(self.database)  # yet as clean as I'd prefer but it's better than what it was.
        self.conn.row_factory = lambda cursor, row: row[0]
        self.c = self.conn.cursor()

    def get_list(self,sql):
        res = []
        try:
            res = self.c.execute(sql).fetchall()
        except Error as e:
            print(f"There was an error: {e}")
        return res

    def get_list_of_years(self):
        res = []
        try:
            res = self.c.execute('select year from entries').fetchall()
        except Error as e:
            print(f"There was an error: {e}")
        return sorted(list(set(res)),reverse=True)

    def get_title(self,id):
        title = self.c.execute(f"select title from entries where id={id};").fetchall()
        print(title)
        return title

    def get(self,sql):
        try:
            results = self.c.execute(sql).fetchall()
        except Error as e:
            print(f"I had a problem getting your data: {e}")
        return results

    def close(self):
        self.c.close()