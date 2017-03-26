# How-to

## Requirements
Cloudroid uses the pyftpdlib library with python 3, which is installed via python3-pip.

To install python3-pip, run: ```sudo apt-get install python3-pip```.

Then to install pyftpdlib, run: ```pip3 install pyftpdlib==1.5.1```.

## Guide

1. Add IP addresses of servers in the network to the file ```PEERS.txt```, seperated by newline:
![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo1.png)


2. Run ```Server.py```


3. Connect to the server using telnet(or any other client): ```telnet 127.0.0.1 6000```


4. After recieveing the 220 return code, login as a guest by sending the FTP commands:

  ```USER guest```
  
  ```PASS guest```

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo4.png)




By default, only one user is available in the network, and all files reside in the shared directory: ```user_files```.


5. Now it's possible to send FTP commands such as:


```CWD``` - Get the current working directory

```DELE myfile.txt``` - Delete a file named myfile.txt

```NETS``` - Get the size of the active network. It's not part of the FTP protocol(we added this command).

More FTP commands can be found on wikipedia.

### Data connection

FTP commands can be divided into two types:

- commands that make use of the data connection.
- commands that don't make use of the data connection.

To use a command of the first type, such as:

```RETR myfile.txt``` - Retrieve a file named myfile.txt

```STOR newfile.txt``` - Store a new file named newfile.txt

```LIST``` - List the contents of the shared directory 

There must be a data connection open. 

To open a data connection, the client needs to send the ```EPSV``` command.

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo6.png)


Then, the server responds with a port number for the data connection, and then the client should connect(using telnet again, for example).

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo5.png)



Note that data connections are disposable and therefore need to be opened before each command of the first type.

![alt tag](https://raw.githubusercontent.com/nathanwallh/Cloudroid/master/images/demo3.jpg)
