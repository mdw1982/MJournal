#!/usr/bin/python3
import logging
import subprocess, os
import time
from os.path import exists

whereami = subprocess.getoutput('pwd')

def runcheck():
    try:
        files = os.listdir(f'{whereami}/logs/')
        filelist = {}
        for f in files:
            filelist[f] = os.stat(f'{whereami}/logs/{f}').st_mtime
        #print(filelist)
        os.chdir(f'{whereami}/logs')
        """
            in the following for look k == the log file name and v it's age in seconds.
            what we're doing here is converting that age in seconds to days. Once that is found
            we're going to move anything older than 7 days off to a subfolder of logs to oldlogs
        """
        for k, v in reversed(filelist.items()):
            age = round((time.time() - v))
            days = round(age / 86400)
            #print(f"age of {k} is {days} days old")
            # print(days)
            filelist[k] = days

        path = '.oldlogs'
        #os.chdir('./logs')
        if not exists(path):
            os.makedirs(path)
        else:
            for filename, age in filelist.items():
                if age > 6:
                    logging.info(f"PROCESSING: module:logcheck.main() moving {filename} which is {age} days old to {path}")
                    os.system(f'mv {filename} {path}')
        os.chdir('../')
    except Exception as e:
        logging.error(f"RUNNING: module: dblib - unable to process logs {e}", exc_info=True)

if __name__ == '__main__':
    runcheck()