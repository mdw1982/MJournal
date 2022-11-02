import sqlite3
class DBConn:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)  # yet as clean as I'd prefer but it's better than what it was.
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def get(self, sql):
        self.c.execute(sql)
        results = [dict(row) for row in self.c.fetchall()]
        return results[0]

    def insert(self,*args):
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