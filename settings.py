import base64
import sys
import time
import PySimpleGUI as sg
import sqlite3
from src.dblib import *
from src import logcheck


window_location = (500, 210)
std_font = ('Sans Mono', 11)
logpath = f'{whereami}/logs/'
lfn = logpath + 'mjournal' + log_name_date() + '.log'
logging.basicConfig(filename=lfn, filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)

try:
    with open('cdb', 'r') as d:
        logging.info(f"STARTUP: Reading file for active database: {d}")
        database = d.read().replace('\n', '')
    print(database)
except Exception as e:
    logging.error(f"RUNNING: problem opening active database: {database} ", exc_info=True)
    sg.PopupError("!!!ERROR!!!", f"Error Opening file cdb to read the current active database file: {e}")


def base64_image(img_path):
    with open(img_path, 'rb') as i:
        imgstr =  base64.b64encode(i.read())
    return imgstr


def get_database():
    with open('cdb', 'r') as d:
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
    with open('cdb', 'r') as d:
        db = d.read().replace('\n', '')
    print(db)
    database = db


def change_database(dname):
    with open('cdb', 'w') as f:
        f.writelines(dname)
    set_database()


def read_dblist():
    dl = []
    with open('dblist', 'r') as d:
        for l in d.readlines():
            dl.append(l)
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
        logging.info(f"RUNNING: module: Settings - entered change_settings()")
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
        logging.error(f"RUNNING: module: change_settings() but ran into a problem: {e}")
        sg.PopupError("!!!ERROR!!!", f"Running in change_settings() but ran into a problem\n{e}")


def is_first_run():
    with open('firstrun', 'r') as f:
        val = f.read()
    print(val)
    if val == 'True':
        with open('firstrun', 'w') as f:
            f.writelines('False')
        return True
    else:
        return False


# def main():
#     ctheme = get_current_theme()
#     layout = [
#         [sg.Text('Program Theme'), sg.Push(), sg.Combo(get_them_list(), default_value=ctheme[0], size=(30,1), key='_THEME_')],
#         [sg.Text("Program Security On/Off (1/0)"), sg.Push(), sg.DropDown((1, 0), default_value=0, key='SEC')],
#         [sg.HSeparator(pad=(3,3))],
#         [sg.Text('Choose Different Database to Use', font=std_font)],
#         [sg.DropDown(read_dblist(), default_value=database, size=(30,1), key='DBNAME'), sg.Button('Change Database', key='DBCHANGE')],
#         [sg.Push(), sg.Button('OK', key='SubmitValues'), sg.Button('Cancel', key='quit')]
#     ]
#
#     settingswindow = sg.Window('Program Settings', layout, location=(500, 210), resizable=True, finalize=True)
#     while True:
#         event, values = settingswindow.read()
#         if event == sg.WIN_CLOSED or event == 'quit':
#             break
#         if event == 'Ok' or event == 'SubmitValues':
#             theme = values['_THEME_']
#             secure = values['SEC']
#             change_settings(theme, secure)
#             break
#         if event == 'DBCHANGE':
#             dbname = values['DBNAME']
#             change_database(dbname)
#             set_database()
#             break
#
#     settingswindow.close()



# if __name__ == '__main__':
#     main()