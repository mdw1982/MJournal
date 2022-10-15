#!/usr/bin/python3
import datetime
import sqlite3
import json
import PySimpleGUI as sg
from settings import *


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
    with open('README', 'r') as r:
        readme = r.read()
    return readme


def first_entry():
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME']
    data = (1, 'WELCOME', int(datetime.datetime.now().strftime('%m')), int(datetime.datetime.now().strftime('%d')), int(datetime.datetime.now().strftime('%Y')),
            '', str(get_readme()), datetime.datetime.now().strftime('%H:%M'),1)
    sql = """insert into entries (id, title, month, day, year, tags, body, time, visible) values(?,?,?,?,?,?,?,?,?);"""
    return sql,data


def drop_dummy():
    os.system('rm -f ./dummy.db')
    return None


def init_setup():
    tables = db_sql()

    # read the local db config json file
    with open('ldb_config.json', 'r') as d:
        lc = json.load(d)

    conn = sqlite3.connect(lc['database'])
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
    dlist = []
    with open('dblist', 'r') as f:
        for l in f.readlines():
            dlist.append(l.replace('\n', ''))
    with open('dblist', 'w') as dl:
        for i in dlist:
            if i == 'dummy.db':
                drop_dummy()
                continue
            dl.writelines(i+'\n')
        dl.write(lc['database'])
    with open('cdb', 'w') as c:
        c.writelines(lc['database'])
    sg.Popup('SUCCESS!', "I was able to create your new database and all the tables.")


def create_new_db(dbname):
    tables = db_sql()

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
    dlist = []
    with open('dblist', 'r') as f:
        for l in f.readlines():
            dlist.append(l.replace('\n',''))
        dlist.append(dbname)
    print(dlist)
    with open('dblist', 'w') as dl:
        for i in dlist:
            dl.writelines(i + '\n')
    sg.Popup('SUCCESS!', "I was able to create your new database and all the tables.")


def new_db_window():
    frm_layout = [
        [sg.Input('', size=(30,1), key='DBNAME')],
        [sg.Button('Create Database', key='GO'), sg.Button('Cancel', key='cancel')]
    ]
    layout = [
        [sg.Text('Input a name for the new database in the form of name.db\n It will be placed'
                 'in the root of the program directory with the other database(s)', font=std_font)],
        [sg.Frame('Create New Database', frm_layout)]
    ]
    window = sg.Window('New Database Creation', layout, location=window_location, finalize=True)
    event, values = window.read()
    while True:
        if event == 'cancel' or sg.WIN_CLOSED:
            break
        if event == 'GO':
            print(values['DBNAME'])
            create_new_db(values['DBNAME'])
            window.close()
            break
    window.close()
