#!/usr/bin/python3

import re

#
# Methods for dealing with the users file Uinfo.txt
#



# Reads and parses Uinfo.txt. Returns a list of dictionaries: [ {username:xxx,password:yyy} ].
def getUsers():
    with open("Uinfo.txt","r") as ufile:
        uinfo = ufile.read()
    uinfo = re.findall( "{\n.*?\n}", uinfo, flags=re.DOTALL )
    uinfo = [ { 'username':x.split("\n")[1], 'password':x.split("\n")[2] } for x in uinfo ]
    return uinfo



# Override Uinfo.txt with new users and passwords from a given dictionary list <newuinfo>
def writeUsers(newuinfo):
    compiled = [ "{\n"+x.get('username')+"\n"+x.get('password')+"\n}\n" for x in newuinfo ]
    with open("Uinfo.txt","w") as ufile:
        ufile.write( ''.join( compiled ) )
    return
