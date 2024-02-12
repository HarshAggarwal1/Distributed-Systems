import zmq
import protos_pb2 
import datetime

clientList=[]
msgList=[]

def sendMessage(msg):
    msgList.append(msg)

def disconnectGroup(msg):
    if msg in clientList:
        clientList.remove(msg)

def connectGroup(msg):
    clientList.append(msg)

def serve(name, port):
    context = zmq.Context()
    
    addr = protos_pb2.Address(ip="127.0.0.1",port=int(port))
    
    serverdata = protos_pb2.Group(name=name,address=addr)
    
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:50051")
    socket1.send_string("reg_grp")
    
    msg = socket1.recv_string()
    
    print(msg)
    
    socket1.send(serverdata.SerializeToString())
    
    msg = socket1.recv_string()
    
    print(f'{datetime.datetime.now()} {msg}')
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:"+port)
    
    print(f"{datetime.datetime.now()}: {name} server is up and listening to upcoming requests on port number {port}")
    
    while True:
        msg=socket.recv_string()
        
        if msg=="con_grp":
            socket.send_string("Processing connectGroup")
            
            res=socket.recv_string()
            connectGroup(res)
            
            socket.send_string("Client got connected")
            
        if msg=="discon_grp":
            socket.send_string("Processing disconnectGroup")
            
            res=socket.recv_string()
            disconnectGroup(res)
            
            socket.send_string("Client got disconnected")
        
        if msg=="send_msg":
            socket.send_string("Processing sendMessage")
            
            msgData=socket.recv()
            msgObj=protos_pb2.Message()
            msgObj.ParseFromString(msgData)
            sendMessage(msgObj)
            
            socket.send_string("Sent Message Successfully")
        
        if msg=="get_msg":
            socket.send_string(str(len(msgList)))
            
            for i in msgList:
                msg=socket.recv_string()
                socket.send(i.SerializeToString())

if __name__=="__main__":
    name=input("Enter Name for your group: ")
    port=input("Enter Port: ")
    
    serve(name,port)

