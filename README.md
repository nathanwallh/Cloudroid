Cloudroid
=========
##How-to use
To join a network and start sharing files:<br>
1. Add IP addresses of servers in the network to the file **PEERS.txt**:<br>
<img>demo1.png</IMG> <br>
2. Run **./Server.py ** command<br>
3. Connect to the server using telnet(or any other client):<br>
**telnet 127.0.0.1 6000** command <br>
3. **After** recieveing the 220 return code, login as a guest:<br>
  **USER guest <br>
  PASS guest**<br>
By default, only one user is available in the network, and all files reside in the shared directory: "user_files". <br>
4. Now it's possible to send FTP commands such as: <br>
**CWD** command - Get the current working directory
**DELE myfile.txt** command - Delete a file named myfile.txt
**NETS** command- Get the size of the active network. It's not part of the FTP protocol and was added by us.

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/embed/VlxFEtmz39s)




## Project for the RBD lab, Haifa University.
