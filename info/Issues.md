## Known issues and future development:

1. If the client wants to run FTP commands that use the data connection(e.g STOR), he must be running a server on the same machine.
   The reason for it is that the control connection and data connection must be, according to the FTP protocol, between the same  machines.
   But in the Cloudroid protocol, the control connection is between proxy server and the FTP server, while the data connection is between the client and the FTP server.
   
   There are two possible solutions for this problem:
   - The most straight forward solution is to use the proxy as an intermediary between the client and the server for the data connection too, not only for the control connection.

   - A second possible solution, which is better in our opinion, is to develop an FTP server from scratch that doesn't stick fully to the FTP protocol, and allows data connections with different
     machines.
     
     The reason for why this solution seems better, is that in future, there might be more constraints coming from the FTP protocol, and this solution will make it possible to fix them all. Also, at some point we might want to change the protocol and abandon the current FTPserver-Proxy model.

2. There are problems with the consistency check procedure:
   - It's slow.
   - It doesn't check subdirectories recursively.
   - It works only in the beggining of a session while it should be running in specified time intervals.
   - The code is dirty.
   
   The best thing to do is to write it again form the beginning and adding improvments to it.

3. Security was not taken care of in the protocol, but it should be. Possibly, using SFTP instead of FTP.
