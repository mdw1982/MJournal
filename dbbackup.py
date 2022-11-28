#!/usr/bin/python3
import os
from os.path import exists
from pathlib import Path
import sys
import datetime as dt
import sqlite3
import io
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# imports from local modules go below here.



def dbbu_runcheck():
    from os.path import exists
    try:
        path = os.path.join(os.getcwd(),'backups')
        files = os.listdir(path)
        filelist = {}
        for f in files:
            filelist[f] = os.stat(os.path.join(path,f)).st_mtime
        #print(filelist)
        os.chdir(path)
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
                    #logging.info(f"PROCESSING: module:setting.dbbu_runcheck() removing {filename} which is {age} days old to {path}")
                    os.remove(os.path.join(path,filename))
                    print(f"{filename} was aged {age} days and was removed.")
                else:
                    print(f"{filename} aged {age} days was not removed.")
        os.chdir('../')
    except Exception as e:
        print(f"RUNNING: module: {__file__}.dbbu_runcheck() - unable to process database backups {e}")
        #logging.error(f"RUNNING: module: setting.dbbu_runcheck() - unable to process database backups {e}", exc_info=True)
    finally:
        print(f"RUNNING: module: {__file__}.dbbu_runcheck() - runcheck completed successfully",flush=True)

def make_backup(path, db):
    for d in db:
        try:
            date = f"{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}" # 2022-10-14_18:44
            print(f"date value: {date}")
            #db = d.replace('\n', '')
            filename = f"{d}_{date}.sql"
            dest = os.path.join(path,filename)
            print(f"file name: {filename}")
            conn = sqlite3.connect(d)
            # Open() function
            with io.open(dest, 'w') as p:
                # iterdump() function
                for line in conn.iterdump():
                    #print('%s\n' % line)
                    p.write('%s\n' % line)
            conn.close()
            print(f"Saving {filename} to {dest}")
            #logging.info(f"RUNNING: module: dbbackups.py - Saving {filename} to {dest}")
        except Exception as e:
            print(f"RUNNING: module: dbbackups.py - I've run into an error {e}")
            #logging.error(f"RUNNING: module: dbbackups.py - I've run into an error {e}", exc_info=True)
        finally:
            print(f"I've finished backing up the database files. Databases backed are are {db}")
            #logging.info(f"I've finished backing up the database files. Databases backed are are {db}")



#############################################################
# step #1: read in the list of databases from the dblist file
dlist = []                          # sending a list of database files
# rather than reading the dblist file for active database we're going to crab and
# backup all databases currently residing in the program directory. this method is
# cleaner and we make sure to get everything. Just because its not current active
# doesn't mean it's not important.
temp = os.listdir(os.getcwd())
for f in temp:
    if f.endswith('.db'):
        dlist.append(f)

#############################################################
# step #2: set the path where we're storing the database backups
here = os.getcwd()
bupath = os.path.join(here,'backups')  # by default this is going to be where this script is running from
if not exists(bupath):
    os.mkdir(bupath)

#############################################################
# step #3: Send the path and dlist off to the function for processing
dbbu_runcheck()
make_backup(bupath, dlist)