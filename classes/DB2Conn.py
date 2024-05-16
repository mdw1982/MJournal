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

    def set_dbname(self, db):
        self.database = db


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
            print(results)
            return results
        except Error as e:
            print(f"I had a problem getting your data: {e}")


    def insert(self, *args):
        '''
        The insert method takes a special argument: *args to accomodate a few instances where sql and data are
        being passed to the dbo.insert method. the insert method will take one or more arguments but mainly just two are
        expected depending on how you structure your insert statement. this is specific to SQLite databases.
        :param *args: sql = 'insert into database (field1, field2, field3) values (?,?,?);'
                      data = f"{dict['id']},{dict['title']},{dict['body']}"
        :return:
        '''
        try:
            self.c.execute(*args)
            self.conn.commit()
        except Error as e:
            print(f"An Error has occurred while performing the insert: {e}")
            return ('failure', e)
        else:
            return ('success', '')

    def update(self, sql):
        try:
            self.c.execute(sql)
            self.conn.commit()
        except Error as e:
            print(f"An Error has occurred while performing the update: {e}")
            return ('failure', e)
        else:
            return ('success', '')


    def close(self):
        self.c.close()