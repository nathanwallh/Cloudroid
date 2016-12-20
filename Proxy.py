#!/usr/bin/python3

# Proxy server that redirects FTP traffic to the right
# computer on the network.

# Technical:
# The proxy server listens on port 6000, while the FTP
# server listens on port 8000.
# The first server to run should be the FTP server( Server.py )
# Then, after running the proxy, an FTP client can make a 
# connection through port 6000 and then things run as usual.


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

    # Serving the client
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
            net_inpt = self.network.net_recv()
            print( "Network says: ", net_inpt.decode() ) 
            self.ret_code = self.network.get_code( net_inpt )
            self.send_client( net_inpt )
            
            if self.curr_cmd == "user":
                self.user = self._get_username( self.cli_inpt )
            elif self.curr_cmd == "quit":
                self.client.close()
                break
            elif self.curr_cmd == "stor":
                local_inpt = self._STOR()
                print("Local server says:" + local_inpt.decode())
                self.send_client( local_inpt )
#            elif cmd == "list":
#                self._LIST()
#            elif cmd == "retr":
#                self._RETR() 
#            elif cmd == "epsv":
#               self._EPSV()

    def _get_filename( self, raw_data ):
        if not raw_data:
            return ''
        return raw_data[5:].decode()

    def _STOR( self ):
        local_inpt = self.network.local_recv()
        code = self.network.get_code( local_inpt )
        self.filename = self.user + "/" + self._get_filename( self.cli_inpt )
        if code == "226":
            self.network.send_data( self.filename )
        return local_inpt
   
    
    def send_client( self, raw_data ):
        try:
            self.client.send( raw_data )
        except( socket.gaierror, socket.timeout ):
            print("The client has suddenly died")
            exit()


    def _get_username( self, raw_inpt ):
        return raw_inpt.decode().split()[1]


    def _get_raw_inpt( self ):
        try:
            inpt = self.client.recv( 256 )
        except (socket.timeout) as e:
            print("Client is dead")
            inpt = ''
        return inpt

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
