import hashlib
import pymysql
from pymysql import Error

'''
    I wasn't able to use MySQL for Python... it was being a real dumb as getting this class put together.
    And, I don't like the fact that the user credentials are in the open as they are, but until/unless 
    I find out how MySQL hashes it's password I can't use hashed passwords to authenticate.
'''
#user, passwd = ('mweaver', 'Lilo0311@')         # don't like having it this way in the open as it were
class MysqlConn():                              # eventually these will be specific credentials to the program.

    def __init__(self, host, user, passwd, database=None):    # database may not always be required for the __init__ method
        self.host = host
        self.user = user
        self.passwd = passwd
        if database == None:
            try:
                # make the connection...
                db = pymysql.Connect(
                    host=self.host,
                    user=self.user,
                    password=self.passwd, cursorclass=pymysql.cursors.DictCursor)
            except Error as e:
                print(f"MysqlConn(__init__): something went wrong when I tried to make the connection: {e}")
        self.database = database
        # make the connection...
        try:
            db = pymysql.Connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.passwd,cursorclass=pymysql.cursors.DictCursor)
            self.cursor = db.cursor()
        except Error as e:
            print(f"MysqlConn(__init__): something went wrong when I tried to make the connection: {e}")

    def open(self):
        db = pymysql.Connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.passwd, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = db.cursor()

    def fetch(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def insert(self, sql):
        try:
            self.cursor.execute(sql)    # interesting that the IDE (PyCharm) doesn't offer the commit() method
            return ('success','values inserted successfully')
        except Error as e:
            return ('failed', e)

    def close(self):
        self.cursor.close()

    def create_db(self, dbname):
        self.cursor.execute("show databases")
        checkdb = self.cursor.fetchall()
        if dbname in checkdb:
            print(f"database {dbname} already exists.")
            return ('exists',f'database {dbname} already exists')
        try:
            self.cursor.execute(f'create database {dbname}')
            self.cursor.execute(f'use {dbname}')
            return ('success',f"I was able to create the database {dbname}")
        except Error as e:
            print(f"I had a problem creating the database as you requested.\n", e)
            return ('failed',e)
    
    def new_table(self,sql):
        try:
            self.cursor.execute(sql)
            print("I've finished creating your tables... all went well!")
        except Error as e:
            print("I ran into an error creating your table(s)\n",e)

    def update(self,sql):
        try:
            self.cursor.execute(sql)
        except Error as e:
            print(f"something has gone wrong with your db update: {e}")

    def get_hashed(self, pw):
        salt = 'dfgasreawaf566dsfkjapios890asdhloijkhsxz'
        dbpass = pw + salt
        self.hashed = hashlib.md5(dbpass.encode())
        self.hashed = self.hashed.hexdigest()
        return self.hashed


