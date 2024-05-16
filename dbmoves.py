import os.path
import shutil as sh
from os.path import exists
import datetime as dt

def detach(dbname):
    src = os.path.relpath(dbname)
    dest = os.path.relpath('olddb')
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

def attach(dbname):
    srcfldr = os.path.relpath('olddb')
    src = os.path.join(srcfldr,dbname)
    destfldr = os.path.relpath(os.getcwd())
    dest = os.path.join(destfldr,dbname)

    print(src)
    print(dest)
    sh.move(src, dest)