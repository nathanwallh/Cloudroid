#!/usr/bin/python3

# Proxy server that redirects FTP traffic to the right
# computer on the network.

# Technical:
# The proxy server listens on port 6000, while the FTP
# server listens on port 8000.
# The first server to run should be the FTP server( Server.py )
# Then, after running the proxy, an FTP client can make a 
# connection through port 6000 and then things run as usual.

DEBUG_val = False
def DEBUG(s):
    if DEBUG_val == True:
        print(s)

import threading
import socket
import FtpNet



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

# Serve the client
    def run( self ):
        self.client.send(b'220 FTPnetwork\r\n')
        while True:
        # Get input from client and send to network
            self.cli_inpt = self._get_raw_inpt()
            print( "Client says: ", self.cli_inpt.decode() ) 
            self.network.net_send(self.cli_inpt)
            if not self.cli_inpt:
                break
            self.curr_cmd = self._get_cmd( self.cli_inpt )
            self.network.cmd_req = self.curr_cmd
            
        # Get input from network and send to client 
            net_inpt = self.network.net_recv( self.network.servers )
            print( "Network says: ", net_inpt.decode() ) 
            self.ret_code = self.network.get_code( net_inpt )
            self.send_client( net_inpt )
           
        # Handling special cases
            if self.curr_cmd == "user":
                self.user = self.cli_inpt[5:].decode().strip()
            elif self.curr_cmd == "quit":
                self.client.close()
                break
            elif self.curr_cmd == "epsv":
                self.network.make_data_connections()
            elif self.curr_cmd == "stor":
                self.filename = self.user + "/" + self.cli_inpt[5:].decode().strip()
                net_inpt = self._STOR()
                print("Network says:" + net_inpt.decode())
                self.send_client( net_inpt )
#            elif cmd == "list":
#                self._LIST()
#            elif cmd == "retr":
#                self._RETR() 
#            elif cmd == "epsv":
#               self._EPSV()


# Wait for 226 from the local server. Then send the file to the rest of the network.
    def _STOR( self ):
        localhost = [server for server in self.network.servers if server.getpeername()[0]=='127.0.0.1']
        external = [server for server in self.network.servers if server.getpeername()[0]!='127.0.0.1']
        local_inpt = self.network.net_recv( localhost )
        code = self.network.get_code( local_inpt )
        if code == "226":
            self.network.send_data( self.filename )
        else:
            return b"421 local server did not recieve the file"
        DEBUG("Proxy._STOR: starting to read responses from servers")
        ext_respone = self.network.net_recv( external )
        DEBUG("Proxy._STOR: finished reading respones from servers")
        code_ext = [ s for s in ext_respone.split() if s.isdigit() ]
        if code_ext.count( b'226' ) != len( code_ext ):
            print("Not all servers recieved the file")
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
