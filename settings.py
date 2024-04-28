import base64
import sys
import time
import os
from pathlib import Path
from os.path import exists
import subprocess
import json
import PySimpleGUI as sg
import sqlite3
import datetime as dt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.


def log_name_date():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    m = n.strftime('%m')
    d = n.strftime('%d')
    return y + '-' + m + '-' + d

def get_year():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    return y


whereami = subprocess.getoutput('pwd')
window_location = (500, 210)
std_font = ('Sans Mono', 11)
logpath = f'{whereami}/logs/'
lfn = logpath + 'mjournal' + log_name_date() + '.log'

try:
    cdbfile = os.getcwd() + '/cdb'
    with open(cdbfile, 'r') as d:
        database = d.read().replace('\n', '')
    # print(database)
except Exception as e:
    sg.PopupError("!!!ERROR!!!", f"Error Opening file cdb to read the current active database file: {e}")



def base64_image(img_path):
    with open(img_path, 'rb') as i:
        imgstr = base64.b64encode(i.read())
    return imgstr


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


# def read_dblist():
#     dl = []
#     dblistfile = os.getcwd() + '/dblist'
#     with open(dblistfile, 'r') as f:
#         dl = list(f.read().split(','))
#         for db in dl:
#             if db == '':
#                 dl.pop()
#     return dl
def read_dblist():
    def load_dblist():
        '''possible replacement for read_dblist'''
        # if detect_os() == 'Linux':
        #     dlistjson = os.getcwd() + "/" + 'dblist.json'
        # if detect_os() == 'windows':
        #     dlistjson = os.getcwd() + "\\" + 'dblist.json'
        dlistjson = os.path.join(os.getcwd(),'dblist.json')
        dblist = []
        temp = os.listdir(os.getcwd())
        for f in temp:
            if f.endswith('.db'):
                dblist.append(f)
        dblist = sorted(dblist, reverse=False)
        # print(dblist)

        # creating/loading the dblist json file
        with open(dlistjson, 'w') as dj:
            temp = {}
            i = 0
            for d in dblist:
                temp[i] = d
                i += 1
            dblist = json.dumps(temp, indent=len(temp))
            dj.write(dblist)

    def get_dblist():
        # if detect_os() == 'Linux':
        #     dlistjson = os.getcwd() + "/" + 'dblist.json'
        # if detect_os() == 'windows':
        #     dlistjson = os.getcwd() + "\\" + 'dblist.json'
        dlistjson = os.path.join(os.getcwd(), 'dblist.json')

        if exists(dlistjson):
            with open(dlistjson, 'r') as d:
                dlist = json.load(d)

            thedblist = []
            for k, v in dlist.items():
                thedblist.append(v)
            # print(thedblist)
            return thedblist
        load_dblist()

    def read_db_ondisk():
        dblist = []
        temp = os.listdir(os.getcwd())
        for f in temp:
            if f.endswith('.db'):
                dblist.append(f)
        dblist = sorted(dblist, reverse=False)
        return dblist

    if get_dblist() != read_db_ondisk():
        print(f"I've found an inconsistency between database files in the dblist and on disk\n"
              f"dblist file reads\n{get_dblist()}\ndatabase files on disk are\n"
              f"{read_db_ondisk()}")
        load_dblist()  # this is sending it back to get_dblist() in the event that dblist.json doesn't exist
        # it will get created... with this check here if there are more database files on disk than
        # in the list, the list will get rewitten... at least that's the plan.
    return get_dblist()


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
    # print(theme)
    return theme


def convert_path_to_file(filename, platform, dir=None):
    '''stupid shit ya gotta go through to make a program cross-platform compatible'''
    if platform == 'Linux':
        if dir != None:
            fullpath = os.getcwd() + f"/{dir}/" + filename
        fullpath = os.getcwd() + '/' + filename
        return fullpath
    if platform == 'windows':
        if dir != None:
            fullpath = os.getcwd() + f"\\{dir}\\" + filename
        fullpath = os.getcwd() + "\\" + filename
        return fullpath


def get_them_list():
    theme_name_list = sg.theme_list()
    return theme_name_list


def common_progress_bar():
    # layout the form
    layout = [
        [sg.Push(), sg.ProgressBar(1, border_width=0, orientation='h', size=(20, 20), key='progress'), sg.Push()]
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


def get_database():
    cdbfile = convert_path_to_file('cdb', detect_os())
    with open(cdbfile, 'r') as d:
        db = d.read().replace('\n', '')
    return db


def set_database():
    global database
    cdbfile = convert_path_to_file('cdb', detect_os())
    with open(cdbfile, 'r') as d:
        db = d.read().replace('\n', '')
    # print(db)
    database = db


def change_database(dname):
    cdbfile = convert_path_to_file('cdb', detect_os())
    with open(cdbfile, 'w') as f:
        f.writelines(dname)
    set_database()


def change_settings(t, s):
    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sid = convert_user_tuple(c.execute('select max(sid) from settings;').fetchall())
        # print('In change Settings sid equals: ', sid[0])
        if sid[0] == None:
            # that means there's nothing in the table and we're doing an insert
            print("did't find any records in the table settings")
            s = 0
            c.execute(f'insert into settings (sid, theme, pwsec) values (1,\"{t}\", {s});')
            conn.commit()
        else:
            # Found something in the table and we're doing an update
            # print(f'Changing sec to {s} The theme going to be set to: ', t)
            sql = f'''update settings set theme=\'{t}\', pwsec={s} where sid={sid[0]};'''
            c.execute(sql)
            conn.commit()
            c.close()
    except Exception as e:
        sg.PopupError("!!!ERROR!!!", f"Running in change_settings() but ran into a problem\n{e}")


def is_first_run():
    frfile = convert_path_to_file('firstrun', detect_os())
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
    try:
        path = os.path.join(os.getcwd(),'backups')
        files = os.listdir(path)
        filelist = {}
        for f in files:
            filelist[f] = os.stat(os.path.join(path,f)).st_mtime
        #print(filelist)
        os.chdir(path)
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
                    #logging.info(f"PROCESSING: module:setting.dbbu_runcheck() removing {filename} which is {age} days old to {path}")
                    os.remove(os.path.join(path,filename))
                    print(f"{filename} was aged {age} days and was removed.")
                else:
                    print(f"{filename} aged {age} days was not removed.")
        os.chdir('../')
    except Exception as e:
        print(f"RUNNING: module: {__file__}.dbbu_runcheck() - unable to process database backups {e}")
        #logging.error(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups {e}", exc_info=True)
    finally:
        print(f"RUNNING: module: {__file__}.dbbu_runcheck() - runcheck completed successfully",flush=True)

def clear_orphans():
    # right now this only works on Linux. I'll have to find a way to get this working
    # in windows.
    procs = subprocess.getoutput('pgrep MJournal')
    plist = procs.splitlines()
    plist = sorted(plist)
    if len(plist) > 1:
        live = plist.pop(len(plist) - 1)
        print(plist)
        print(live)
        for p in plist:
            print(f"killing process: {p}")
            os.system(f"kill -9 {p}")


def restart():      # I REALLY need to be able to tell if the program is running as binary or script
    '''
    :param: NONE
    :return: returns the command to restart the program after clearing orphaned processes/instances of
             the program that were left running in the past. Over time these orphanced processes would
             build up and cause problems.
             -----------------------------------------
             I'm not sure I'm going to keep this block of code because it's only useful on the windows
             branch and doesn't do anything here. On linux it's literally the last three lines of the
             block and it literally doesn't better if I'm running the binary version of the source file
             from within the IDE.
    '''
    # if detect_os() == 'windows':
    #     if exists(os.path.join(os.getcwd(),'MJournal.exe')):
    #         # I'll have to write a version of this for windows
    #         #clear_orphans()
    #         command = 'MJournal.exe'
    #         return os.system(os.path.join(os.getcwd(),command))
    #     else:
    #         #clear_orphans()
    #         command = 'MJournal'
    #         print(f"restarting the program: {command}")
    #         return os.system(os.path.join(os.getcwd(), command))
    print('inside the restart() function... sending command')
    clear_orphans()
    return os.execl(sys.executable, sys.executable, *sys.argv)

def close_app(app_name):
    import psutil
    prdt_lst = []
    pid_lst = []
    for proc in psutil.process_iter():
        if proc.name() == app_name:
            prdt = proc.create_time()
            prdt_lst.append(prdt)
            pid_lst.append(proc.pid)

    if prdt_lst > [0]:
        (m, i) = max((v, i) for i, v in enumerate(prdt_lst))
        # print(m, i)

        for indx, value in enumerate(prdt_lst):
            if indx == i:
                continue

            # print(pid_lst[indx])
            psutil.Process(pid_lst[indx]).terminate()
