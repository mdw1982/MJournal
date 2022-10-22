#!/usr/bin/python3
import hashlib
import logging
from os.path import exists
from crontab import CronTab
import calendar
from pathlib import Path
import os
import io
import sqlite3
import subprocess
import time
import PySimpleGUI as sg
import SplashScreen
import dbsetup
from dbsetup import *
import sqlite3 as sl
import datetime as dt


######################################################################
# GLOBAL VARIABLES ###################################################

curr_theme = get_current_theme()
sg.theme(curr_theme[0])
platform = detect_os()
if platform == 'Linux':
    mascot = 'images/Penguin.png'
if platform == 'windows':
    mascot = 'images/Windiows_mascot.png'
version = '0.7.6.7'
mainWindowSize = (1000, 870)
searchWindowSize = (990, 630)
database = get_database()
tree_font = ('Trebuchet MS',10)
std_font = ('Trebuchet MS',11)
windowTitle = f"MJpournal -- {version} -- Connected to Database: {database}:: Current Theme: {curr_theme}"
icon_img = base64_image('images/MjournalIcon_36x36.png')
popup_location = (870,470)
#print = sg.Print


def convertMonthShortName(m):
    months = []
    for i in range(1, 13):
        months.append(calendar.month_abbr[i])
    return months[m - 1]


def readme_header():
    date = dt.datetime.now().strftime('%m/%d/%Y')
    header = f'''
    =====================================
    README	MJOURNAL PROGRAM - {date}
    =====================================
    AUTHOR: 
    Mark Weaver
    mdw1982@gmail.com
    
    LICENSE:
    GnuPL - for more information about copyright
    please view the licens file in the program
    directory or view it from the main program
    help menu.
    
    VERSION:	{version}'''
    return header


def convert_to_list(l):
    n = []
    for line in l:
        line = list(line)
        n.append(line)
    return n


def check_security():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select pwsec from settings;')
    val = [dict(row) for row in c.fetchall()]
    c.close()
    if val[0]['pwsec'] == 0:
        return False
    else:
        return True


'''
    changing the way new entries are made. Rather than opening up a brand new screen to take in the information
    we'll just take it from the main screen and gather the other data that was previously hidden on the new entry
    screen.
'''


def quick_entry(title, body, tags):
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME', 'VISIBLE']
    try:
        conn = sqlite3.connect(database)
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        check_title = c.execute(f"select title from entries where title=\"{title}\" and visible=1;").fetchall()
        print('title exists already', check_title)
        if title in check_title:
            sg.Popup('Title Exists', "It looks like you've attempted to use a title for an entry that already exists. "
                                     "Please create a new entry. Use File->New Entry")
        else:
            new_id = c.execute("select max(id) from entries;").fetchall()
            new_id = new_id[0]
            new_id += 1
            print(new_id)
            this_body = body.replace('\"', '&dbquo')
            this_body = body.replace('\'', '&sngquo')
            data = (new_id, title, int(dt.datetime.now().strftime('%m')), int(dt.datetime.now().strftime('%d')),
                    int(dt.datetime.now().strftime('%Y')), tags, this_body, str(dt.datetime.now().strftime('%H:%M')))
            sql = """insert into entries (id, title, month, day, year, tags, body, time) values(?,?,?,?,?,?,?,?);"""
            c.execute(sql, data)
            conn.commit()
            c.close()
    except Exception as e:
        detail = exc_info=True
        logging.error(f"RUNNING: module: main() - quick_entry unknown issue... {e}", exc_info=True)
        sg.Popup('ERROR', f"Error making quick_entry: {e} - {detail}")


def add_new_entry(dic):
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME', 'VISIBLE']
    conn = sqlite3.connect(database)
    c = conn.cursor()
    this_body = dic['B_ENTRY'].replace('\"', '&dbquo')
    this_body = this_body.replace('\'', '&sngquo')
    data = (dic['ID'], dic['TITLE'], dic['MONTH'], dic['DAY'], dic['YEAR'], dic['TAGS'], this_body, dic['TIME'])
    sql = """insert into entries (id, title, month, day, year, tags, body, time) values(?,?,?,?,?,?,?,?);"""
    c.execute(sql, data)
    conn.commit()
    c.close()


def show_body(id):
    conn = sqlite3.Connection(database)
    c = conn.cursor()
    c.execute(f'select body from entries where id={id}')
    b = c.fetchall()
    c.close()
    t = convert_to_list(b)
    text = t[0][0]
    return text


def get_title(id):
    conn = sqlite3.Connection(database)
    c = conn.cursor()
    c.execute(f'select title from entries where id={id}')
    b = c.fetchone()
    c.close()
    print(b)
    t = list(b)
    return t[0]


def load_tree_data():
    td = sg.TreeData()
    conn = sl.connect(database)
    c = conn.cursor()
    c.execute("select year from entries")
    a = c.fetchall()

    a = list(a)
    db_years = []
    for l in a:
        l = list(l)
        if l not in db_years:
            db_years.append(l)
        else:
            continue
    db_years = sorted(db_years, reverse=True)

    years = []
    for i in db_years:
        years.append(i[0])

    data = {}
    # ['id', 'title', 'month', 'day', 'year', 'time']
    for y in years:
        # print(y)
        c.execute(f"select id, title, month, day, time from entries where year = {y} and visible=1")
        r = c.fetchall()
        r = convert_to_list(list(sorted(r, reverse=True)))
        data[y] = r

    c.close()

    # print('First Stage', data)
    # treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
    # treedata.Insert("", '_B_', 'B', [])
    # treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
    # ['id', 'title', 'month', 'day', 'time']
    for k in data.keys():
        lm = ''
        # print(k)
        td.Insert("", '_A_', f'{k}', [], )
        for entry in data[k]:
            m = convertMonthShortName(entry[2])
            if lm == m:
                # print('\t\t', entry)
                td.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
            else:
                # print('\t', m)
                td.Insert("_A_", '_A1_', f'{m}', [])
                td.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
                # print('\t\t', entry)
            lm = m
    return td


def search_tree_data(ids,v):
    searchTree = sg.TreeData()
    conn = sl.connect(database)
    c = conn.cursor()
    for x in ids:
        a = c.execute(f"select year from entries where id={x};").fetchall()
        a = list(a)
        db_years = []
        for l in a:
            l = list(l)
            if l not in db_years:
                db_years.append(l)
            else:
                continue
        db_years = sorted(db_years, reverse=True)

        years = []
        for i in db_years:
            years.append(i[0])

        data = {}
        # ['id', 'title', 'month', 'day', 'year', 'time']
        for y in years:
            # print(y)
            c.execute(f"select id, title, month, day, time from entries where id={x} and year = {y} and visible={v};")
            r = c.fetchall()
            r = convert_to_list(list(sorted(r, reverse=True)))
            data[y] = r

        # ['id', 'title', 'month', 'day', 'time']
        for k in data.keys():
            lm = ''
            print(k)
            searchTree.Insert("", '_A_', f'{k}', [], )
            for entry in data[k]:
                m = convertMonthShortName(entry[2])
                if lm == m:
                    # print('\t\t', entry)
                    searchTree.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
                else:
                    # print('\t', m)
                    searchTree.Insert("_A_", '_A1_', f'{m}', [])
                    searchTree.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
                    # print('\t\t', entry)
                lm = m
    c.close()
    return searchTree


def getHiddenValues():
    # ['id', 'title', 'month', 'day', 'year', 'tags', 'body', 'time']
    conn = sqlite3.Connection(database)
    c = conn.cursor()
    c.execute('select max(id) from entries')
    id = convert_to_list(c.fetchall())
    c.close()
    today = dt.datetime.today()
    m = int(today.strftime('%m'))
    d = int(today.strftime('%d'))
    y = int(today.strftime('%Y'))
    t = today.strftime('%H:%M')
    dic = {
        'id': id[0][0] + 1,
        'month': m,
        'day': d,
        'year': y,
        'time': t
    }
    return dic


def convert_user_tuple(l):
    n = []
    for line in l:
        line = list(line)
        n.append(line)
    if n[0]:
        return n[0]
    else:
        return n


def convert_tuple(l):
    n = []
    for line in l:
        # line = list(line)
        n.append(line[0])
    return n


def new_user_window():
    def create_user_account(vals):
        # values coming in as dictionary
        user = vals['UserName']
        pw = vals['UserPass']
        salt = 'dfgasreawaf566'
        dbpass = pw + salt
        hashed = hashlib.md5(dbpass.encode())
        hashed_pass = hashed.hexdigest()

        # connect to db and check if user exists
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(f'select user, password from users where user=\"{user}\";')
        results = [dict(row) for row in c.fetchall()]
        res = {}
        if len(results) == 0:
            c.execute(f'insert into users (user, password) values(\"{user}\", \"{hashed_pass}\")')
            conn.commit()
            c.close()
            sg.Print('New User Created', f'A new user has been created for {user}')
        if len(results) > 0:
            res = results[0]
            if user == res['user']:
                sg.Popup('User Exists', f'Nothing to be done here...The user account for {user} already exists for this database.',
                         icon=icon_img, location=popup_location)
                result = sg.PopupYesNo('Change Password?', 'Would you like to change your current password?',
                              location=popup_location, icon=icon_img)
                if result == 'Yes':
                    change_user_password(pw)
                if result == 'No':
                    userwindow.close()
            #time.sleep(.5)
        # values coming out in dictionary: [{'user': 'mweaver', 'password': '98e04149be480bdd2d7fcc4666f82061'}]

    whoami = os.getlogin()

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input(whoami, size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    userwindow = sg.Window(f'User Information Input -- {windowTitle}', layout, icon=icon_img, location=(500, 210), resizable=True,
                           finalize=True)
    while True:
        event, values = userwindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event in ('UserInfoInput'):
             print(event,values)
            #change_user_password(values['UserPass'])
        if event == 'Ok' or event == 'UserInfoInput':
            # print(values)
            create_user_account(values)
            userwindow.close()

    userwindow.close()


def new_entry_window():
    f1title = [
        [sg.Input(size=(40, 1), key='TITLE')]
    ]

    f2body = [
        [sg.Multiline('', size=(100, 20), key='B_ENTRY', font='Sans 11', write_only=False)]
    ]
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME']
    hv = getHiddenValues()
    layout = [
        [sg.Frame('Entry Title', f1title)],
        [sg.Frame('New Entry', f2body)],
        [sg.Text('Tags: words separated by comas... no spaces')],
        [sg.Input('', key='TAGS')],
        [sg.Input(hv['id'], key='ID', visible=False)],
        [sg.Input(hv['month'], key='MONTH', visible=False)],
        [sg.Input(hv['day'], key='DAY', visible=False)],
        [sg.Input(hv['year'], key='YEAR', visible=False)],
        [sg.Input(hv['time'], key='TIME', visible=False)],
        [sg.Push(), sg.Button('Submit', key='SubmitNewEntry'), sg.Button('Cancel', key='Exit')]
    ]

    newindow = sg.Window(f'New M Journal Entry -- {windowTitle}', layout, modal=False,size=(650, 540), location=(500, 210),
                         resizable=True,
                         finalize=True)
    # newindow.bind('', '_TREE_', propagate=True)

    while True:
        event, values = newindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'SubmitNewEntry':
            print(values)
            add_new_entry(values)
            break
    newindow.close()
    common_progress_bar()


def show_about():
    msg = f"MJournal version: {version}\n" \
          f"Copyright 2022\n" \
          f"Release under the GbuPL"
    sg.Popup('About Mjournal', msg, location=(510, 220), icon=icon_img)


def show_readme():
    with open('README', 'r') as r:
        readme = r.read()
    content = f"{readme_header()}\n\n{readme}"
    frm_layout = [
        [sg.Multiline(content, font=("Sans Mono", 11), size=(100, 28), pad=(0, 0), do_not_clear=True)]
    ]
    layout = [
        [sg.Frame('README', frm_layout)],
        [sg.Push(), sg.Button('Close')]
    ]
    rmwindow = sg.Window(f'MJournal README -- {windowTitle}', layout, icon=icon_img, location=(500, 210),
                         resizable=False,
                         finalize=True)
    while True:
        event, values = rmwindow.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
    rmwindow.close()


def show_howto():
    # making special dispensation depending on what the platform running the program is
    # I reckon I'll have to do something similar all over the place where a local file is
    # being opend for reading/writing. I f'ing hate Windows!
    if detect_os() == 'Linux':
        howtofile = os.getcwd() + '/HOWTO'
    if detect_os() == 'windows':
        howtofile = os.getcwd() + "\\" + "HOWTO"

    with open(howtofile, 'r') as r:
        howto = r.read()
    content = f"{howto}"
    frm_layout = [
        [sg.Multiline(content, font=("Sans Mono", 11), size=(100, 28), pad=(0, 0), do_not_clear=True)]
    ]
    layout = [
        [sg.Frame('HOWTO', frm_layout)],
        [sg.Push(), sg.Button('Close')]
    ]
    hwindow = sg.Window(f'MJournal HOWTO -- {windowTitle}',layout, icon=icon_img, location=(500, 210),
                         resizable=False,
                         finalize=True)
    while True:
        event, values = hwindow.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
    hwindow.close()


def settings_window():
    ctheme = get_current_theme()

    layout = [
        [sg.Text('Program Theme'), sg.Push(),
         sg.Combo(get_them_list(), default_value=ctheme[0], size=(30, 1), key='_THEME_')],
        [sg.Text("Program Security On/Off (1/0)"), sg.Push(), sg.DropDown((1, 0), default_value=0, key='SEC')],
        [sg.HSeparator(pad=(3, 3))],
        [sg.Push(), sg.Button('OK', key='SubmitValues'), sg.Button('Cancel', key='quit')]
    ]

    settingswindow = sg.Window('Program Settings', layout, location=(600, 210), resizable=True, finalize=True)
    while True:
        event, values = settingswindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Ok' or event == 'SubmitValues':
            theme = values['_THEME_']
            secure = values['SEC']
            change_settings(theme, secure)
            break

    settingswindow.close()


def verify_userpass(vals):
    un = vals['UserName']
    pw = vals['CurrPass']
    # incoming value is a user's password. We're going to look it up
    # in the database and see if it matches with what's in there already.
    # we're doing this to verify that they've typed it in correctly while
    # attampting to change their current password.
    salt = 'dfgasreawaf566'
    dbpass = pw + salt
    hashed = hashlib.md5(dbpass.encode())
    hashed_pass = hashed.hexdigest()
    # connect to db and check if user exists
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f'select password from users where user=\"{un}\";')
    results = [dict(row) for row in c.fetchall()]
    c.close()
    if len(results) == 0:
        sg.PopupError('Information Error','Nothing was returned when I looked for your current password. Its '
                                          'most likely you haven not set one for this database. Please do that'
                                          'now.', icon=icon_img, location=popup_location)
        return False
    info = results[0]
    if hashed_pass == info['password']:
        return True
    if hashed_pass != info['password']:
        return False

def change_user_password(p=None):
    if p != None:
        defaultpw = p
    else:
        defaultpw = ''
    def update_user_pass(vals):
        # values coming in as dictionary
        # vals['UserName'], vals['UserPass']
        # 1. we're going to hash the password value
        user = vals['UserName']
        pw = vals['NewPass']
        salt = 'dfgasreawaf566'
        dbpass = pw + salt
        hashed = hashlib.md5(dbpass.encode())
        hashed_pass = hashed.hexdigest()
        # connect to db and check if user exists
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(f'update users set password=\"{pw}\" where user=\"{user}\";')
        conn.commit()
        c.close()

    def check_newpass_match(input):
        if input['NewPass'] == input['RetypePass']:
            return 'Match'
        if input['NewPass'] != input['RetypePass']:
            return 'NoMatch'


    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input(os.getlogin(), size=(30, 1), key='UserName')],
        [sg.Text('Current Password', size=(30, 1))],
        [sg.Input(defaultpw, size=(30, 1), password_char='x', key='CurrPass')],
        [sg.Text('New Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='NewPass')],
        [sg.Text('ReType Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='RetypePass')],
        [sg.Push(), sg.Button('OK', key='ChangePass'), sg.Button('Cancel', key='quit')]
    ]

    pwindow = sg.Window(f' User Information Input -- {windowTitle}', layout, icon=icon_img, location=(500, 210),
                        resizable=True,
                        finalize=True)
    while True:
        event, values = pwindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'ChangePass':
            if verify_userpass(values):
                result = check_newpass_match(values)
                if result == 'NoMatch':
                    sg.PopupError('Password Change Error', 'Values for your new password do not match, Please try again',
                                  icon=icon_img, location=popup_location)
                    pwindow['NewPass'].update('')
                    pwindow['RetypePass'].update('')
                    pwindow.close()                 # also have to check current password is correct.
                    pw = values['CurrPass']
                    change_user_password(pw)          # if the new passwords don't match need to go back to the window and try again.
                if result == "Match":
                    print(event,values)
                    update_user_pass(values)
                    pwindow.close()
                sg.Popup('SUCCESS! Password Change','Your password has successfully been change.\nPlease remember it or write it down '
                                                    'somewhere in a safe place. Forgotten passwords cannot be retrieved!', icon=icon_img, location=popup_location)
            else:
                print('Current Password validation failed. Closing Window...')
                sg.PopupError('Password Validation Error','I was unable to validate your current password.', icon=icon_img, location=popup_location)
            break

    pwindow.close()


def start_window():
    '''
    The start window only appears when user security is enabled. That security amounts to a username and hashed
    password that the user sets. when set, the user is promoted at program startup for their username and password.
    These values are stored in the table users.
    :return:
    '''
    def check_user_account(vals):
        # values coming in as dictionary
        # vals['UserName'], vals['UserPass']
        # 1. we're going to hash the password value
        user = vals['UserName']
        pw = vals['UserPass']
        salt = 'dfgasreawaf566'
        dbpass = pw + salt
        hashed = hashlib.md5(dbpass.encode())
        hashed_pass = hashed.hexdigest()
        # connect to db and check if user exists
        conn = sqlite3.connect(database)
        c = conn.cursor()
        userinfo = convert_user_tuple(c.execute(f'select user, password from users where user=\"{user}\";').fetchall())
        c.close()

        if user in userinfo:
            if userinfo[1] == hashed_pass:
                sg.Popup('Welcome Back!', "Credentials Accepted...", location=popup_location, icon=icon_img)
                swindow.close()
                main()
        else:
            sg.PopupError('Login Error', 'Either your username or password was incorrect.\n'
                                         'I cannot start the program at this time.', location=popup_location, icon=icon_img)
            exit()

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input('', size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    swindow = sg.Window(f' User Information Input -- {windowTitle}', layout, icon=icon_img, location=(500, 210), resizable=True,
                        finalize=True)
    while True:
        event, values = swindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Ok' or event == 'UserInfoInput':
            # print(values)
            check_user_account(values)
            swindow.close()

    swindow.close()


treedata = load_tree_data()


# theme_name_list = sg.theme_list()

def search_results(v,command):
    # 'STERMS': 'string', 'STARG': 'body', 'tags', 'title', 'all'
    terms = v['STERMS']
    targ = v['STARG']
    # print(terms,targ)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    if targ == 'all':
        res = convert_tuple(c.execute(f"select id from entries where "
                                      f"body like '%{terms}%'"
                                      f"or tags like '%{terms}%'"
                                      f"or title like '%{terms}%';").fetchall())
    else:
        res = convert_tuple(c.execute(f"select id from entries where {targ} like '%{terms}%';").fetchall())
    c.close()
    print(res)
    if not res:
        sg.Popup('Empty Results Set', 'There were no results returned from your search. Please try again with '
                                      'different search terms', location=popup_location, icon=icon_img)
    else:
        if command == 'search':
            result_tree = search_tree_data(res,1)
        if command == 'restore':
            result_tree = search_tree_data(res, 0)
        results_window(result_tree, command)


def get_hidden_entries(command):
    conn = sqlite3.Connection(database)
    c = conn.cursor()
    r = convert_tuple(c.execute(f"select id from entries where visible=0;").fetchall())
    c.close()
    print(r)
    if not r:
        sg.Popup('Empty Results Set', 'There were no results returned from your search. Please try again with '
                                      'different search terms', location=popup_location, icon=icon_img)
    else:
        result_tree = search_tree_data(r,0)
        results_window(result_tree, command)


def unhide_entry(i):
    try:
        conn = sqlite3.Connection(database)
        c = conn.cursor()
        c.execute(f"update entries set visible=1 where id={i};")
        conn.commit()
        c.close()
    except Exception as e:
        sg.PopupError('Unhide Entry Error', f"there was an error restoring a hidden entry: {e}", location=popup_location, icon=icon_img)



def results_window(rt, command):
    '''
    This function/window is a work in progress and will likely take a while to completely get
    sorted out. it's functional, however the tree menu does not display in the manner I was intending.
    The correct manner of display would be the way the tree menu displays journal entries. For whatever reason
    search results aren't being displayed that way even though I'm using most of the same code for the search result
    tree menu.
    :param rt:
    :param command:
    :return:
    '''
    def update_search_entry(id, title, body):
        '''
        This function allows the user to update entries returned from a search and displayed in the
        search results window.
        :param id:
        :param title:
        :param body:
        :return:
        '''
        try:
            # filtering entry body for double quptes. sqlite doesn't like them... this program because
            # of sqlite has really been giving me the business with quote characters.
            #b = body
            body = body.replace('\"', '&dbqup')
            body = body.replace('\'', '&sngquo')
            print('this is whats coming to get updated:::: ',id, title, body)
            conn = sqlite3.connect(database)
            c = conn.cursor()
            sql = f"""update entries set title=\"{title}\", body=\"{body}\" where id={id};"""
            c.execute(sql)
            conn.commit()
            c.close()
        except Exception as e:
            sg.PopupError('Error Updating Entry', f'I have found an error for the update of the entry record: {id}. '
                                                  f'the error was: {e}', location=popup_location, icon=icon_img)
        finally:
            sg.Popup('Update Processed', "I've successfully processed your update request.", location=popup_location, icon=icon_img)

    curr_theme = get_current_theme()
    sg.theme(curr_theme[0])
    dbchoosea_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value=database, size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    colac = [
        [sg.Tree(rt, ['', ], font=('Sans Mono', 9), key='_TREE_', enable_events=True, col0_width=38,
                 show_expanded=True, num_rows=34)]
    ]
    colbc = [
        [sg.Input('', key='E_TITLE', size=(40, 1), font=std_font)],
        [sg.Multiline('', font=("Sans Mono", 11), size=(90, 28), pad=(0, 0), key='VIEW')]
    ]
    if command == 'search':
        func_frameac = [
            [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False),
             sg.Button("Reload Tree", key='refresh', visible=False),
             sg.Button('Update Entry', key='UpdateEntry', visible=True),
             sg.Button('New Entry', key='NewEntry', visible=False),
             sg.Button('Load', key='LoadEntry', visible=False), sg.Button('Exit', key='quit')]
        ]
    if command == 'restore':
        func_frameac = [
            [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False),
             sg.Button("Reload Tree", key='refresh', visible=False),
             sg.Button('Restore Entry', key='RestoreEntry', visible=True),
             sg.Button('New Entry', key='NewEntry', visible=False),
             sg.Button('Load', key='LoadEntry', visible=False), sg.Button('Exit', key='quit')]
        ]
    searcha_framec = [
        [sg.Push(), sg.Text('Search Entrys: Body or Tags'), sg.Input('', size=(40, 1), key='STERMS'),
         sg.DropDown(('body', 'tags'), default_value='body', key='STARG'), sg.Button('GO', key='SEARCH'), sg.Push()]
    ]
    if command == 'search':
        menua_defc = [
            ['&File', ['&New Entry', '&Exit']],
            ['&Edit', ['&Utilities',['Insert Date/Time']],],
            ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
            ['&Help', ['&ReadMe', '&About']]
        ]
    if command == 'restore':
        menua_defc = [
            ['&File', ['&New Entry', '&Restore Entry(unhide)', '&Exit']],
            ['&Edit', ['&Utilities',['Insert Date/Time']],],
            ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
            ['&Help', ['&ReadMe', '&About']]
        ]
    refresh_layoutc = [
        [sg.Menu(menua_defc, tearoff=False, key='-MENU_BAR-')],
        [sg.Column(colac, vertical_alignment='top'), sg.Column(colbc, vertical_alignment='top')],
        [sg.Push(), sg.Frame('Functions', func_frameac)],
        [sg.Frame('Search Entries', searcha_framec, visible=False)],
        [sg.Frame('Switch Database', dbchoosea_layout, visible=False)]
    ]
    window = sg.Window(windowTitle, refresh_layoutc, size=searchWindowSize, icon=icon_img,location=(500, 210), resizable=True,
                       finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")
    while True:
        event, values = window.read()
        if event == 'quit' or event == sg.WIN_CLOSED:
            break
        if event == 'Insert Date/Time':
            date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
            text = window['VIEW']
            text.update(text.get()+ '\n\n'+date_time)
        if ' SelectTreeItem' in event:
            if values['_TREE_'][0] == '_A1_' or values['_TREE_'][0] == '_A_':
                continue
            print(values['_TREE_'][0])
            title = get_title(values['_TREE_'][0])
            body = show_body(values['_TREE_'][0])
            body = body.replace('&sngquo', '\'')
            body = body.replace('&hellip;', '... ')
            body = body.replace('&dbqup', '\"')
            window['E_TITLE'].update(title)
            window['VIEW'].update(body)
        if event == 'RestoreEntry':
            unhide_entry(values['_TREE_'][0])
            window['_TREE_'].update(rt)
            sg.Popup('Restore Successful', f"I was able to successfully restore your hidden entry with the "
                                           f"entry id of {values['_TREE_'][0]}. You will see the restored entry in the tree menu of "
                                           f"the main screen as soon as you click 'OK'", location=popup_location, icon=icon_img)
            break
        if event == 'UpdateEntry':
            u_title = values['E_TITLE']
            u_body = values['VIEW']
            update_search_entry(values['_TREE_'][0], u_title, u_body)
            break
    window.close()


def database_maintenance():
    '''
    this function is specifically for creating manual backups of the database chosen from the
    screen. I wanted to provide a method so the user was able to make backups of their database(s).
    Other personal journal programs i've seen don't offer this which I found odd. At least programs
    that Utilize a database for entries.
    :return:
    '''
    def make_backup(path,db):
        import io
        date = f"{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}"
        print(f"date value: {date}")
        db = db.replace('\n', '')
        filename = f"{path}/{db}_{date}.sql"
        print(f"file name: {filename}")
        conn = sqlite3.connect(db)
        # Open() function
        with io.open(filename, 'w') as p:
            # iterdump() function
            for line in conn.iterdump():
                print('%s\n' % line)
                p.write('%s\n' % line)
        conn.close()
        print(f"Saving {filename} to {path}/{filename}")

    '''
    It's ugly but useful. Just needed to load a list of lists to return values back to the dropdown
    lists that populate the dropdowns to build the crontab entry.
    :return:
    '''
    def load_cron_lists():
        master = []
        mins = []
        for i in range(0, 60):
            mins.append(i)
        master.append(mins)
        hrs = []
        for i in range(0, 24):
            hrs.append(i)
        master.append(hrs)
        mdays = []
        for i in range(1, 32):
            mdays.append(i)
        master.append(mdays)
        mons = []
        for i in range(1, 13):
            mons.append(i)
        master.append(mons)
        wdays = []
        for i in range(0, 7):
            wdays.append(i)
        master.append(wdays)
        return master

    def load_user_crontab():
        user = subprocess.getoutput('whoami')
        cron = CronTab(user=True)
        clist = []
        for job in cron:
            print(job)
            clist.append(job)
        return clist

    def process_cronvals(dic):
        '''
        source of information for CronTab module
        https://pypi.org/project/python-crontab/
        :param dic:
        :return:
        '''
        here = os.getcwd()
        home = Path.home()
        user = os.getlogin()
        location = os.path.expanduser('~') + '/bin'
        startupFile = location + '/startbu.sh'
        if not exists(location):
            os.mkdir(location)
            sshContent = f'''#!/bin/sh\n\ncd {here}\npython3 dbbackup.py\nexit'''
            with open(startupFile, 'w') as s:
                s.write(sshContent)
            os.chmod(startupFile, 0o755)
        if exists(location):
            sshContent = f'''#!/bin/sh\n\ncd {here}\npython3 dbbackup.py\nexit'''

            with open(startupFile, 'w') as s:
                s.write(sshContent)
            os.chmod(startupFile, 0o755)
        if exists(startupFile):
            print("SUCCESS! we made a file")
            print(startupFile)
        if not exists(startupFile):
            print('FAILED! WTF')
        #--------- end making startbu.sh ----------#
        print("entering process cronvals")
        d = {}
        for k, v in dic.items():
            if k in ['min','hrs','mday','mon','wday']:
                d[k] = v
            else:
                continue

        cron = CronTab(user=user)
        # fixed issue with cron driven db backups. typp in the file name being called.
        job = cron.new(command=f'{location}/startbu.sh')
        job.setall(f"{d['min']} {d['hrs']} {d['mday']} {d['mon']} {d['wday']}")
        return d,job

    '''
    the remove_db function actually doesn't delete or remove the database but removes the database name
    from the dblist file that the program reads from to list the available database for the program.
    :return:
    '''

    def edit_dlist(name, c):
        print(name)
        if '.db' not in name:
            dbname = f"{name}.db"
        else:
            dbname = name
        nlist = []
        if detect_os() == 'Linux':
            dblistfile = os.getcwd() + '/dblist'
        if detect_os() == 'windows':
            dblistfile = os.getcwd() + "\\" + 'dblist'
        with open(dblistfile, 'r') as f:
            nlist = list(f.read().split(','))
        # checking to see if dbname already exists in dblist (nlist)
        if dbname in nlist and c == 'add':
            sg.PopupError('DB Add Error',f"The database {dbname} already present in dblist", location=popup_location, icon=icon_img)
            c = 'err'
            window['ATTDB'].update('')
        if c == 'add':
            nlist.append(dbname)
        if c == 'del':
            for l in nlist:
                if l == dbname:
                    print(f"found a match! {l}")
                    nlist.remove(l)
        slist = ''
        for i in nlist:
            if i == '':
                continue
            slist += f'{i},'
        slist.rstrip(",")
        with open(dblistfile, 'w') as file:
            file.write(slist)
        if c == 'add':
            sg.Popup(f"I've finished attaching {name} to the dblist", location=popup_location, icon=icon_img)
        if c == 'del':
            sg.Popup(f"I've finished removing {name} from the dblist", location=popup_location, icon=icon_img)
        if c == 'err':
            sg.Popup(f"{name} couldn't be added to the dblist file because it's present in the file. "
                     f"please choose a different file or quit.", location=popup_location, icon=icon_img)

    def attachDB(db):
        '''
        1.  incoming path with db file to attache: /home/user/PycharmProjects/Mjournal/craters.db
            split path strink on '/' into a list and take the last element which will be the db
        2.  send dbname to edit_dlist(name,command) i.e. name,add
        :return:
        '''
        pathlist = list(db.split('/'))
        dbname = pathlist[-1]
        print('Sending database name to edit_dlist: ',dbname)
        edit_dlist(dbname,'add')
        pass


    col1 = [
        [sg.Input('', size=(50,1), key='BUPATH')],
        [sg.FolderBrowse('Browse', target='BUPATH')],
        [sg.Push(), sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME')],
        [sg.Button('Create Backup', key='PerformBackup')],
        [sg.HSeparator()],
        [sg.Text('Remove Database'),
         sg.DropDown(read_dblist(),default_value=None, key='dbname_remove'),
         sg.Button('Remove Database', key='RemoveDB',tooltip='Simply removes database from dblist file and does not delete the database')],
        [sg.HSeparator()],
        [sg.T('Attach Database')],
        [sg.I('', size=(30,1), key='ATTDB'),
         sg.FileBrowse('Browse', target='ATTDB',file_types=(("DB Files", "*.db"),))],
        [sg.Push(), sg.Button('Attach Datanase', key='-ATTACHDB-')]
    ]

    mlist = load_cron_lists()
    cl = load_user_crontab()

    #load_user_crontab()
    if len(cl) == 0:
        # build an entry
        pass
    else:
        pass
    col2 = [
        [sg.T('Min...'),sg.T('Hrs...'),sg.T('Day\nMon...'),sg.T('Mon...'),sg.T('Day\nWk...')],
        [sg.DropDown(mlist[0], size=(3,1),default_value='*', key='min'),
         sg.DropDown(mlist[1], size=(3,1),default_value='*',key='hrs'),
         sg.DropDown(mlist[2],size=(3,1),default_value='*',key='mday'),
         sg.DropDown(mlist[3],size=(3,1),default_value='*',key='mon'),
         sg.DropDown(mlist[4], size=(3,1), default_value='*',key='wday')],
        [sg.Multiline(load_user_crontab(), key='CRONSTMNT',size=(50,5))],
        [sg.Push(),sg.Button('Create Cron Job', key='build'),sg.Button('Submit Job', key='bless') ]
    ]
    main_layout = [
        [sg.Frame('Database Backup', col1, vertical_alignment='top'), sg.Frame('Linux Only - Scheduled Backup', col2, vertical_alignment='top')],
        [sg.Push(), sg.Button('Quit', key='quit')]
    ]
    window = sg.Window('Database Maintenance', main_layout, icon=icon_img, resizable=True, location=window_location, finalize=True)
    window['dbname_remove'].bind("<Return>", '_Enter')

    while True:
        event, values = window.read()
        if event == 'quit' or sg.WIN_CLOSED:
            break
        if event == '-ATTACHDB-':
            attachDB(values['ATTDB'])
        if event == 'RemoveDB':
            edit_dlist(values['dbname_remove'],'del')
            #print(msg)
            window.refresh()
        if event == 'PerformBackup':
            print(event,values)
            make_backup(values['BUPATH'], values['DBNAME'])
            break
        if event == 'build':
            #print(event, values)
            window['CRONSTMNT'].update('')
            d,vd = process_cronvals(values)
            window['CRONSTMNT'].update(vd)
        if event == 'bless':
            d, vd = process_cronvals(values)
            user = os.getlogin()
            location = os.path.expanduser('~') + '/bin'
            cron = CronTab(user=user)
            job = cron.new(command=f'{location}/startbu.sh')
            job.setall(f"{d['min']} {d['hrs']} {d['mday']} {d['mon']} {d['wday']}")
            cron.write()
            sg.Popup('Cron Job Written',f"I was able to successfully write to your crontab the following information\n"
                                        f"{job}\n"
                                        f"Your Databases will now be automatically backed up according to the settings "
                                        f"in your crontab.", location=popup_location, icon=icon_img)
            break

    window.close()


# print(theme_name_list)
def main():
    def update_entry(id, title, body):
        if not id:
            print("the value sent for ID was empty... I cannot update the entry")
        if id:
            #try:
            # filtering entry body for double quptes. sqlite doesn't like them... this program because
            # of sqlite has really been giving me the business with quote characters.
            #b = body
            body = body.replace('\"', '&dbqup')
            body = body.replace('\'', '&sngquo')
            #print('this is whats coming to get updated:::: ',id, title, body)
            conn = sqlite3.connect(database)
            c = conn.cursor()
            sql = f"""update entries set title=\"{title}\", body=\"{body}\" where id={id};"""
            c.execute(sql)
            conn.commit()
            c.close()
            # except Exception as e:
            #     sg.PopupError('Error Updating Entry', f'I have found an error for the update of the entry record: {id}. '
            #                                           f'the error was: {e}')
            # finally:
            sg.Popup('Update Processed', "I've successfully processed your update request.", location=popup_location, icon=icon_img)
            return id


    def delete_entry(id):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = f"""update entries set visible=0 where id={id};"""
        c.execute(sql)
        conn.commit()
        c.close()
        window['_TREE_'].update(load_tree_data())

    col1 = [  # from Trr
        [sg.Tree(treedata, ['', ], font=tree_font, col0_width=42, key='_TREE_', enable_events=True,
                 show_expanded=True, num_rows=32, pad=(10,10), expand_x=True, tooltip='click a record node to new the entry')]

    ]
    col2 = [
        [sg.Input('', focus=True, tooltip='Click the Clear Screen button to clear Title and Entry fields', key='E_TITLE', size=(40, 1), font=std_font, enable_events=True, pad=(5,5))],
        [sg.Multiline('Click Tree menu node to View', font=std_font, size=(90, 28), pad=(5,5),key='VIEW')],
    ]

    menu_def = [
        ['&File', ['&New Entry Window', '&Remove Entry(hide)','&Restore Entry(unhide)', '&Exit']],
        ['&Edit', ['&Utilities',['Insert Date/Time']],],
        ['&Settings', ['&User Settings',['&Set User Password', '&Change User Password'], '&Program Settings', '&Make New Database', '&Database Maintenance']],
        ['&Help', ['&ReadMe', '&HowTo','&About']]
    ]
    dbchoose_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    func_frame = [
        [sg.Push(), sg.Button('Reload Program', key='Reload', tooltip=tp_reload(), visible=True), sg.Button("Clear Screen", key='clear', visible=False),
         sg.Button('Update Entry', key='UpdateEntry'), sg.Button('New Entry', key='New Entry Window'),
         sg.Button('Load', key='LoadEntry', visible=False), sg.Button('Exit', key='quit')]
    ]

    tag_frame = [
        [sg.Input('', size=(40, 1), key='_TAGS_')]
    ]

    search_frame = [
        [sg.Push(), sg.Text('Search Entrys: Body or Tags', visible=False),
         sg.Input('', size=(40, 1), key='STERMS', enable_events=True),
         sg.DropDown(('body', 'tags', 'title', 'all'), default_value='body', key='STARG'), sg.Button('GO', key='SEARCH'), sg.Push()]
    ]
    frame_col1 = [
        [sg.Frame('Tree menu', col1, pad=(5, 5))],
        [sg.Image(filename=mascot, pad=(5, 5)), sg.Push()]
    ]
    frame_col2 = [
        [sg.Frame('Entries Input and View', col2, pad=(5, 5))],
        [sg.Push(), sg.Frame('Tags', tag_frame, vertical_alignment='top'),sg.Push()],
        [sg.Push(), sg.Frame('Functions', func_frame),sg.Push()],
        [sg.Push(), sg.Frame('Search Entries', search_frame, element_justification='center'),sg.Push()],
        [sg.Push(), sg.Frame('Switch Database', dbchoose_layout),sg.Push()]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU_BAR-')],
        [sg.Column(frame_col1, vertical_alignment='top', expand_x=True, expand_y=True),
         sg.Column(frame_col2, vertical_alignment='top', expand_x=True, expand_y=True)]
    ]

    window = sg.Window(windowTitle, layout, icon=icon_img, size=mainWindowSize, modal=False, location=(460, 160), resizable=True, finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        print(event, values, flush=True)
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'Change User Password':
            change_user_password()
            window.refresh()
        if event == 'HowTo':
            show_howto()
            window.refresh()
        if event == 'Reload':
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'Insert Date/Time':
            date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
            text = window['VIEW']
            text.update(text.get()+ '\n\n'+date_time)
        if event == 'Database Maintenance':
            database_maintenance()
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'Restore Entry(unhide)':
            get_hidden_entries('restore')
            window['_TREE_'].update(load_tree_data())
        if event == 'SEARCH':
            # print(event,values)
            search_results(values,'search')
            window['_TREE_'].update(load_tree_data())
        if event == 'STERMS' + '_Enter':
            search_results(values,'search')
            window['_TREE_'].update(load_tree_data())
        if event == 'Make New Database':
            dbsetup.new_db_window()
            # window['DBNAME'].update(read_dblist())
            # window['DBNAME'].update('choose')
            #window.refresh()
            window.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'Set User Password':
            new_user_window()
        if event == 'Program Settings':
            settings_window()
            window.close()
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'ReadMe':
            show_readme()
        if event == 'New Entry Window':
            new_entry_window()
            window['_TREE_'].update(load_tree_data())
        if ' SelectTreeItem' in event:
            print(f"Stepped Inside SelectTreeItem (IF) event: {event} values: {values}")
            try:
                print(values['_TREE_'][0], flush=True)
                if values['_TREE_'][0] == '_A1_' or values['_TREE_'][0] == '_A_':
                    continue
                print(values['_TREE_'][0])
                title = get_title(values['_TREE_'][0])
                body = show_body(values['_TREE_'][0])
                body = body.replace('&rsquo;', '\'')
                body = body.replace('&hellip;', '... ')
                body = body.replace('&dbqup', '\"')
                body = body.replace('&sngquo', '\'')
                window['E_TITLE'].update(title)
                window['VIEW'].update(body)
            except Exception as e:      # hiding the error from the user and moving on
                print(f"RUNNING: module: {__name__} - {event}: probably clicked an empty portion of tree menu: {e}", flush=True)
            # finally:
            #     print(f"RUNNING: module: {__name__} - {event} - probably clicked an empty portion of tree menu...moving on...\n---\n", flush=True)
        if event == 'NewEntry' or event == 'New Entry':
            quick_entry(values['E_TITLE'], values['VIEW'], values['_TAGS_'])
            window['_TREE_'].update(load_tree_data())
        if event == 'clear':
            window['E_TITLE'].update('')
            window['VIEW'].update('')
        if event == 'DBCHANGE' or event == 'Change Database':
            # print(values['DBNAME'])
            change_database(values['DBNAME'])
            window.close()
            # completely restarting the program to be able to use the chosen database
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'UpdateEntry':
            print("just entered the if event statement for the update_entry()")
            print(f"Stepped Inside UpdateEntry (IF) event: {event} values: {values}")
            selected = values['_TREE_']
            if not selected:
                print(f"there was no usable value sent back from the tree node: {selected}")
                continue
            u_id = selected[0]
            print(f"value coming from the tree for the update: {selected} is the ID for the entry")
            u_title = values['E_TITLE']
            u_body = values['VIEW']
            print(f"sending values to update_entry u_title:u_body\n", flush=True)
            returned = update_entry(u_id, u_title, u_body)  # sending ID, TITLE and BODY to update_entry()
                                                            # from time to time this action results in a crash or program exit.
                                                            #------------------------------------------------------------------
            #window['_TREE_'].update(load_tree_data())       # sending reload tree data in case title changed. this will update
                                                            # tried using the tree reload before assigning and doesn't work
                                                            #------------------------------------------------------------------
            values['_TREE_'] = returned                     # returning ID value from update_entry() and re-assigning it to values['_TREE_']
                                                            # where it came from originally
            print("back from the update_entry() function...", flush=True)
            print("received ID value returned from update_entry ",values['_TREE_'], flush=True)
            print('---------------------------------------------------', flush=True)
            window.refresh()
        if event == 'DelEntry' or event == 'Remove Entry(hide)':
            try:
                delete_entry(values['_TREE_'][0])
            except Exception as e:
                sg.PopupError('REMOVE ENTRY ERROR!',
                              f"It appears that you didn't select an entry to be removed first "
                              f"before sending your request to me. Please try again and this time "
                              f"select and load an entry to be removed\n{e}.", location=popup_location, icon=icon_img)
        if event == 'About':
            show_about()
        # print(event,values)
    window.close()
    logging.info("PROGRAM Stop: program is closing... exit code 0")


if __name__ == '__main__':
    #SplashScreen.main()
    init_logs()
    if is_first_run():
        init_setup()
        os.execl(sys.executable, sys.executable, *sys.argv)
    # if not is_first_run():
    #     # we need to check for the presence of the setup.py file. after initial setup
    #     # it should have been moved to the src directory
    #     if exists('./setup.py'):
    #         os.system('mv ./setup.py ./src')
    # check sec file to see if we're using credentials to start program
    if check_security():
        start_window()
    else:
        main()