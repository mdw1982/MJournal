import base64
import sys
import time
import os
from pathlib import Path
import subprocess
path_root = Path(__file__).parents[0] #subprocess.getoutput('pwd')
sys.path.append(str(path_root))
import PySimpleGUI as sg
import sqlite3
import datetime as dt
import logging
#from src.dblib import *
from src import logcheck

def log_name_date():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    m = n.strftime('%m')
    d = n.strftime('%d')
    return y + '-' + m + '-' + d

whereami = subprocess.getoutput('pwd')
window_location = (500, 210)
std_font = ('Sans Mono', 11)
logpath = f'{whereami}/logs/'
lfn = logpath + 'mjournal' + log_name_date() + '.log'


try:
    cdbfile = os.getcwd() + '/cdb'
    with open(cdbfile, 'r') as d:
        database = d.read().replace('\n', '')
    print(database)
except Exception as e:
    sg.PopupError("!!!ERROR!!!", f"Error Opening file cdb to read the current active database file: {e}")


def base64_image(img_path):
    with open(img_path, 'rb') as i:
        imgstr =  base64.b64encode(i.read())
    return imgstr


def get_database():
    cdbfile = os.getcwd() + '/cdb'
    with open(cdbfile, 'r') as d:
        db = d.read().replace('\n', '')
    return db


def tp_reload():
    msg = '''
    This button has one purpose... to reload the program after it's been sitting for a while doing nothing but 
    sitting idle. Comes in handy to prevent the program from exiting during an entry update.'''
    return msg


def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'


def set_database():
    global database
    cdbfile = os.getcwd() + '/cdb'
    with open(cdbfile, 'r') as d:
        db = d.read().replace('\n', '')
    print(db)
    database = db


def change_database(dname):
    cdbfile = os.getcwd() + '/cdb'
    with open(cdbfile, 'w') as f:
        f.writelines(dname)
    set_database()


def read_dblist():
    dl = []
    dblistfile = os.getcwd() + '/dblist'
    with open(dblistfile, 'r') as f:
        dl = list(f.read().split(','))
        for db in dl:
            if db == '':
                dl.pop()
    return dl


def convert_user_tuple(l):
    n = []
    for line in l:
        line = list(line)
        n.append(line)
    if n[0]:
        return n[0]
    else:
        return n


def get_current_theme():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    theme = convert_user_tuple(c.execute('select theme from settings;').fetchall())
    #print(theme)
    return theme


def get_them_list():
    theme_name_list = sg.theme_list()
    return theme_name_list


def common_progress_bar():
    # layout the form
    layout = [
        [sg.Push(),sg.ProgressBar(1, border_width=0, orientation='h', size=(20, 20), key='progress'),sg.Push()]
        ]

    # create the form`
    window = sg.Window('', layout, location=(530, 320), size=(200, 50), border_depth=0, resizable=True)
    progress_bar = window['progress']
    # loop that would normally do something useful
    for i in range(2095):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        if event == 'Cancel' or event == None:
            break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.update_bar(i + 1, 2095)
    # done with loop... need to destroy the window as it's still open
    window.close()


def change_settings(t,s):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sid = convert_user_tuple(c.execute('select max(sid) from settings;').fetchall())
        #print('In change Settings sid equals: ', sid[0])
        if sid[0] == None:
            # that means there's nothing in the table and we're doing an insert
            print("did't find any records in the table settings")
            s = 0
            c.execute(f'insert into settings (sid, theme, pwsec) values (1,\"{t}\", {s});')
            conn.commit()
        else:
            # Found something in the table and we're doing an update
            #print(f'Changing sec to {s} The theme going to be set to: ', t)
            sql = f'''update settings set theme=\'{t}\', pwsec={s} where sid={sid[0]};'''
            c.execute(sql)
            conn.commit()
            c.close()
    except Exception as e:
        sg.PopupError("!!!ERROR!!!", f"Running in change_settings() but ran into a problem\n{e}")


def is_first_run():
    frfile = cdbfile = os.getcwd() + '/firstrun'
    with open(frfile, 'r') as f:
        val = f.read()
    print(val)
    if val == 'True':
        with open(frfile, 'w') as f:
            f.writelines('False')
        return True
    else:
        return False

def dbbu_runcheck():
    from os.path import exists
    whereami = os.getcwd()
    try:
        path = f'{whereami}/backups'
        files = os.listdir(path)
        filelist = {}
        for f in files:
            filelist[f] = os.stat(f'{path}/{f}').st_mtime
        #print(filelist)
        os.chdir(f'{path}')
        """
            in the following for look k == the log file name and v it's age in seconds.
            what we're doing here is converting that age in seconds to days. Once that is found
            we're going to move anything older than 7 days off to a subfolder of logs to oldlogs
        """
        for k, v in reversed(filelist.items()):
            age = round((time.time() - v))
            days = round(age / 86400)       # 7 days
            print(f"age of {k} is {days} days old", flush=True)
            print(days, flush=True)
            filelist[k] = days

        if not exists(path):
            os.makedirs(path)
        else:
            for filename, age in filelist.items():
                if age > 7:
                    os.remove(f'{path}/{filename}')
                else:
                    print("PROCESSING: module:setting.dbbu_runcheck() - no backups have aged out. nothing to remove...",flush=True)
        os.chdir('../')
    except Exception as e:
        print(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups {e}")
    finally:
        print(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups. Check log for more information",flush=True)