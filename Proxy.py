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
    
    # Serving the client
    def run( self ):
        self.client.send(b'220 FTPnetwork\r\n')
        while True:
            # Get input from client and send to network
            cli_inpt = self._get_raw_inpt()
            print( "Client says: ", cli_inpt.decode() ) 
            self.network.net_send(cli_inpt)
            if not cli_inpt:
                break
            cmd = self._get_cmd( cli_inpt )
            self.network.curr_cmd = cmd
            
            # Get input from network and send to client 
            net_inpt = self.network.net_recv()
            print( "Network says: ", net_inpt.decode() ) 
            self.client.send( net_inpt )
            if not net_inpt:
                break
            code = net_inpt.decode().split()[0]
            
            self.network.curr_cmd = ''
            if code == "221":
                self.client.close()
                break;
            
            # Code 125 
            elif code == "125":
                net_inpt = self.network.net_recv()
   
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
        return raw_inpt[:3].decode().strip()


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
