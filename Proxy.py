#!/usr/bin/python3

# Proxy server that redirects FTP traffic to the right
# computer on the network.

# Technical:
# The proxy server listens on port 6000, while the FTP
# server listens on port 8000.
# The first server to run should be the FTP server( Server.py )
# Then, after running the proxy, an FTP client can make a 
# connection through port 6000 and then things run as usual.
USERS_FILE = "Uinfo.txt"
CONSISTENCY_THRESHOLD = 0.7

DEBUG_val = False
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
        self.client = client
        self.network = FtpNet.FtpNet('Netinfo.txt')
        threading.Thread.__init__( self )
        self.cli_inpt = ''
        self.curr_cmd = ''
        self.user = ''
        self.filename = ''
        self.ret_code = ''
        self.hash = Hasher.Hasher()
        self._consistency_check()
# Serve the client
    def run( self ):
        self.client.send(b'220 FTPnetwork\r\n')
        while True:
        # Get input from the client
            self.cli_inpt = self._get_raw_inpt()
            print( "Client says: ", self.cli_inpt.decode() ) 
            if not self.cli_inpt:
                break
            self.curr_cmd = self._get_cmd( self.cli_inpt )
            self.network.cmd_req = self.curr_cmd
        # Send the client's input to the network
            if self.curr_cmd == "list" or self.curr_cmd =="retr":
                self.network.net_send(self.cli_inpt, self._localhost())
            else:
                self.network.net_send(self.cli_inpt, self.network.servers)
        # Handling special commands
            if self.curr_cmd == "user":
                self.user = self.cli_inpt[5:].decode().strip()
            elif self.curr_cmd == "quit":
                self.client.close()
                break 
            elif self.curr_cmd == "epsv":
                self.EPSV = True;
            elif self.curr_cmd == "stor":
                self.filename = self.user + "/" + self.cli_inpt[5:].decode().strip()
                net_inpt = self._STOR()
            elif self.curr_cmd == "list" or self.curr_cmd == "retr":
                net_inpt = self._LISTRETR()
            if self.curr_cmd == "stor" or self.curr_cmd == "list" or self.curr_cmd =="retr":
                self.EPSV = False
                self.send_client( net_inpt)
                print("Network says: " + net_inpt.decode())
        # Get input from network and send to client 
            net_inpt = self.network.net_recv( self.network.servers )
            print( "Network says: ", net_inpt.decode() ) 
            self.ret_code = self.network.get_code( net_inpt )
            self.send_client( net_inpt )
           


# Check consistency of server with others on network
    def _consistency_check( self ):
        DEBUG("_consistency_check: Server started consistency check")
        threshold = round( self.network.size() * CONSISTENCY_THRESHOLD )
        DEBUG("_consistency_check: networks size = " + str( self.network.size() ) + ". threshold = " +str(threshold) )
        network_hashes = self.get_hashes()
        for server_hash in network_hashes:
            if self.hash.isEqual( server_hash[1] ) == False:
                threshold -= 1
    # Server is consistent
        if threshold > 0:
            DEBUG("_consistency_check: Server found to be consistent")
            return
    # Server is not consistent
        DEBUG("_consistency_check: Server found to be not consistent")
        occurrences_list = []
        for hsh in network_hashes:
            occurrences = len( [h[1] for h in network_hashes if h[1] == hsh[1]] )
            occurrences_list.append(  ( hsh[0], occurrences) )
        max_occur = max( occurrences_list, key=lambda tup: tup[1] )
        DEBUG("_consistency_check: Updating from the server:" + max_occur[0])
        self._not_consistent( [ self.network.get_server_sock( max_occur[0] ) ] )
        return
    


# Update all server files
    def _not_consistent( self, server_sock ):
        rmtree("user_files")
        mkdir("user_files")
        DEBUG("_not_consistent: Cleaned directory user_files")
        self.network.net_send(b"USER guest\r\n", server_sock)
        self.network.net_recv( server_sock )
        self.network.net_send(b"PASS guest\r\n", server_sock)
        net_inpt = self.network.net_recv( server_sock )
        DEBUG("_not_consistent: Logged in as guest")
        if self.network.get_code( net_inpt ) != "230":
            print("_not_consistent: Failed to login as guest. Aborting.")
            exit()
        files = self._get_files_list( server_sock )
        DEBUG("_not_consistent: Got files list to retrieve: " + str(files))
        for f in files:
            self._get_file( f, server_sock )
            DEBUG("_not_consistent: Updated the file " + f)



    def _get_files_list( self, server_sock ):
        self.network.net_send(b"EPSV\r\n", server_sock)
        self.network.cmd_req = "epsv"
        net_inpt = self.network.net_recv( server_sock )
        self.network.cmd_req = ""
        if self.network.get_code( net_inpt ) != "229":
            print("_get_files_list_: failed with epsv. Aborting")
            exit()
        self.network.net_send(b"LIST\r\n", server_sock)
        self.network.net_recv( server_sock )
        fList = self.network.clean_data_buffers()
        self._read_226( server_sock )
        files_list_full = fList.decode().split("\n")[:-1]
        files_list_clean = list()
        DEBUG("_get_files_list: got full files list: " + str(files_list_full) )
        for f in files_list_full:
            files_list_clean.append( f.split()[-1] )
        return files_list_clean




    def _get_file( self, filename, server_sock ):
        self.network.net_send(b"EPSV\r\n", server_sock)
        self.network.cmd_req = "epsv"
        self.network.net_recv( server_sock )
        self.network.cmd_req = ""
        self.network.net_send(b"RETR " + filename.encode() + b"\r\n", server_sock)
        self.network.net_recv( server_sock )
        file_data = self.network.clean_data_buffers()
        self._read_226( server_sock )
        with open( "user_files/" + filename, "w" ) as f:
            f.write( file_data.decode() )
    


# Get all server hashes on the EXTERNAL network
    def get_hashes( self ):
        self._anon_login()
        external = self._external_hosts()
        self.network.net_send( b"EPSV\r\n", external )
        self.network.cmd_req = "epsv"
        self.network.net_recv( external )
        self.network.cmd_req = ""
        self.network.net_send( b"RETR ServerHash.txt\r\n", external )
        self.network.net_recv( external )
        hashlist = self.network.get_hash_list()
        self._read_226( external )
        return hashlist



# Login to all servers on network as anonymous
    def _anon_login( self ):
        self.network.net_send(b"USER anonymous\r\n")
        net_inpt = self.network.net_recv( self.network.servers )
        if self.network.get_code( net_inpt ) != "331":
            print("Consistency check failure. anonymous user denied by server.")
            return
        self.network.net_send(b"PASS anonymous\r\n")
        net_inpt = self.network.net_recv( self.network.servers )
        if self.network.get_code( net_inpt ) != "230":
            print("Consistency check failure. anonymous user denied by server.")
            return
        return





#  Clean all data buffers of the external servers and return the local server output
    def _LISTRETR( self ):
        localhost = self._localhost()
        
        local_inpt = self.network.net_recv( localhost )
        code = self.network.get_code( local_inpt )
         
        self.network.close_data_connections()
        return local_inpt
    


# Wait for 226 from the local server. Then send the file to the rest of the network.
    def _STOR( self ):
        localhost = self._localhost()
        external = self._external_hosts()
        
        local_inpt = self.network.net_recv( localhost )
        code = self.network.get_code( local_inpt )
        if code == "226":
            self.network.send_to_data_connection( self.filename )
        else:
            return b"421 local server did not recieve the file"
        self._read_226( external )
        return local_inpt
   

# Send raw data to client's control connection
    def send_client( self, raw_data ):
        try:
            self.client.send( raw_data )
        except( socket.gaierror, socket.timeout ):
            print("The client has suddenly died")
            exit()


# Recieve raw data from the client's control connection
    def _get_raw_inpt( self ):
        try:
            inpt = self.client.recv( 256 )
        except (socket.timeout) as e:
            print("Client is dead")
            inpt = ''
        return inpt


# Extract the command from the client's raw input
    def _get_cmd( self, raw_inpt ):
        if not raw_inpt:
            return ''
        return raw_inpt[:4].decode().strip().lower()


# Return a list containing only the local FTP server socket
    def _localhost( self ):
        return [server for server in self.network.servers if server.getpeername()[0]=='127.0.0.1']



# Return a list containing all but not the local FTP server sockets
    def _external_hosts( self ):
        return [server for server in self.network.servers if server.getpeername()[0]!='127.0.0.1']


# Receive input from all external servers after a data command was completed, and check that they all sent 226 as the return code.
    
    def _read_226( self, servers ):
        servers_respone = self.network.net_recv( servers )
        codes = [ s for s in servers_respone.split() if s.isdigit() ]
        if codes.count( b'226' ) != len( codes ):
            print("Not all servers returned 226")



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
    Proxy = ProxyServer(6000)
    Proxy.serve()
