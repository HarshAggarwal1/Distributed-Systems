import zmq
import article_pb2 

clientList=[]
artList=[]

def publishArticle(msg):
    artList.append(msg)

def disconnectServer(msg):
    if msg in clientList:
        clientList.remove(msg)

def connectServer(msg):
    clientList.append(msg)

def serve(name,port):
    context = zmq.Context()
    addr=article_pb2.Address(ip="127.0.0.1",port=int(port))
    serverdata=article_pb2.Server(name=name,address=addr)
    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:50051")
    socket1.send_string("regser")
    msg=socket1.recv_string()
    print(msg)
    socket1.send(serverdata.SerializeToString())
    msg=socket1.recv_string()
    print(msg)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:"+port)
    print(name+" server is up and listening to upcoming requests on port number "+port)
    while True:
        msg=socket.recv_string()
        if msg=="conser":
            socket.send_string("Processing connectServer")
            res=socket.recv_string()
            connectServer(res)
            socket.send_string("Client got connected")
        if msg=="disconser":
            socket.send_string("Processing disconnectServer")
            res=socket.recv_string()
            disconnectServer(res)
            socket.send_string("Client got disconnected")
        if msg=="pubart":
            socket.send_string("Processing publishArticle")
            artData=socket.recv()
            artObj=article_pb2.Article()
            artObj.ParseFromString(artData)
            publishArticle(artObj)
            socket.send_string("Article got added to the server")
        if msg=="getart":
            socket.send_string(str(len(artList)))
            for i in artList:
                msg=socket.recv_string()
                socket.send(i.SerializeToString())

if __name__=="__main__":
    name=input("enter the name of the server:")
    port=input("enter the port where you wish to connect I.E 500XX: ")
    serve(name,port)

