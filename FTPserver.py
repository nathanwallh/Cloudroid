#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import mkdir
from os import path
import UinfoFunc

# Add users from Uinfo.txt and create directories for them.
auth = DummyAuthorizer( )
users =  UinfoFunc.getUsers()
for user in users:
    if False == path.exists( user.get('username') ):
        mkdir( user.get('username') )
    auth.add_user( user.get('username'), user.get('password'), './'+user.get('username'), perm='elradfmw' )

handler = FTPHandler
handler.authorizer = auth

server = FTPServer( ( '', '8000' ), handler )
server.max_cons=5
server.max_cons_per_ip=5

server.serve_forever( )


