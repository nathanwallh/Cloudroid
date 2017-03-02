##Known issues and future development:
There are several issues that we know of, and think that they should be fixed:


1. If the client wants to run FTP commands that use the data connection(e.g STOR), he must be running a server on the same machine.
   The reason for it is that the control connection and data connection must be, according to the FTP protocol, between the same  machines.
   
   But in the Cloudroid protocol, the control connection is between proxy server and FTP server, while the data connection is between the client and the FTP server.
   
   There are two possible solutions for this problem:
   - The trivial solution is to let the proxy server "hijact" the data connection too, not only the control connection.
     This way, when the proxy recieves an EPSV command, it should create data connections with all FTP servers(including the local FTP server). Then, it should listen on a random port and
     send it back to the client.

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
   
   The best thing to do is to write it again in a cleaner and faster way.

4. Security was not taken care of in the protocol, but it should be. Possibly, using SFTP instead of FTP.
