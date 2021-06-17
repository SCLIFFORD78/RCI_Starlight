import socket
import sys
import commands
import data

# Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
#host = '192.168.1.20'
#port = 10071
#print (sys.stderr, 'connecting to %s' % host)
#sock.connect((host, port))
#sock.connect_ex(server_address)
while True:


    print(commands.connect('localhost', 10071))
    print (commands.host)
    status = commands.status()
    print (status)
    #print (commands.disconnect())
    #print(commands.connect('localhost', 10071))
    start = commands.start()
    print (start)
    #print (commands.status())
    #start = commands.start()
    #print (start)
    #print (commands.status())
    print (commands.stop())
    #print (commands.status())
    print (commands.getJobs())
    print(commands.loadJob('OemSimulatorJob'))
    #print(data.connect('localhost',10072))
    #print(data.getFifo())
    #print(data.sendDataRecord('blank.bmp,,,,',44))

    
  
    

#finally:
    #print (sys.stderr, 'closing socket')
    #sock.close()