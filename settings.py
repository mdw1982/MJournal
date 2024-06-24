import base64
import hashlib
import sys
import time
import os
from pathlib import Path
from os.path import exists
import subprocess
import json
import FreeSimpleGUI as sg
import sqlite3
import datetime as dt
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.
from classes.DB2Conn import DB2Conn

######################################################################################################################
#   MJOURNAL MAIN LIBRARY FILE                                                                                       #
#   ==============================================                                                                   #
#   CONTAINS ALL THE BITS AND BOBS THAT HAVE BEEN STUFFED IN HERE IN AN EFFORT TO KEEP THE MAIN                      #
#   PROGRAM FILE AS CLEAN AS POSSIBLE.
salt = 'qP8JAx!mk527QWfFYd8C1FBg'
######################################################################################################################
def get_hashed_pass(upass: str):
    #salt = 'dfgasreawaf566'
    dbpass = upass + salt
    hashed = hashlib.md5(dbpass.encode())
    hashed_pass = hashed.hexdigest()
    return hashed_pass

def check_user_info():
    pass

def entry_encode(entry: str):
    pass

def entry_decode(enc_entry: str):
    pass

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


def runcheck():
    try:
        files = os.listdir('logs')
        filelist = {}
        logs = os.path.join(os.getcwd(), 'logs')
        for f in files:
            filelist[f] = os.stat(os.path.join(logs, f)).st_mtime
            #filelist[f] = os.stat(f'./logs/{f}').st_mtime
        #print(filelist)

        os.chdir(os.path.join(os.getcwd(), 'logs'))
        """
            in the following for look k == the log file name and v it's age in seconds.
            what we're doing here is converting that age in seconds to days. Once that is found
            we're going to move anything older than 7 days off to a subfolder of logs to oldlogs
        """

        for k, v in reversed(filelist.items()):
            age = round((time.time() - v))
            days = round(age / 86400)
            # print(f"age of {k} is {days} days old")
            # print(days)
            filelist[k] = days

        path = os.path.join(os.getcwd(), 'oldlogs')
        # os.chdir('./logs')
        if not exists(path):
            os.makedirs(path)
        else:
            for filename, age in filelist.items():
                if age > 6:
                    logging.info(f"PROCESSING: module:logcheck.main() moving {filename} which is {age} days old to {path}")
                    os.system(f'mv {filename} {path}/{filename}')
        os.chdir('../')
    except Exception as e:
        logging.error(f"RUNNING: module: settings - unable to process logs {e}", exc_info=True)


def init_logs():
    try:
        print(f"Initializing logger...")
        logpath = os.path.join(os.getcwd(), 'logs')
        if not exists(logpath):
            os.mkdir(logpath)
        runcheck()
        fname = 'mjournal_' + log_name_date() + '.log'
        lfn = os.path.join(logpath, fname)
        logging.basicConfig(filename=lfn, filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)
    except Exception as e:
        print(f"::ERROR:: init_logs() - I wasn't able to create the log file: {e}")


def reload_dblist():
    dlistjson = os.path.join(os.getcwd(), 'dblist.json')
    dblist = []
    temp = os.listdir(os.getcwd())
    for f in temp:
        if f.endswith('.db'):
            dblist.append(f)
    dblist = sorted(dblist, reverse=False)
    return dblist

def set_new_db(nd: str) -> str:
    '''
    :type: str
    :param nd: type:str single argument that should be a dbname to be written into
               the defaults.json file. sole purpose is to write new dhname into defaults
    :return: None
    '''
    if not nd.endswith('.db'):
        sg.PopupError(f"{__name__}.set_new_db received incorrect information: {nd}\n"
                      f"was expecting a DB file. a file that ends with .db\n"
                      f"!!!PROGRAM ABEND!!!")
        exit(1)
    print(f"received new dbname: {nd}")
    dj = {}
    try:
        deffile = os.path.join(os.getcwd(), 'defaults.json')
        logging.info(f"{__name__}.set_new_db: checking to see if the file exists: {deffile}")
        #if exists(deffile):
        with open(deffile, 'r') as n:
            dj = json.load(n)
        dj['dbname'] = nd
        with open(deffile, 'w') as n:
            json.dump(dj, n, indent=4)
        #return nd
        #else:
            #sg.PopupError(f"Running in module {__file__}: {deffile} does not exist... no write has happened.")
    except Exception as e:
        sg.PopupError(f"Running in module {__name__}:set_new_db, line 241\n{e}")


def load_defaults() -> dict:
    '''
    :param: None
    :return: dict
    '''
    dfs = {}
    ldf = os.path.join(os.getcwd(), 'defaults.json')
    if exists(ldf):
        with open(ldf, 'r') as d:
            dfs = json.load(d)
    return dfs


def set_theme(t: str) -> str:
    '''
    :type: str
    :param t: takes one argyment type string. should be the name of a desired and writes it
              to the defaults.json file
    :return: None - once set in defaults dict it's available by name: defaults['theme']
    '''
    defset = os.path.join(os.getcwd(), 'defaults.json')
    df = load_defaults()
    df['theme'] = t
    with open(defset, 'w') as dts:
        json.dump(df, dts, indent=4)




def base64_image(img_path: str) -> str:
    '''
    :param img_path: Receives an image path complete with the image name...
    :return: Returns binary string for the image.
    '''
    with open(img_path, 'rb') as i:
        imgstr = base64.b64encode(i.read())
    return imgstr


def tp_reload():
    '''
    :param: None
    :return: Returns a message string for the tooltip when the user does a mouse over of the main screen Reload button.
    '''
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


def read_dblist():
    def load_dblist():
        '''possible replacement for read_dblist'''
        dlistjson = os.path.join(os.getcwd(), 'dblist.json')
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


def convert_user_tuple(lines):
    n = []
    for line in lines:
        line = list(line)
        n.append(line)
    if n[0]:
        return n[0]
    else:
        return n


def get_current_theme():
    # conn = sqlite3.connect(database)
    # c = conn.cursor()
    # theme = convert_user_tuple(c.execute('select theme from settings;').fetchall())
    # # print(theme)
    defs = load_defaults()
    return defs['theme']


def convert_path_to_file(filename, platform, dir=None):
    '''stupid shit ya gotta go through to make a program cross-platform compatible'''
    if platform == 'Linux':
        if dir != None:
            #fullpath = os.getcwd() + f"/{dir}/" + filename
            fullpath = os.path.join(os.getcwd(), filename)
        #fullpath = os.getcwd() + '/' + filename
        fullpath = os.path.join(os.getcwd(), filename)
        return fullpath
    if platform == 'windows':
        if dir != None:
            #fullpath = os.getcwd() + f"\\{dir}\\" + filename
            fullpath = os.path.join(os.getcwd(), filename)
        fullpath = os.path.join(os.getcwd(), filename)
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
    dfs = load_defaults()
    return dfs['dbname']


# def set_database():
#     global database
#     cdbfile = convert_path_to_file('cdb', detect_os())
#     with open(cdbfile, 'r') as d:
#         db = d.read().replace('\n', '')
#     # print(db)
#     database = db


def change_database(dname):
    # cdbfile = convert_path_to_file('cdb', detect_os())
    # with open(cdbfile, 'w') as f:
    #     f.writelines(dname)
    #set_database()
    set_new_db(dname)

def update_settings(t: str, s: int):
    '''
       Gets current values stored in defaults.json and loads them into a dict. from there it reads the current database,
       checks the value of pwsec and theme. updates the theme in the settings table and if parameter (s) different from
       what exists in that table the new value is inserted into the pwsec field.
       :param t: str: incoming theme name - requires program restart to take affect
       :param s: int: pwsec value which determines if we're using a password to open the database or not.
       :return: None
       '''
    defs = load_defaults()
    try:
        dbs = DB2Conn(defs['dbname'])
        sid = dbs.get('select max(sid) from settings;')
        if sid == None:
            # that means there's nothing in the table and we're doing an insert
            print("did't find any records in the table settings")
            print("did't find any records in the table settings")
            s = 0
            status, msg = dbs.insert(f'insert into settings (sid, theme, pwsec) values (1,\"{t}\", {s});')
            if status == 'success':
                sg.Popup('Your changes were applied successfully!', auto_close=True, auto_close_duration=2)
            if status == 'failure':
                sg.PopupError(f"I'm sorry there was a problem\n{msg}\nYour updates were not applied.")
        else:
            # Found something in the table and we're doing an update
            # print(f'Changing sec to {s} The theme going to be set to: ', t)
            dbs.update(f'''update settings set theme=\'{t}\', pwsec={s} where sid={sid[0]};''')
        dbs.close()
        set_theme(t)
    except Exception as e:
        sg.PopupError(f"!!!PROGRAM ERROR!!! settings.update_settings line 291\n"
                      f"I had a problem updating your settings...\n"
                      f"{e}")


def change_settings(t, s):
    '''
    Legacy function that has been re-written in update_settings() of the settings.py file. This function only exists
    until all calls made to it are switched over to calling update_settings().
    :param t: str: incoming theme name - requires program restart to take affect
    :param s: int: pwsec value which determines if we're using a password to open the database or not. if pwsec = 0 no
                    no password used. If s = 1 we're using a password at startup to open database.
    :return:
    '''
    update_settings(t, s)


def is_first_run() -> bool:
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


# ############################################################################################### #
# WHEN NECESSARY THESE ARE THE FUNCTIONS THAT RESTART THE PROGRAM                                 #
# ############################################################################################### #

def start(p: str):
    '''
    This function is never called from any other part of the program except from restart() below it. It has a singular
    purpose and that is to restart the program when necessary. Either from a call within the program or from the restart
    button on the main screen.
    :param p: str: parameter passed to this function from restart() and contains the filename of the binary form of the program.
    :return: returns subprocess.Popen system commands to restart the program passwed to it
    '''
    try:
        if detect_os() == "windows":
            return subprocess.Popen([os.getcwd() + '\\' + p], creationflags=subprocess.CREATE_NO_WINDOW)
        if detect_os() == "Linux":
            return subprocess.Popen([os.getcwd() + '/' + p])
    except Exception as e:
        sg.Popup(f"I was unable to start the program because: {e}")

def restart():      # I REALLY need to be able to tell if the program is running as binary or script
    if detect_os() == 'windows':
        if exists(os.path.join(os.getcwd(),'MJournal.exe')):
            p = 'MJournal.exe'
            start(p)
        else:
            # this bit is strictly for running in the IDE and won't work from the command line.
            command = 'main.py'
            return os.system(os.path.join(os.getcwd(), command))
    if detect_os() == 'Linux':
        if exists(os.path.join(os.getcwd(),'MJournal')):
            p = 'MJournal'
            start(p)
        else:
            # this bit is strictly for running in the IDE and won't work from the command line.
            command = 'main.py'
            #return os.system(os.path.join(os.getcwd(), command))
            return os.execl(sys.executable, sys.executable, *sys.argv)
