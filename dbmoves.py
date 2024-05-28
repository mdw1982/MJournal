import os.path
import shutil as sh
import time
from os.path import exists
import datetime as dt
import FreeSimpleGUI as sg
from settings import detect_os
import os


def damaged_db(db: str):
    try:
        src = os.path.join(os.getcwd(), db)
        dest = os.path.relpath('damageddb')
        #sh.move(src, dest)
        os.remove()
    except Exception as e:
        print(f"[damaged_db]:[ERROR_DBD1] Something unexpected happened while trying to deal with the damanged database: {e}")
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