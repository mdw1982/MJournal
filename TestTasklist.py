import os
import subprocess
import re

def get_pids():
    p = subprocess.Popen(["powershell","Get-Process | where-object {$_.ProcessName -eq 'python'} | ForEach-Object{$_.Id}"],stdout=subprocess.PIPE)
    n = p.communicate()
    b = n[0]
    temp = b.decode('utf-8')
    nlist = list()
    plist = temp.splitlines()
    for s in plist:
        nlist.append(int(s))
    return nlist

'''
    I can kill once process successfully and the program keeps running. that is the lowest
    value pid. If i kill more than that the program goes away. it's not crashing, but effectively 
    being shut down. however, after that the program will not restart/reload. even though
    I found a sort of answer it's not reliable like so much other windows shitware.
'''

pid_list = get_pids()
klist = sorted(pid_list,reverse=False)
print(klist)
keep = klist.pop(0)
os.system(f"taskkill /F /PID {keep}")

# for p in klist:
#     print(f"killing process: {p}")
#     os.system(f"taskkill /F /PID {p}")