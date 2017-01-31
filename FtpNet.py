#!/usr/bin/python3

# FtpNet object
# An object that represents the network of FTP servers.
# It contains all methods for sending and recieveing FTP commands and data.

BUF_SIZE = 2048
DEBUG_val = True
def DEBUG(s):
    if DEBUG_val == True:
        print(s)

import socket

class FtpNet:
    def __init__( self, netfile ):        
        self.servers = list()
        self.data_sockets = list()
        self.curr_cmd = '' 
        self.cons_check = False
        self.data_addresses = list()
        self.external = list()
        self.local = list()
        self.connect_to_network( netfile )
        self.external = [server for server in self.servers if server.getpeername()[0]!='127.0.0.1']
        self.local = [server for server in self.servers if server.getpeername()[0]=='127.0.0.1']


# Connect to the addresses in netfile
    def connect_to_network( self, netfile ):
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


# Read all hashes from the data sockets and return them as a list with ports
    def retrieve_hash_tuples( self ):
        hash_tuples = []
        addresses = [address.getpeername()[0] for address in self.data_sockets]
        hashes = self.read_data_buffers( self.external )
        hash_tuples = zip( addresses, hashes )
        return list(hash_tuples)


# Close all data connections
    def close_data_connections( self ):
        for data_s in self.data_sockets:
            try:
                data_s.close()
            except Exception:
                pass
        self.data_sockets = []


# Read all buffers from data sockets and close them
    def read_data_buffers( self, Servers=None ):
        data = []
        if Servers == None:
            d_sockets = self.data_sockets
        else:
            d_sockets = [d_socket for d_socket in self.data_sockets if \
                d_socket.getpeername()[0] in [ s.getpeername()[0] for s in Servers ] ]
        for data_s in d_sockets:
            try:
                data.append( data_s.recv(BUF_SIZE) )
                self.data_sockets.remove(data_s)
                data_s.close()
            except Exception as e:
                print("connection broke down with " + data_s.getpeername()[0])
        return data


# Send the a file to the external network
    def send_file( self, filename ):
        for data_s in self.data_sockets:
            with open( filename, "r" ) as f:
                try:
                    data_s.send( f.read().encode() )
                    data_s.close()
                except:
                    print("Problem in sending data")
        self.data_sockets = []


# Receive input from all external servers after a data command was completed, and check that they all sent 226 as the return code.    
    def read_226( self, Servers ):
        servers_respone = self.net_recv( Servers )
        codes = [ s for s in servers_respone.split() if s.isdigit() ]
        if codes.count( b'226' ) != len( codes ):
            print("Not all servers returned 226")



# Make data connection with all addresses in self.data_addresses
    def make_data_connections( self, data_addresses):
        self.close_data_connections()
        for addr in data_addresses:
            data_sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            try:
                data_sock.connect( addr )
                self.data_sockets.append( data_sock )
            except Exception as e:
                print("Data connection to " + str( comp ) + " has failed." )



# Send buf to all servers in the network
    def net_send( self, buf, Servers=None ):
        if Servers==None:
            Servers = self.servers
        for server in Servers:
            try:
                server.send( buf )
            except( socket.gaierror, socket.timeout ):
                print("Failed sending to one of the servers")
                self.servers.remove ( server )



# Recieve data from list of servers.
    def net_recv( self, Servers=None ):
        if Servers == None:
            Servers = self.servers
        if self.curr_cmd == "epsv":
            self.net_recv_EPSV( self.external )
            if self.cons_check == True:
                return b''
            else:
                return self.local_recv()
        total = list()
        for server in Servers:
            raw_inpt = self.get_raw_input( server )
            total.append( raw_inpt )
        total = list( set( total ) )
        return b'\n'.join( total )


# Save all ports for data connection and send back only the localhost port 
    def net_recv_EPSV( self, Servers=None  ):
        if Servers == None:
            Servers = self.external
        data_addresses = []
        total = list()
        for server in Servers:
            raw_inpt = self.get_raw_input( server )
            total.append( raw_inpt )
            code = self.get_code( raw_inpt )
            if code != "229":
                print("Server: " + str( server.getpeername() ) +" failed with EPSV")
                total = total[:-1]
            else:
                port = int( raw_inpt.decode()[3:].split("|")[-2] )
                data_addresses.append( (server.getpeername()[0], port) )
    # There are 2 cases corresponding to whether EPSV was sent as a part of consistency check or not.
        self.make_data_connections( data_addresses )
        total = list( set( total ) )
        return b'\n'.join( total )




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



    def get_server_sock( self, serverIP ):
            return [ sock for sock in self.servers if sock.getpeername()[0]==serverIP ][0]


    def local_recv( self ):
            return self.get_raw_input( self.local[0] )
