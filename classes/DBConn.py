import os.path
import sqlite3
from sqlite3 import Error
import logging


class DBConn:

    def __init__(self, database):
        '''
        The __init__ method takes one parameter: the database name. this value is set at the very beginning of
        the program as a global variable read from a file on disk (cdb). it is the active database for the program.
        :param database:
        '''
        self.database = database
        self.conn = sqlite3.connect(self.database)  # yet as clean as I'd prefer but it's better than what it was.
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        logging.info(f"DBConn.init: new instance created...")


    def set_dbname(self,db):
        self.database = db

    def set_user(self, user):
        self.user = user

    def get_user(self):
        return self.user


    def update_property(self, property, value):
        setattr(self, property, value)


    def open(self):
        '''
        open takes no parameters but gets its information from the existing dbo object. this allows the cursor to be
        closed and reopened without creating a new DBConn object. the original remains in tact the entire time the
        program runs.
        :return:
        '''
        self.conn = sqlite3.connect(self.database)  # yet as clean as I'd prefer but it's better than what it was.
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()


    def get(self,sql):
        '''
        standard query to retrieve inforamtion from the active datbbase. all get methods return results as a dictionary.
        field names as keys are returned.
        :param sql:
        :return:
        '''
        results = []
        try:
            self.c.execute(sql)
            logging.info(f"DBConn.get: received a call to get() {sql}")
            results = [dict(row) for row in self.c.fetchall()]
            logging.info(f"DBConn.get: have results of query")
        except Error as e:
            logging.error(f"DBConn.get: I had a problem getting your data: {e}", exc_info=True)
        if not results:
            logging.warning(f"DBConn.set: Results empty set: {results}", exc_info=True)
            return ''
        else:
            logging.info(f"")
            return results[0]

    def get_list(self,sql):
        res = []
        try:
            logging.info(f"DBConn.get_list: {sql}")
            res = self.c.execute(sql).fetchall()
        except Error as e:
            logging.error(f"DBConn.get_list: There was an error: {e}",exc_info=True)
        return res

    def get_rows(self, sql):
        '''
        standard query to retrieve inforamtion from the active datbbase. all get methods return results as a dictionary.
        field names as keys are returned.
        :param sql:
        :return:
        '''
        try:
            logging.info(f"{__name__}.get_rows: {sql}")
            self.c.execute(sql)
            results = [dict(row) for row in self.c.fetchall()]
            if not results:
                logging.warning(f"DBConn.get_rows: empty set - {results}")
                return ''
            else:
                logging.info(f"DBConn.get_rows-else: building list of rows {sql}")
                rows = []
                for k, v in results[0].items():
                    rows.append(v)
                return rows
        except Error as e:
            logging.error(f"DBConn.get_rows: I had a problem getting your data: {e}",exc_info=True)


    def insert(self,*args):
        '''
        The insert method takes a special argument: *args to accomodate a few instances where sql and data are
        being passed to the dbo.insert method. the insert method will take one or more arguments but mainly just two are
        expected depending on how you structure your insert statement. this is specific to SQLite databases.
        :param *args: sql = 'insert into database (field1, field2, field3) values (?,?,?);'
                      data = f"{dict['id']},{dict['title']},{dict['body']}"
        :return:
        '''
        try:
            logging.info(f"DBConn.insert: *****")
            self.c.execute(*args)
            self.conn.commit()
        except Error as e:
            logging.error(f"DBConn.insert: An Error has occurred while performing the insert: {e}",exc_info=True)
            return ('failure',e)
        else:
            return ('success','')

    def restore(self, sql, path):
        try:
            logging.info(f"DBConn.restore: {sql}:{path}")
            db = os.path.join(path, 'restore.db')
            conn = sqlite3.connect(db)  # yet as clean as I'd prefer but it's better than what it was.
            conn.cursor()
            c = conn.cursor()
            c.executescript(sql)
        except Error as e:
            logging.error(f"I experienced a problem restoring your database: {e}", exc_info=True)
            return ('failure', e)
        else:
            logging.info(f"DBConn.restore: Successfully restored {db}")
            return ('success',f'restoration was successful. Restored database: {db}')

    def update(self,sql):
        try:
            logging.info(f"DBConn.update: ")
            self.c.execute(sql)
            self.conn.commit()
        except Error as e:
            logging.error(f"DBConn.update: {e}")

    '''
        this method added 3.30.24 to support the unlock utility built to be used in the event the 
        user locked themselves out of the program by turning on password protection BEFORE setting 
        their username and password. It is essentially an update statement, however I created it
        so things would be a bit more clear in the code.
    '''
    def unlock(self,sql):
        try:
            logging.info(f"DBConn.unlock: {sql}")
            self.c.execute(sql)
            self.conn.commit()
            self.conn.execute('delete from users where uid > 0')
            self.conn.commit()
            logging.info(f"DBConn.unlock: successful")
        except Exception as e:
            logging.error(f"something went wrong with your query {sql}: {e}",exc_info=True)
            return (f"something went wrong with your query {sql}: {e}")
        return "I was able to unlock your database"

    def get_title(self,id):
        try:
            logging.info(f"{__name__}.get_title: fetching title for entry id: {id}")
            self.c.execute(f"select title from entries where id={id};")
            title = [dict(row) for row in self.c.fetchall()]
            return title[0]
        except Error as e:
            logging.error(f"{__name__}.get_title: Error: if {id} -- {e}")

    def get_body(self,id):
        try:
            self.c.execute(f"select body from entries where id={id}")
            body = [dict(row) for row in self.c.fetchall()]
            return body[0]
        except Error as e:
            logging.error(f"{__name__}.get_body: Error fetching body: id {id} -- {e}")

    def close(self):
        logging.info(f"{__name__}.close: Closing cursor: ")
        self.c.close()