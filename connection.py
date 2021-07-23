import socket
import sys
import RCIcommands
import RCIdata

# Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#host = '192.168.1.20'
#port = 10071
#print (sys.stderr, 'connecting to %s' % host)
#sock.connect((host, port))
#sock.connect_ex(server_address)
while True:


    print(RCIcommands.connect('localhost', 10071))
    print (RCIcommands.host)
    status = RCIcommands.status()
    print (status)
    #print (RCIcommands.disconnect())
    #print(RCIcommands.connect('localhost', 10071))
    start = RCIcommands.start()
    print (start)
    #print (RCIcommands.status())
    #start = RCIcommands.start()
    #print (start)
    #print (RCIcommands.status())
    print (RCIcommands.stop())
    #print (RCIcommands.status())
    print (RCIcommands.getJobs())
    #print (RCIcommands.queryJob('OemSimulatorJob'))
    print(RCIcommands.loadJob('OemSimulatorJob'))
    #print(RCIdata.connect('localhost',10072))
    #print(RCIdata.getFifo())
    #print(RCIdata.sendDataRecord('blank.bmp,,,,',44))

    
  
    

#finally:
    #print (sys.stderr, 'closing socket')
    #sock.close()