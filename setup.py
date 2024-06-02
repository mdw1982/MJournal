import base64
import json
import subprocess
import os
import sys
import shutil as sh
from os.path import exists
import FreeSimpleGUI as sg
import time
from dbsetup import init_setup
from settings import base64_image
import datetime as dt
from pathlib import Path
from launcher import make_launcher


def get_year():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    return y


def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'



def_src = os.getcwd()
with open(os.path.join(def_src, 'defaults.json'), 'r') as dfs:
    default_values = json.load(dfs)


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

def start(p: str, path: str):
    try:
        # if detect_os() == 'windows':
        #     return subprocess.Popen([path + '\\' + p], creationflags=subprocess.CREATE_NO_WINDOW)
        # if detect_os() == 'Linmux':
        #     return subprocess.Popen([path + '/' + p])
        return subprocess.Popen([os.path.join(path,  p)])
    except Exception as e:
        sg.Popup(f"I was unable to start the program because: {e}")


def sleep():
    return time.sleep(.05)


def init_msg():
    msg = '''Thank you for choosing the MJournal Program. I hope your experience with the program is a good one.'''
    print(msg)


def display_msg():
    print('You are about to install the MJournal Program on your system. If you wish to continue press Install, otherwise hit Cancel.')



def main():
    def get_prog_home():
        if detect_os() == 'windows':
            return default_values['Wprog_dir']
        if detect_os() == 'Linux':
            return default_values['Lprog_dir']

    def check_destination():
        if not exists(destination):
            print(f"Creating Destination directory: {destination}")
            os.mkdir(destination)

    def new_install():
        # 1. list of everything in packages
        try:
            flist = os.listdir(os.getcwd())
            print(f":::FLIST CONTAINS::: created the file list to be copied: {flist}")
            check_destination()
            print(f"successfully created the program directory here: {destination}")
            print(f"Install destination is {destination}")
            print(f"::::DESTINATION::: {destination}")
            cnt = 2
            for file in flist:
                fle = os.path.join(os.getcwd(), file)
                if os.path.isdir(file):
                    cnt += 3.5
                    dst = os.path.join(destination,file)
                    print(f"copying directory {file} to {destination}")
                    sh.copytree(fle, dst)
                    Out_window['progress'].update(cnt)
                    sleep()
                if os.path.isfile(file):
                    cnt += 3.5
                    dst = os.path.join(destination, file)
                    print(f"copying file {file} to {destination}")
                    sh.copy(file, dst)
                    Out_window['progress'].update(cnt)
                    sleep()
        except sh.Error as e:
            sg.PopupError(f"::::Install Error Copying Files. {e}")


    msg = ("To run this setup in Sandbox Mode enter 'S' in the text field and click OK. If you want\n"
           "to run setup in Live mode enter 'L' in the text field and click OK. The default value\n"
           "is 'L' for Live Mode. Running in SandboxMode will setup everything in your Downloads folder.\n"
           "Running Setup in Sandbox Mode will not create a program shortcut. You'll have to do that manually.\n"
           "Hit the TAB key to enter the input field:")

    mode = sg.PopupGetText(msg,'Choose Setup Type: Sandbox or Live', default_text='L', size=(5,1),location=location)
    mode = mode.capitalize()

    user_home = str(Path.home())
    #destination = os.path.join(user_home, prog_home)
    match mode:
        case 'S':
            # running in sandbox mode
            sg.Popup("Running In Sandbox Mode... this will install the program to your Doanloads folder", auto_close=True,auto_close_duration=3,location=location)
            sandbox = os.path.join(str(Path.home()),'Downloads')
            destination = os.path.join(sandbox,get_prog_home())
        case 'L':
            # running live setup
            sg.Popup("Running in Live mode. This will install the program to your home directory.", auto_close=True,auto_close_duration=3,location=location)
            destination = os.path.join(user_home,get_prog_home())
        case x:
            sg.PopupError(f"Setup cannot continue... you've entered and unknown argument: {mode}."
                          f"You must enther either an 'S' for sandbox mode, or 'L' for a live setup."
                          f"The setup program will end now. Please try again with the correct input.",location=location)
            exit(1)



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

    while True:
        event, values = Out_window.read(multiline.update(init_msg()))

        match event:
            case sg.WIN_CLOSED | 'quit' | 'Exit':
                sg.Popup('Leaving so Soon?',"Maybe Next Time\nSee you later.\n\n", auto_close=True, auto_close_duration=10,location=sgPopupLoc)
                break
            case 'Go':
                try:
                    Out_window['OUTPUT'].update('')
                    Out_window['progress'].update(2)
                    # set journal.db as the default for first run
                    default_values['dbname'] = 'journal.db'
                    with open('defaults.json', 'w') as defs:
                        json.dump(default_values,defs, indent=4)
                    print('going to file copy...')
                    # create new Journal database journal.db
                    init_setup()
                    new_install()
                    # make the launcher
                    make_launcher()
                    sg.Popup('Setup Complete', button_type=0, location=sgPopupLoc)
                    if detect_os() == 'windows':
                        program = 'MJournal.exe'
                    if detect_os() == 'Linux':
                        program = 'MJournal'
                    start(program,destination)  # launching program for the first time.
                except Exception as e:
                    sg.Popup(f"Something happened:\n {e}")
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