#!/usr/bin/python3

# Proxy server that redirects FTP traffic to the right
# computer on the network.

# Technical:
# The proxy server listens on port 6666, while the FTP
# server listens on port 8000.
# The first server to run should be the FTP server( Server.py )
# Then, after running the proxy, an FTP client can make a 
# connection through port 6666 and then things run as usual.


import socket

# Connect to the FTP server( Server.py )
FTPsrvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
FTPsrvsock.connect( ('127.0.0.1',8000) )
serv_inpt = FTPsrvsock.recv( 256 )
firstcode = serv_inpt.decode().split(' ')[0]

if( firstcode != "220" ):
    print("Connection to the FTP network has failed.\nCode recieved: ", firstcode )
    exit()
print ("Connected to the FTP network")

# Listen on port 6666 and wait for clients
srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srvsock.bind( ('0.0.0.0',6666) )
srvsock.listen( 1 )
client = srvsock.accept()[0]

# Send the FTP accept code to the client
client.send(b'220 FTPnetwork\r\n')

# Send clients data to the FTP server and vice versa.
# Print output of client and server for logging reasons.
while True:
    cli_inpt = client.recv(256)
    print( "Client say: ", cli_inpt.decode() )
    if not cli_inpt:
        break
    FTPsrvsock.send( cli_inpt )
    serv_inpt =  FTPsrvsock.recv( 256 )
    print( "Server say: ", serv_inpt.decode() )
    if not serv_inpt:
        break
    client.send( serv_inpt )
# Code 125 means that now a data connection is open and therefore the FTP server
# will reply before the client does.
    if serv_inpt.decode().split(' ')[0] == "125":
        serv_inpt = FTPsrvsock.recv( 256 )
        print("Server say: ", serv_inpt.decode() )
        client.send( serv_inpt )
print( "Client finished" )
