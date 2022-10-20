#!/usr/bin/python3
import os
from os.path import exists
from pathlib import Path
import sys
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))
import datetime as dt
import logging
import sqlite3
import io
import time


def dbbu_runcheck():
    from os.path import exists
    whereami = os.getcwd()
    try:
        path = f'{whereami}/backups'
        files = os.listdir(path)
        filelist = {}
        for f in files:
            filelist[f] = os.stat(f'{path}/{f}').st_mtime
        #print(filelist)
        os.chdir(f'{path}')
        """
            in the following for look k == the log file name and v it's age in seconds.
            what we're doing here is converting that age in seconds to days. Once that is found
            we're going to move anything older than 7 days off to a subfolder of logs to oldlogs
        """
        for k, v in reversed(filelist.items()):
            age = round((time.time() - v))
            days = round(age / 86400)       # 7 days
            print(f"age of {k} is {days} days old", flush=True)
            print(days, flush=True)
            filelist[k] = days

        if not exists(path):
            os.makedirs(path)
        else:
            for filename, age in filelist.items():
                if age > 7:
                    logging.info(f"PROCESSING: module:setting.dbbu_runcheck() removing {filename} which is {age} days old to {path}")
                    os.remove(f'{path}/{filename}')
                else:
                    logging.info(f"PROCESSING: module:setting.dbbu_runcheck() - no backups have aged out. nothing to remove...")
                    print("PROCESSING: module:setting.dbbu_runcheck() - no backups have aged out. nothing to remove...",flush=True)
        os.chdir('../')
    except Exception as e:
        logging.error(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups {e}", exc_info=True)
    finally:
        print(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups. Check log for more information",flush=True)

def make_backup(path, db):
    for d in db:
        try:
            date = f"{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}" # 2022-10-14_18:44
            print(f"date value: {date}")
            #db = d.replace('\n', '')
            filename = f"{path}/{d}_{date}.sql"
            print(f"file name: {filename}")
            conn = sqlite3.connect(d)
            # Open() function
            with io.open(filename, 'w') as p:
                # iterdump() function
                for line in conn.iterdump():
                    #print('%s\n' % line)
                    p.write('%s\n' % line)
            conn.close()
            print(f"Saving {filename} to {path}/{filename}")
            logging.info(f"RUNNING: module: dbbackups.py - Saving {filename} to {path}/{filename}")
        except Exception as e:
            logging.error(f"RUNNING: module: dbbackups.py - I've run into an error {e}", exc_info=True)
        finally:
            logging.info(f"I've finished backing up the database files. Databases backed are are {db}")



#############################################################
# step #1: read in the list of databases from the dblist file
dlist = []                          # sending a list of database files
dblistfile = os.getcwd() + '/dblist'
with open(dblistfile, 'r') as f:
    dlist = list(f.read().split(','))

#############################################################
# step #2: set the path where we're storing the database backups
here = os.getcwd()
path = f'{here}/backups'  # by default this is going to be where this script is running from
if not exists(path):
    os.mkdir(path)

#############################################################
# step #3: Send the path and dlist off to the function for processing
dbbu_runcheck()
make_backup(path, dlist)