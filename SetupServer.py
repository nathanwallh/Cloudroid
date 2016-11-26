#!/usr/bin/python3
from sys import argv
from shutil import rmtree
from os import path
from Uinfo import getUsers
from Uinfo import compileUsers

introduction = """SetupServer.py
Setup the FTP server.

-delall 
    Delete all users.

-del <username1> <username2> ...
    Delete users by username.

-add (<username1>,<password1>) (<username2>,<password2>) ...
    Add users.
"""

if len(argv) == 1:
    print( introduction )
    exit()

if argv[1] == "-delall":
    open("Uinfo.txt", "w").close()
elif argv[1] == "-del":
    uinfo = getUsers()
    for x in uinfo:
        if path.exists( x.get('username') ):
            rmtree( x.get('username') )
    uinfo = [ x for x in uinfo if x.get('username') not in argv[2:] ]
    compileUsers( uinfo )
