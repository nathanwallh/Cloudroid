#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import mkdir
from os import path
from os import getcwd
from UinfoFunc import get_all_usernames_from_file


FTPPORT = 8000


# Add users from Uinfo.txt and create directories for them.
auth = DummyAuthorizer()
if path.exists("user_files") is False:
    mkdir("user_files")
auth.add_user("guest", "guest", './user_files', perm='elradfmw')
auth.add_anonymous( getcwd() + '/Hash' )

handler = FTPHandler
handler.authorizer = auth

server = FTPServer(('', FTPPORT), handler)
server.max_cons = 5
server.max_cons_per_ip = 5

server.serve_forever()
