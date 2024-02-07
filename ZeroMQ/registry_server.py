import time
import zmq
import article_pb2
import sys

serverList=[]

def registerServer(serverData):
    serverList.append(serverData)

def serve():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:50051")
    print("Registry server is up and listening to upcoming requests on port number 50051")
    while True:
        msg = socket.recv_string()
        print(msg)
        if msg=="regser":
            socket.send_string("Processing registerServer")
            serverData=socket.recv()
            serverObj=article_pb2.Server()
            serverObj.ParseFromString(serverData)
            registerServer(serverData=serverObj)
            socket.send_string(serverObj.name+" got added to the registry server.")
        if msg=="getser":
            socket.send_string(str(len(serverList)))
            for i in serverList:
                msg=socket.recv_string()
                socket.send(i.SerializeToString())



if __name__=="__main__":
    serve()
