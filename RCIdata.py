import sys
import socket
import binascii

host = '192.168.1.20'
port = 10072

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reply from starlight on message sent
def messageRecieved(message):
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(4096)
        amount_received += len(data)
        print (sys.stderr, 'received %s' % data)
    return data

#convert string to hex
def toHex(s):
    lst = []
    str = b''
    for ch in s:
        hv = hex(ord(ch))
        if len(hv) > 1:
            hv = hv.replace('0x','\\x')
        lst.append(hv)
    for i in range(len(lst)):
        str = str + lst[i]
    return str

def check_hex_length(decimal_number):
    hex_number = '\\x' + hex(decimal_number) # hex_number now contains your number as hex.
    return (len(hex_number) - 2) == 16



#This command is sent on port 2. This command is used to ask how many records can be sent to the buffer of the controller.
def getFifo (): 
    message = b'\x60\x00\x00\x00\x00'
    fifo = 0

    sock.sendall(message,0)

    data = messageRecieved(message)
    byte = []
    for i in range(len(data)):
        byte.append('0x'+ binascii.hexlify(data[i]))

    fifo = int(byte[5],16)
    return fifo

#This command is sent on port 2. This command is used to send data. 
# Bitmaps can be printed by downloading them into a defined directory
#on the Editor Starlight and sending the name as a text. In the controller the bitmaps must be setup as variable printing.
#For single layouts the number of data is the count of fields in one data record. For step & repeat layouts is the number of data
def sendDataRecord (dataRecord,id): 
    print(dataRecord)
    fields = []
    fieldCount = 0
    field = ""
    dataRecord = '\"' + dataRecord + '\"'
    for i in range(len(dataRecord)):
        if dataRecord[i] != ",":
            field += dataRecord[i] 
        if dataRecord[i] == "," or i == len(dataRecord)-1:
            fields.append(field)
            field = ""
            fieldCount +=1
            if i == len(dataRecord):
                field = '  '
                fields.append(field)
                field = ""
                fieldCount +=1
    for i in range(len(fields)):
        if len(hex(len(fields[i])).replace('0x',b'\\x'))==3:
            field = field + hex(len(fields[i])).replace('0x','\\x0')+ '\\x00' + toHex(fields[i])
        else:
            field = field + str(hex(len(fields[i])).replace('0x','\\x'))+ '\\x00' + toHex(fields[i])
    field = field.lstrip(' ')

    print(field)
    #rtnMessage = b'\x22\x01\x00\x00\x00\x00'
    messageLength = b''
    message = b'\\x00\\x00\\x00'
    messageId = b''
    if len(hex(id).replace('0x',b'\\x'))==3:
        messageId =hex(id).replace('0x','\\x0')
    else:
        messageId = hex(id).replace('0x','\\x')
    message1 = b'\\x00\\x00\\x00'
    message2 = messageId+message1+field
    message3 = bytes(message2).decode('unicode-escape').encode('ISO-8859-1')
    messageLength = hex(len(message3)).replace('0x','\\x61\\x')
    message4 = messageLength +message +  message2
    hexMessageLength = bytes(message4).decode('unicode-escape').encode('ISO-8859-1')

    print(field)


    sock.sendall(hexMessageLength,0)
    
    data = messageRecieved(message)
    byte = []
    for i in range(len(data)):
        byte.append('0x'+ binascii.hexlify(data[i]))
    resp = {'0x00':'Data accepted', '0x01':'Data refused, Buffer overflow','0x02':'Data refused, too little data fore number of fields', '0x03':'Data refused, too big data for number of fields','0x04':'Data accepted, but step and repeat not complete'}
    if len(byte)==14:
        for item in resp.keys():
            if byte[13] == item :
                
                return {'id':int(byte[4],16), 'fifo space':int(byte[9],16), 'Response':resp[item]}
        else:
            return {'Error':'Error'}
        
    
 
    
def connect(host, port):
    message = False
    try:
        connection = sock.getsockname()
        print(connection[0])
        message =  True
        
    except socket.error :
        message = False
        print ("No Connection");
    try:
        sock.connect((host, port))
        test = sock.getsockname()
        print (sys.stderr, 'connecting to %s' % host)

        message =  True
    except socket.error:
        message = False
        print ("Error connecting")
    return message

def disconnect ():
    message = ""
    conn = False
    try:
        connection = sock.getsockname()
        print(connection[0])
        print( "Connected on " + connection[0])
        message = "Connected on " + connection[0]
        conn = True
    except socket.error :
        print("No Connection")
        message ="No Connection"
        
    if conn:
        try:
            sock.close()
            #time.sleep(15)
            #sock.shutdown(socket.SHUT_RDWR)
            message = "Connection Closed"
        except socket.error:
            message = "Error closing Connection"
    return message

