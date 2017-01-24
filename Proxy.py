#!/usr/bin/python3

# Proxy server that broadcasts FTP requests to the network.
# The proxy is listening on port 6000
# server listens on port 8000.
# The first server to run should be the FTP server( Server.py )
# Then, after running the proxy, an FTP client can make a 
# connection through port 6000 and then things run as usual.
USERS_FILE = "Uinfo.txt"
CONSISTENCY_THRESHOLD = 0.7
NETWORK_FILE = "Netinfo.txt"
BUF_SIZE = 2048
PORT = 6000

DEBUG_val = True
def DEBUG(s):
    if DEBUG_val == True:
        print(s)

from os import mkdir
import threading
import socket
import FtpNet
import UinfoFunc
import Hasher
from shutil import rmtree



class ProxyThread( threading.Thread ):
    def __init__( self, client ): 
        threading.Thread.__init__( self )
        self.curr_cmd = ''
        self.user = ''
        self.filename = ''
        self.EPSV = False
        self.client = client
        self.network = FtpNet.FtpNet(NETWORK_FILE)
        self.hash = Hasher.Hasher()
#        self.consistency_check()
        self.repeater = threading.Thread( target=self.localhost_repeater )
        self.repeater.daemon = True
        print("Completed connection to servers")


# Serve the client
    def run( self ):
        self.send_client(b'220 FTPnetwork\r\n')
        self.repeater.start()
        
        while True:
        # Get input from the client
            cli_inpt = self.get_raw_inpt()
            print( "Client says: ", cli_inpt.decode() ) 
            if not cli_inpt:
                break
            self.curr_cmd = cli_inpt[:4].decode().strip().lower()
            self.network.curr_cmd = self.curr_cmd
        
        # Send the client's input to the network
            if self.curr_cmd == "list" or self.curr_cmd =="retr":
                self.network.net_send(cli_inpt, self.network.local)
            else:
                self.network.net_send(cli_inpt)
        
        # Handling special commands
            if self.curr_cmd == "user":
                self.user = cli_inpt[5:].decode().strip()
            elif self.curr_cmd == "quit":
                self.client.close()
                break 
            elif self.curr_cmd == "epsv":
                self.EPSV = True;
            elif self.curr_cmd == "stor":
                self.filename = "user_files/" + cli_inpt[5:].decode().strip()
                if self.EPSV == True:
                    self.STOR()
            elif self.curr_cmd == "list" or self.curr_cmd == "retr":
                if self.EPSV == True:
                    self.LISTRETR()
            
            if self.EPSV == True and \
                (self.curr_cmd == "stor" or self.curr_cmd == "list" or self.curr_cmd =="retr"):
                self.EPSV = False
        
        # Get input from network
            self.network.net_recv( self.network.external )
        

# A thread that recieves data from the local FTP and sends it to the user
    def localhost_repeater( self ):
        while True:
            server_response = self.network.local_recv()
            print("Network says: " + server_response.decode())
            self.send_client( server_response )


# Check consistency of server with others on network
    def consistency_check( self ):
        threshold = round( self.network.size() * CONSISTENCY_THRESHOLD )
        network_hashes = self.get_hashes()
        for server_hash in network_hashes:
            if self.hash.isEqual( server_hash[1] ) == False:
                threshold -= 1
    # Server is consistent
        if threshold > 0:
            return
    # Server is not consistent
        occurrences_list = []
        for hsh in network_hashes:
            occurrences = len( [h[1] for h in network_hashes if h[1] == hsh[1]] )
            occurrences_list.append(  ( hsh[0], occurrences) )
        max_occur = max( occurrences_list, key=lambda tup: tup[1] )
        self.not_consistent( [ self.network.get_server_sock( max_occur[0] ) ] )
        return
    


# Update all server files from a single server
    def not_consistent( self, server_sock ):
        rmtree("user_files")
        mkdir("user_files")
        self.network.net_send(b"USER guest\r\n", server_sock)
        self.network.net_recv( server_sock )
        self.network.net_send(b"PASS guest\r\n", server_sock)
        inpt = self.network.net_recv( server_sock )
        if self.network.get_code( inpt ) != "230":
            print("_not_consistent: Failed to login as guest. Aborting.")
            exit()
        files = self.get_file_list( server_sock )
        for f in files:
            self.retrieve_file( f, server_sock )
        self.anon_login( server_sock )



# Get the files list of a single server
    def get_file_list( self, server_sock ):
        self.network.net_send(b"EPSV\r\n", server_sock)
        self.network.curr_cmd = "epsv"
        net_inpt = self.network.net_recv( server_sock )
        self.network.curr_cmd = ""
        self.network.net_send(b"LIST\r\n", server_sock)
        self.network.net_recv( server_sock )
        file_List = self.network.read_data_buffers()
        raw_file_list = file_List.decode().split("\n")[:-1]
        clean_file_list = list()
        for f in raw_file_list:
            clean_file_list.append( f.split()[-1] )
        return clean_file_list



# Retrieve a file from a single server
    def retrieve__file( self, filename, server_sock ):
        self.network.net_send(b"EPSV\r\n", server_sock)
        self.network.curr_cmd = "epsv"
        self.network.net_recv( server_sock  )
        self.network.curr_cmd = ""
        self.network.net_send(b"RETR " + filename.encode() + b"\r\n", server_sock)
        self.network.net_recv( server_sock )
        file_data = self.network.read_data_buffers( server_sock )
        with open( "user_files/" + filename, "w" ) as f:
            f.write( file_data.decode() )
    


# Get all server hashes on the EXTERNAL network
    def get_hashes( self ):
        self.anon_login()
        self.network.net_send( b"EPSV\r\n", self.network.external )
        self.network.curr_cmd = "epsv"
        self.network.net_recv( self.network.external )
        self.network.curr_cmd = ""
        self.network.net_send( b"RETR ServerHash.txt\r\n", self.network.external )
        self.network.net_recv( self.network.external )
        hashlist = self.network.retrieve_hash_tuples()
        return hashlist




# Login to all servers on network as anonymous
    def anon_login( self, Servers=None ):
        if Servers == None:
            Servers = self.network.external
        self.network.net_send(b"USER anonymous\r\n", Servers)
        self.network.net_recv( Servers )
        self.network.net_send(b"PASS anonymous\r\n", Servers)
        self.network.net_recv( Servers )
        return





    def LISTRETR( self ):
        self.network.close_data_connections()
        return ''
    


    def STOR( self ):
        self.network.send_file( self.filename )
        return ''
   

# Send raw data to client's control connection
    def send_client( self, raw_data ):
        try:
            self.client.send( raw_data )
        except Exception as e:
            if self.curr_cmd != "quit":
                print("The client has suddenly died")
            exit()


# Recieve raw data from the client's control connection
    def get_raw_inpt( self ):
        try:
            inpt = self.client.recv( BUF_SIZE )
        except (socket.timeout) as e:
            print("Client is dead")
            inpt = ''
        return inpt




class ProxyServer:
    def __init__( self, port ):
        # Initialize the server socket
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind( ('0.0.0.0',port) )
        self.sock.listen( 5 )

    def serve( self ):
        while True:
            # Wait for clients and serve them
            client = self.sock.accept()[0]
            serve_thread = ProxyThread( client )
            serve_thread.daemon = True
            serve_thread.start()
            
                    
if __name__ == '__main__':
    Proxy = ProxyServer(PORT)
    Proxy.serve()
