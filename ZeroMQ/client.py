from __future__ import print_function
import uuid
import logging
import zmq
import protos_pb2
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

groups=[]

def getGroup():
    """
        This function is used to get all the active groups from the server.

        Args:
            None
            
        Returns:
            None
    """
    global groups
    groups=[]
    
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:50051")
    socket1.send_string("get_grp")
    
    msg=int(socket1.recv_string())
    
    for i in range(msg):
        socket1.send_string("")
        
        msg=socket1.recv()
        groupObj=protos_pb2.Group()
        groupObj.ParseFromString(msg)
        
        groups.append(groupObj)
    
    for i in groups:
        print(f'{datetime.datetime.now()}: {str(i)}')
    
def connectGroup():
    """
        This function is used to connect to a group.
        
        Args:
            None
            
        Returns:
            list: [port,cid,clientObj]
    """
    print(f"{datetime.datetime.now()}: Currently following group are active")
    count = 1
    for i in groups:
        print(count, " || ", i.name, " || ", i.address.ip, " || ", i.address.port)
        count += 1
        
    q=int(input("Enter the group number to connect: "))
    
    ip = groups[q-1].address.ip
    port = groups[q-1].address.port
    
    print(f"{datetime.datetime.now()}: Connecting to the group at {ip}:{port}")
    
    cid = str(uuid.uuid4())
    clientObj = protos_pb2.Client(uuid = cid)
    
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("con_grp")
    
    msg = socket1.recv_string()
    
    print(f"{datetime.datetime.now()}: {msg}")
    
    socket1.send_string(cid)
    msg = socket1.recv_string()
    
    print(f"{datetime.datetime.now()}: {msg}")
    
    return [port,cid,clientObj]

def disconnectGroup(port,clientObj):
    """
        This function is used to disconnect from a group.
        
        Args:
            port (int): Port number of the group.
            clientObj (protos_pb2.Client): Client object.
            
        Returns:
            None
    """
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+ str(port))
    socket1.send_string("discon_grp")
    
    msg=socket1.recv_string()
    print(f"{datetime.datetime.now()}: {msg}")
    
    socket1.send_string(clientObj)
    msg = socket1.recv_string()
    print(f"{datetime.datetime.now()}: {msg}")

def sendMessage(port,clientObj):
    """
        This function is used to send a message to a group.
        
        Args:
            port (int): Port number of the group.
            clientObj (protos_pb2.Client): Client object.
            
        Returns:
            None
    """
    now = datetime.datetime.now()
    timestamp = Timestamp()
    time = timestamp.FromDatetime(now)
    
    content = input("Enter your message: ")
    
    ad=protos_pb2.Message(time=time, content=content)
    
    pubreq=protos_pb2.SendRequest(client=clientObj,message=ad)
    
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("send_msg")
    
    msg = socket1.recv_string()
    print(f"{datetime.datetime.now()}: {msg}")
    
    socket1.send(ad.SerializeToString())
    msg=socket1.recv_string()
    print(f"{datetime.datetime.now()}: {msg}")

def getMessage(port):
    """
        This function is used to get messages from a group.
        
        Args:
            port (int): Port number of the group.
            
        Returns:
            None
    """
    time_str=input("Enter the date in HH:MM::SS format: ")
    dtime=datetime.datetime.strptime(time_str,'%H-%M-%S')
    timestamp = Timestamp()
    timestamp.FromDatetime(dtime)
    
    artreq=protos_pb2.MessageRequest(time=timestamp)
    
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("get_msg")
    
    msg=int(socket1.recv_string())
    
    for i in range(msg):
        socket1.send_string("")
        msg=socket1.recv()
        artObj=protos_pb2.Message()
        artObj.ParseFromString(msg)
        print(str(artObj))

if __name__ == '__main__':
    
    logging.basicConfig()
    flag=False
    while True:
        q=input("1. Get all active groups \n2. Connect to a group \n3. Disconnect from a group \n4. Send a message to a group \n5. Get messages \n0. Quit \n\nEnter your choice: ")
        if q=="1":
            getGroup()
        elif q=="2":
            data=connectGroup()
            flag=True
        elif q=="3":
            if flag:
                disconnectGroup(data[0],data[1])
                flag=False
            else:
                print("Alert, You have not joined any group")
            #break
        elif q=="4":
            if flag:
                sendMessage(data[0],data[2])
            else:
                print("Alert, Please connect to a group first.")
        elif q=="5":
            if flag:
                getMessage(data[0])
            else:
                print("Alert, First connect to a group. ")
        else:
            break
    

