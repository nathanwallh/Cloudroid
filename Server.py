#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import re
from os import mkdir
from os import path
from Uinfo import getUsers


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


