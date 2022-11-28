import os.path
import shutil as sh

def detach(dbname):
    src = os.path.relpath(dbname)
    dest = os.path.relpath('olddb')

    print(src)
    print(dest)
    sh.move(src,dest)

def attach(dbname):
    srcfldr = os.path.relpath('olddb')
    src = os.path.join(srcfldr,dbname)
    destfldr = os.path.relpath(os.getcwd())
    dest = os.path.join(destfldr,dbname)

    print(src)
    print(dest)
    sh.move(src, dest)