from __future__ import print_function
import uuid
import logging
import zmq
import grpc
import article_pb2 
import article_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

servers=[]

def getServers():
    global servers
    servers=[]
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:50051")
    socket1.send_string("getser")
    msg=int(socket1.recv_string())
    for i in range(msg):
        socket1.send_string("")
        msg=socket1.recv()
        serverObj=article_pb2.Server()
        serverObj.ParseFromString(msg)
        servers.append(serverObj)
    for i in servers:
        print(str(i))
    
def connectServer():
    print("Currently following servers are active: \n S.no || name || ip || port")
    sno=0
    for i in servers:
        print(sno+1, " || ",i.name, " || ",i.address.ip," || ",i.address.port)
        sno=sno+1
    q=int(input("Please choose one of the above server and input it's S.No to connect:"))
    ip=servers[q-1].address.ip
    port=servers[q-1].address.port
    print("Establishingpip install grpcio connection")
    cid=str(uuid.uuid4())
    clientObj=article_pb2.Client(uuid=cid)
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("conser")
    msg=socket1.recv_string()
    print(msg)
    socket1.send_string(cid)
    msg=socket1.recv_string()
    print(msg)
    return [port,cid,clientObj]

def disconnectServer(port,clientObj):
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("disconser")
    msg=socket1.recv_string()
    print(msg)
    socket1.send_string(clientObj)
    msg=socket1.recv_string()
    print(msg)

def publishArticle(port,clientObj):
    auth=input("enter the name of Author:")
    mtype=input("Choose. \n sports, fassion or politics:")
    now = datetime.datetime.now()
    timestamp = Timestamp()
    time=timestamp.FromDatetime(now)
    print(time)
    content=input("Enter the article content:")
    ad=article_pb2.Article(author=auth,type=mtype,time=time,content=content)
    pubreq=article_pb2.PublishRequest(client=clientObj,article=ad)
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("pubart")
    msg=socket1.recv_string()
    print(msg)
    socket1.send(ad.SerializeToString())
    msg=socket1.recv_string()
    print(msg)

def getArticles(port):
    auth=input("enter the name of Author:")
    mtype=input("Choose. \n sports, fassion or politics:")
    time_str=input("Enter the date in YY-mm-dd format:")
    dtime=datetime.datetime.strptime(time_str,'%Y-%m-%d')
    timestamp = Timestamp()
    timestamp.FromDatetime(dtime)
    artreq=article_pb2.ArticleRequest(author=auth,type=mtype,time=timestamp)
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:"+str(port))
    socket1.send_string("getart")
    msg=int(socket1.recv_string())
    for i in range(msg):
        socket1.send_string("")
        msg=socket1.recv()
        artObj=article_pb2.Article()
        artObj.ParseFromString(msg)
        print(str(artObj))

if __name__ == '__main__':
    logging.basicConfig()
    flag=False
    while True:
        q=input("Press 1 to get all active servers: \n Press 2 to connect to a server \n press 3 to disconnect from a server \n press 4 to publish an article to a server \n press 5 to get articles \n and press 0 to quit")
        if q=="1":
            getServers()
        elif q=="2":
            data=connectServer()
            flag=True
        elif q=="3":
            if flag:
                disconnectServer(data[0],data[1])
                flag=False
            else:
                print("Alert, You have not joined any server")
            #break
        elif q=="4":
            if flag:
                publishArticle(data[0],data[2])
            else:
                print("Alert, Please connect to a server first.")
        elif q=="5":
            if flag:
                getArticles(data[0])
            else:
                print("Alert, First connect to a server. ")
        else:
            break
    

