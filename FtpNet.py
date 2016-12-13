#!/usr/bin/python3
import socket

class FtpNet:
    def __init__( self, netfile ):

        # Read the addresses from <netfile>
        f = open( netfile, 'r' )
        addr = f.read().split()
        self.addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in addr ]
        
        # Connect to the addresses in netfile
        self.net_sockets = list()
        for comp in self.addresses:
            self.net_sockets.append( socket.socket( socket.AF_INET, socket.SOCK_STREAM ) )
            self.net_sockets[-1].settimeout(3)
            try:
                self.net_sockets[-1].connect( comp )
            except (socket.gaierror,socket.timeout):
                print("connection to " + str(comp) + " has failed")
                self.net_sockets.pop()
        # Make sure that an FTP server is up
        for con in self.net_sockets:
            if "220" != con.recv( 256 ).decode().split()[0]:
                    print("connection to FTP server at" + str( con.getpeername() ) + " has failed")
                    self.net_sockets.remove( con )
        print("Completed connection to servers")
    
    def net_recv( self, buf ):
        total = list()
        for con in self.net_sockets:
            total.append( con.recv(256) )
        return b'\n'.join(total)

    
    def net_send( self, buf ):
        for con in self.net_sockets:
            con.send( buf )
