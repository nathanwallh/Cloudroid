#!/usr/bin/python3
import re
import socket

class FtpNet:
    def __init__( self, netfile ):
        
        # Private variables declarations
        self.servers = list()
        self.data_sockets = list()
        self.cmd_req = '' 

        # Read the addresses from <netfile>
        # Connect to the addresses in netfile
        with open( netfile, 'r' ) as f:
            raw_addr = f.read().split()
        addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in raw_addr ]
        for comp in addresses:
            server_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            if comp[0] != '127.0.0.1':
                server_sock.settimeout(3)
            else:
                server_sock.settimeout(120)
            try:
                server_sock.connect( comp )
                self.servers.append( server_sock )
            except (socket.gaierror,socket.timeout):
                print("connection to " + str(comp) + " has failed")
        for server in self.servers:
            code = self.get_code( self._get_raw_inpt( server ) )
            if not code:
                continue
            if code != "220":
                print("connection to FTP server at" + str( server.getpeername() ) + " has failed")
                self.servers.remove( server )
        print("Completed connection to servers")


    def get_code( self, raw_inpt ):
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
                    if type(e).__name__=='timeout' and self.cmd_req.lower() == "stor":
                        continue
                    print("connection broke down with " + str( server.getpeername() ) )
                    print("cmd_req = " + self.cmd_req)
                    print("type(e) = " + type(e).__name__ )
                    self.servers.remove( server )
                    inpt = b''
                    break
            return inpt
    



    def send_data( self, filename ):
        for data_s in self.data_sockets:
            if data_s.getpeername()[0] != '127.0.0.1':
                continue
            with open( filename, "r" ) as f:
                try:
                    data_s.send( f.read().encode() )
                except:
                    print("Problem in sending data")
                    exit()
        
    
    def net_recv( self, servers ):
        if self.cmd_req == "epsv":
            return self.net_recv_EPSV()
        elif self.cmd_req == "list":
            return self.net_recv_LIST()
        total = list()
        for server in servers:
            raw_inpt = self._get_raw_inpt( server )
            total.append( raw_inpt )
        total = list( set( total ) )
        return b'\n'.join( total )



    def net_recv_EPSV( self ):
        # Extract the addresses with ports
        addresses = list()
        for server in self.servers:
            raw_inpt = self._get_raw_inpt( server )
            code = self.get_code( raw_inpt )
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
        retval = "229 Entering extended passive mode (|||"+str(loopback_port)+"|).\n" 
        return str.encode(retval) 


    def net_send( self, buf ):
        for server in self.servers:
            server.send( buf )


