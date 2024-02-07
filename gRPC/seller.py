import grpc
from concurrent import futures

import protos_pb2 as protos_pb2
import protos_pb2_grpc as protos_pb2_grpc
import notify_pb2 as notify_pb2
import notify_pb2_grpc as notify_pb2_grpc

import datetime
import time
import uuid

ip = 'localhost'
port = '60051'
s_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'{ip}:{port}'))


def register_seller(channel):
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.RegisterSeller(protos_pb2.RegisterSellerRequest(ip=ip, port=port, uuid=s_uuid))
    
    print(f'{datetime.datetime.now()}: {response.status}')
    
    if (response.status == 'SUCCESS'):
        return True
    else:
        return False

def sell_item(name, category, quantity, description, price, channel):
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    item = protos_pb2.Item();
    item.itemId = str(uuid.uuid5(uuid.NAMESPACE_DNS, name + "" + category))
    item.price = price
    item.name = name
    item.category = category
    item.description = description
    item.quantity = quantity
    item.rating = 0
    
    response = stub.SellItem(protos_pb2.SellItemRequest(ip=ip, port=port, uuid=s_uuid, item=item))
    print(f'{datetime.datetime.now()}: {response.status}')

def update_item(channel, itemId, newPrice, newQuantity):
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.UpdateItem(protos_pb2.UpdateItemRequest(itemId=itemId, newPrice=newPrice, newQuantity=newQuantity, ip=ip, port=port, uuid=s_uuid))
    print(f'{datetime.datetime.now()}: {response.status}')

def delete_item(channel, itemId):
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.DeleteItem(protos_pb2.DeleteItemRequest(itemId=itemId, ip=ip, port=port, uuid=s_uuid))
    print(f'{datetime.datetime.now()}: {response.status}')

def display_seller_items(channel):
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.DisplaySellerItems(protos_pb2.DisplaySellerItemsRequest(ip=ip, port=port, uuid=s_uuid))
    
    item = response.item
    
    print(f'{datetime.datetime.now()}')
    count = 1
    for i in item:
        print("==================================================")
        print(f'Item {count}:')
        print(f'Item ID: {i.itemId}')
        print(f'Name: {i.name}')
        print(f'Category: {i.category}')
        print(f'Description: {i.description}')
        print(f'Quantity: {i.quantity}')
        print(f'Price: {i.price}')
        print(f'Rating: {i.rating}')
        print("==================================================")
        count += 1

def run(registered):
    with grpc.insecure_channel("localhost:50051") as channel:
        response = True
        if not registered[0]:
            print("==================================================")
            print("Registering Seller...")
            response = register_seller(channel=channel)
        
        if (not response):
            channel.close()
            print("==================================================")
            print('FAILED')
            print("==================================================")
        
        else:
            registered[0] = True
            print("==================================================")
            print("WELCOME TO THE MARKETPLACE")
            print("==================================================")
            print("1. Sell Item")
            print("2. Update Item")
            print("3. Delete Item")
            print("4. Display Seller Items")
            print("==================================================")
            
            input_ = int(input("Enter your choice: "))
            
            if (input_ == 1):
                print("==================================================")
                name = input("Enter the name of the item: ")
                category = input("Enter the category of the item: ")
                quantity = int(input("Enter the quantity of the item: "))
                description = input("Enter the description of the item: ")
                price = float(input("Enter the price of the item: "))
                print("==================================================")
                sell_item(name=name, category=category, quantity=quantity, description=description, price=price, channel=channel)
                print("==================================================")
            elif (input_ == 2):
                print("==================================================")
                itemId = input("Enter the item ID: ")
                newPrice = float(input("Enter the new price: "))
                newQuantity = int(input("Enter the new quantity: "))
                print("==================================================")
                update_item(channel=channel, itemId=itemId, newPrice=newPrice, newQuantity=newQuantity)
                print("==================================================")
            elif (input_ == 3):
                print("==================================================")
                itemId = input("Enter the item ID: ")
                print("==================================================")
                delete_item(channel=channel, itemId=itemId)
                print("==================================================")
            elif (input_ == 4):
                print("==================================================")
                display_seller_items(channel=channel)
                print("==================================================")
        
        channel.close()
        
class NotifyService(notify_pb2_grpc.NotifyServiceServicer):
    def Notify(self, request, context):
        
        item = notify_pb2.Item()
        item.itemId = request.item.itemId
        
        print("\n==================================================")
        print(f'The following item is bought by buyer: {request.ip}:{request.port}')
        print(f'Item ID: {item.itemId}')
        print("==================================================")    
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.NotifyResponse(status="SUCCESS")

def serve():
    registered = [False]
    
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        notify_pb2_grpc.add_NotifyServiceServicer_to_server(NotifyService(), server)
        server.add_insecure_port(ip+':'+port)
        server.start()
        
        try:
            while True:
                run(registered)
                time.sleep(2)
        except KeyboardInterrupt:
            server.stop(0)
            print("\n==================================================")
            print("Exiting...")
            print("==================================================")
    except Exception as e:
        print("\n==================================================")
        print('FAILED')
        print("Exiting...")
        print("==================================================")
        
        
if __name__ == '__main__':
    serve()