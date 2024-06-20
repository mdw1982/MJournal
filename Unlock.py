import os
import sys
import sqlite3 as sl
import datetime as dt
import FreeSimpleGUI as sg
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.
#import SplashScreen         # I have you turned off for now so quite yer bitchin
import dbsetup
from dbsetup import *
from settings import read_dblist
from classes.DBConn import DBConn
# I'm not at all sure I'm going to continue using DBConn at this time
# given the fact that it's being squirrly and not giving me the data I know
# is there.
####################################################
#     conn = sl.connect(database)
#     c = conn.cursor()
#     c.execute("select id from entries where visible=0")
#     results = convert_tuple(c.fetchall()) (the results always come back as tuples...
#     c.close()                              if you need things in a list you must
#                                            de-tuple them with convert_tuple() )
'''
    This is a standalone program. It has one job and that is to unlock the program if/when 
    the user forgets their password and is unable to get into the program. It is not run
    from within the program but outside and apart from the main program.
    ===================================================================================
    Its job is:
    1.  Once started by the user it will display a simple UI. 
    2.  it will present the recommended choice which is to edit two database tables
        1.  Modify the settings table and set field pwsec value to 0
        2.  Delete the simgle user entry in user table
        Once this is complete the user should start the program to confirm they are able
        to access the database via the MJournal program.
    3.  THE NUCLEAR OOPTION
        1. Remove and recreate the user and settings table
    WHAT THE SCREEN SHOULD SHOW
    1.  The left column screen.
        1.  the left column should present an input field for the user's user name. this will be used
            query the database user table for the entry with the username and delete it.
        2.  set the pwsec field in the settings table to 0 which indicates to the program no 
            security is turned on.
    2.  Each column on the screen should have its own submit button the trigger the event that will initial
        the changes.
    
'''
######################################################################################
# program global variables
######################################################################################
winloc = (660, 340)  # location the window will appear on the screen
                    # this is done because on Linux with more than one screen
                    # the window tends to go right to the very center and appears
                    # on both screens.
winsize = (375, 275)
def unset_pwsec(db):
    dbo = DBConn(db)
    print(f"received database {db}")
    result = dbo.unlock('update settings set pwsec=0')
    return result


def main():
    dblist = read_dblist() # get a list of databases to presemt to screem
    print(dblist)
    layout = [
        [sg.Push(),sg.OptionMenu(dblist,default_value='choose database to unlock',size=(40,10),key='DBUL',pad=(30,30))],
        [sg.Push(),sg.Text('',key='output',background_color='black',text_color='white',visible=False,size=(50,5))],
        [sg.Push(),sg.Button('Unlock',key='-GO-'),sg.Button('Cancel',key='quit'),
         sg.Button('Close',key='-QUIT-',visible=False)],
        [sg.Push(),sg.Text("Unlocking a database will perform two functions:\n"
                           "1. it will turn off security...\n"
                           "2. it will remove the username and password record \n"
                           "set in the user table. If you wish to re-enable \n"
                           "security you'll have to create a new username/password \n"
                           "for the database after unlocking. Then, you can \n"
                           "turn security on again...", pad=(10,10)),sg.Push()]
    ]

    window = sg.Window('Unlock Database Utility', layout, size=winsize, modal=False, location=winloc,
                       resizable=True, finalize=True)

    while True:
        event, values = window.read()
        print(event,values)
        match event:
            case sg.WIN_CLOSED | 'quit' | '-QUIT-':
                break
            case '-GO-':
                dbo = DBConn(values['DBUL'])
                curr_theme = get_current_theme()
                sg.theme(curr_theme[0])
                dbo.close()
                # 1. access the settings table and set pwsec to 0
                message = unset_pwsec(values['DBUL'])
                # 2. make visible button to close - make invisible buttons for Unlock and Cancel
                window['-GO-'].update(visible=False)
                window['quit'].update(visible=False)
                # 3. show message on screen of success or failure of operation
                window['output'].update(message,visible=True)
                window['-QUIT-'].update(visible=True)
                print(event)
                dbo.close()
            case x:
                print('Unknown event... leaving program')
                break
    window.close()



if __name__ == '__main__':
    main()