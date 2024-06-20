import os
import sys
import time
from os.path import exists
import shutil as sh
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.
#from main import __version__

'''
    THIS FILE REQUIRES THE HASH-BANK LINE AT THE TOP BECAUSE IT TAKES AN ARGUMENT TO RUN.
    1. ARGUMENT TO GENERATE THE FILE LIST: 'ml'
    2. ARGUMENT TO GENERATE THE PACKAGE: 'p'
    just the argument without the single quotes.
    YOU'LL NEED TO CHANGE THE BANG LINE TO SUITE YOUR SYSTEM.
    ------------------------
    I typically run this script thusly from the command line within the IDE
    ./pkg.py p
    ------------------------
    5-13-24: at some point re-write this with a gui
    1. perform preflight
        1.1 display current version in an Input field and checkbox
        1.2 text above input field should read 'leave if correct - otherwise change
        1.3 display two button: continue, end
            1.3.1 if continue... process data entered show next screen
            1.3.2 if end close program
    2. 
'''
# a few global veriables...
def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'

def load_defaults() -> dict:
    '''
    :param: None
    :return: dict
    '''
    dfs = {}
    ldf = os.path.join(os.getcwd(), 'defaults.json')
    if exists(ldf):
        with open(ldf, 'r') as d:
            dfs = json.load(d)
    return dfs


defaults = load_defaults()
defaults['dbname'] = 'dummy.db'


def nail_down_defaults(db: str, vers: str):
    dfs = load_defaults()
    dfs['dbname'] = db
    dfs['version'] = vers
    with open('defaults.json', 'w') as d:
        json.dump(dfs, d, indent=4)


def update_defaults(val: str):
    # we're updating the version field in the defaults.json file.
    defs = load_defaults()
    defs['version'] = val
    with open('defaults.json', 'w') as d:
        json.dump(defs, d, indent=4)

    print(f"finished updating defaults file with {defs}")


def load_previous():
    with open('previous.json', 'r') as p:
        pver = json.load(p)
    return pver


def check_previous(incoming):
    previous = load_previous()
    if incoming not in previous:
        # we can allow this version value to be used.
        return True


def add_to_previous(inc):
    prev = load_previous()
    keys = sorted(prev.keys(),reverse=False)
    res = sorted([eval (i) for i in keys], reverse=True)
    print(res,'\n')
    nkey = res[0] + 1
    prev[nkey] = inc
    with open('previous.json', 'w') as p:
        json.dump(prev, p, indent=4)

    print(f"added new version {prev[nkey]} to previous versions list")
    print('updating defaults with new value...')
    defaults['version'] = prev[nkey]
    print(defaults['version'])


def cleanup_dblist():
    tp = {}
    tp[0] = 'dummy.db'
    with open(os.path.relpath('dblist.json'), 'w') as d:
        json.dump(tp, d, indent=4)
    print(tp)


def clear_screen():
    os.system('clear')


def pre_flight():
    print('=========================================================\n'
          'Pre-Flight requires Input... it will ask you to confirm'
          'if the program version is correct: you can answer (yes): y\n'
          'or you can answer (no): n\n'
          'OR, you can answer with the word (end). That will terminate\n'
          'this packaging program\n'
          '=========================================================')
    print(f"MJournal Current Version: {defaults['version']}\n")
    expected_ans = ['y', 'n', 'end']
    ans = input('Before we start are you certain the program version is correct: (y/n): ')
    if ans not in expected_ans:
        print(f"I didn't understand your answer... perhaps you mis-typed it!\n"
              f"Please try again:")
        time.sleep(2)
        os.system('clear')
        pre_flight()
    else:
        match ans:
            case 'y':
                cleanup_dblist()
                nail_down_defaults('dummy.db',defaults['version'])
                return True
            case 'n':
                ask = input(f"What value shall we set for the version:? ")
                if ask != defaults['version']: # it is possible to back rev the version because
                    if check_previous(ask):
                        defaults['version'] = ask
                        add_to_previous(ask)
                        cleanup_dblist()
                        nail_down_defaults('dummy.db', defaults['version'])
                    return True
            case 'end':
                return 'end'
            case x:
                return False


def make_filelist():
    dblist = []
    # list of items not to be included in package
    # the list of items not to include that appears below may change in your environment.
    # these are the items I'm not including in the package
    noinc = ['.venv','TestConn.py','venv','dist','old','main_new.py',
             '.gitignore','.idea','olddb','build','filelist,json','.git','__pycache__',
             'json','scratch.py','_Linux_','_Win64','create_load_dblistjson.py','pkg_new.py']
    temp = os.listdir(os.getcwd())
    for f in temp:
        if f.endswith('.spec') or f in noinc:
            continue
        if f.endswith('.db') and f != 'dummy.db':
            continue
        if '_Linux_' in f:
            continue
        if '_Win64_' in f:
            continue
        if '_new'in f:
            continue
        if f.endswith('.manifest'):
            continue
        dblist.append(f)
    dblist = sorted(dblist, reverse=False)
    print(dblist)

    # creating/loading the dblist json file
    with open(os.path.relpath('filelist.json'), 'w') as dj:
        temp = {}
        i = 0
        for d in dblist:
            temp[i] = d
            i += 1
        dblist = json.dumps(temp, indent=4)
        dj.write(dblist)


def main():
    match pre_flight():
        case True:
            #get the file list for package
            '''setting the path according to OS for the package directory'''
            filelist = []
            dest = os.path.relpath('dist')
            if detect_os() == 'Linux':
                src = os.path.relpath(dest + '/' + 'src')
                if not exists(src):
                    os.mkdir(src)
                print(src)
            if detect_os() == 'windows':
                src = os.path.relpath(dest + '\\' + 'src')
                if not exists(dest + '\\' + src):
                    os.mkdir(src)
                print(src)

            if detect_os() == 'Linux':
                newfolder = os.path.relpath('MJournal_Linux_'+ defaults['version'])
            if detect_os() == 'windows':
                newfolder = os.path.relpath('MJournal_Win64_' + defaults['version'])
            if not exists(dest):
                os.mkdir(dest)

            # make the file list - this was added 3.23.24 because it was found that for some reason the file
            # ldb_config.json was wasn't being included which lead to setup problems. If you run 'pkg.py ml' from
            # from the command line first everything would be ok, but that's stupid. It should also be happening
            # in main() just in case the filelist.json doesn't exist.
            make_filelist()
            with open(os.path.realpath('filelist.json'), 'r') as fl:
                temp = json.load(fl)
            for k,f in temp.items():
                filelist.append(f)

            '''this section was refactored 3.18.24 in order to get the python src files into a separate directory
               to keep the program directory as clean as possible.'''
            if detect_os() == 'Linux':
                for file in filelist:
                    if file == 'dist':
                        continue
                    time.sleep(1.5)
                    if os.path.isdir(os.path.realpath(file)):
                        sh.copytree(file, dest + '/' + file)
                        print(f"copying directory {file} to {dest}")
                    if os.path.isfile(os.path.relpath(file)):
                        if file.endswith('.py'):
                            print(f"Source File: {file}")
                            print(f"copying file {file} to {src}")
                            sh.copy(file, src)
                            continue
                        print(f"copying file {file} to {dest}")
                        sh.copy(file, dest)
                print("finished copying files... renaming destination folder")
                os.renames(os.path.relpath(dest), os.path.relpath(newfolder))

            if detect_os() == 'windows':

                for file in filelist:
                    time.sleep(.70)
                    if os.path.isdir(os.path.realpath(file)):
                        time.sleep(1)
                        sh.copytree(file, dest + '\\' + file)
                        print(f"copying directory {file} to {dest}")
                    if os.path.isfile(os.path.relpath(file)):
                        if file.endswith('.py'):
                            print(f"Source File: {file}")
                            print(f"copying file {file} to {src}")
                            sh.copy(file, src)
                            continue
                        print(f"copying file {file} to {dest}")
                        sh.copy(file, dest)
                print("finished copying files... renaming destination folder")
                os.renames(os.path.relpath(dest), os.path.relpath(newfolder))
        case False:
            print('Pre Flight check failed... ending program...')
            exit(0)
        case 'end':
            print("You've chosen to end the program. Exiting now....")
            exit(0)
        case x:
            print("I didn't understand the input... exiting program...")
            exit(1)


if __name__ == "__main__":
    comm = sys.argv[1]
    match comm:
        case 'ml':
            make_filelist()
            exit(0)
        case 'p':
            main()
        case x:
            print('ERROR:...I need the correct argument to run. \n use \'ml\' to create file list\n use \'p\' to create the package')
            exit(1)
