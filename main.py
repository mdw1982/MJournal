import hashlib
import time
import webbrowser
import calendar
from random import random, randint
import os
import sys
import sqlite3 as sl
import datetime as dt
import FreeSimpleGUI as sg

import dbmoves

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# imports from local modules go below here.
#import SplashScreen         # I have you turned off for now so quite yer bitchin
import dbsetup
from dbsetup import *
from classes.Entry import Entry
from classes.DBConn import DBConn

######################################################################

global dbo
'''defaults.json holds the database name and first run information... at least for now thats
   what is contains.'''
defaults = load_defaults()

'''calling it initdb because the database name contained within default.json is the last one used
   when the program was last closed. Thats the one it will start with. If this is a new install of
   the program then that file will of course have dummy.db in it, and then be overwritten to contain
   the default database, journal.db'''
initdb = defaults['dbname']

'''setting the database happens first thing and calls get_database() which reads the CDB file on disk
    then returns the value written there. each time the user changes the database being used that file
    is re-written.: 05.10.24_2141: thia is going away... working on a solution to make this a bit more 
    dynamic.
    line numbers where the variable database appears:
    43
    199
    476
    530
    853
    892
    945
    965
    '''
database = defaults['dbname']

'''the dbo object is created here and stays in an open state the entire time the program is running.
    there are commits in the DBConn class that see to the inserts and updates. dbo.close() isn't called
    till the program closes at the very end of the while loop in the main function. Also, the dbo object
    is never passed to another module, but used exclusively in main.py.'''

dbo = DBConn(database)              # creating the dbo object that the program will use to talk to the active database
curr_theme = get_current_theme()    # this setting is stored in the settings table and read each time the program starts
sg.theme(curr_theme)

'''the platform detection function was added to allow the program to detect whether it is running on Linux or 
    windows. At first, the function was created to detect the OS so the correct mascot image was displayed
    on the main screen. The windows mascot is an image of the Windows logo with flames coming up from the bottom.
    a subtle nod to just how much of a pain in the ass it is to make what works so easily on Linux work on Windows.'''
platform = detect_os()

__version__ = defaults['version']

mainWindowSize = (1090, 790)
new_ent_win = (650, 610)    # new entry screen/window size
win_location = (360, 90)
searchWindowSize = (990, 630)
'''at this time - 11.13.22 - the font used for displaying text on the screen is set statically. I haven't yet
    developed a method to allow the user to change the font dynamically. I personally prefer this True Type font
    to most others. If this font doesn't exist on the system where this program is running it will default to
    the system or theme default font. in that order.'''
tree_font = ('Trebuchet MS', 10)
std_font = ('Trebuchet MS', 11)
windowTitle = f"MJournal -- {__version__} "
status_bar = f"Date: {dt.datetime.now().strftime('%Y-%m-%d')}\t Connected to Database: {database}:: \tCurrent Theme: {curr_theme}"
'''
    commented out the code below that controls which mascot image to show because thats being removed
    from the program. Originally it was just placed there as a place holder for something else with actual
    functionality. I've extended the tree menu on the Y axis to take up the space left by the mascot. Better
    use of space in my humble opinion.
'''
# if detect_os() == 'windows':
#     icon_img = base64_image('images/MjournalIcon_36x36.ico')
# icon_img = base64_image('images/MjournalIcon_36x36.png')

'''both the win_location and popup_location values are set statically to work around the odd behavior of windows
    appearing in the very center of two monitors on the Linux desktop when more than one monitor is in use. this isn't
    a thing on Windows.'''
popup_location = (870, 470)
# print = sg.Print      # current disabled and will likely remain so. it has a singular purpose which is to display stdout
                        # stderr information to a debugging screen. the downside to using this is that if/when the program
                        # crashes so goes the debug window unless you're catching the exception that brought down the program
'''this object is not yet implemented. its sole purpose for existing was to help detect when an update is being made
    to an entry using the main screen. it will likely be abandoned. to create instance of the object it requires only a 
    name. the name attribute is irrelevant and serves no real purpose other than allowing the object to be instantiated.'''
entry = Entry('bob')

def who_am_i():
    return __file__


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

    VERSION:	{__version__}'''
    return header


def get_random_int():
    return randint(0, 99)


def get_random_quote():
    quotes = []
    with open(os.path.join(os.getcwd(),'quotes.txt'), 'r') as q:
        quotes = q.read().split('\n')
    return quotes[get_random_int()]


def convert_to_list(l):
    n = []
    for line in l:
        line = list(line)
        n.append(line)
    return n


# def tuble_to_list(l):  # in it's current form this fuction will convert a single tuple nice and neat to to a list
#     n = []  # working on a version of this function that will take multiple args and put them into a list
#     l = list(l)  # then return that list. 10.30.22
#     for line in l:
#         n.append(line)
#     return n


def check_security():
    '''
    converted to use dbo object 11.2.22
    :return:
    '''
    val = dbo.get('select pwsec from settings;')
    print(val)
    if val['pwsec'] == 0:
        return False
    else:
        return True


def add_new_entry(dic):
    '''
    changed the way the insert is working by using the dbo object. I had to adjust the class method to accept
    *args because this function is sending sql and data. Change made 11.1.22
    :var sql: this parameter has the sql - values (?,?,?,?,?,?,?,?) etc...
    :param dic: this parameter has the actual data that's being inserted into the database the data is contained in a dictionary.
    I don't remember now why I did it this way other than that I saw it somewhere and wanted to try it. I seriously doubt it would
    work with MySQL.
    :return: function returns nothing but takes information sent to it and inserts it into the database
    '''
    # ['ID', 'TITLE', 'MONTH', 'DAY', 'YEAR', 'TAGS', 'B_ENTRY', 'TIME', 'VISIBLE']
    this_body = dic['B_ENTRY'].replace('\"', '&dbquo')
    this_body = this_body.replace('\'', '&sngquo')
    '''this is useful but damn! there's gotta be an easier way to accomplish this'''
    data = (dic['ID'], dic['TITLE'], dic['MONTH'], dic['DAY'], dic['YEAR'], dic['TAGS'], this_body, dic['TIME'])
    sql = """insert into entries (id, title, month, day, year, tags, body, time) values(?,?,?,?,?,?,?,?);"""
    (status,msg) = dbo.insert(sql,data)
    if status == 'success':
        sg.Popup('New Entry Complete', 'Your new journal entry has been successfully added to the database.',
             auto_close=True, auto_close_duration=1, location=popup_location)
    if status == 'failure':
        print(f"there was a problem with submitting your entry: {msg}")
        sg.PopupError('Submission Error', f"there was a problem with submitting your entry: {msg}", location=popup_location)



def show_body(id):
    title = get_title(id)
    text = dbo.get_body(id)
    entry.setter(id, title, text)
    print(entry.id, entry.blenth)
    return text['body']


def get_title(id):
    b = dbo.get_title(id)
    print(b['title'])
    return b['title']


def load_tree_data():
    td = sg.TreeData()
    conn = sl.connect(dbo.database)
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
    # this is the SQL statement that will select the record information in a manner that accomodate
    # changing the the date and time information of the entry to move them up the tree menu list
    # select id, title year, month, day from entries where visible=1 order by year desc, month desc, day desc;
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


def search_tree_data(ids, v):
    searchTree = sg.TreeData()
    db_years = {}
    #ids = sorted(ids, reverse=True)
    '''
        building a dictionary list of IDs and the year in which they appear. doing this so that the 
        entry id has a connection to the year it was made. this is just later when displaying the search
        results in tree menu on the screen.
    '''
    # added: 3.25.23
    # added this single line to sort the id value in the list being passed in. It definitely sorted them
    # and on the screen looks correct however there are still some entries being placed in the wrong year
    # and month.
    ids = sorted(ids,reverse=True) #experimental addition
    for x in ids:
        a = dbo.get(f"select year from entries where id={x};")
        db_years[x] = a['year']
    print(db_years)

    rows = []
    #ids = {1: 2017, 57: 2017, 59: 2017, 66: 2017, 72: 2017, 73: 2017, 97: 2020, 112: 2021, 156: 2022, 158: 2022}
    years = []
    for y in db_years.values():
        if y in years:
            continue
        years.append(y)
    print(years)
    for k in db_years:
        res = dbo.get_rows(f"select year,id,title,month,day,time from entries where id={k} and year={db_years[k]} and visible={v};")
        if not res:
            continue
        else:
        # print(res)
            rows.append(res)
    print(rows)

    '''separate the rows and place them into a dictionary where the year is now the key and the values are a
        list of rows for that year. the first element of each list is the year for the entry'''
    temp = []
    data = {}
    i = 0
    old = 0
    for row in rows:
        try:
            if len(years) < 2:
                year = row.pop(0)
                temp.append(row)
                data[years[years.index(year)]] = temp
            else:
                print(row)
                year = row.pop(0)
                temp.append(row)
                if year != old:
                    data[years[years.index(year)]] = temp
                    i += 1
                    temp = []
                old = year
        except Exception as e:
            sg.PopupError('!!!ERROR!!!', f"I've experienced an error creating the tree menu for your search results\n"
                                         f"{e}", location=popup_location, icon=icon_img)
    print(data)
    #data = dict(sorted(data.items(),reverse=True))
    #exit()

    # ['id', 'title', 'month', 'day', 'time']
    '''building the tree menu for display'''
    for k in data.keys():
        print(data[k][0])
        lm = ''
        print(k)
        searchTree.Insert("", '_A_', f'{k}', [], )
        i = 0
        for entry in data[k]:
            m = convertMonthShortName(entry[2])
            if lm == m:
                # print('\t\t', entry)
                searchTree.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}',
                                  values=[entry[0]])
            else:
                # print('\t', m)
                searchTree.Insert("_A_", '_A1_', f'{m}', [])
                searchTree.Insert("_A1_", f'{entry[0]}', f'{entry[3]}, {entry[1][0:20]}...\t{entry[4]}',
                                  values=[entry[0]])
                # print('\t\t', entry)
            lm = m
            i += 1
    #c.close()
    return searchTree


def getHiddenValues():
    # keys = {'id', 'title', 'month', 'day', 'year', 'tags', 'body', 'time'}
    res = dbo.get("select max(id) from entries;")
    id = res['max(id)']
    today = dt.datetime.today()
    m = int(today.strftime('%m'))
    d = int(today.strftime('%d'))
    y = int(today.strftime('%Y'))
    t = today.strftime('%H:%M')
    dic = {
        'id': id + 1,
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
        '''
        converted to dbo object use 11.2.22
        :param vals:
        :return:
        '''
        # values coming in as dictionary
        user = vals['UserName']
        pw = vals['UserPass']
        salt = 'dfgasreawaf566'
        dbpass = pw + salt
        hashed = hashlib.md5(dbpass.encode())
        hashed_pass = hashed.hexdigest()

        # connect to db and check if user exists
        '''calling the dbo.get method returns a dictionary'''
        results = dbo.get(f'select user, password from users where user=\"{user}\";')

        if len(results) == 0:
            dbo.insert(f'insert into users (user, password) values(\"{user}\", \"{hashed_pass}\")')
            sg.Popup('New User Created', f'A new user has been created for {user}', auto_close=True, auto_close_duration=2)
        if len(results) > 0:
            if user == results['user']:
                sg.Popup('User Exists',
                         f'Nothing to be done here...The user account for {user} already exists for this database.',
                         icon=icon_img, location=popup_location)
                ans = sg.PopupYesNo('Change Password?', 'Would you like to change your current password?',
                                       location=popup_location, icon=icon_img)
                if ans == 'Yes':
                    change_user_password(pw)
                if ans == 'No':
                    userwindow.close()
            # time.sleep(.5)
        # values coming out in dictionary: [{'user': 'mweaver', 'password': '98e04149be480bdd2d7fcc4666f82061'}]

    whoami = os.getlogin()

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input(whoami, size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    userwindow = sg.Window(f'Create User', layout, icon=icon_img, location=(500, 210), resizable=True,
                           finalize=True)
    userwindow.bind("<Return>", "UserInfoInput")

    while True:
        event, values = userwindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event in ('UserInfoInput'):
            print(event, values)
        # change_user_password(values['UserPass'])
        if event == 'Ok' or event == 'UserInfoInput':
            # print(values)
            create_user_account(values)
            userwindow.close()

    userwindow.close()


def new_entry_window(id=None, title=None, body=None):
    if title != None and body != None:
        f1title = [
            [sg.Input(title, size=(40, 1), key='TITLE')]
        ]
        f2body = [
            [sg.Multiline(body, size=(100, 20), key='B_ENTRY', font=std_font, write_only=False)]
        ]
    f1title = [
        [sg.Input(size=(40, 1), key='TITLE')]
    ]
    f2body = [
        [sg.Multiline('', size=(100, 20), key='B_ENTRY', font=std_font, write_only=False)]
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
        [sg.Push(), sg.Button('Submit (F5)', key='SubmitNewEntry'), sg.Button('Cancel', key='Exit')]
    ]

    newindow = sg.Window(f'New MJournal Entry -- {database}', layout, modal=False, size=new_ent_win, location=(500, 210),
                         resizable=True, icon=icon_img, finalize=True)
    # newindow.bind('', '_TREE_', propagate=True)
    newindow.bind('<F5>', 'SubmitNewEntry')  # added the hotkey binding for consistancy's sake.

    while True:
        event, values = newindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'SubmitNewEntry':
            # print(values)
            if values['TITLE'] == '':
                sg.PopupError('!!!ENTRY ERROR!!!', "you didn't give your entry a title. please fix this!", auto_close=True,
                          auto_close_duration=5,location=popup_location)
                continue
            add_new_entry(values)
            break
    newindow.close()


def update_entry_window(id):
    def this_entry_update(id,vals):
        title = vals['U_TITLE']
        body = vals['U_ENTRY']
        u_body = body      #send the updated body content back down to the main window VIEW element
        body = body.replace('\"', '&dbqup')
        body = body.replace('\'', '&sngquo')
        # print('this is whats coming to get updated:::: ',id, title, body)

        sql = f"""update entries set title=\"{title}\", body=\"{body}\" where id={id};"""
        dbo.update(sql)
        return u_body

    results = dbo.get(f"select title, body from entries where id={id}")
    body = results['body']
    body = body.replace('&dbqup', '\"')     # cleaning things up for presentation to the screen
    body = body.replace('&sngquo', '\'')    # displaying human readable double and single quotes
    f1title = [
        [sg.Input(results['title'], size=(40, 1), key='U_TITLE'),sg.Button('Insert Date/Time (F4)', key='Insert Date/Time')]
    ]
    f2body = [
        [sg.Multiline(body, size=(100, 20), key='U_ENTRY', font=std_font, autoscroll=True, focus=True)]
    ]

    layout = [
        [sg.Frame('Entry Title', f1title)],
        [sg.Frame('Entry', f2body)],
        [sg.Text('Tags: words separated by comas... no spaces')],
        [sg.Input('', key='TAGS')],
        [sg.Push(), sg.Button('Submit Update (F8)', key='SubmitUpdate'), sg.Button('Cancel', key='Exit')]
    ]

    window = sg.Window(f'Update Entry -- {database}', layout, modal=False, size=new_ent_win, location=(500, 210),
                         resizable=True, icon=icon_img, finalize=True)
    # newindow.bind('', '_TREE_', propagate=True)
    window.bind('<F8>', 'SubmitUpdate')  # added the hotkey binding for consistancy's sake.
    window.bind('<F4>', 'Insert Date/Time')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Exit':
            break
        if event == 'Insert Date/Time' or event == 'Insert Date/Time - (F4)':
            date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
            text = window['U_ENTRY']
            text.update(text.get() + '\n\n' + date_time)
        if event == 'SubmitUpdate':
            # print(values)
            if values['U_TITLE'] == '':
                sg.PopupError('!!!ENTRY ERROR!!!', "you didn't give your entry a title. please fix this!", auto_close=True,
                          auto_close_duration=5,location=popup_location)
                continue
            b = this_entry_update(id,values)
            window.close()
            return b
    window.close()


def show_about():
    msg = f"MJournal version: {__version__}\n" \
          f"Copyright {dt.datetime.now().strftime('%Y')}\n" \
          f"Release under the GnuPL" 
    col1 = [
        [sg.Image('images/MjournalIcon_80x80.png', )]
    ]
    # {'GitHub': 'https://github.com/mdw1982/MJournal'}

    col2 = [
        [sg.T(msg)],
        [sg.Text('On GitGub... Click text Below')],
        [sg.T('https://github.com/mdw1982/MJournal', enable_events=True, key='URL')]
    ]
    frm_layout = [
        [sg.Column(col1, vertical_alignment='top'), sg.Column(col2, vertical_alignment='top')],
        [sg.Push(), sg.Button('Close', key='CLOSE')]
    ]
    win_layout = [
        [sg.Frame('About MJournal', frm_layout)]
    ]
    window = sg.Window('About', win_layout, location=(510, 220), icon=icon_img, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'CLOSE'):
            print(event, values)
            break
        if event == 'URL':
            url = 'https://github.com/mdw1982/MJournal'
            webbrowser.open(url)
        print(event, values)

    window.close()


def show_readme():
    from tkhtmlview import html_parser

    def set_html(widget, readme, strip=True):
        prev_state = widget.cget('state')
        widget.config(state=sg.tk.NORMAL)
        widget.delete('1.0', sg.tk.END)
        widget.tag_delete(widget.tag_names)
        html_parser.w_set_html(widget, readme, strip=strip)
        widget.config(state=prev_state)

    with open('README.html', 'r') as h:
        readme = h.read()

    layout = [[sg.Multiline(readme, key='content', expand_y=True, expand_x=True, text_color='Black',
                            background_color='White')],
              [sg.Push(), sg.B('Close', key='quit')]
              ]

    window = sg.Window('MJournal HowTo', layout, size=(950, 600), location=(550, 245), modal=True, finalize=True,
                       resizable=True)
    advertise = window['content'].Widget
    html_parser = html_parser.HTMLTextParser()
    set_html(advertise, readme)
    width, height = advertise.winfo_width(), advertise.winfo_height()

    while True:
        event, values = window.read()
        match event:
            case 'quit':
                break
    window.close()


def show_howto():
    from tkhtmlview import html_parser
    def set_html(widget, howto, strip=True):
        prev_state = widget.cget('state')
        widget.config(state=sg.tk.NORMAL)
        widget.delete('1.0', sg.tk.END)
        widget.tag_delete(widget.tag_names)
        html_parser.w_set_html(widget, howto, strip=strip)
        widget.config(state=prev_state)

    with open('HOWTO.html', 'r') as h:
        howto = h.read()

    layout = [[sg.Multiline(howto, key='content', expand_y=True, expand_x=True, text_color='Black',
                            background_color='White')],
              [sg.Push(), sg.B('Close', key='quit')]
              ]

    window = sg.Window('MJournal HowTo', layout, size=(950, 600), location=(550, 245), modal=True, finalize=True,
                       resizable=True)
    advertise = window['content'].Widget
    html_parser = html_parser.HTMLTextParser()
    set_html(advertise, howto)
    width, height = advertise.winfo_width(), advertise.winfo_height()

    while True:
        event, values = window.read()
        match event:
            case 'quit':
                break
    window.close()


def settings_window():
    ctheme = get_current_theme()

    layout = [
        [sg.Text('Program Theme'), sg.Push(),
         sg.Combo(get_them_list(), default_value=ctheme, size=(30, 1), key='_THEME_')],
        [sg.Text("Program Security On/Off (1/0)"), sg.Push(), sg.DropDown([1,0], default_value=0, key='SEC')],
        [sg.HSeparator(pad=(3, 3))],
        [sg.Push(), sg.Button('OK', key='SubmitValues'), sg.Button('Cancel', key='quit')]
    ]

    settingswindow = sg.Window('Program Settings', layout, location=(680, 310), resizable=True, finalize=True)
    settingswindow.bind("<Return>", "SubmitValues")

    while True:
        event, values = settingswindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'Ok' or event == 'SubmitValues':
            theme = values['_THEME_']
            secure = values['SEC']
            update_settings(theme, secure)
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
    # conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    # c = conn.cursor()
    # c.execute(f'select password from users where user=\"{un}\";')
    info = dbo.get(f'select password from users where user=\"{un}\";')#[dict(row) for row in c.fetchall()]
    # c.close()
    if len(info) == 0:
        sg.PopupError('Information Error', 'Nothing was returned when I looked for your current password. Its '
                                           'most likely you haven not set one for this database. Please do that'
                                           'now.', icon=icon_img, location=popup_location)
        return False

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
        '''
        converted to dbo object 11.2.22
        :param vals:
        :return:
        '''
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
        dbo.update(f'update users set password=\"{pw}\" where user=\"{user}\";')

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

    pwindow = sg.Window(f'Change User Password', layout, icon=icon_img, location=(500, 210),
                        resizable=True,
                        finalize=True)
    pwindow.bind("<Return>", "ChangePass")

    while True:
        event, values = pwindow.read()
        if event == sg.WIN_CLOSED or event == 'quit':
            break
        if event == 'ChangePass':
            if verify_userpass(values):
                result = check_newpass_match(values)
                if result == 'NoMatch':
                    sg.PopupError('Password Change Error',
                                  'Values for your new password do not match, Please try again',
                                  icon=icon_img, location=popup_location)
                    pwindow['NewPass'].update('')
                    pwindow['RetypePass'].update('')
                    pwindow.close()  # also have to check current password is correct.
                    pw = values['CurrPass']
                    change_user_password(pw)  # if the new passwords don't match need to go back to the window and try again.
                if result == "Match":
                    # print(event,values)
                    update_user_pass(values)
                    pwindow.close()
                sg.Popup('SUCCESS! Password Change',
                         'Your password has successfully been change.\nPlease remember it or write it down '
                         'somewhere in a safe place. Forgotten passwords cannot be retrieved!',
                         icon=icon_img, location=popup_location, auto_close=True, auto_close_duration=2)
            else:
                print('Current Password validation failed. Closing Window...')
                sg.PopupError('Password Validation Error', 'I was unable to validate your current password.',
                              icon=icon_img, location=popup_location)
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
        '''
        converted to use the dbo object 11.2.22
        :param vals:
        :return:
        '''
        # values coming in as dictionary
        # vals['UserName'], vals['UserPass']
        # 1. we're going to hash the password value
        user = vals['UserName']
        pw = vals['UserPass']
        salt = 'dfgasreawaf566'
        dbpass = pw + salt
        hashed = hashlib.md5(dbpass.encode())
        hashed_pass = hashed.hexdigest()
        print(hashed_pass)

        userinfo = dbo.get(f'select user, password from users where user=\"{user}\";')
        print('User info coming back from users table: ',userinfo)

        if user == userinfo['user'] and userinfo['password'] == hashed_pass:
            # if userinfo['password'] == hashed_pass:
            sg.Popup('Welcome Back!', "Credentials Accepted...", location=popup_location, icon=icon_img,
                     auto_close=True, auto_close_duration=1)
            swindow.close()
            main()
        else:
            sg.PopupError('Login Error', 'Either your username or password was incorrect.\n'
                                         'I cannot start the program at this time.', location=popup_location,
                          icon=icon_img)
            exit()

    layout = [
        [sg.Text('Username', size=(30, 1))],
        [sg.Input('', size=(30, 1), key='UserName')],
        [sg.Text('Password', size=(30, 1))],
        [sg.Input('', size=(30, 1), password_char='x', key='UserPass')],
        [sg.Push(), sg.Button('OK', key='UserInfoInput'), sg.Button('Cancel', key='quit')]
    ]

    swindow = sg.Window(f'Login', layout, icon=icon_img, location=(500, 210), resizable=True,
                        finalize=True)
    swindow.bind("<Return>", "UserInfoInput")

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

def search_results(v, command):
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
                                      f"or title like '%{terms}%' and visible=1;").fetchall())
    else:
        res = convert_tuple(c.execute(f"select id from entries where {targ} like '%{terms}%' and visible=1;").fetchall())
    c.close()
    print(res)
    if not res:
        sg.Popup('Empty Results Set', 'There were no results returned from your search. Please try again with '
                                      'different search terms', location=popup_location, icon=icon_img)
    else:
        if command == 'search':
            result_tree = search_tree_data(res, 1)
        if command == 'restore':
            result_tree = search_tree_data(res, 0)
        results_window(result_tree, command)


def get_hidden_entries(command):
    '''
    converted to dbo object 11.1.22
    :param command:
    :return:
    '''

    '''
    r = dbo.get(f"select id from entries where visible=0")
        above was replaced 03.28.24 2034
        the line above has been taken out of the code base because for some unknown reason it is not
        functioning as it should. It consistantly returns an empty result set. I know this because
        I know there are hidden records in the database which the query is looking for. When I replaced
        this line of code with the code below I got the results I was expecting. a list of record IDs
        that are hidden. Clearly there is something wrong in the class DBConn, but at this time I don't 
        know what that is.
    '''
    conn = sl.connect(database)
    c = conn.cursor()
    c.execute("select id from entries where visible=0")
    r = convert_tuple(c.fetchall())
    print(r)
    if not r:
        sg.Popup('Empty Results Set', 'There were no results returned from your search. Please try again with '
                                      'different search terms', location=popup_location, icon=icon_img)
    else:
        result_tree = search_tree_data(r, 0)
        results_window(result_tree, command)
    c.close()

def unhide_entry(i):
    try:
        '''dbo object added 11.2.22: one line takes the place of five. at least in the main program. 
            there is no close statement for the cursor because that is handled when the program exits.
            essentially the dbo object (database connection) remains open while the program is running.
            I could open and close the cursor but I do not see much sense in doing so since the database(s)
            are SQLite and local to the program.'''
        dbo.update(f"update entries set visible=1 where id={i};")
    except Exception as e:
        print(f"there was an error restoring a hidden entry: {e}")
        sg.PopupError('Unhide Entry Error', f"there was an error restoring a hidden entry: {e}",
                      location=popup_location, icon=icon_img)


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
        :param changedate: this parameter, if True, changes the year, month, day and time values for the entry
        :return:
        '''
        try:
            body = body.replace('\"', '&dbqup')
            body = body.replace('\'', '&sngquo')
            print('this is whats coming to get updated:::: ', id, title, body)
            conn = sqlite3.connect(database)
            c = conn.cursor()
            sql = f"""update entries set title=\"{title}\", body=\"{body}\" where id={id};"""
            c.execute(sql)
            conn.commit()
            c.close()
        except Exception as e:
            print(f'I have found an error for the update of the entry record: {id}. '
                                                  f'the error was: {e}')
            sg.PopupError('Error Updating Entry', f'I have found an error for the update of the entry record: {id}. '
                                                  f'the error was: {e}', location=popup_location, icon=icon_img)
        finally:
            print("I've successfully processed your update request.")
            sg.Popup('Update Processed', "I've successfully processed your update request.", location=popup_location,
                     icon=icon_img)

    curr_theme = get_current_theme()
    sg.theme(curr_theme)
    dbchoosea_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value=database, size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    colac = [
        [sg.Tree(rt, ['', ], font=std_font, key='_TREE_', enable_events=True, col0_width=38,
                 show_expanded=True, num_rows=34)]
    ]
    colbc = [
        [sg.Input('', key='E_TITLE', size=(40, 1), font=std_font)],
        [sg.Multiline('', font=std_font, size=(90, 28), pad=(0, 0), key='VIEW')]
    ]
    if command == 'search':
        func_frameac = [
            [sg.Push(), sg.Button('Remove Entry', key='DelEntry', visible=False),
             sg.Button("Reload Tree", key='refresh', visible=False),
             sg.Text("Select CheckBox to update entry's date values", visible=False),
             sg.Check('', key='ChangeEntryDate', default=False, pad=(3, 3), visible=False),
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
            ['&Edit', ['&Utilities', ['Insert Date/Time']], ],
            ['&Settings', ['&Set User Password', '&Program Settings', '&Make New Database']],
            ['&Help', ['&ReadMe', '&About']]
        ]
    if command == 'restore':
        menua_defc = [
            ['&File', ['&New Entry', '&Restore Entry(unhide)', '&Exit']],
            ['&Edit', ['&Utilities', ['Insert Date/Time']], ],
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
    if command == 'search':
        windowTitle = 'Search Results Display'
    if command == 'restore':
        windowTitle = 'Restore Hidden Entries'

    # 10.23.22: removed size=searchWindowSize, from search results display screen. considering adding more functions
    # to this screen IF command == 'search'
    window = sg.Window('Search Results', refresh_layoutc, icon=icon_img, location=(500, 210), resizable=True,
                       finalize=True)
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")
    window.bind('<F1>', 'HowTo')
    window.bind('<F4>', 'Insert Date/Time')
    window.bind('<F5>', 'UpdateEntry')
    window.bind('<F11>', 'ReloadTreeData')
    window.bind('<F12>', 'quit')

    while True:
        event, values = window.read()
        if event == 'quit' or event == sg.WIN_CLOSED:
            break
        if event == 'Insert Date/Time':
            date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
            text = window['VIEW']
            text.update(text.get() + '\n\n' + date_time)
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
            body = body.replace('&ldquo;', '\"')
            body = body.replace('&rdquo;', '\"')
            window['E_TITLE'].update(title)
            window['VIEW'].update(body)
        if event == 'RestoreEntry':
            unhide_entry(values['_TREE_'][0])
            window['_TREE_'].update(rt)
            sg.Popup('Restore Successful', f"I was able to successfully restore your hidden entry with the "
                                           f"entry id of {values['_TREE_'][0]}. You will see the restored entry in the tree menu of "
                                           f"the main screen as soon as you click 'OK'", location=popup_location,
                     icon=icon_img)
            break
        if event == 'UpdateEntry':
            u_title = values['E_TITLE']
            u_body = values['VIEW']
            # chngDateEntry = values['ChangeEntryDate']
            update_search_entry(values['_TREE_'][0], u_title, u_body)
            break
    window.close()

def rename_db():
    file = os.path.join(os.getcwd(), 'restore.db')

    frm_layout = [
        [sg.Text('Database Name')],
        [sg.Input('', key='_NEWDBNAME_', size=(30,1))],
        [sg.Push(),sg.B('OK', key='_RENAME_')]
    ]
    layout = [
        [sg.Frame('Rename Restored Database', frm_layout)],
        [sg.Push(),sg.Button('Quit', key='quit')]
    ]
    window = sg.Window('Restored Database', layout, location=win_location, icon=icon_img, finalize=True)

    while True:
        event, values = window.read()
        if event in ('quit', sg.WIN_CLOSED):
            break
        if event == '_RENAME_':
            dbname = values['_NEWDBNAME_'] + '.db'
            dest = os.path.join(os.getcwd(), dbname)
            current = get_database()
            if current == dbname:
                sg.PopupError('!!!Procedural ERROR!!!',f"You can't rename a database with {dbname} while that is your current database. "
                                                       f"Please choose another name.", location=popup_location, icon=icon_img)
                window.close()
                rename_db()
            try:
                if exists(dest):
                    sg.Popup('!!Rename Error!!',f'Database {dbname} already exists. Please choose another.',location=popup_location, icon=icon_img)
                    window.close()
                    rename_db()
                else:
                    os.rename(file,dest)
            except Exception as e:
                print(f"there was a problem... I wasn't able to rename your database file: {e}")
                sg.PopupError('!!!Renaming ERROR!!!', f"I wasn't able to rename your file {file}: {e}\n"
                                                       f"you may have to rename the file manually.", location=popup_location, icon=icon_img)
            else:
                print(f"file {file} successfully rename to {dest}")
                sg.Popup('SUCCESS!', f"file {file} successfully rename to {dest}", location=popup_location, icon=icon_img, auto_close=True, auto_close_duration=2)
                break

    window.close()


def database_maintenance():
    dbmaint_loc = (660,200)
    def restore_db(rfile):
        print(rfile)
        with open(rfile, 'r') as dbf:
            sql = dbf.read()
        print(sql)
        (status, msg) = dbo.restore(sql, os.getcwd())
        if status == 'success':
            print(msg)
            ans = sg.popup_yes_no('SUCCESS!',f"The restoration of the database {rfile} was successful. You should rename the file before "
                                             f"using it. Would you like to do that now? If you don't do it now "
                                             f"you'll have to rename the database manually later.", location=popup_location)
            print(ans)
            if ans == 'Yes':
                print('WONDERFUL')
                sg.Popup('Wonderfull!','Sending you there momentarily...', auto_close=True, auto_close_duration= 2, location=popup_location)
                '''sending the file name of the restored database off to be renamed.'''
                rename_db()
            else:
                print("you'll want to rename this file before using it.")
        if status == 'failure':
            print("Tis a very, very sad day...  wasn't able to restore your database: ",msg)


    if detect_os() == 'Linux':
        from crontab import CronTab
    '''
    this function is specifically for creating manual backups of the database chosen from the
    screen. I wanted to provide a method so the user was able to make backups of their database(s).
    Other personal journal programs i've seen don't offer this which I found odd. At least programs
    that Utilize a database for entries.
    :return:
    '''

    def make_backup(path, db):
        import io
        print(path)
        date = f"{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}"
        print(f"date value: {date}")
        db = db.replace('\n', '')

        filename = f"{db}_{date}.sql"
        print(f"file name: {filename}")
        dest = os.path.join(path,filename)
        conn = sqlite3.connect(db)
        # Open() function
        with io.open(dest, 'w') as p:
            # iterdump() function
            for line in conn.iterdump():
                #print('%s\n' % line)
                p.write('%s\n' % line)
        conn.close()
        print(f"Saving {filename} to {dest}")

    '''
    It's ugly but useful. Just needed to load a list of lists to return values back to the dropdown
    lists that populate the dropdowns to build the crontab entry.
    :return:
    '''
    if detect_os() == "Linux":
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
                sshContent = f'''#!/bin/sh\n\ncd {here}\n./dbbackup\nexit'''
                with open(startupFile, 'w') as s:
                    s.write(sshContent)
                os.chmod(startupFile, 0o755)
            if exists(location):
                sshContent = f'''#!/bin/sh\n\ncd {here}\n./dbbackup\nexit'''

                with open(startupFile, 'w') as s:
                    s.write(sshContent)
                os.chmod(startupFile, 0o755)
            if exists(startupFile):
                print("SUCCESS! we made a file")
                print(startupFile)
            if not exists(startupFile):
                print('FAILED! WTF')
            # --------- end making startbu.sh ----------#
            print("entering process cronvals")
            d = {}
            for k, v in dic.items():
                if k in ['min', 'hrs', 'mday', 'mon', 'wday']:
                    d[k] = v
                else:
                    continue

            cron = CronTab(user=user)
            # fixed issue with cron driven db backups. typp in the file name being called.
            job = cron.new(command=f'{location}/startbu.sh')
            job.setall(f"{d['min']} {d['hrs']} {d['mday']} {d['mon']} {d['wday']}")
            return d, job

        mlist = load_cron_lists()
        cl = load_user_crontab()

    '''
    the remove_db function actually doesn't delete or remove the database but removes the database name
    from the dblist file that the program reads from to list the available database for the program.
    :return:
    '''

    def edit_dlist(name, c):
        from dbmoves import attach,detach
        '''the path information in this function separately needs redone. it's coded for Linux but needs
            to be more pythonic using os.path.realpath and such... perhaps using .join to the os.path call...'''
        print(name)
        if '.db' not in name:
            dbname = f"{name}.db"
        else:
            dbname = name
        nlist = read_dblist()
        if dbname in nlist and c == 'add':
            sg.PopupError('DB Add Error', f"The database {dbname} already present in dblist", location=popup_location,
                          icon=icon_img)
            c = 'err'
            window['ATTDB'].update('')
        if c == 'add':
            # as we're attaching a previously detached database we just need to move it out from
            # the olddb folder and back to the root of the program directory. just the reverse of c == del
            attach(dbname)
            read_dblist()
            sg.Popup(f"I successfully attached the requested database: dbname")
        if c == 'del':
            if name == get_database():
                sg.PopupError('!!!Error Removing Database', f'You cannot delete (remove) the current database: {name}\n'
                                                            f'The database you are attempting to move is currently open.\n'
                                                            f'Switch to another database then try again...', location=popup_location,
                              icon=icon_img)
                return None
            # folder = 'olddb'
            # if detect_os() == 'windows':
            #     folderpath = os.getcwd() + f'\\{folder}\\'
            folderpath = os.path.relpath('olddb')
            if not exists(folderpath):
                os.mkdir(folderpath)
            detach(dbname)
            read_dblist()
        if c == 'add':
            sg.Popup(f"I've finished attaching {name} to the dblist", location=popup_location, icon=icon_img)
        if c == 'del':
            sg.Popup(f"I've finished removing {name} from the dblist", location=popup_location, icon=icon_img)
        if c == 'err':
            sg.Popup(f"{name} couldn't be added to the dblist file because it's present in the file. "
                     f"please choose a different file or quit.", location=popup_location, icon=icon_img)

    col1 = [
        [sg.Input('', size=(50, 1), key='BUPATH')],
        [sg.FolderBrowse('Browse', target='BUPATH',initial_folder='backups')],
        [sg.Push(), sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME')],
        [sg.Button('Create Backup', key='PerformBackup')],
        [sg.HSeparator()],
        [sg.Text('Remove Database'),
         sg.DropDown(read_dblist(), default_value=None, key='dbname_remove'),
         sg.Button('Remove Database', key='RemoveDB',
                   tooltip='Simply removes database from dblist file and does not delete the database')],
        [sg.HSeparator()],
        [sg.T('Attach Database')],
        [sg.I('', size=(30, 1), key='ATTDB'),
         sg.FileBrowse('Browse', target='ATTDB', file_types=(("DB Files", "*.db"),), initial_folder='olddb')],
        [sg.Push(), sg.Button('Attach Datanase', key='-ATTACHDB-')],
        [sg.HSeparator()],
        [sg.Text('Restore Database from Backup')],
        [sg.I('', size=(30, 1), key='RESTDBSQL'),
         sg.FileBrowse('Browse', target='RESTDBSQL', file_types=(("DB Backup Files", "*.sql"),), initial_folder='backups')],
        [sg.Push(),sg.Button('Restore DB Backup', key='_RESTDB_')]
    ]

    if detect_os() == 'Linux':
        col2 = [
            [sg.T('Min...'), sg.T('Hrs...'), sg.T('Day\nMon...'), sg.T('Mon...'), sg.T('Day\nWk...')],
            [sg.DropDown(mlist[0], size=(3, 1), default_value='*', key='min'),
             sg.DropDown(mlist[1], size=(3, 1), default_value='*', key='hrs'),
             sg.DropDown(mlist[2], size=(3, 1), default_value='*', key='mday'),
             sg.DropDown(mlist[3], size=(3, 1), default_value='*', key='mon'),
             sg.DropDown(mlist[4], size=(3, 1), default_value='*', key='wday')],
            [sg.Multiline(load_user_crontab(), key='CRONSTMNT', size=(50, 5))],
            [sg.Push(), sg.Button('Create Cron Job', key='build'), sg.Button('Submit Job', key='bless')]
        ]
    elif detect_os() == 'windows':
        col2 = [
            [sg.Text('Create a Schedule Task')],
            [sg.Button('Create Scheduled Task for Backup', key='schdtask')]
        ]

    main_layout = [
        [sg.Frame('Database Backup', col1, vertical_alignment='top'),
         sg.Frame('Windows Task Scheduler - Scheduled Backup', col2, vertical_alignment='top')],
        [sg.Push(), sg.Button('Close', key='quit')]
    ]
    window = sg.Window('Database Maintenance', main_layout, icon=icon_img, resizable=True, location=dbmaint_loc,
                       finalize=True)
    window['dbname_remove'].bind("<Return>", '_Enter')

    while True:
        event, values = window.read()
        match event:
            case 'quit' | sg.WIN_CLOSED:
                break
            case '_RESTDB_':
                restore_db(values['RESTDBSQL'])
                break
            case '-ATTACHDB-':
                print(values['ATTDB'])
                dbfile = os.path.basename(os.path.realpath(values['ATTDB']))
                edit_dlist(dbfile, 'add')
            case 'RemoveDB':
                returned = edit_dlist(values['dbname_remove'], 'del')
                print('Tried to delete (move) a database that was currently open.')
            case 'PerformBackup':
                print(event, values)
                make_backup(values['BUPATH'], values['DBNAME'])
                break
            case 'build':
                window['CRONSTMNT'].update('')
                d, vd = process_cronvals(values)
                window['CRONSTMNT'].update(vd)
            case 'bless':
                d, vd = process_cronvals(values)
                user = os.getlogin()
                location = os.path.expanduser('~') + '/bin'
                cron = CronTab(user=user)
                job = cron.new(command=f'{location}/startbu.sh')
                job.setall(f"{d['min']} {d['hrs']} {d['mday']} {d['mon']} {d['wday']}")
                cron.write()
                sg.Popup('Cron Job Written', f"I was able to successfully write to your crontab the following information\n"
                                             f"{job}\n"
                                             f"Your Databases will now be automatically backed up according to the settings "
                                             f"in your crontab.", location=popup_location, icon=icon_img)
                break
            case 'schdtask':
                os.system('taskschd')
            case x:
                sg.Popup('Unknown event', "An unknown event has occurred. There is nothing I can do.", location=popup_location, icon=icon_img)
                break

    window.close()


def main():
    global dbo

    def update_entry(id, title, body):
        if not id:
            print("the value sent for ID was empty... I cannot update the entry")
        if id:
            # try:
            # filtering entry body for double quptes. sqlite doesn't like them... this program because
            # of sqlite has really been giving me the business with quote characters.
            # b = body
            body = body.replace('\"', '&dbqup')
            body = body.replace('\'', '&sngquo')
            sql = f"""update entries set title=\"{title}\", body=\"{body}\" where id={id};"""
            dbo.update(sql)
            # except Exception as e:
            #     sg.PopupError('Error Updating Entry', f'I have found an error for the update of the entry record: {id}. '
            #                                           f'the error was: {e}')
            # finally:
            # 10.23.22: removed param any_key_closes=True from the popup. If you use F5 to send the update the popup appears
            # and then closes immediately. too fast to be properly visible. added auto_close_duration=1
            sg.Popup('Update Processed', "I've successfully processed your update request.\n"
                                         "this message will self-distruct in 2 seconds...", auto_close=True,
                     auto_close_duration=1, location=popup_location, icon=icon_img)
            return id

    def delete_entry(id):
        '''
        converted to dbo object 11.2.22
        :param id:
        :return:
        '''
        sql = f"""update entries set visible=0 where id={id};"""
        dbo.update(sql)
        window['_TREE_'].update(load_tree_data())

    col1 = [  # from Trr
        [sg.Tree(treedata, ['', ], font=tree_font, col0_width=42, key='_TREE_', enable_events=True,
                 show_expanded=True, num_rows=22, pad=(10, 10), expand_x=True,expand_y=True,
                 tooltip='click a record node to view the entry')]

    ]
    right_click_menu = ['', ['Copy', 'Paste', 'Select All']]
    col2 = [
        [sg.Input('',key='E_TITLE', size=(40, 1), font=std_font, pad=(5, 5), readonly=True, visible=False)],
        [sg.Multiline('', font=std_font, size=(89, 23), pad=(5, 5), key='VIEW',
                      right_click_menu=right_click_menu, autoscroll=True, disabled=True)]
    ]

    menu_def = [
        ['&File', ['&New Entry Window - (F8)', '&Remove Entry(hide)', '&Restore Entry(unhide)', '&Exit']],
        ['&Edit', ['&Utilities', ['Insert Date/Time - (F4)']], ],
        ['&Tools', ['&Debug']],
        ['&Settings', ['&User Settings', ['&Set User Password', '&Change User Password'], '&Program Settings',
                       '&Make New Database - (F6)', '&Database Maintenance']],
        ['&Help', ['&ReadMe', '&HowTo', '&About']]
    ]
    dbchoose_layout = [
        [sg.Text('Choose Different Database to Use', font=std_font)],
        [sg.DropDown(read_dblist(), default_value='choose', size=(30, 1), key='DBNAME'),
         sg.Button('Change Database', key='DBCHANGE')]
    ]
    func_frame = [
        [sg.Push(), sg.Button('Reload Tree', key='ReloadTree'),sg.Button('Reload Program', key='Reload', tooltip=tp_reload(), visible=True),
         sg.Button('Update Entry (F5)', key='UpdateEntry'), sg.Button('New Entry (F8)', key='New Entry Window'),
         sg.Button('Exit (F12)', key='quit')]
    ]

    tag_frame = [
        [sg.Text("DON'T FORGET TO SUBUT YOUR UPDATE", text_color='red', font=('Sans Bold', 14), key='WARNING',
                 visible=False)],
        [sg.Input('', size=(40, 1), key='_TAGS_', visible=False)]
    ]

    search_frame = [
        [sg.Push(), sg.Text('Search Entrys: Body or Tags', visible=False),
         sg.Input('', size=(40, 1), key='STERMS'),
         sg.DropDown(('body', 'tags', 'title', 'all'), default_value='body', key='STARG'),
         sg.Button('GO', key='SEARCH'), sg.Push()]
    ]
    frame_col1 = [
        [sg.Frame('Tree menu', col1, pad=(5, 5),expand_y=True)]#,
        #[sg.Image(filename=mascot, pad=(5, 5), visible=False), sg.Push()]
    ]
    frame_col2 = [
        [sg.Frame('Entry View', col2, pad=(5, 5))],
        [sg.Push(), sg.Frame('', tag_frame, vertical_alignment='top', visible=False), sg.Push()],
        [sg.Push(), sg.Frame('Functions', func_frame), sg.Push()],
        [sg.Push(), sg.Frame('Search Entries', search_frame, element_justification='center'), sg.Push()],
        [sg.Push(), sg.Frame('Switch Database', dbchoose_layout),
         sg.Text('Show Output', key="ShowOutput", enable_events=True, visible=False), sg.Push()]
    ]

    col0 = [
        [sg.Column(frame_col1, vertical_alignment='top', expand_x=True, expand_y=True),
         sg.Column(frame_col2, vertical_alignment='top', expand_x=True, expand_y=True)]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU_BAR-')],
        [sg.Column(col0, vertical_alignment='top', expand_x=False, expand_y=True, scrollable=False, key='COLMAIN')],
        [sg.Push(),sg.Text(status_bar, key='sbar'),sg.Push()]

    ]

    window = sg.Window(windowTitle, layout, icon=icon_img, size=mainWindowSize, modal=False, location=win_location,
                       resizable=True, finalize=True)
    mline: sg.Multiline = window['VIEW']
    window['_TREE_'].bind("<ButtonRelease-1>", ' SelectTreeItem')
    window['STERMS'].bind("<Return>", "_Enter")
    window.bind('<F1>', 'HowTo')
    window.bind('<F2>', 'Program Settings')
    window.bind('<F3>', 'Set User Password')
    window.bind('<F4>', 'Insert Date/Time')
    window.bind('<F5>', 'UpdateEntry')
    window.bind('<F6>', 'Make New Database')
    window.bind('<F8>', 'New Entry Window')
    window.bind('<F9>', 'Database Maintenance')
    window.bind('<F11>', 'ReloadTreeData')
    window.bind('<F12>', 'Exit')
    window.bind('<F7>', 'DEBUG')


    while True:
        event, values = window.read()
        print(event, values, flush=True)
        match event:
            case sg.WIN_CLOSED | 'quit' | 'Exit':
                break
            case 'ReloadTree':
                window['_TREE_'].update(load_tree_data())
            case 'DEBUG' | 'Debug':  # experimental
                sg.EasyPrint(echo_stdout=True, blocking=False, do_not_reroute_stdout=False, text_color='Blue')
            case 'Select All':
                mline.Widget.selection_clear()
                mline.Widget.tag_add('sel', '1.0', 'end')
            case 'Copy':
                try:
                    text = mline.Widget.selection_get()
                    window.TKroot.clipboard_clear()
                    window.TKroot.clipboard_append(text)
                except:
                    print('Nothing selected')
            case 'Paste':
                mline.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
            case 'ReloadTreeData':
                window['_TREE_'].update(load_tree_data())
                window.refresh()
            case 'Change User Password':
                change_user_password()
                window.refresh()
            case 'HowTo':
                show_howto()
                window.refresh()
            case 'Reload':
                window.close()
                restart()
            case 'Insert Date/Time' | 'Insert Date/Time - (F4)':
                date_time = dt.datetime.now().strftime('%m.%d.%y -%H%M-')
                text = window['VIEW']
                text.update(text.get() + '\n\n' + date_time)
            case 'Database Maintenance':
                database_maintenance()
                window['DBNAME'].update(values=reload_dblist(), size=(30, 10))
                window.Refresh()
                # window.close()
                # restart()
            case 'Restore Entry(unhide)':
                get_hidden_entries('restore')
                window['_TREE_'].update(load_tree_data())
            case 'SEARCH':
                # print(event,values)
                search_results(values, 'search')
                window['_TREE_'].update(load_tree_data())
            case 'STERMS_Enter':
                search_results(values, 'search')
                window['_TREE_'].update(load_tree_data())
            case 'Make New Database' | 'Make New Database - (F6)':
                dbsetup.new_db_window()
                window['DBNAME'].update(values=reload_dblist(), size=(30, 10))
                window.refresh()
                # window.close()
                # restart()
            case 'Set User Password':
                new_user_window()
            case 'Program Settings':
                settings_window()
                window.close()
                restart()
            case 'ReadMe':
                show_readme()
            case 'New Entry Window' | 'New Entry Window - (F8)':
                new_entry_window()
                window['_TREE_'].update(load_tree_data())
                #window.refresh()
            case '_TREE_ SelectTreeItem':
                window.refresh()
                print(f"Stepped Inside SelectTreeItem (IF) event: {event} values: {values}")
                try:
                    # print(values['_TREE_'][0], flush=True)     # that is holding the entry id
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
                    window['WARNING'].update(visible=True)
                except Exception as e:  # hiding the error from the user and moving on
                    print(f"RUNNING: module: {__name__} - {event}: probably clicked an empty portion of tree menu: {e}",
                          flush=True)
            case 'clear':                # this can be removed since it's no longer in use
                window['E_TITLE'].update('')
                window['VIEW'].update('')
            case 'DBCHANGE' | 'Change Database':
                prevdb = (dbo.database)
                try:
                    print(f"current dbo object database value: {dbo.database}")
                    dbo.close()
                    set_new_db(values['DBNAME'])
                    dbo = DBConn(values['DBNAME'])
                    print(f"New dbo database: {dbo.database}")
                    window['_TREE_'].update(load_tree_data())
                    window['VIEW'].update('')
                    window['sbar'].update(
                        f"Date: {dt.datetime.now().strftime('%Y-%m-%d')}\t Connected to Database: {dbo.database}:: \tCurrent Theme: {curr_theme}")
                    window.refresh()
                    sg.PopupOK(f"I've successfully switch to the new database: {dbo.database},",
                               auto_close=True, auto_close_duration=3)
                except Exception as e:
                    dbo.close()
                    fsize = os.path.getsize(os.path.join(os.getcwd(),values['DBNAME']))
                    if fsize == 0:
                        sg.PopupError(f"ERROR_[DBC1] The requested database file {values['DBNAME']} has {fsize} bytes. Most likely\n"
                                      f"this database file has been damaged in some way. Please restore from backups...\n"
                                      f"Returning to the previous database...")
                        dbmoves.damaged_db(values['DBNAME'])
                    else:
                        sg.PopupError(f"ERROR_[DBC2] I have experienced an error switching database to {values['DBNAME']}: {e}\n"
                                  f"I'm returning you to the previous database until this problem can be corrected...")
                        dbmoves.damaged_db(values['DBNAME'])
                finally:
                    set_new_db(prevdb)
                    dbo = DBConn(prevdb)
                    print(f"going back to database: {dbo.database}")
                    window['_TREE_'].update(load_tree_data())
                    window['VIEW'].update('')
                    window['sbar'].update(
                        f"Date: {dt.datetime.now().strftime('%Y-%m-%d')}\t Connected to Database: {dbo.database}:: \tCurrent Theme: {curr_theme}")
                    window['DBNAME'].update(values=reload_dblist(), size=(30, 10))
                    window.refresh()
            case 'UpdateEntry':
                # currid = values['_TREE_'][0]
                print("just entered the if event statement for the update_entry()")
                print(f"Stepped Inside UpdateEntry (IF) event: {event} values: {values}")
                if not values['_TREE_']:
                    sg.PopupError('!!!ERROR!!!',
                                  f"I didn't receive a value for the Entry ID.  Perhaps you forgot to select an entry "
                                  f"before clicking the Update Entry button. \nPlease try again...", location=popup_location)
                    continue
                the_update = update_entry_window(values['_TREE_'][0])
                if not the_update:
                    continue
                else:
                    the_update = the_update.replace('&dbqup', '\"')
                    the_update = the_update.replace('&sngquo', '\'')
                    window['_TREE_'].update(load_tree_data())
                    window['VIEW'].update(the_update)
                    sg.Popup('Update Processed', "I've successfully processed your update request.\n"
                                                 "this message will self-distruct in 2 seconds...", auto_close=True,
                             auto_close_duration=1, location=popup_location, icon=icon_img)
                    print("back from the update_entry() function...", flush=True)
                window.refresh()
            case 'DelEntry' | 'Remove Entry(hide)':
                try:
                    delete_entry(values['_TREE_'][0])
                except Exception as e:
                    sg.PopupError('REMOVE ENTRY ERROR!',
                                  f"It appears that you didn't select an entry to be removed first "
                                  f"before sending your request to me. Please try again and this time "
                                  f"select and load an entry to be removed\n{e}.", location=popup_location, icon=icon_img)
            case 'About':
                show_about()
            case x:
                print(f"unknown event: {x}")
            # print(event,values)
    dbo.close()
    window.close()


if __name__ == '__main__':
    # SplashScreen.main()
    # init_logs()
    # if is_first_run():
    #     init_setup()
    #     restart()
    # check sec file to see if we're using credentials to start program
    if check_security():
        start_window()
    else:
        main()