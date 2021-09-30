import sys
import socket
import binascii
import time
import struct
import json



host = '192.169.1.111'
port = 10071
e = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reply from starlight on message sent
def messageRecieved(message):
    amount_received = 0
    amount_expected = len(message)
    data = sock.recv(4096)
    #while amount_received < amount_expected:
        #data = sock.recv(4096)
        #amount_received += len(data)
        #print (sys.stderr, 'received %s' % data)
    return data

#convert string to hex
def toHex(s):
    lst = []
    str = b''
    for ch in s:
        hv = hex(ord(ch))
        test = len(hv)
        if len(hv) > 1:
            hv = hv.replace('0x','\\x')
        lst.append(hv)
    for i in range(len(lst)):
        str = str + lst[i]
    return str

def check_hex_length(decimal_number):
    hex_number = hex(decimal_number) # hex_number now contains your number as hex.
    return (len(hex_number) - 2) == 16


#Configuration to send status only on request
def config (): 
    message = b'\x19\x01\x00\x00\x00\x00'
    resMessage = b'\x19\x01\x00\x00\x00\x00'
    sock.sendall(message,0)
    
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print (sys.stderr, 'received "%s"' % data)
    if message == data:
        return "configuration OK"
    else:
        return "Configuration error"

# This command is sent to reload the actual loaded job.  
def jobReload (): 
    message = b'\x25\x00\x00\x00\x00'
    jobReloaded = b'\x25\x01\x00\x00\x00\x00'
    jobNotReloaded = b'\x25\x01\x00\x00\x00\x00'
    sock.sendall(message,0)
    
    amount_received = 0
    amount_expected = len(message)
    
    data = messageRecieved(message)
    if data == jobReloaded:
        return True
    elif data == jobNotReloaded:
        return False
    else:
        return False
    
def connect(host, port=10071):
    message = False
    conn = False
    try:
        connection = sock.getsockname()
        print(connection[0])
        message =  True
        conn = True
        
    except socket.error :
        message = False
    if not conn:
        try:
            sock.connect((host, port))
            test = sock.getsockname()
            print (sys.stderr, 'connecting to %s' % host)
            
            message =  True
        except socket.error:
            message = False
        try:
            config()
        except socket.error:
            print( ". Configuration error")
            message = False
    return message
# Gets status of the printer
def status (): 
    resp = {}
    status = {'0x00':'Unknown', '0x01':'Stopped', '0x02':'Running', '0x03': 'Starting', '0x04':'Stopping','0x05':'Loading Job','0x06':'Paused','0x07':'Error', '0x08':'Waiting'}
    messageType = {'0x00': 'Warning' , '0x01':'Error', '0x02':'Status'}
    message = b'\x24\x00\x00\x00\x00'
    resMessage = b'\x19\x01\x00\x00\x00\x00'    
    sock.sendall(message,0)
    
    data = messageRecieved(resMessage)
    byte = []
    for i in range(len(data)):
        #print(data[i])
        byte.append('0x'+ binascii.hexlify(data[i])) 

    if  byte[0] == '0x24':
        for item in status.keys():

            if byte[5] == item:
                #print (status[item])
                resp['Status'] = status[item]
                resp['Messages'] = []
        if len(byte) > 6:
            step = 0
            respMessage = [];
            for i in range(6,len(byte)-3):
                
                if i == 6+step and (step+6) < len(byte):
                    messageText = '';
                    for item in messageType.keys():
                        if byte[i] == item:
                            respMessage.append(messageType[item]);
                    #print(int(byte[7],16))
                    for j in range(i+2,((i+2)+int(byte[i+1],16))):
                        messageText = messageText + data[j];
                    respMessage.append(messageText);
                    step = step + int(byte[i+1],16) + 2 
            resp['Messages'] = respMessage         
                            
        #print(resp)                     
        return resp
    else:
        resp['Status'] = 'Unknown'
        resp['Messages'] = ['Unable to retrieve status, please try again!']
        return resp

#Start message for printer
def start (): 
    message = b'\x20\x00\x00\x00\x00'
    state = status()
    if state['Status'] == 'Stopped'or state['Status'] == 'Paused'or state['Status'] ==  'Waiting' :
        sock.sendall(message,0)
    
        data = messageRecieved(message)
        byte = []
        for i in range(len(data)):
            byte.append('0x'+ binascii.hexlify(data[i])) 
        if byte[5] == '0x00':
            return {'Status':status()['Status'],'Response':'Starting'}
        elif byte[5] == '0x01':
            return {'Status':status()['Status'],'Response':'Production cant be started'}
        else:
            return {'Status':status()['Status'],'Response':'error in comminication'}
    elif state['Status'] == 'Unknown':
        return {'Status':status()['Status'],'Response':'Printer in Unknown State'}
    else:
        return {'Status':status()['Status'],'Response':'Printer already started'}
    
#Stop message for printer
def stop (): 
    message = b'\x21\x00\x00\x00\x00'
    state = status()
    if state['Status'] == 'Running'or state['Status'] == 'Paused'or state['Status'] == 'Starting'or state['Status'] ==  'Waiting' :
        sock.sendall(message,0)
    
        data = messageRecieved(message)
        bytes = []
        for i in range(len(data)):
            bytes.append('0x'+ binascii.hexlify(data[i])) 
        if bytes[5] == '0x00':
            return {'Status':status()['Status'],'Response':'Stopping'}
        elif bytes == '0x01':
            return {'Status':status()['Status'],'Response':'Production cant be stopped'}
        else:
            return {'Status':status()['Status'],'Response':'error in comminication'}
    else:
        return {'Status':status()['Status'],'Response':'Printer already stopped'}
    
#This command is sent on port 1. This command is sent to confirm the number of variable data points expected for a specific job.
def queryJob (job): 
    hexJob = toHex(job)
    returnMessage = b'\x26\x03\x00\x00\x00\x00\x00\x00'
    rtnMessage = {'jobStatus': '', 'dataPoints':0, 'records':0}
    message = b"\\x00\\x00\\x00"
    jobLength = b''
    if len(hex(len(job)).replace('0x',b'\\x'))==3:
        jobLength =hex(len(job)).replace('0x','\\x26\\x0')
    else:
        jobLength = hex(id).replace('0x','\\x26\\x')
    message2 = jobLength+message+hexJob
    message3 = message2.decode('unicode-escape').encode('ISO-8859-1')
    sock.sendall(message3,0)
    data = messageRecieved(returnMessage)
    byte = []
    for i in range(len(data)):
        byte.append('0x'+ binascii.hexlify(data[i])) 
    if byte[5] == '0x01':
        rtnMessage['jobStatus']= 'job does not exist'
        return rtnMessage
    elif byte[5] == '0x00':
        rtnMessage['jobStatus'] = 'job exists';rtnMessage['dataPoints']=int(byte[6],16);rtnMessage['records']=int(byte[7],16)
        return rtnMessage
    else:
        rtnMessage['jobStatus'] = 'Error reading'
        return rtnMessage
        
        
    
    
#This command is sent on port 1. It is used to get the jobs that are available on the controller.
def getJobs (): 
    message = b'\x23\x00\x00\x00\x00'
    sock.sendall(message,0)
    data = messageRecieved(message)
    print (data)
    if(len(data)>4):
        jobs = []
        job=""
        for i in range(5,len(data)):
            if data[i]!='\r' and data[i]!= '\n':
                print(data[i])
                job = job + data[i]
            if data[i]=='\r':
                job.replace('\n','')
                jobs.append(job)
                job=""
        return jobs
    else:
        return ["No Jobs"]
    
#This command is sent on port 1. It is used to load a job on the controller.
def loadJob (job): 
    hexJob = toHex(job)
    rtnMessage = b'\x22\x01\x00\x00\x00\x00'
    message = b"\\x00\\x00\\x00"
    
    jobLength = b''
    if len(hex(len(job)).replace('0x',b'\\x'))==3:
        jobLength =hex(len(job)).replace('0x','\\x22\\x0')
    else:
        jobLength = hex(id).replace('0x','\\x22\\x')
    message3 = jobLength+message+hexJob
    message2 = message3.decode('unicode-escape').encode('ISO-8859-1')
    state = status()
    if state['Status'] == 'Stopped'or state['Status'] == 'Unknown' :
        sock.sendall(message2,0)
    
        data = messageRecieved(rtnMessage)
        byte = []
        for i in range(len(data)):
            byte.append('0x'+ binascii.hexlify(data[i])) 
        if byte[5] == '0x00':
            return job + ' has been loaded'
        elif byte == '0x01':
            return job + ' could not be loaded'
        else:
            return 'error in communication'
    else:
        return "Cant load Job. Machine ", status()
    
    

        
        
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

def clearCommands(commands):
    for item in commands["bools"]:
        if commands["bools"][item] != 0:
            commands["bools"][item] = 0
    for item in commands["strings"]:
        if len(commands["strings"][item]) != 0:
            commands["strings"][item] = ""
    with open('commands.json', 'w') as outfile:
        json.dump(commands, outfile)

with open('commands.json','r') as json_file:
    commands = json.load(json_file)
clearCommands(commands)

while True:
    time.sleep(2)
    with open('commands.json','r') as json_file:
        commands = json.load(json_file)
        for item in commands["bools"]:
            print(commands["bools"][item])
            if commands["bools"][item] != 0:
                if item == 'status':
                    status()
                    clearCommands(commands)
                if item == 'getJobs':
                    getJobs()
                    clearCommands(commands)
                if item == 'start':
                    start()
                    clearCommands(commands)
                if item == 'stop':
                    stop()
                    clearCommands(commands)
                if item == 'jobReload':
                    jobReload()
                    clearCommands(commands)
                if item == 'disconnect':
                    disconnect()
                    clearCommands(commands)
                if item == 'quit':
                    clearCommands(commands)
                    quit()
                
        for item in commands["strings"]:
            if len(commands["strings"][item]) != 0:
                if item == "loadJob":
                    loadJob(commands["strings"][item])
                    clearCommands(commands)
                if item == "queryJob":
                    queryJob(commands["strings"][item])
                    clearCommands(commands)
                if item == "connect":
                    connect(commands["strings"][item])
                    clearCommands(commands)
                