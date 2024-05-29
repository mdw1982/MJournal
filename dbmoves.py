import json
import os.path
import shutil as sh
import time
from os.path import exists
import datetime as dt
import FreeSimpleGUI as sg
from settings import detect_os
import os


def damaged_db(db: str):
    '''
    Takes in the name of a damanage database that the program is unable to load and read. This function is split
    off to a new thread to work while the main program continues to run. In most cases the damage to the db file
    is that it has been zeroed out or ccompletely empty. reason as yet unknown... Up to this point the program
    has been unable to actually MOVE the file because it's being held by some process of the program which is why
    I started using a seperate thread to mitigate that but so far it isn't working.
    :param db: Name of the damaged database sent as type str
    :return: returns a message of sucess or failure to the main program after thread finishes.
    '''
    try:
        # path to damaage database
        src = os.path.join(os.getcwd(), db)
        with open(src, 'w') as jnk:
            jnk.write('junk')

        # path to where it's going
        dest = os.path.join(os.getcwd(), 'damageddb')
        # path to the dblist.json file.. doing it this way makes things nice and clean for both Windows and Linux
        dlist = os.path.join(os.getcwd(), 'dblist.json')
        # opening the dblist.json file and reading in the contents to a temporary dict
        with open(dlist, 'r') as dl:
            tlist = json.load(dl)

        temp = {}
        for k,v in tlist.items():
            if tlist[k] == db:
                continue
            temp[k] = v

        with open(dlist, 'w') as nl:
            json.dump(temp, nl, indent=4)

        sh.move(src, dest)
        msg = f"::SUCCESS:: Damaged database {db} has been removed and dblist updated."
        return msg
    except WindowsError as e:
        print(f"[damaged_db]:[ERROR_DBD1] Something unexpected happened while trying to deal with the damanged database: {e}")
        msg = f":::FAILED::: [damaged_db]:[ERROR_DBD1] Couldn't complete of the damanged database: {e}"
        return msg
        #sg.PopupError(f"[damaged_db]:[ERROR_DBD1] Something unexpected happened while trying to move the damanged database: {e}")


def detach(dbname):
    try:
        src = os.path.join(os.getcwd(),  dbname)
        dest = os.path.relpath('olddb')
        if detect_os() == 'windows':
            epoch = dt.datetime.now().strftime('%S')
        else:
            epoch = dt.datetime.now().strftime('%s')

        print(src)
        print(dest)
        if exists(os.path.join(dest, dbname)):
            temp,ext = dbname.split('.')
            ndbname = temp+'_'+epoch+'.db'
            os.rename(dbname,ndbname)
            src = os.path.relpath(ndbname)
            sh.move(src, dest)
        else:
            sh.move(src,dest)
    except Exception as e:
        sg.PopupError(f"Something went wrong detaching the database: {dbname}\n{e}")

def attach(dbname):
    srcfldr = os.path.relpath('olddb')
    src = os.path.join(srcfldr,dbname)
    destfldr = os.path.relpath(os.getcwd())
    dest = os.path.join(destfldr,dbname)

    print(src)
    print(dest)
    sh.move(src, dest)