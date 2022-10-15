#!/usr/bin/python3
import base64
import subprocess
import os
from dbsetup import init_setup
import settings


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


def get_splash_image():
    with open("images/SplashScreen.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return  my_string



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
    OS = settings.detect_os()
    print(OS)
    if OS == 'Linux':
        filename = 'Mjournal.desktop'
        from pathlib import Path
        home = str(Path.home())
        name = 'MJournal'
        path = f"{home}/Desktop/{filename}"
        whereami = subprocess.getoutput('pwd')
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
        os.system(f"chmod +x {path}")

    if OS == 'windows':
        import PySimpleGUI as sg
        sg.Popup('No Shortcut Created', "You'll need to create the shortcut on your desktop to the Mjournal"
                                        "program manually.")

###################################################################
# step #1:

###################################################################
# step #2:

###################################################################
# step #X: Create the program launcher
#make_launcher()