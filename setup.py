import base64
import subprocess
import os
import sys
from shutil import move
from os.path import exists
import PySimpleGUI as sg
import time
from dbsetup import init_setup
from settings import base64_image
import datetime as dt
#from main import __version__

def get_year():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    return y

default_values = {
    'name': 'MJournal',
    'version': '0.9.8.3',
    'copyright': get_year(),
    'url': 'http://projects.mdw1982.com/category/mjournal/',
    'license': 'GnuPL',
    'author': 'Mark Weaver',
    'author_email': 'mdw1982@gmail.com',
    'description': 'A Simple Database driven daily Journal program',
    'database': 'journal.db'
}

def start(p):
    try:
        return subprocess.Popen([os.getcwd() + '\\' + p], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        sg.Popup(f"I was unable to start the program because: {e}")

# some variables go here for the main window
windowTitle = f"MJournal Setup -- {default_values['version']}"
# -- give the path to the 36x36 image for the window icon
icon = base64_image('images/MjournalIcon_36x36.png')
# this is a tuple value x - number of colums y = number of rows. this depends a lot on the size of the
# multiline text box
# ------------------
# overall size of the window containing the elements. tuple value denotes x and y values
wsize = (690, 470)
# another tuple value x and y, determines where on the screen the main window will appear.
location = (760, 270)
sg.theme('Python')

def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'

def sleep():
    return time.sleep(.7)

def make_launcher():
    '''
    we have to accomplish a few things here.
    1.  we have to detect the operating system where we find ourselves. Regardless of
        the OS the program has been downloaded into the Downloads folder. where they've put
        the program folder is irrelevant. where ever they store the program folder when they
        run the setup file is where the launcher will map to.
    2.  we're going to make a launcher for the program binary.
    :return:
    '''
    OS = detect_os()
    print(OS)
    if OS == 'Linux':
        filename = 'Mjournal.desktop'
        from pathlib import Path
        home = str(Path.home())
        name = 'MJournal'
        path = f"{home}/Desktop/{filename}"
        if exists(path):
            filename = 'Mjournal_1.desktop'
            path = f"{home}/Desktop/{filename}"
        whereami = os.getcwd()
        # we'er going to use the information below
        launcher = f'''[Desktop Entry]
                        Comment[en_US]=
                        Comment=
                        Exec={whereami}/MJournal
                        GenericName[en_US]=
                        GenericName=
                        Icon={whereami}/Mjournal/images/MjournalIcon_80x80.png
                        MimeType=
                        Name[en_US]=MJournal
                        Name={name}
                        Path={whereami}/Mjournal
                        WorkingDirectory={whereami}
                        StartupNotify=true
                        Terminal=false
                        TerminalOptions=
                        Type=Application
                        X-DBUS-ServiceName=
                        X-DBUS-StartupType=
                        X-KDE-SubstituteUID=false
                        X-KDE-Username='''
        with open(path, 'w') as l:
            l.write(launcher)
        os.chmod(path, 0x755)

    if OS == 'windows':
        sg.Popup('No Shortcut Created', "You'll need to create the shortcut on your desktop to the Mjournal"
                                        "program manually.")


def check(f):
    curdir = os.getcwd()
    if f == 'cdb':
        f = os.path.relpath(f)
        with open(f,'r') as file:
            contents = file.read()
            # changed: 5.3.24 seems to make things a little clearer
        if 'journal.db' not in contents:
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('journal.db')
            sleep()
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            sleep()
            print('File Check', f"The file {f} is good to go.")
    if f == 'creds':
        f = os.path.relpath(f)
        with open(f,'r') as file:
            contents = file.read()
        if contents != '0':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('0')
            sleep()
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            sleep()
            print('File Check', f"The file {f} is good to go.")
    if f == 'dblist':
        #f = curdir + '/' + f
        f = os.path.relpath(f)
        with open(f,'r') as file:
            contents = file.read()
        #if contents != 'dummy.db,' or contents != 'dummy.db\n':
        # changed: 5.3.24 seems to make things a little clearer
        if 'journal.db' not in contents:
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('journal.db')
            sleep()
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            sleep()
            print('File Check', f"The file {f} is good to go.")
    if f == 'firstrun':
        #f = curdir + '/' + f
        f = os.path.relpath(f)
        with open(f,'r') as file:
            contents = file.read()
        if contents != 'True':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('True')
            sleep()
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            sleep()
            print('File Check', f"The file {f} is good to go.")


def do_the_work():
    '''
        Placing all the stuff that _was_ living in main() up here so that I can create a GUI to run while
        things are being setup. That should improve the user experience. I recently ran the install on my windows
        machine and wasn't sure where in the install it was till suddenly the popup at the end displayed on the screen,
        Not a good look. It's about time too.
        3.21.24: seems like forever since I've laid down the code for a GUI...
    :return:
    '''
    print('getting ready to get things setup!')
    here = os.getcwd()

    print('Step #1: Checking dependencies files exists and contain correct information')
    filelist = ['cdb', 'creds', 'dblist', 'firstrun', 'ldb_config.json']
    files = os.listdir(os.path.relpath(here))
    for file in filelist:
        print(file)
        sleep()
        if file in files:
            print(f'file {file} exists. Checking contents...')
            check(file)
        if file not in files:
            # create the file as long as it's 'cdb', 'creds', 'dblist', 'firstrun'
            sleep()
            print(f"file {file} not found... correcting")
            if file in ['cdb', 'creds', 'dblist', 'firstrun']:
                with open(file, 'w') as x:
                    x.write('0')
                print(f"Created missing file {file}... adding correct values")
                check(file)

    '''step #3
        create the new default database, run make_launcher() and launch the program
    '''
    init_setup()
    print("SETUP COMPLETE! I'm going to make a launcher on your desktop, then launch the program!")
    print("ENJOY!! When the program starts the first time it will create your default database\n"
          "then automatically restart.")
    sleep()
    '''
        Originally making the launcher. i.e. program shortcut was attempting to be done here. On linux
        one of the attributs of the shortcut needs to be the working directory. If you're running KDE and 
        you manually create a shortcut one the fields filled in is for WorkingDirectory, however attempting to 
        this programatically isn't working. Could be I don't have the attribute right or there's a different
        problem I'm not yet aware of. So, for now 3.23.24 1336 I've decided to take this part out and 
        concentrate on the order of events during the actual setup. Meaning getting the order of windows
        being presented to the user as setup progresses.
    '''
    # try:
    #     print("attempting to create the program launcher on your desktop")
    #     make_launcher()
    #     print("launcher creation successful")
    # except Exception as e:
    #     print(f"something went wrong creating your launcher... \nyou'll have to do it manually: {e}\n"
    #           f"everything else went fine...")
    # finally:
    #     time.sleep(1.5)
    #     if detect_os() == 'Linux':
    #         program = os.getcwd() + '/MJournal'
    #     if detect_os() == 'windows':
    #         program = os.getcwd() + '/MJournal.exe'
    #     os.system(program)  # launching program for the first time.

def init_msg():
    msg = '''Thank you for choosing the MJournal Program. I hope your experience with the program is a good one.'''
    print(msg)

def display_msg():
    print('You are about to install the MJournal Program on your system. If you wish to continue press Install, otherwise hit Cancel.')

def main():
    multiline = sg.Output(key='OUTPUT',size=(89, 20), pad=(5, 5),wrap_lines=True,background_color='black',text_color='white')
    progressbar = sg.ProgressBar(100,orientation='h',key='progress',size=(140,20))
    sgPopupLoc = (1160, 470)
    sgPopUpSize = (199,100)
    # layouts go here
    layout = [
        [multiline],
        [sg.Button('Install->>', key='Go', visible=False, button_color='green'),
         sg.Button('Continue->>', key='Next', visible=True, button_color='green'),
         sg.Button('Cancel',key='quit', button_color='black')],
        [progressbar]
    ]

    Out_window = sg.Window(windowTitle, layout, icon=icon, size=wsize, modal=False, location=location,
                       resizable=True, finalize=True)

    '''in order to get this to work with the setup GUI once we're actually doing the work you have to comment out
        the printer statement below in the for loop'''
    def pbar() -> int:
        i = 0
        for i in range(0, 99):
            # comment out the print statement below to use with live setup program
            #print(i)
            Out_window['progress'].update(i)
            time.sleep(.005)

    while True:
        event, values = Out_window.read(multiline.update(init_msg()))

        match event:
            case sg.WIN_CLOSED | 'quit' | 'Exit':
                sg.Popup('Leaving so Soon?',"Maybe Next Time\nSee you later.\n\n", auto_close=True, auto_close_duration=10,location=sgPopupLoc)
                break
            case 'Go':
                try:
                    Out_window['OUTPUT'].update('')
                    pbar()
                    do_the_work()
                    sg.Popup('Setup Complete', button_type=0, location=sgPopupLoc)
                    program = 'MJournal.exe'
                    start(program)  # launching program for the first time.
                except Exception as e:
                    sg.Popup(f"RUNNING: module: setup on line 272: {e}")
                break
            case 'Next':
                Out_window['OUTPUT'].update('')
                display_msg()
                Out_window['Next'].update(visible=False)
                Out_window['Go'].update(visible=True)
            case x:
                break
    Out_window.close()


if __name__ == '__main__':
    main()