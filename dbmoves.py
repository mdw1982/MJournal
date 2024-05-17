import os.path
import shutil as sh
from os.path import exists
import datetime as dt
import FreeSimpleGUI as sg
from settings import detect_os

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