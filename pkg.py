import os
import time
from os.path import exists
import sys
import shutil as sh
import json
from main import __version__

def make_filelist():
    dblist = []
    temp = os.listdir(os.getcwd())
    for f in temp:
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

#get the file list for package
filelist = []
dest = os.path.relpath('temp')
newfolder = os.path.relpath('MJournal_Linux_'+ __version__)
if not exists(dest):
    os.mkdir(dest)

with open(os.path.relpath('filelist.json'),'r') as fl:
    temp = json.load(fl)
for k,f in temp.items():
    filelist.append(f)

for file in filelist:
    time.sleep(.70)
    if os.path.isdir(os.path.relpath(file)):
        time.sleep(1)
        sh.copytree(file,dest + '/' + file)
        print(f"copying directory {file} to {dest}")
    if os.path.isfile(os.path.relpath(file)):
        print(f"copying file {file} to {dest}")
        sh.copy(file,dest)

print("finished copying files... renaming destination folder")
os.renames(os.path.relpath(dest), os.path.relpath(newfolder))