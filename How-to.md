##How-to

First, make sure that you have installed pyftpdlib using python3-pip.

To install python3-pip run:```sudo apt-get install python3-pip```.

To install pyftpdlib run: ```pip3 install pyftpdlib==1.5.1```.

To join a network and start sharing files:<br>
1. Add IP addresses of servers in the network to the file ```PEERS.txt```, seperated by newline: <br>
<br>
![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo1.png)
<br>
<br>
2. Run ```Server.py```<br>
3. Connect to the server using telnet(or any other client):<br>```telnet 127.0.0.1 6000```
<br>
3. After recieveing the 220 return code, login as a guest by sending the FTP commands:<br>
  ```USER guest```

  ```PASS guest```

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo4.png)
<br>
<br>
By default, only one user is available in the network, and all files reside in the shared directory: ```user_files```. <br>
4. Now it's possible to send FTP commands such as: <br>
```CWD``` - Get the current working directory <br>
```DELE myfile.txt``` - Delete a file named myfile.txt <br>
```NETS``` - Get the size of the active network. It's not part of the FTP protocol(we added this command). <br>

FTP commands can be divided into two types:<br>
- commands that make use of the data connection.
- commands that don't make use of the data connection.

To use a command of the first type, such as:<br>
```RETR myfile.txt``` - Retrieve a file named myfile.txt <br>
```STOR newfile.txt``` - Store a new file named newfile.txt <br>
```LIST``` - List the contents of the shared directory <br>
There must be a data connection open. <br>
To open a data connection, the client needs to send the ```EPSV``` command.
![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo6.png)
<br>
<br>
Then, the server responds with a port number for the data connection, and then the client should connect(using telnet again, for example).<br>
![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo5.png)
<br>
<br>
Note that data connections are disposable and therefore need to be opened before each command of the first type.<br>

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo3.jpg)
<br><br>
