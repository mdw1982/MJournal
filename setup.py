#!/usr/bin/python3
import base64
import subprocess
import os
from shutil import move
from os.path import exists
import PySimpleGUI as sg
import time

print = sg.Print

default_values = {
    'name': 'MJournal',
    'version': '0.4.7',
    'copyright': '2022',
    'url': '',
    'license': 'GnuPL',
    'author': 'Mark Weaver',
    'author_email': 'mdw1982@gmail.com',
    'description': 'A Simple Database driven daily Journal program',
    'database': 'journal.db'
}


def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'



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
        f = curdir + '/' +f
        with open(f,'r') as file:
            contents = file.read()
        if contents != 'dummy.db':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('dummy.db')
            time.sleep(1.5)
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            time.sleep(1.5)
            print('File Check', f"The file {f} is good to go.")
    if f == 'creds':
        f = curdir + '/' + f
        with open(f,'r') as file:
            contents = file.read()
        if contents != '0':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('0')
            time.sleep(1.5)
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            time.sleep(1.5)
            print('File Check', f"The file {f} is good to go.")
    if f == 'dblist':
        f = curdir + '/' + f
        with open(f,'r') as file:
            contents = file.read()
        if contents != 'dummy.db,' or contents != 'dummy.db':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('dummy.db')
            time.sleep(1.5)
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            time.sleep(1.5)
            print('File Check', f"The file {f} is good to go.")
    if f == 'firstrun':
        f = curdir + '/' + f
        with open(f,'r') as file:
            contents = file.read()
        if contents != 'True':
            # open the file and write the correct value to
            with open(f, 'w') as file:
                file.write('True')
            time.sleep(1.5)
            print('File Check', f"I've set the correct value in {f}. We're good to go.")
        else:
            time.sleep(1.5)
            print('File Check', f"The file {f} is good to go.")


def main():
    print('getting ready to get things setup!')
    '''step #1:
        copy (move) all the source files (*.py) files to src directory EXCEPT setup.py
    '''
    print('STEP #1. Moving source files to src directory')
    dest =  os.getcwd() + '/src'
    here = os.getcwd()
    for file in os.listdir("./"):
        time.sleep(.3)
        if file.endswith(".py"):
            if file == 'setup.py' or file == 'dbbackup.py':
                print(f"not moving {file}")
                continue
            move(f"{file}", f"{dest}")
            print(f"moving {file} to ./src directory")

    '''step #2:
        make sure that all dependent files are located in the program dir root
        along with the executable file. cdb creds dblist firstrun *.json *.db
    '''
    print('Step #2: Checking dependencie files exists and containt correct information', grab_anywhere=True)
    filelist = ['cdb', 'creds', 'dblist', 'firstrun','ldb_config.json']
    files = os.listdir(os.getcwd())
    for file in filelist:
        print(file)
        time.sleep(.4)
        if file in files:
            print(f'file {file} exists. Checking contents...')
            check(file)
        if file not in files:
            # create the file as long as it's 'cdb', 'creds', 'dblist', 'firstrun'
            time.sleep(.2)
            print(f"file {file} not found... correcting")
            if file in ['cdb', 'creds', 'dblist', 'firstrun']:
                with open(file, 'w') as x:
                    x.write('0')
                print(f"Created missing file {file}... adding correct values")
                check(file)

    '''step #3
        run make_launcher() and launch the program
    '''
    print("SETUP COMPLETE! I'm going to make a launch on your desktop, then launch the program!")
    print("ENJOY!! When the program starts the first time it will create your default database\n"
          "then automatically restart.")
    time.sleep(2)
    make_launcher()
    program = os.getcwd() + '/MJournal'
    os.system(program)          # launching program for the first time.



if __name__ == '__main__':
    main()