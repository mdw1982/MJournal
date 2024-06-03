import os
from os.path import exists
from settings import detect_os
import subprocess
import FreeSimpleGUI as sg

def make_launcher(prog: str, dest: str):
    '''
    :param prog: str - name pf the program for the launcher
    :param dest: str - path where the launcher is going to be created.
    :return: None: it creates a launcher either on the desktop or (in the case of Ubuntu Unity DT it creates and stores
                   the launcher in /usr/share/applications which requires elevated privileges.
    '''
    ################################################################################################
    ## do we want to make the shortcut for the program available system wide or local? Since this
    ## is a one user program the answer may seem obvious, however, for convenience sake we "could"
    ## create a launcher that is available system wide such as on the main menu or app launcher Ubuntu style...
    ## now we're getting into multiple user territory. By that I mean the setup would have to be configured
    ## in a manner to accomodate a new instance for any user wishing to use the program on a single
    ## system... I'm not inclined to go that route just yet. Let each user download and create their own
    ## local instance. So, it's launcher on the desktop for each user using the program from an install
    ## instance of their own.
    #################################################################################################
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

        # we'er going to use the information below
        launcher = f'''
        [Desktop Entry]
        Comment[en_US]=
        Comment=
        Exec={os.path.join(dest, prog)}
        GenericName[en_US]=
        GenericName=
        Icon={os.path.join(dest, 'images/MjournalIcon_80x80.png')}
        MimeType=
        Name[en_US]=Mjournal
        Name=Mjournal
        Path={dest}
        StartupNotify=true
        Terminal=false
        TerminalOptions=
        Type=Application
        X-KDE-SubstituteUID=false
        X-KDE-Username='''

        with open(path, 'w') as l:
            l.write(launcher)
        os.chmod(path, 0o775)

    if OS == 'windows':
        try:
            subprocess.Popen("powershell.exe Shortcut.ps1")
        except Exception as e:
            sg.PopupError(f"There was a problem making the program's shortcut: {e}")

if __name__ == '__main__':
    make_launcher()