#!/usr/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

auth = DummyAuthorizer( )
auth.add_user( 'nathan', '123', './nathanuser', perm='elradfmw' )

handler = FTPHandler
handler.authorizer = auth

server = FTPServer( ( '', '8000' ), handler )
server.max_cons=5
server.max_cons_per_ip=5

server.serve_forever( )


