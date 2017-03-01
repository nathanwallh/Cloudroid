##How-to
To join a network and start sharing files:<br>
1. Add IP addresses of servers in the network to the file **PEERS.txt**: <br>
<br>
![alt tag](http://sites.hevra.haifa.ac.il/rbd/wp-content/uploads/sites/63/2017/02/demo1.png)
<br>
<br>
2. Run **Server.py**<br>
3. Connect to the server using telnet(or any other client):<br>
**telnet 127.0.0.1 6000**<br>
3. After recieveing the 220 return code, login as a guest by sending the FTP commands:<br>
  **USER guest <br>
  PASS guest**<br>
By default, only one user is available in the network, and all files reside in the shared directory: "user_files". <br>
4. Now it's possible to send FTP commands such as: <br>
**CWD** - Get the current working directory <br>
**DELE myfile.txt** - Delete a file named myfile.txt <br>
**NETS** - Get the size of the active network. It's not part of the FTP protocol(we added this command). <br>
<br><br>

Note that FTP commands can be divided into two types: 
commands that make use of the data connection, and commands that don't.<br>

To use a command of the first type, such as:
**RETR myfile.txt** - Retrieve a file named myfile.txt <br>
**STOR newfile.txt** - Store a new file named newfile.txt <br>
**LIST** - List the contents of the shared directory <br>
There must be a data connection open. <br>

To open a data connection, the client needs to send the command:
**EPSV**
Then, the server responds with a port number for the data connection, and then the client should connect(using telnet again, for example).<br>
Note that data connections are disposable and therefore need to be opened before each command of the first type.<br>


