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
        self.curr_cmd = '' 
        self.data_addresses = list()
        self.external = list()
        self.local = list()

    # Connect to the addresses in netfile
        with open( netfile, 'r' ) as f:
            raw_addr = f.read().split()
        addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in raw_addr ]
        for comp in addresses:
            server_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            try:
                server_sock.connect( comp )
                self.servers.append( server_sock )
            except (socket.gaierror,socket.timeout,ConnectionRefusedError,OSError):
                print("connection to " + str(comp) + " has failed")
        for server in self.servers:
            code = self.get_code( self.get_raw_input( server ) )
            if not code:
                continue
            if code != "220":
                print("connection to FTP server at" + str( server.getpeername() ) + " has failed")
                self.servers.remove( server )
        self.external = [server for server in self.servers if server.getpeername()[0]!='127.0.0.1']
        self.local = [server for server in self.servers if server.getpeername()[0]=='127.0.0.1']
        print("Completed connection to servers")

    def get_server_sock( self, serverIP ):
        return [ sock for sock in self.servers if sock.getpeername()[0]==serverIP ][0]


    def local_recv( self ):
        return self.get_raw_input( self.local[0] )

# Read all hashes from the data sockets and return them as a list
    def get_hash_list( self ):
        hashlist = []
        for data_s in self.data_sockets:
            try:
                s_hash = data_s.recv( 128 ).decode()
                hashlist.append( (data_s.getpeername()[0], s_hash) )
                data_s.close()
            except( socket.timeout ) as e:
                print("connection broke down with " + data_s.getpeername()[0])
        self.data_sockets = []
        self._read_226()
        return hashlist

# Close all data connections
    def close_data_connections( self ):
        for data_s in self.data_sockets:
            data_s.close()
        self.data_sockets = []

# Read all buffers from data sockets and close them
    def clean_data_buffers( self ):
        data = []
        for data_s in self.data_sockets:
            try:
                data = data_s.recv(2048)
                data_s.close()
            except(socket.timeout) as e:
                print("connection broke down with " + data_s.getpeername()[0])
        self.data_sockets = []
        return data


# Send the file specified in <filename> to all servers on the network except localhost
    def send_to_data_connection( self, filename ):
        for data_s in self.data_sockets:
            with open( filename, "r" ) as f:
                try:
                    data_s.send( f.read().encode() )
                    data_s.close()
                except:
                    print("Problem in sending data")
                    exit()
        self.data_sockets = []
        self._read_226()


# Receive input from all external servers after a data command was completed, and check that they all sent 226 as the return code.
    
    def _read_226( self ):
        servers_respone = self.net_recv( )
        codes = [ s for s in servers_respone.split() if s.isdigit() ]
        if codes.count( b'226' ) != len( codes ):
            print("Not all servers returned 226")


# Make data connection with all addresses in self.data_addresses
    def _make_data_connections( self, data_addresses):
        for comp in data_addresses:
            data_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            try:
                data_sock.connect( comp )
                self.data_sockets.append( data_sock )
            except (socket.gaierror,socket.timeout,ConnectionRefusedError) as e:
                print("Data connection to " + str( comp ) + " has failed." )
                exit()



# Send buf to all servers in the network
    def net_send( self, buf, servers=None ):
        if servers==None:
            servers = self.servers

        for server in servers:
            try:
                server.send( buf )
            except( socket.gaierror, socket.timeout ):
                print("Failed sending to one of the servers")
                self.servers.remove ( server )



# Return a list containing onlt the local FTP server socket
    def localhost( self ):
        return


# Return a list containing all but not the local FTP server sockets
    def external_hosts( self ):
        return [server for server in self.network.servers if server.getpeername()[0]!='127.0.0.1'];


# Recieve data from all servers on the network, join it together and send back to proxy
    def net_recv( self ):
        if self.curr_cmd == "epsv":
            return self._net_recv_EPSV( )
        total = list()
        for server in self.external:
            raw_inpt = self.get_raw_input( server )
            total.append( raw_inpt )
        total = list( set( total ) )
        return b'\n'.join( total )


# Save all ports for data connection and send back only the localhost port 
    def _net_recv_EPSV( self  ):
        data_addresses = []
        for server in self.external:
            raw_inpt = self.get_raw_input( server )
            code = self.get_code( raw_inpt )
            if code != "229":
                print("Server: " + str( server.getpeername() ) +" failed with EPSV")
            else:
                port = int( raw_inpt.decode()[3:].split("|")[-2] )
                data_addresses.append( (server.getpeername()[0], port) )
    # There are 2 cases corresponding to whether EPSV was sent as a part of consistency check or not.
        self._make_data_connections( data_addresses )
        return ''

# Extract the code from the FTP servers response
    def get_code( self, raw_inpt ):
        if not raw_inpt:
            return ''
        return raw_inpt.decode().split()[0]



# Recieve input from FTP server
    def get_raw_input( self, server ):
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
    

# Return number of active servers
    def size( self ):
        return len( self.servers )



