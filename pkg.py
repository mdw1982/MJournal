#!/usr/bin/python3
import os
import sys
import time
from os.path import exists
import shutil as sh
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.
from main import __version__
from settings import detect_os

def make_filelist():
    dblist = []
    # list of items not to be included in package
    noinc = ['venv','dist','old','.gitignore','.idea','logs','olddb','build','dblist,json','.git','__pycache__','json','toys.db','scratch.py']
    temp = os.listdir(os.getcwd())
    for f in temp:
        if f.endswith('.spec') or f in noinc:
            continue
        dblist.append(f)
    dblist = sorted(dblist, reverse=False)
    # print(dblist)

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
            os.mkdir(dest + 'src')
        print(src)

    if detect_os() == 'Linux':
        newfolder = os.path.relpath('MJournal_Linux_'+ __version__)
    if detect_os() == 'windows':
        newfolder = os.path.relpath('MJournal_Win64_' + __version__)
    if not exists(dest):
        os.mkdir(dest)

    # make the file list - this was added 3.23.24 because it was found that for some reason the file
    # ldb_config.json was wasn't being included which lead to setup problems. If you run 'pkg.py ml' from
    # from the command line first everything would be ok, but that's stupid. It should also be happening
    # in main() just in case the filelist.json doesn't exist.
    make_filelist()
    with open(os.path.realpath('filelist.json'),'r') as fl:
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


if __name__ == "__main__":
    comm = sys.argv[1]
    match comm:
        case 'ml':
            make_filelist()
        case 'p':
            main()
        case x:
            print('ERROR:...I need the correct argument to run. \n use \'ml\' to create file list\n use \'p\' to create the package')
            exit(1)
