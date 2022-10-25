import os
import json
from os.path import exists


def detect_os():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "win32":
        return 'windows'

def read_dblist():
    def load_dblist():
        '''possible replacement for read_dblist'''
        if detect_os() == 'Linux':
            dlistjson = os.getcwd() + "/" + 'dblist.json'
        if detect_os() == 'windows':
            dlistjson = os.getcwd() + "\\" + 'dblist.json'
        dblist = []
        temp = os.listdir(os.getcwd())
        for f in temp:
            if f.endswith('.db'):
                dblist.append(f)
        dblist = sorted(dblist, reverse=False)
        #print(dblist)

        # creating/loading the dblist json file
        with open(dlistjson, 'w') as dj:
            temp = {}
            i = 0
            for d in dblist:
                temp[i] = d
                i += 1
            dblist = json.dumps(temp, indent=len(temp))
            dj.write(dblist)

    def get_dblist():
        if detect_os() == 'Linux':
            dlistjson = os.getcwd() + "/" + 'dblist.json'
        if detect_os() == 'windows':
            dlistjson = os.getcwd() + "\\" + 'dblist.json'

        if exists(dlistjson):
            with open(dlistjson, 'r') as d:
                dlist = json.load(d)

            thedblist = []
            for k, v in dlist.items():
                thedblist.append(v)
            #print(thedblist)
            return thedblist
        load_dblist()

    def read_db_ondisk():
        dblist = []
        temp = os.listdir(os.getcwd())
        for f in temp:
            if f.endswith('.db'):
                dblist.append(f)
        dblist = sorted(dblist, reverse=False)
        return dblist

    if get_dblist() != read_db_ondisk():
        get_dblist()
    return get_dblist()

print(read_dblist())