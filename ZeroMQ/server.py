import datetime
import zmq
import protos_pb2

groupList=[]

def registerServer(groupData):
    groupList.append(groupData)

def serve():
    context = zmq.Context()
    
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:50051")
    
    print(f'{datetime.datetime.now()}: Server listening on 127.0.0.1:50051')
    
    while True:
        msg = socket.recv_string()
        print(f'{datetime.datetime.now()} : {msg} received')
        if msg=="reg_grp":
            socket.send_string(f'{datetime.datetime.now()}: Registering the Group')
            
            groupData = socket.recv()
            groupObj = protos_pb2.Group()
            groupObj.ParseFromString(groupData)
            
            registerServer(groupData=groupObj)
            
            socket.send_string(f"{datetime.datetime.now()}: {groupObj.name} got added to the registry server.")
            
        if msg=="get_grp":
            socket.send_string(str(len(groupList)))
            
            for i in groupList:
                msg = socket.recv_string()
                socket.send(i.SerializeToString())

if __name__=="__main__":
    serve()
