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
        for server in self.net_sockets:
            code = self.__get_code( self.__get_raw_inpt( server ) )
            if not code:
                continue
            if code != "220":
                print("connection to FTP server at" + str( server.getpeername() ) + " has failed")
                self.net_sockets.remove( server )
        print("Completed connection to servers")


    def __get_code( self, raw_inpt ):
        if not raw_inpt:
            return ''
        return raw_inpt.decode().split()[0]


    def __get_raw_inpt( self, server ):
            try:
                inpt = server.recv( 256 )
                if not inpt:
                    raise ValueError("got empty string")
            except (socket.timeout) as e:
                print("connection broke down with " + str( server.getpeername() ) )
                self.net_sockets.remove( server )
                inpt = ''
            return inpt


    def net_recv( self, buf ):
        total = list()
        for server in self.net_sockets:
            raw_inpt = self.__get_raw_inpt( server )
            total.append( raw_inpt )
        return b'\n'.join(total)

 
    def net_send( self, buf ):
        for server in self.net_sockets:
            server.send( buf )
