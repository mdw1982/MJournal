import os
from settings import detect_os

'''
    for obvious reasons this small utility only works on Linux... at least
    at for the moment. If you wish to use this file on the windows platform
    you'll have to change the hash-bang at the top for your system. Unless, 
    of course you run it within your IDE in which case the hash-bang is 
    irrelevant. This entire project was and is being developed using
    PyCharm so if you're using another IDE your mileage may vary.
    ========================================================================
    WARNING!!! If you don't have pyinstaller installed within your IDE this
    script WILL NOT WORK!=
    ========================================================================
    I made this because I am lazy and it helps to streamline the packaging
    process... the packaging script is named pkg.py. That too should be run
    from within the IDE.
'''

if detect_os() == 'Linux':
    os.system('pyinstaller -F --windowed -n MJournal main.py')
    os.system('pyinstaller -F --windowed -n dbbackup dbbackup.py')
    os.system('pyinstaller -F --windowed -n setup setup.py')
    os.system('pyinstaller -F --windowed -n Unlock Unlock.py')

if detect_os() == 'windows':
    #os.system('pyinstaller --noconfirm --onefile --windowed -n MJournal.exe main.py')
    os.system('pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/images/MjournalIcon_36x36.ico" --name "MJournal.exe" --version-file "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/vfileMJournal.txt"  "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/main.py"')
    #os.system('pyinstaller --noconfirm --onefile --windowed -n dbbackup.exe dbbackup.py')
    os.system('pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/images/MjournalIcon_36x36.ico" --name "dbbackup.exe" --version-file "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/vfileDBbu.txt"  "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/dbbackup.py"')
    #os.system('pyinstaller --noconfirm --onefile --windowed -n setup.exe setup.py')
    os.system('pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/images/MjournalIcon_36x36.ico" --name "setup.exe" --version-file "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/vfileSetup.txt"  "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/setup.py"')
    #os.system('pyinstaller --noconfirm --onefile --windowed -n Unlock Unlock.py')
    os.system('pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/images/MjournalIcon_36x36.ico" --name "Unlock.exe" --version-file "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/vfileUnlock.txt"  "C:/Users/mweaver.MDW1982/PycharmProjects/MJournal/Unlock.py"')