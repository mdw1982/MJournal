#!/usr/bin/python3
import hashlib
import json
import datetime as dt
import calendar
import logging
import sqlite3
import subprocess
import SplashScreen
import dbsetup
import settings
from dbsetup import *
import sqlite3 as sl
#from settings import *

#global database

curr_theme = get_current_theme()
sg.theme(curr_theme[0])
version = '0.6.5'
mainWindowSize = (990, 850)
searchWindowSize = (990,630)
database = get_database()
windowTitle = f"MJpournal -- {version} -- Connected to Database: {database}"
print(database)



def convertMonthShortName(m):
    months = []
    for i in range(1,13):
        months.append(calendar.month_abbr[i])
    return months[m-1]



def convert_to_list(l):
    n = []
    for line in l:
        line = list(line)
        n.append(line)
    return n


def check_security():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    val = convert_user_tuple(c.execute('select pwsec from settings').fetchall())
    c.close()
    if val[0] == 0:
        return False
    else:
        return True

'''
    changing the way new entries are made. Rather than opening up a brand new screen to take in the information
    we'll just take it from the main screen and gather the other data that was previously hidden on the new entry
    screen.
'''
def quick_entry(title,body, tags):
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME', 'VISIBLE']
    conn = sqlite3.connect(database)
    c = conn.cursor()
    new_id = convert_tuple(c.execute("select max(id) from entries;").fetchall())
    new_id = new_id[0]
    new_id += 1
    print(new_id)
    this_body = body.replace('\"', '&dbquo')
    this_body = body.replace('\'','&sngquo')
    data = (new_id, title, int(dt.datetime.now().strftime('%m')), int(dt.datetime.now().strftime('%d')),
            int(dt.datetime.now().strftime('%Y')), tags, this_body, str(dt.datetime.now().strftime('%H:%M')))
    sql = """insert into entries (id, title, month, day, year, tags, body, time) values(?,?,?,?,?,?,?,?);"""
    c.execute(sql, data)
    conn.commit()
    c.close()


def add_new_entry(dic):
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME', 'VISIBLE']
    conn = sqlite3.connect(database)
    c = conn.cursor()
    this_body = dic['B_ENTRY'].replace('\"', '&dbquo')
    this_body = this_body.replace('\'','&sngquo')
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

    #print('First Stage', data)
    # treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
    # treedata.Insert("", '_B_', 'B', [])
    # treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
    # ['id', 'title', 'month', 'day', 'time']
    for k in data.keys():
        lm = ''
        #print(k)
        td.Insert("", '_A_', f'{k}', [], )
        for entry in data[k]:
            m = convertMonthShortName(entry[2])
            if lm == m:
                #print('\t\t', entry)
                td.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
            else:
                #print('\t', m)
                td.Insert("_A_", '_A1_', f'{m}', [])
                td.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}', values=[entry[0]])
                #print('\t\t', entry)
            lm = m
    return td

def search_tree_data(ids):
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
            c.execute(f"select id, title, month, day, time from entries where id={x} and year = {y} and visible=1;")
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
        'id': id[0][0]+1,
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
        #line = list(line)
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

    userwindow = sg.Window(f'User Information Input -- {windowTitle}', layout, location=(500, 210), resizable=True, finalize=True)
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

    newindow = sg.Window(f'New M Journal Entry -- {windowTitle}', layout, size=(650, 540), location=(500, 210), resizable=True,
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
    with open('../README', 'r') as r:
        readme = r.read()

    frm_layout = [
        [sg.Multiline(readme, font=("Sans Mono", 11), size=(90,28), pad=(0, 0), wrap_lines=True)]
    ]
    layout = [
        [sg.Frame('README', frm_layout)],
        [sg.Push(), sg.Button('Close')]
    ]
    rmwindow = sg.Window(f'MJournal README -- {windowTitle}', layout, size=(680, 580), location=(500, 210), resizable=False,
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

    swindow = sg.Window(f' User Information Input -- {windowTitle}', layout, location=(500, 210), resizable=True, finalize=True)
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

def search_results(v):
    # 'STERMS': 'wonder', 'STARG': 'body',
    terms = v['STERMS']
    targ = v['STARG']
    #print(terms,targ)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    res = convert_tuple(c.execute(f"select id from entries where {targ} like '%{terms}%';").fetchall())
    c.close()
    print(res)
    if not res:
        sg.Popup('Empty Results Set', 'There were no results returned from your search. Please try again with '
                                      'different search terms')
    else:
        result_tree = search_tree_data(res)
        results_window(result_tree)


def results_window(rt):
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
        [sg.Multiline('', font=("Sans Mono", 11), size=(90, 28), pad=(0, 0),
                      wrap_lines=True, key='VIEW')]
    ]
    func_frameac = [
        [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False), sg.Button("Reload Tree", key='refresh', visible=False),
         sg.Button('Update Entry', key='UpdateEntry', visible=False), sg.Button('New Entry', key='NewEntry', visible=False),
         sg.Button('Load', key='LoadEntry', visible=False), sg.Button('Exit', key='quit')]
    ]
    searcha_framec = [
        [sg.Push(), sg.Text('Search Entrys: Body or Tags'), sg.Input('', size=(40, 1), key='STERMS'),
         sg.DropDown(('body', 'tags'), default_value='body', key='STARG'), sg.Button('GO', key='SEARCH'), sg.Push()]
    ]

    menua_defc = [
        ['&File', ['&New Entry', '&Remove Entry', '&Exit']],
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
    window.close()


# def make_window():
#     curr_theme = get_current_theme()
#     sg.theme(curr_theme[0])
#     dbchoosea_layout = [
#         [sg.Text('Choose Different Database to Use', font=std_font)],
#         [sg.DropDown(read_dblist(), default_value=database, size=(30, 1), key='DBNAME'),
#          sg.Button('Change Database', key='DBCHANGE')]
#     ]
#     cola = [
#         [sg.Tree(treedata, ['', ], font=('Sans Mono', 9), key='_TREE_', enable_events=True, col0_width=38,
#                  show_expanded=True, num_rows=34)]
#     ]
#     colb = [
#         [sg.Input('Title goes here', key='E_TITLE', size=(40, 1), font=std_font, enable_events=True)],
#         [sg.Multiline('', font=("Sans Mono", 11), size=(90, 28), pad=(0, 0),
#                       wrap_lines=True, key='VIEW', enable_events=True)]
#     ]
#     func_framea = [
#         [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False), sg.Button("Reload Tree", key='refresh'),
#          sg.Button('Update Entry', key='UpdateEntry'), sg.Button('Save New Entry', key='NewEntry'),
#          sg.Button('Load', key='LoadEntry', visible=False), sg.Button('Exit', key='quit')]
#     ]
#     searcha_frame = [
#         [sg.Push(), sg.Text('Search Entrys: Body or Tags'), sg.Input('', size=(40, 1), key='STERMS'),
#          sg.DropDown(('body', 'tags'), default_value='body', key='STARG'), sg.Button('GO', key='SEARCH'), sg.Push()]
#     ]
#
#     menua_def = [
#         ['&File', ['&New Entry Window', '&Remove Entry', '&Exit']],
#         ['&Edit', ['&Search']],
#         ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
#         ['&Help', ['&ReadMe', '&About']]
#     ]
#
#     taga_frame = [
#         [sg.Input('', size=(40, 1), key='_TAGS_')]
#     ]
#
#     refresh_layout = [
#         [sg.Menu(menua_def, tearoff=False, key='-MENU_BAR-')],
#         [sg.Column(cola, vertical_alignment='top'), sg.Column(colb, vertical_alignment='top')],
#         [sg.Push(), sg.Frame('Tags', taga_frame)],
#         [sg.Push(), sg.Frame('Functions', func_framea, )],
#         [sg.Frame('Search Entries', searcha_frame)],
#         [sg.Frame('Switch Database', dbchoosea_layout)]
#     ]
#     window = sg.Window(windowTitle, refresh_layout, size=mainWindowSize, location=(500, 210), resizable=True, finalize=True)
#     window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
#     return window


# print(theme_name_list)
def main():
    def update_entry(id,title,body):
        try:
            # filtering entry body for double quptes. sqlite doesn't like themtitle =
            b = body[0].replace('\"','&dbqup')
            print(id, b)
            conn = sqlite3.connect(database)
            c = conn.cursor()
            sql = f"""update entries set title={title}, body=\"{b}\" where id={id};"""
            c.execute(sql)
            conn.commit()
        except Exception as e:
            sg.PopupError('Error Updating Entry', f'I have found bare words in the data coming\n'
                          f'for the update of the entry record: {id}.\n'
                          f'the error was: {e}')
        c.close()

    def delete_entry(id):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        sql = f"""update entries set visible=0 where id={id};"""
        c.execute(sql)
        conn.commit()
        c.close()
        window['_TREE_'].update(load_tree_data())

    # treedata.Insert("", '_A_', 'Tree Item 1', [1234], )
    # treedata.Insert("", '_B_', 'B', [])
    # treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
    right_click_menu = ['', ['Copy', 'Paste', 'Select All', 'Cut']]
    col1 = [ # from Trr
        [sg.Tree(treedata, ['',], font=('Sans Mono',9), col0_width=38, key='_TREE_', enable_events=True, show_expanded=True, num_rows=34)]
    ]
    col2 = [
        [sg.Input('Quick Entry Title', key='E_TITLE', size=(40,1), font=std_font, enable_events=True)],
        [sg.Multiline('Quick Entry Body', font=("Sans Mono", 11), size=(90,28), pad=(0, 0), wrap_lines=True, key='VIEW')]
    ]
    #col3 = [[sg.Sizer(5,5)]]

    menu_def = [
        ['&File', ['&New Entry Window', '&Remove Entry', '&Exit']],
        ['&Edit', ['&Search']],
        ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
        ['&Help',['&ReadMe', '&About']]
    ]
    dbchoose_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    func_frame = [
        [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False), sg.Button("Reload Tree", key='refresh'),
         sg.Button('Update Entry', key='UpdateEntry'), sg.Button('Save New Entry', key='NewEntry'),
         sg.Button('Load', key='LoadEntry',visible=False), sg.Button('Exit', key='quit')]
    ]

    tag_frame = [
        [sg.Input('', size=(40,1), key='_TAGS_')]
    ]

    search_frame = [
        [sg.Push(), sg.Text('Search Entrys: Body or Tags'), sg.Input('', size=(40, 1), key='STERMS', enable_events=True),
         sg.DropDown(('','body'), default_value='body', key='STARG'), sg.Button('GO', key='SEARCH'), sg.Push()]
    ]
    frame_col1 = [
        [sg.Frame('Tree menu', col1, pad=(5,5))]
    ]
    frame_col2 = [
        [sg.Frame('Entries Input and View', col2,pad=(5,5))]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU_BAR-')],
        [sg.Column(frame_col1, vertical_alignment='top', expand_x=True, expand_y=True), sg.Column(frame_col2,vertical_alignment='top', expand_x=True, expand_y=True)],
        [sg.Push(), sg.Frame('Tags', tag_frame)],
        [sg.Push(), sg.Frame('Functions', func_frame)],
        [sg.Frame('Search Entries', search_frame, element_justification='center')],
        [sg.Frame('Switch Database', dbchoose_layout)]
    ]

    window = sg.Window(windowTitle, layout, size=mainWindowSize, location=(460, 160), resizable=True, finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'SEARCH':
            #print(event,values)
            search_results(values)
        if event == 'STERMS' + '_Enter':
            search_results(values)
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
        if ' SelectTreeItem' in event:
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
        if event == 'NewEntry' or event == 'New Entry':
            quick_entry(values['E_TITLE'], values['VIEW'], values['_TAGS_'])
            window['_TREE_'].update(load_tree_data())
        if event == 'refresh' or event == 'Refresh':
            window['_TREE_'].update(load_tree_data())
        if event == 'DBCHANGE' or event == 'Change Database':
            #print(values['DBNAME'])
            change_database(values['DBNAME'])
            window.close()
            # completely restarting the program to be able to use the chosen database
            os.execl(sys.executable, sys.executable, *sys.argv)
        if event == 'Db Setup':
            dbsetup.main()
        if event == 'UpdateEntry':
            #'_TREE_': ['15'], 'E_TITLE': 'bare word error back', 'VIEW':
            print(values)
            common_progress_bar()
            b = []
            b.append(values['E_TITLE'])
            b.append(values['VIEW'])
            # sending the body content back to the update function as a list with one element
            # to get around the bard word issue.
            update_entry(values['_TREE_'][0], b)
        if event == 'DelEntry' or event == 'Remove Entry':
            try:
                delete_entry(values['_TREE_'][0])
            except Exception as e:
                sg.PopupError('REMOVE ENTRY ERROR!',
                              f"It appears that you didn't select an entry to be removed first "
                              f"before sending your request to me. Please try again and this time "
                              f"select and load an entry to be removed\n{e}.")
        if event == 'About':
            show_about()
        #print(event,values)
    window.close()
    logging.info("PROGRAM Stop: program is closeing... exit code 0")


if __name__ == '__main__':
    SplashScreen.main()
    init_logs()
    if is_first_run():
        init_setup()
        os.execl(sys.executable, sys.executable, *sys.argv)
    # check sec file to see if we're using credentials to start program
    if check_security():
        start_window()
    else:
        main()