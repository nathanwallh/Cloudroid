#!/usr/bin/python3
DEBUG_val = False
def DEBUG(s):
    if DEBUG_val == True:
        print(s)

import socket

class FtpNet:
    def __init__( self, netfile ):
        
    # Private variables declarations
        self.servers = list()
        self.data_sockets = list()
        self.cmd_req = '' 
        self.data_addresses = ''

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
            except (socket.gaierror,socket.timeout,ConnectionRefusedError):
                print("connection to " + str(comp) + " has failed")
        for server in self.servers:
            code = self.get_code( self._get_raw_inpt( server ) )
            if not code:
                continue
            if code != "220":
                print("connection to FTP server at" + str( server.getpeername() ) + " has failed")
                self.servers.remove( server )
        DEBUG("FtpNet.__init__: servers are " + str( self.servers ) )
        print("Completed connection to servers")

# Extract the code from the FTP servers response
    def get_code( self, raw_inpt ):
        if not raw_inpt:
            return ''
        return raw_inpt.decode().split()[0]


# Recieve input from FTP server
    def _get_raw_inpt( self, server ):
            while True:
                try:
                    inpt = server.recv( 256 )
                    if not inpt:
                        raise ValueError("EOF")
                    break
                except (ValueError,socket.timeout) as e:
                    print("connection broke down with " + str( server.getpeername() ) )
                    self.servers.remove( server )
                    inpt = b''
                    break
            return inpt
    


# Send the file specified in <filename> to all servers on the network except localhost
    def send_data( self, filename ):
        for data_s in self.data_sockets:
            with open( filename, "r" ) as f:
                try:
                    DEBUG("FtpNet.send_data: starting to send the file to the network")
                    data_s.send( f.read().encode() )
                    data_s.close()
                    self.data_sockets.remove( data_s )
                    DEBUG("FtpNet.send_data: the data had been sent successfully to the network")
                except:
                    print("Problem in sending data")
                    exit()
        
# Recieve data from all servers on the network, join it together and send back to proxy
    def net_recv( self, servers ):
        if self.cmd_req == "epsv":
            return self.net_recv_EPSV()
        total = list()
        for server in servers:
            raw_inpt = self._get_raw_inpt( server )
            total.append( raw_inpt )
        total = list( set( total ) )
        return b'\n'.join( total )


# Save all ports for data connection and send back only the localhost port 
    def net_recv_EPSV( self ):
        addresses = list()
        for server in self.servers:
            raw_inpt = self._get_raw_inpt( server )
            code = self.get_code( raw_inpt )
            if code != "229":
                print("Server: " + str( server.getpeername() ) +" failed with EPSV")
            else:
                port = int( raw_inpt.decode()[3:].split("|")[-2] )
                addresses.append( (server.getpeername()[0], port) )
        localhost_port = dict(addresses)["127.0.0.1"]
        self.data_addresses = [ addr for addr in addresses if addr[0] != "127.0.0.1" ]
        return str.encode("229 Entering extended passive mode (|||"+str(localhost_port)+"|).\n")

# Make data connection with all addresses in self.data_addresses
    def make_data_connections( self ):
        for comp in self.data_addresses:
            data_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            data_sock.settimeout(3)
            try:
                data_sock.connect( comp )
                self.data_sockets.append( data_sock )
            except (socket.gaierror,socket.timeout):
                print("Data connection to " + str( data_sock.getpeername() ) + " has failed." )

# Send buf to all servers in the network
    def net_send( self, buf ):
        for server in self.servers:
            try:
                server.send( buf )
            except( socket.gaierror, socket.timeout ):
                print("Failed sending to one of the servers")
                self.servers.remove ( server )


