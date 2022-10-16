#!/usr/bin/python3
from pathlib import Path
import sys
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))
import datetime as dt
import logging
import sqlite3
import io
import subprocess
from settings import init_logs


def make_backup(path, db):
    for d in db:
        try:
            date = f"{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}" # 2022-10-14_18:44
            print(f"date value: {date}")
            db = d.replace('\n', '')
            filename = f"{path}/{db}_{date}.sql"
            print(f"file name: {filename}")
            conn = sqlite3.connect(db)
            # Open() function
            with io.open(filename, 'w') as p:
                # iterdump() function
                for line in conn.iterdump():
                    print('%s\n' % line)
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
with open('dblist', 'r') as list:
    for line in list.readlines():
        line = line.replace('\n', '')
        #print(line)
        dlist.append(line)

#############################################################
# step #2: set the path where we're storing the database backups
path = subprocess.getoutput('pwd')  # by default this is going to be where this script is running from

#############################################################
# step #3: Send the path and dlist off to the function for processing
make_backup(path, dlist)
