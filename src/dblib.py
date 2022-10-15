import os, getpass
import random
import logging
import subprocess
import datetime as dt
from os.path import exists
import subprocess as sp
from cryptography.fernet import Fernet
from src.logcheck import *
import json
# from lib.logcheck import *


# ===================================================================
# def version():
#     with open('./version', 'r') as f:
#         v = f.read()
#     return v

def init_logs():
    whereami = subprocess.getoutput('pwd')
    runcheck()
    logpath = f'{whereami}/logs/'
    lfn = logpath + 'mjournal_' + log_name_date() + '.log'
    logging.basicConfig(filename=lfn, filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)



def get_epoc():
    tstamp = int(round(dt.datetime.now().timestamp()))
    return tstamp


def give_time():
    return str(dt.datetime.now())


def log_name_date():
    n = dt.datetime.now()
    y = n.strftime('%Y')
    m = n.strftime('%m')
    d = n.strftime('%d')
    return y + '-' + m + '-' + d


def pass_gen():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$*123456789'
    n = 1  # number of passwords to be generated
    l = 14  # length of password generated
    for pwd in range(n):
        password = ''
        for c in range(l):
            password += random.choice(chars)
        return password


def cat_source(path):
    arr = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path)) for f in fn]
    return arr

"""
Any changes made to the information below would likely break many things in the program as
a whole, so it's a good idea not to change anything... These are essentially Global variables 
for the program.
"""
whereami = subprocess.getoutput('pwd')
# setup key and config file access
keyfile = f'{whereami}/key.txt'  # path and file for the encryption key
config = f'{whereami}/config'  # path and file for the config file
database = f'{whereami}/dbu.db'
yearly = f'{whereami}/yearly'
# open the log file for logging
logpath = f'{whereami}/logs/'
lfn = logpath + 'mjournal_' + log_name_date() + '.log'
logging.basicConfig(filename=lfn, filemode='a', format='%(asctime)s - %(message)s', level=logging.DEBUG)
