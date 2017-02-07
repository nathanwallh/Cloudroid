#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import mkdir
from os import path
from os import getcwd


FTPPORT = 8000
USER_DIR = "user_files"
HASH_DIR = "Hash"
USERNAME = "guest"
USERPASS = "guest"

# Add users from Uinfo.txt and create directories for them.
auth = DummyAuthorizer()
if path.exists(USER_DIR) is False:
    mkdir(USER_DIR)
if path.exists(HASH_DIR) is False:
    mkdir(HASH_DIR)
auth.add_user(USERNAME, USERPASS, './' + USER_DIR, perm='elradfmw')
auth.add_anonymous( getcwd() + '/' + HASH_DIR )

handler = FTPHandler
handler.authorizer = auth

server = FTPServer(('', FTPPORT), handler)
server.max_cons = 10
server.max_cons_per_ip = 10

server.serve_forever()
