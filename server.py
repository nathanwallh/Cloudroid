#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import re
from os import mkdir
from os import path

# Extract users info(name and password) from the file Uinfo.txt.
# Return them as a list of dicionaries: {username:xxx, password:yyy}.
def getUsers():
    ufile = open("Uinfo.txt","r")
    uinfo = ufile.read()
    uinfo = re.findall( "AddUser{\n.*?\n}", uinfo, flags=re.DOTALL )
    uinfo = [ { 'username':x.split("\n")[1], 'password':x.split("\n")[2] } for x in uinfo ]
    return uinfo

# Add users from Uinfo.txt and create directories for them.
auth = DummyAuthorizer( )
for x in getUsers():
    if False == path.exists( x.get('username') ):
        mkdir( x.get('username') )
    auth.add_user( x.get('username'), x.get('password'), './'+x.get('username'), perm='elradfmw' )


handler = FTPHandler
handler.authorizer = auth

server = FTPServer( ( '', '8000' ), handler )
server.max_cons=5
server.max_cons_per_ip=5

server.serve_forever( )


