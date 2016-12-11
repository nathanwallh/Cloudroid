#!/usr/bin/python3
class FtpNet:
    def __init__( self, netfile ):
        f = open( netfile, 'r' )
        addr = f.read().split()
        self.addresses = [ (address.split(':')[0],int(address.split(':')[1])) for address in addr ]
        self.current = 0;

    def __iter__( self ):
        return self
    
    def __next__(self):
        if self.current >= len( self.addresses ):
            raise StopIteration
        else:
            self.current += 1
            return self.addresses[ self.current - 1 ]
        
