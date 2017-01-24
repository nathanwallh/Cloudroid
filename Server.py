#!/usr/bin/python3

# The FTPNetwork server as a whole. Proxy + FTPserver together.

import subprocess
import sys
import atexit
from os import wait,devnull
from signal import SIGTERM

def clean_exit():
    if FTPs.poll() == None:
        FTPs.terminate()
    if Proxy.poll() == None:
        Proxy.terminate()


# forking the FTPserver
with open(devnull,"w") as FNULL:
    FTPs = subprocess.Popen(["./FTPserver.py"],stdout=FNULL,stderr=subprocess.STDOUT)
Proxy = subprocess.Popen(["./Proxy.py"],stdout=sys.stdout)

atexit.register(clean_exit)
wait()
