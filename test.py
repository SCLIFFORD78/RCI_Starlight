import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
host = '127.0.0.1'
port = 10071
print (sys.stderr, 'connecting to %s' % host)
sock.connect((host, port))
#sock.connect_ex(server_address)
try:
    
    # Send data
    message = b'\x20\x00\x00\x00\x00'
    length = len(message)
    #byteLength = length.to_bytes(2,'big')
    print (sys.stderr, 'sending "%s"' % message)
    sock.sendall(message,0)
    

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
  
    data = sock.recv(1024)
    print (sys.stderr, 'received "%s"' % data)

finally:
    print (sys.stderr, 'closing socket')
    sock.close()