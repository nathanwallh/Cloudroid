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
import FtpNet



# Listen on port 6000 and wait for clients
srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srvsock.bind( ('0.0.0.0',6000) )
srvsock.listen( 1 )

while True:
    # Wait for clients and serve them
    client = srvsock.accept()[0]
    client.send(b'220 FTPnetwork\r\n')
    network = FtpNet.FtpNet('Netinfo.txt')

    # Mediate between the client and the network
    while True:
        
        # Get input from client and send to network
        cli_inpt = client.recv(256)
        
        print( "Client says: ", cli_inpt.decode() ) 
        network.net_send(cli_inpt)

        if not cli_inpt:
            break
        
        cmd = cli_inpt.decode().split()[0]
        
        if cmd == "BYEBYE":
            exit()
        
        # Get input from network and send to client
        net_inpt = network.net_recv(256)
         
        print( "Network says: ", net_inpt.decode() ) 
        client.send( net_inpt )

        if not net_inpt:
            client.close()
            break
        
        code = net_inpt.decode().split()[0]
        
        if code == "221":
            client.close()
            break;
        # Code 125 
        elif code == "125":
            net_inpt = network.net_recv( 256 )
