Cloudroid
=========
##How-to use
To join a network and start sharing files:<br>
1. Add IP addresses of servers in the network to the file **PEERS.txt**: <br>
<br>
![alt tag](http://sites.hevra.haifa.ac.il/rbd/wp-content/uploads/sites/63/2017/02/demo1.png)
<br>
<br>
2. Run **./Server.py** command<br>
3. Connect to the server using telnet(or any other client):<br>
**telnet 127.0.0.1 6000** command <br>
3. **After** recieveing the 220 return code, login as a guest:<br>
  **USER guest <br>
  PASS guest**<br>
By default, only one user is available in the network, and all files reside in the shared directory: "user_files". <br>
4. Now it's possible to send FTP commands such as: <br>
**CWD** command - Get the current working directory <br>
**DELE myfile.txt** command - Delete a file named myfile.txt <br>
**NETS** command- Get the size of the active network. It's not part of the FTP protocol and was added by us. <br>
<br><br>

###FTP commands can be divided into two types: 

commands that make use of the data connection, and commands that don't.<br>
To use a command of the first type, such as:
**RETR myfile.txt** - Retrieve a file named myfile.txt <br>
**STOR newfile.txt** - Store a new file named newfile.txt <br>
**LIST** - List contents of the directory <br>
There must be a data connection open. <br>

###To open a data connection, the client needs to send the command:
**EPSV** Then, the server responds with a port number for the data connection, and then the client can open the data connection(using telnet again, for example).<br>
Note that data connections are disposable and therefore need to be opened before each command of the first type.<br>

## Youtube video
[![Everything Is AWESOME](http://www.interload.co.il/upload/7847117.png)](https://www.youtube.com/watch?v=VlxFEtmz39s)

##Known issues and future development:
1. If the client wants to run FTP commands that use the data connection(e.g STOR), he must be running a server on the same machine.br>
   The reason for it is that the control connection and data connection must be, according to the FTP protocol, between the same  machines. But in the Cloudroid protocol, the control connection is between proxy server and FTP server, while the data connection is between the client and the FTP server.
   There are two possible solutions for this problem:
   - The trivial solution is to let the proxy server "hijact" the data connection too, not only the control connection.
     When the proxy recieves an EPSV command, it should create data connections with all FTP servers(including the local FTP server). Then, it should listen on a random port and
     send it back to the client. The data on this new connection should be broadcasted on all data connections.
   - A second possible solution, which is better in our opinion, is to write an FTP server that doesn't stick fully to the FTP protocol, and allows data connections with different
     machines.
     The reason why this solution seems better, is that in future, there might be more constraints coming from the FTP protocol, and this solution will make it possible to fix them all.

2. FTP commands are a little bit slow when there are many servers in the network. This problem is probably due to the commands passing through the proxy server first.
   It can be solved using the second solution for the first problem. Ideally, the proxy server and the FTP server are combined into a single server program. Therefore, writing an FTP server
   that doesn't stick fully to the FTP protocol can be useful in doing so.
   
3. The consistency check procedure has several issues that need to be taken care of:
   - It's slow.
   - It doesn't check subdirectories recursively.
   - It works only in the beggining of a session while it should be running in specified time intervals.
   The best thing to do is to write it again, but only after solving the first 2 issues we listed.

4. Security was not taken care of in the protocol, but it should be. Possibly, using SFTP instead of FTP.
