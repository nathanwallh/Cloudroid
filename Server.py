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
users = get_all_usernames_from_file("Uinfo.txt")
for user, password in users.items():
    if path.exists(user) is False:
        mkdir(user)
    auth.add_user(user, password, './' + user, perm='elradfmw')
auth.add_anonymous( getcwd() + '/anon' )

handler = FTPHandler
handler.authorizer = auth

server = FTPServer(('', FTPPORT), handler)
server.max_cons = 5
server.max_cons_per_ip = 5

server.serve_forever()
