## Protocol overview

### Basics
A "Cloudroid" server consists of 2 processes running together: <br>
- FTP server - Taken from the pyftpdlib library. <br>
- Proxy server - Implemented by us. <br>
The FTP server works in the background while the proxy server serves clients. The tasks of the proxy server are to accept clients connections, broadcast traffic(client requests) to the network, and to multiplex replies to the client.<br>
When a client connection is made, the proxy server connects to all FTP servers on the network.

Before we can fully describe the Cloudroid protocol, we'd like to overview a major concept of the FTP protocol.

### The data connection
It should be noted that connections between proxy servers and FTP servers(or equivalently: between FTP clients and FTP servers), actually consist of 2 different connections:<br>
- Control connection.<br>
- Data connection.<br>
This is a inherent part of the FTP protocol that the proxy server must take care of.<br>
The control connection is used to send FTP commands and recieve return codes, while the data connection is used to send and recieve data(e.g sending files).<br>
Data connections are opened when the client requests them using the FTP command: ```EPSV```. They are disposable, which means that they need to be opened again for each command that needs them.

### The Cloudroid protocol
- The proxy server listens to client connections. When a connection is made:
    1. The proxy reads addresses of other servers in the network from the file ```PEERS.txt```, and creates FTP connections with them and with the local FTP server( address 127.0.0.1 ). Failed connections are to be prompted.
    2. Then it initiates the consistency check procedure(that will be explained later), and sends the success code the client.
- FTP commands sent by the client, are broadcasted to the network by the proxy server.
- Replies from the FTP servers are immediately collected by the proxy, then they are checked for errors and sended to the client as one reply(multiplexed).
- EPSV requests for data connection by the client are dealt by the proxy in the following way:
    1. The proxy broadcasts the EPSV command to all FTP servers in the network.
    2. Then it creates data connections with all sFTP ervers, except of the local FTP server.
    3. The reply of the local FTP server(which is, a open port) is sent back to the client, so that he can create a data connection with the local server.
- Commands that user the data connection, such as STOR, are not being treated as regular FTP commands. Instead, when such command(STOR) is identified:
    1. The proxy server broadcasts it normally, and then waits for the "Transfer finished" return code(226) of the local FTP server.
    2. Then it sends the file that have just been recieved to all other FTP servers in the network.
- LIST and RETR are dealt in a much simpler way. No need to send files over the data connections.
- The proxy is multithreaded, so it can server multiple clients at the same time.

#### A diagram of the network:
![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/Diagram1.png)


### The consistency check procedure
This procedure ensures that the files in the shared directory of one server will be the same files in the shared directory of other servers in the network.<br>
To decide if a server is consistent or not, a special parameter named ```CONSISTENCY_THRESHOLD``` is defined. It is a number between 0 to 1, that gives the percentile of servers allowed to differ 
from the local server.<br>
To check the difference between local server and the network, the procedure is using FTP to retrieve the checksum of ``` user_files ```
from all servers. Then, it compares them to the local hash.
Checksums are stored in the file ``` ServerHash.txt ```.
If the server is found to be not consistent with most peers, the procedure deleted all files and retrieves the files of another  consistent server in the network.






