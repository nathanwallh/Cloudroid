#!/usr/bin/python3

import socket

FTPsrvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
FTPsrvsock.connect( ('127.0.0.1',8000) )
serv_inpt = FTPsrvsock.recv( 256 )
firstcode = serv_inpt.decode().split(' ')[0]

if( firstcode != "220" ):
    print("Connection to the FTP network has failed.\nCode recieved: ", firstcode )
    exit()
print ("Connected to the FTP network")


srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srvsock.bind( ('0.0.0.0',6666) )
srvsock.listen( 1 )
client = srvsock.accept()[0]

client.send(b'220 FTPnetwork\r\n')
while True:
    cli_inpt = client.recv(512)
    print( "Client say: ", cli_inpt.decode() )
    if not cli_inpt:
        break
    FTPsrvsock.send( cli_inpt )
    serv_inpt =  FTPsrvsock.recv( 512 )
    print( "Server say: ", serv_inpt.decode() )
    if not serv_inpt:
        break
    client.send( serv_inpt )
print( "Client finished" )
