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


    print(RCIcommands.connect('192.168.1.111', 10071))
    print (RCIcommands.host)
    status = RCIcommands.status()
    print (status)
    #print (RCIcommands.disconnect())
    #print(RCIcommands.connect('localhost', 10071))
    #start = RCIcommands.start()
    #print (start)
    #print (RCIcommands.status())
    #start = RCIcommands.start()
    #print (start)
    #print (RCIcommands.status())
    #print (RCIcommands.stop())
    #print (RCIcommands.status())
    print (RCIcommands.getJobs())
    #print (RCIcommands.queryJob('GIS\\RCI job 1'))
    print(RCIcommands.loadJob('GIS\\RCI job 1'))#OemSimulatorJob
    print(RCIcommands.status());
    print(RCIcommands.status());
    print(RCIcommands.status());
    print(RCIcommands.status());
    #print(RCIcommands.jobReload());
    print(RCIdata.connect('192.168.1.111',10072))
    print(RCIdata.getFifo())
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',1))
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',2))
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',3))
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',4))
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',5))
    print (RCIcommands.start())
    print(RCIdata.sendProductConfirmListen(5))
    print(RCIdata.sendDataRecord('blank.bmp,,, , ',1))
    #print(RCIdata.sendDataRecord('blank.bmp,,, , ',4))
    print(RCIdata.sendProductConfirmListen(1))
    print(RCIcommands.queryJob('TestJob3'))

    
  
    

#finally:
    #print (sys.stderr, 'closing socket')
    #sock.close()