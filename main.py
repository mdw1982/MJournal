#!/usr/bin/python3
import hashlib
from crontab import CronTab
import calendar
import os
import io
import sqlite3
import subprocess
import time
import PySimpleGUI
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
version = '0.7.5.9'
mainWindowSize = (990, 850)
searchWindowSize = (990, 630)
database = get_database()
windowTitle = f"MJpournal -- {version} -- Connected to Database: {database}"
icon_img = base64_image('images/MjournalIcon_36x36.png')
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

        if user in userinfo:
            sg.Popup('User Exists', f'The user account for {user} already exists for this program.')
        else:
            c.execute(f'insert into users (user, password) values(\"{user}\", \"{hashed_pass}\")')
            conn.commit()
            sg.Popup('New User Created', f'A new user has been created for {user}')
        c.close()

    whoami = subprocess.getoutput('whoami')

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input(whoami, size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    userwindow = sg.Window(f'User Information Input -- {windowTitle}', layout, location=(500, 210), resizable=True,
                           finalize=True)
    while True:
        event, values = userwindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
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

    newindow = sg.Window(f'New M Journal Entry -- {windowTitle}', layout, size=(650, 540), location=(500, 210),
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
    sg.Popup('About Mjournal', msg, location=(510, 220))


def show_readme():
    with open('README', 'r') as r:
        readme = r.read()
    content = f"{readme_header()}\n\n{readme}"
    frm_layout = [
        [sg.Multiline(content, font=("Sans Mono", 11), size=(90, 28), pad=(0, 0), )]
    ]
    layout = [
        [sg.Frame('README', frm_layout)],
        [sg.Push(), sg.Button('Close')]
    ]
    rmwindow = sg.Window(f'MJournal README -- {windowTitle}', layout, size=(680, 580), location=(500, 210),
                         resizable=False,
                         finalize=True)
    while True:
        event, values = rmwindow.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
    rmwindow.close()


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
        # if event == 'DBCHANGE':
        #     dbname = values['DBNAME']
        #     change_database(dbname)
        #     break
    settingswindow.close()


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
                sg.Popup('Welcome Back!', "Credentials Accepted...")
                swindow.close()
                main()
        else:
            sg.PopupError('Login Error', 'Either your username or password was incorrect.\n'
                                         'I cannot start the program at this time.')
            exit()

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input('', size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    swindow = sg.Window(f' User Information Input -- {windowTitle}', layout, location=(500, 210), resizable=True,
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
                                      'different search terms')
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
                                      'different search terms')
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
        sg.PopupError('Unhide Entry Error', f"there was an error restoring a hidden entry: {e}")



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
                                                  f'the error was: {e}')
        finally:
            sg.Popup('Update Processed', "I've successfully processed your update request.")

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
            ['&Edit', ['&Search']],
            ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
            ['&Help', ['&ReadMe', '&About']]
        ]
    if command == 'restore':
        menua_defc = [
            ['&File', ['&New Entry', '&Restore Entry(unhide)', '&Exit']],
            ['&Edit', ['&Search']],
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
    window = sg.Window(windowTitle, refresh_layoutc, size=searchWindowSize, location=(500, 210), resizable=True,
                       finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")
    while True:
        event, values = window.read()
        if event == 'quit' or event == sg.WIN_CLOSED:
            break
        if ' SelectTreeItem' in event:
            if values['_TREE_'][0] == '_A1_' or values['_TREE_'][0] == '_A_':
                continue
            print(values['_TREE_'][0])
            title = get_title(values['_TREE_'][0])
            body = show_body(values['_TREE_'][0])
            body = body.replace('&rsquo;', '\'')
            body = body.replace('&hellip;', '... ')
            body = body.replace('&dbqup', '\"')
            window['E_TITLE'].update(title)
            window['VIEW'].update(body)
        if event == 'RestoreEntry':
            unhide_entry(values['_TREE_'][0])
            window['_TREE_'].update(rt)
            sg.Popup('Restore Successful', f"I was able to successfully restore your hidden entry with the "
                                           f"entry id of {values['_TREE_'][0]}. You will see the restored entry in the tree menu of "
                                           f"the main screen as soon as you click 'OK'")
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
        for i in range(1, 60):
            mins.append(i)
        master.append(mins)
        hrs = []
        for i in range(1, 24):
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
        for i in range(1, 8):
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
        user = subprocess.getoutput('whoami')
        location = subprocess.getoutput('pwd')
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
    def remove_db(dbname):
        g = []
        with open('dblist', 'r') as d:
            dlist = d.readlines()
        with open('dblist', 'w') as f:
            for e in dlist:
                e.replace("\n",'')
                if e == dbname:
                    continue
                else:
                    e.replace('\n','')
                    g.append(e)
            for line in g:
                f.write(line)
        return f"I've finished and have removed {dbname} from the dblist file"


    col1 = [
        [sg.Input('', size=(50,1), key='BUPATH')],
        [sg.FolderBrowse('Browse', target='BUPATH')],
        [sg.Push(), sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME')],
        [sg.Button('Create Backup', key='PerformBackup')],
        [sg.HSeparator()],
        [sg.Text('Remove Database'),
         sg.DropDown(read_dblist(),default_value=None, key='dbname_remove',tooltip='Simply removes database from dblist file and does not delete the database'),
         sg.Button('Remove Database', key='RemoveDB')]
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

    while True:
        event, values = window.read()
        if event == 'quit' or sg.WIN_CLOSED:
            break
        if event == 'RemoveDB':
            msg = remove_db(values['dbname_remove'])
            print(msg)
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
            location = subprocess.getoutput('pwd')
            user = subprocess.getoutput('whoami')
            cron = CronTab(user=user)
            job = cron.new(command=f'python3 {location}/dbbackups.py')
            job.setall(f"{d['min']} {d['hrs']} {d['mday']} {d['mon']} {d['wday']}")
            cron.write()
            sg.Popup('Cron Job Written',f"I was able to successfully write to your crontab the following information\n"
                                        f"{job}\n"
                                        f"Your Databases will now be automatically backed up according to the settings "
                                        f"in your crontab.")
            break

    window.close()


# print(theme_name_list)
def main():
    def update_entry(id, title, body):
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
                                                  f'the error was: {e}')
        finally:
            sg.Popup('Update Processed', "I've successfully processed your update request.")


    def delete_entry(id):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = f"""update entries set visible=0 where id={id};"""
        c.execute(sql)
        conn.commit()
        c.close()
        window['_TREE_'].update(load_tree_data())

    col1 = [  # from Trr
        [sg.Tree(treedata, ['', ], font=('Sans Mono', 9), col0_width=38, key='_TREE_', enable_events=True,
                 show_expanded=True, num_rows=34, pad=(10,10), expand_x=True, tooltip='click a record node to new the entry')]

    ]
    col2 = [
        [sg.Input('Quick Entry Title', focus=True, tooltip='Click the Clear Screen button to clear Title and Entry fields', key='E_TITLE', size=(40, 1), font=std_font, enable_events=True, pad=(5,5))],
        [sg.Multiline('Quick Entry Body', font=("Sans Mono", 11), size=(90, 28), pad=(5,5),key='VIEW')],
    ]

    menu_def = [
        ['&File', ['&New Entry Window', '&Remove Entry(hide)','&Restore Entry(unhide)', '&Exit']],
        ['&Edit', ['&Utilities',['Insert Date/Time']],],
        ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database', '&Database Maintenance']],
        ['&Help', ['&ReadMe', '&About']]
    ]
    dbchoose_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    func_frame = [
        [sg.Push(), sg.Button('Reload Program', key='Reload', tooltip=tp_reload(), visible=True), sg.Button("Clear Screen", key='clear'),
         sg.Button('Update Entry', key='UpdateEntry'), sg.Button('Save Quick Entry', key='NewEntry'),
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

    window = sg.Window(windowTitle, layout, icon=icon_img, size=mainWindowSize, location=(460, 160), resizable=True, finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        print(event)
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'Reload':
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'Insert Date/Time':
            date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
            text = window['VIEW']
            text.update(text.get()+ '\n\n'+date_time)
        if event == 'Database Maintenance':
            database_maintenance()
            window.refresh()
        if event == 'Restore Entry(unhide)':
            get_hidden_entries('restore')
            window['_TREE_'].update(load_tree_data())
        if event == 'SEARCH':
            # print(event,values)
            search_results(values,'search')
        if event == 'STERMS' + '_Enter':
            search_results(values,'search')
        if event == 'Make New Database':
            dbsetup.new_db_window()
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
            try:
                print(values['_TREE_'][0], flush=True)
                if values['_TREE_'][0] == '_A1_' or values['_TREE_'][0] == '_A_':
                    continue
                #print(values['_TREE_'][0])
                title = get_title(values['_TREE_'][0])
                body = show_body(values['_TREE_'][0])
                body = body.replace('&rsquo;', '\'')
                body = body.replace('&hellip;', '... ')
                body = body.replace('&dbqup', '\"')
                body = body.replace('&sngquo', '\'')
                window['E_TITLE'].update(title)
                window['VIEW'].update(body)
            except Exception as e:      # hiding the error from the user and moving on
                logging.error(f"RUNNING: module: {__name__} - {event}: probably clicked an empty portion of tree menu", exc_info=True)
            finally:
                print(f"RUNNING: module: {__name__} - {event} - probably clicked an empty portion of tree menu...moving on...\n---\n")
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
            print("just entered the if event statement for the update_entry()\n\n")
            try:
                print(values)
                common_progress_bar()
                print('coming back from calling the progress bar\n\n')
                u_title = values['E_TITLE']
                u_body = values['VIEW']
                print(f"sending values to update_entry u_title:u_body\n", flush=True)
                update_entry(values['_TREE_'][0], u_title, u_body)  # sending ID, TITLE and BODY to update_entry()
                                                                    # from time to time this action results in a crash or program exit.
                print("back from the update_entry() function...\n\n")
                print('---------------------------------------------------\n\n')
            except Exception as e:
                print(f"problem ocurred during the update of the entry: {e}")
                logging.error(f"RUNNING: module: {__name__} - not sure what happened... maybe you can tell me:", exc_info=True)
        if event == 'DelEntry' or event == 'Remove Entry(hide)':
            try:
                delete_entry(values['_TREE_'][0])
            except Exception as e:
                sg.PopupError('REMOVE ENTRY ERROR!',
                              f"It appears that you didn't select an entry to be removed first "
                              f"before sending your request to me. Please try again and this time "
                              f"select and load an entry to be removed\n{e}.")
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
    # check sec file to see if we're using credentials to start program
    if check_security():
        start_window()
    else:
        main()
