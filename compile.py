#!/usr/bin/python3
import os
from settings import detect_os

if detect_os() == 'Linux':
    os.system('pyinstaller -F -n MJournal main.py')
    os.system('pyinstaller -F -n dbbackup dbbackup.py')
    os.system('pyinstaller -F -n setup setup.py')

if detect_os() == 'windows':
    os.system('pyinstaller -F -n MJournal.exe main.py')
    os.system('pyinstaller -F -n dbbackup.exe dbbackup.py')
    os.system('pyinstaller -F -n setup.exe setup.py')