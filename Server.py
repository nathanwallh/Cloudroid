#!/usr/bin/python3

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import re
from os import mkdir
from os import path
from UinfoFunc import getUsers


# Add users from Uinfo.txt and create directories for them.
auth = DummyAuthorizer( )
for user in getUsers():
    if False == path.exists( user.get('username') ):
        mkdir( user.get('username') )
    auth.add_user( user.get('username'), user.get('password'), './'+user.get('username'), perm='elradfmw' )


handler = FTPHandler
handler.authorizer = auth

logging.basicConfig( filename='./serverlog', level=logging.INFO )

server = FTPServer( ( '', '8000' ), handler )
server.max_cons=5
server.max_cons_per_ip=5

server.serve_forever( )


