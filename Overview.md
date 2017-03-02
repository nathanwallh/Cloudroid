## Protocol overview
A "Cloudroid" server consists of 2 processes running together: <br>
<li>FTP server - Taken from the pyftpdlib library. <br>
<li>Proxy server - Implemented by us. <br>
The FTP server works in the background while the proxy server works in the front. The proxy accepts clients connections, broadcasts traffic to the network, and multiplexes replies to the client.<br>
When a client connection is made, the proxy server connects to all FTP servers on the network. These servers are listed in the file PEERS.txt.<br>
Therefore, the network can be diagrammed as follows:
![alt tag](images/diagram.png)


<p>
It should be noted that connections between proxy servers and FTP servers(or equivalently: between FTP clients and FTP servers), actually consist of 2 different connections:<br>
<li>Control connection.<br>
<li>Data connection.<br>
This is a inherent part of the FTP protocol that the proxy server must take care of.<br>
The control connection is used to send FTP commands and recieve return codes, while the data connection is used to send and recieve data(e.g: when sending files).<br>
Data connections are opened for client requests and they are disposable. For each session, many data connections might be opened and closed, but the control connection remain.<br>
The proxy server deals with it by creating data connection with all FTP servers in the network except of the local FTP server. The data connection of the local FTP server is redirected back to the client.<br>
Therefore, when the client exchanges data with the network, he actually exchanges it with one server only. When he finishes, the proxy server uses it's own data connections with other servers to broadcast<br>
the data to the network.<br>
</p>
<p>
Another important aspect of the protocol is a consistency check procedure that runs every time a new session with client begins.<br>
This procedure ensures that the files in the shared directory of one server will be the same files in the shared directory of other servers in the network.<br>
To decide if a server is consistent or not, a special parameter named CONSISTENCY_THRESHOLD is defined. It is a number between 0 to 1, that gives the percentile of servers allowed to differ<br>
from the server under check.
The consistency check procedure is using hashes of files(that get stored in the ServerHash.txt file) to compare them.<br>
</p>


