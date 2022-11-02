import sqlite3
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

    def get(self, sql):
        '''
        standard query to retrieve inforamtion from the active datbbase. all get methods return results as a dictionary.
        field names as keys are returned.
        :param sql:
        :return:
        '''
        self.c.execute(sql)
        results = [dict(row) for row in self.c.fetchall()]
        return results[0]

    def insert(self,*args):
        '''
        The insert method takes a special argument: *args to accomodate a few instances where sql and data are
        being passed to the dbo.insert method. the insert method will take one or more arguments but mainly just two are
        expected depending on how you structure your insert statement. this is specific to SQLite databases.
        :param *args: sql = 'insert into database (field1, field2, field3) values (?,?,?);'
                      data = f"{dict['id']},{dict['title']},{dict['body']}"
        :return:
        '''
        self.c.execute(*args)
        self.conn.commit()

    def update(self,sql):
        self.c.execute(sql)
        self.conn.commit()

    def get_title(self,id):
        self.c.execute(f"select title from entries where id={id};")
        title = [dict(row) for row in self.c.fetchall()]
        return title[0]

    def get_body(self,id):
        self.c.execute(f"select body from entries where id={id}")
        body = [dict(row) for row in self.c.fetchall()]
        return body[0]

    def close(self):
        self.c.close()