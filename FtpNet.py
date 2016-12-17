#!/usr/bin/python3
import re
import socket

class FtpNet:
    def __init__( self, netfile ):

        # Read the addresses from <netfile>
        f = open( netfile, 'r' )
        raw_addr = f.read().split()
        addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in raw_addr ]
        self.servers = list()
        self.data_sockets = list()
        self.curr_cmd = '' 

        # Connect to the addresses in netfile
        for comp in addresses:
            server_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            server_sock.settimeout(3)
            try:
                server_sock.connect( comp )
                self.servers.append( server_sock )
            except (socket.gaierror,socket.timeout):
                print("connection to " + str(comp) + " has failed")
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
            while True:
                try:
                    inpt = server.recv( 256 )
                    if not inpt:
                        raise ValueError("EOF")
                    break
                except (ValueError,socket.timeout) as e:
                    if type(e).__name__=='timeout' and self.curr_cmd.lower() == "STOR".lower():
                        continue
                    print("connection broke down with " + str( server.getpeername() ) )
                    print("curr_cmd = " + self.curr_cmd)
                    print("type(e) = " + type(e).__name__ )
                    self.servers.remove( server )
                    inpt = b''
                    break
            return inpt
    

    def net_recv( self ):
        if self.curr_cmd.lower() == "EPSV".lower():
            return self.net_recv_EPSV()
        total = list()
        for server in self.servers:
            raw_inpt = self._get_raw_inpt( server )
            total.append( raw_inpt )
        total = list( set( total ) )
        return total[0]


    def net_recv_EPSV( self ):
        # Extract the addresses with ports
        addresses = list()
        for server in self.servers:
            raw_inpt = self._get_raw_inpt( server )
            code = self._get_code( raw_inpt )
            if code != "229":
                print("Server: " + str( server.getpeername() ) +" failed with EPSV")
            else:
                port = int( re.search('\d+', raw_inpt.decode()[3:]).group() )
                addresses.append( (server.getpeername()[0], port) )
        # create data connections with all servers except the loopback
        loopback_port = dict(addresses)["127.0.0.1"]
        addresses = [ addr for addr in addresses if addr[0] != "127.0.0.1" ]
        for comp in addresses:
            data_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            data_sock.settimeout(3)
            try:
                data_sock.connect( comp )
                self.data_sockets.append( data_sock )
            except (socket.gaierror,socket.timeout):
                print("Data connection to " + str( server.getpeername() ) + " has failed." )
        retval = "229 Entering extended passive mode (|||"+str(loopback_port)+"|)." 
        return str.encode(retval) 


    def net_send( self, buf ):
        for server in self.servers:
            server.send( buf )


