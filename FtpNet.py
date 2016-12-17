#!/usr/bin/python3
import re
import socket

class FtpNet:
    def __init__( self, netfile ):

        # Read the addresses from <netfile>
        f = open( netfile, 'r' )
        addr = f.read().split()
        addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in addr ]
        self.servers = list()
        
        # Connect to the addresses in netfile
        for comp in addresses:
            self.servers.append( socket.socket( socket.AF_INET, socket.SOCK_STREAM ) )
            self.servers[-1].settimeout(3)
            try:
                self.servers[-1].connect( comp )
            except (socket.gaierror,socket.timeout):
                print("connection to " + str(comp) + " has failed")
                self.servers.pop()         
        for server in self.servers:
            code = self._get_code( self._get_raw_inpt( server ) )
            if not code:
                continue
            if code != "220":
                print("connection to FTP server at" + str( server.getpeername() ) + " has failed")
                self.servers.remove( server )
        print("Completed connection to servers")


    def _get_code( self, raw_inpt ):
        if not raw_inpt:
            return ''
        return raw_inpt.decode().split()[0]


    def _get_raw_inpt( self, server ):
            try:
                inpt = server.recv( 256 )
                if not inpt:
                    raise ValueError("got empty string")
            except (socket.timeout) as e:
                print("connection broke down with " + str( server.getpeername() ) )
                self.servers.remove( server )
                inpt = ''
            return inpt


    def net_recv( self ):
        total = list()
        for server in self.servers:
            raw_inpt = self._get_raw_inpt( server )
            total.append( raw_inpt )
        return b'\n'.join(total)



    def net_send( self, buf ):
        for server in self.servers:
            server.send( buf )


