import datetime
import os
import sqlite3
import json
import time

import PySimpleGUI as sg
from settings import *


icon_img = base64_image('images/MjournalIcon_36x36.png')
popup_location = (870,470)

def db_sql():
    entries = '''create table entries (
                id integer PRIMARY KEY,
                title varchar(500),
                month integer,
                day integer,
                year integer,
                tags varchar(300),
                body blob,
                time varchar(5),
                visible int DEFAULT 1           
                );
                '''

    users = '''create table users (
                    uid INTEGER NOT NULL,
                    user text,
                    password text,
                    PRIMARY KEY("uid" AUTOINCREMENT));'''

    settings = '''CREATE TABLE settings(
    	                sid	INTEGER NOT NULL,
    	                theme	TEXT DEFAULT 'none',
    	                pwsec	INTEGER DEFAULT 0,
    	                PRIMARY KEY("sid" AUTOINCREMENT)
                    );'''
    t = []
    t.append(entries)
    t.append(users)
    t.append(settings)
    return t

def first_settings_entry():
    #['SID', 'THEME', 'PWSEC', 'CURRENT_DATABASE']
    data = (None, 'DarkBlue1', 0)
    sql = """insert into settings (sid, theme, pwsec) values(?,?,?);"""
    return sql,data


def get_readme():
    # if detect_os() == 'Linux':
    #     readmefile = os.getcwd() + '/README'
    # if detect_os() == 'windows':
    #     readmefile = os.getcwd() + "\\" + 'README'
    readmefile = os.path.join(os.getcwd(),'README')
    with open(readmefile, 'r') as r:
        readme = r.read()
    return readme

def get_first_entry():
    # if detect_os() == 'Linux':
    #     firstmsg = os.getcwd() + '/FIRSTMSG'
    # if detect_os() == 'windows':
    #     firstmsg = os.getcwd() + "\\" + 'FIRSTMSG'
    firstmsg = os.path.join(os.getcwd(),'FIRSTMSG')
    with open(firstmsg, 'r') as r:
        frstmsg = r.read()
    return frstmsg

def first_entry():
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME']
    data = (1, 'WELCOME', int(datetime.datetime.now().strftime('%m')), int(datetime.datetime.now().strftime('%d')), int(datetime.datetime.now().strftime('%Y')),
            '', str(get_first_entry()), datetime.datetime.now().strftime('%H:%M'),1)
    sql = """insert into entries (id, title, month, day, year, tags, body, time, visible) values(?,?,?,?,?,?,?,?,?);"""
    return sql,data


def drop_dummy():                   # this one is definitely going to need to be refactored. This function and command
    os.system('rm -f ./dummy.db')   # function depricated... will be removed. no longer used.
    return None


def init_setup():
    tables = db_sql()
    # getting path to the config file
    ldbjsonfile = os.path.join(os.getcwd(),'ldb_config.json')

    # read the local db config json file
    with open(ldbjsonfile, 'r') as d:
        lc = json.load(d)

    conn = sqlite3.connect(lc['database'])  # creating the jounal database
    print(f"creating db connection to {lc['database']}... just inside init_setup()")
    c = conn.cursor()
    try:
        for sql in tables:
            print(sql)
            c.execute(sql)
            conn.commit()
    except Exception as e:
        sg.PopupError('SQL Error', f"I've experienced a problem creating the tables in your new database\n{e}")
    sql, data = first_entry()
    c.execute(sql,data)
    conn.commit()
    s, d = first_settings_entry()
    c.execute(s, d)
    conn.commit()
    conn.close()

    dlist = read_dblist()   # setup program bombing on Windows when it hits this statement
    for i in dlist:
        if i == 'dummy.db':
            #drop_dummy()
            srcpath =  os.getcwd() + '\\' + i
            #destpath = convert_path_to_file(i,detect_os(),'olddb')
            #print(f"checking for directory: {destpath}")
            olddb = os.getcwd() + '\\' + 'olddb'
            if not exists(olddb):    # need to create the destination path to moce dummy.db into it
                print(f"Destination path: {olddb} does not exist. creating it.")
                os.mkdir(olddb)
                time.sleep(1.5)
            destpath = olddb + '\\' + i
    print('getting ready to move dummy.db to olddb')
    os.rename(srcpath, destpath)  # setup program bombing on Windows when it hits this statement
    print('from module dbsetup about to read dblist - read_dblist()')
    read_dblist()
    cdbtfile = os.getcwd() + '\\' + 'cdb'
    try:
        print(f"writing new database name- {lc['database']} to cdb file")
        with open(cdbtfile, 'w') as c:
            c.writelines(lc['database'])
        print('SUCCESS!', "I was able to create your new database and all the tables.")
        print('returning from dbsetup to setup program.........................')
    except Exception as e:
        print(f"I experienced an issue finishing up with init_setup: {e} : starting at line 131")


def create_new_db(dbname):
    if '.db' not in dbname:
        dbname = f"{dbname}.db"
    tables = db_sql()
    dirdbfile = []
    dir = os.getcwd()
    oldfiles = []
    # check root dir for database files
    for file in os.listdir(dir):
        if file.endswith(".db"):
            dirdbfile.append(file)
    olddir = os.path.join(os.getcwd(),'olddb')
    for oldfile in os.listdir(olddir):
        if oldfile.endswith('.db'):
            oldfiles.append(oldfile)
    if dbname in dirdbfile:
        return sg.PopupError('DB Create Error',f'The database {dbname} already exists.', icon=icon_img, location=popup_location)
        #return window.refresh()
    if dbname in oldfiles:
        return sg.PopupError('!!!DB Create Error', f'The database {dbname} already exists in folder olddb. '
                                         f'If you are certain the file is good, use database maintenace '
                                         f'and attach it to the active database list.', icon=icon_img,
                      location=popup_location)

    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    try:
        for sql in tables:
            print(sql)
            c.execute(sql)
            conn.commit()
    except Exception as e:
        sg.PopupError('SQL Error', f"I've experienced a problem creating the tables in your new database\n{e}")
    sql, data = first_entry()
    c.execute(sql,data)
    conn.commit()
    s, d = first_settings_entry()
    c.execute(s, d)
    conn.commit()
    conn.close()
    read_dblist()
    sg.Popup('SUCCESS!', f"I was able to create your new database {dbname} and all the tables.", icon=icon_img, location=popup_location)


def new_db_window():
    frm_layout = [
        [sg.Input('', size=(30,1), key='DBNAME', enable_events=True, tooltip='just input the name with no extension')],
        [sg.Button('Create Database', key='GO'), sg.Button('Cancel', key='cancel')]
    ]
    layout = [
        [sg.Text('Input a name for the new database in the form of name...\n no extension. That will be added by the program.\n It will be placed'
                 'in the root of the program directory with the other database(s)', font=std_font)],
        [sg.Push(),sg.Frame('Create New Database', frm_layout)]
    ]
    window = sg.Window('New Database Creation', layout, location=window_location, icon=icon_img, finalize=True)
    window['DBNAME'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event == 'cancel' or sg.WIN_CLOSED:
            break
        if event == 'GO' or '_Enter' in event:
            print(values['DBNAME'])
            create_new_db(values['DBNAME'])
            window.close()
            break
    window.close()