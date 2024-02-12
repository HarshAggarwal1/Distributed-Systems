import grpc
from concurrent import futures

import protos_pb2 as protos_pb2
import protos_pb2_grpc as protos_pb2_grpc
import notify_pb2 as notify_pb2
import notify_pb2_grpc as notify_pb2_grpc

import datetime
import time

def register_buyer(channel):
    """
        Function to register the buyer
        
        Args:
            channel: The channel to connect to the server
            
        Returns:
            bool: The status of the registration
    """
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.RegisterBuyer(protos_pb2.RegisterBuyerRequest(ip=ip, port=port))
    
    print(f'{datetime.datetime.now()}: {response.status}')
    
    if (response.status == 'SUCCESS'):
        return True
    else:
        return False
    
def search_item(channel, name, category):
    """
        Function to search the item
        
        Args:
            channel: The channel to connect to the server
            name: The name of the item
            category: The category of the item
            
        Returns:
            None
    """
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.SearchItem(protos_pb2.SearchItemRequest(name=name, category=category))
    
    items = response.item
    
    print(f'{datetime.datetime.now()}')
    count = 1
    for i in items:
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
        
def buy_item(channel, itemId, quantity, ip, port):
    """
        Function to buy the item
        
        Args:
            channel: The channel to connect to the server
            itemId: The ID of the item
            quantity: The quantity of the item
            ip: The IP of the buyer
            port: The port of the buyer
            
        Returns:
            None
    """
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.BuyItem(protos_pb2.BuyItemRequest(itemId=itemId, quantity=quantity, ip=ip, port=port))
    
    print(f'{datetime.datetime.now()}: {response.status}')
    
def add_to_wishlist(channel, itemId, ip, port):
    """
        Function to add the item to the wishlist
        
        Args:
            channel: The channel to connect to the server
            itemId: The ID of the item
            ip: The IP of the buyer
            port: The port of the buyer
            
        Returns:
            None
    """
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.AddToWishList(protos_pb2.AddToWishListRequest(itemId=itemId, ip=ip, port=port))
    
    print(f'{datetime.datetime.now()}: {response.status}')
    
def rate_item(channel, itemId, rating, ip, port):
    """
        Function to rate the item
        
        Args:
            channel: The channel to connect to the server
            itemId: The ID of the item
            rating: The rating of the item
            ip: The IP of the buyer
            port: The port of the buyer
            
        Returns:
            None
    """
    stub = protos_pb2_grpc.MarketServiceStub(channel)
    
    response = stub.RateItem(protos_pb2.RateItemRequest(itemId=itemId, rating=rating, ip=ip, port=port))
    
    print(f'{datetime.datetime.now()}: {response.status}')

def run():
    """
        Function to run the client
        
        Args:
            None
            
        Returns:
            None
    """
    with grpc.insecure_channel("34.131.57.38:50051") as channel:
        response = register_buyer(channel=channel)
        
        if (not response):
            channel.close()
            print("==================================================")
            print('FAILED TO CONNECT TO THE MARKETPLACE')
            print("==================================================")
        
        else:
            print("==================================================")
            print("WELCOME TO THE MARKETPLACE")
            print("==================================================")
            print("1. Search Item")
            print("2. Buy Item")
            print("3. Add to Wishlist")
            print("4. Rate Item")
            print("==================================================")
            
            input_ = int(input("Enter your choice: "))
            
            if (input_ == 1):
                print("==================================================")
                name = input("Enter the name of the item: ")
                category = input("Enter the category of the item: ")
                if name == None:
                    name = ""
                print("==================================================")
                search_item(channel=channel, name=name, category=category)
                print("==================================================")
            elif (input_ == 2):
                print("==================================================")
                itemId = input("Enter the item ID: ")
                quantity = int(input("Enter the quantity: "))
                print("==================================================")
                buy_item(channel=channel, itemId=itemId, quantity=quantity, ip=ip, port=port)
                print("==================================================")
            elif (input_ == 3):
                print("==================================================")
                itemId = input("Enter the item ID: ")
                print("==================================================")
                add_to_wishlist(channel=channel, itemId=itemId, ip=ip, port=port)
                print("==================================================")
            elif (input_ == 4):
                itemId = input("Enter the item ID: ")
                rating = int(input("Enter the rating(integer): "))
                print("==================================================")
                rate_item(channel=channel, itemId=itemId, rating=rating, ip=ip, port=port)
                print("==================================================")
        
        channel.close()

class NotifyService(notify_pb2_grpc.NotifyServiceServicer):
    def Notify(self, request, context):
        """
            Function to notify the buyer about the item update

            Args:
                request: The request from the seller
                context: The context of the request

            Returns:
                protos_pb2.NotifyResponse: The response to the seller
        """
        item = notify_pb2.Item()
        item.itemId = request.item.itemId
        item.price = request.item.price
        item.name = request.item.name
        item.category = request.item.category
        item.description = request.item.description
        item.quantity = request.item.quantity
        item.rating = request.item.rating
        
        print("\n==================================================")
        print(f'The following item is updated by seller: {request.ip}:{request.port}')
        print(f'Item ID: {item.itemId}')
        print(f'Name: {item.name}')
        print(f'Category: {item.category}')
        print(f'Description: {item.description}')
        print(f'Quantity: {item.quantity}')
        print(f'Price: {item.price}')
        print(f'Rating: {item.rating}')
        print("==================================================")    
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.NotifyResponse(status="SUCCESS")

def serve():
    """
        Function to start the server

        Args:
            None
            
        Returns:
            None
    """
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        notify_pb2_grpc.add_NotifyServiceServicer_to_server(NotifyService(), server)
        server.add_insecure_port(ip+':'+port)
        server.start()
        
        try:
            while True:
                run()
                time.sleep(2)
        except KeyboardInterrupt:
            server.stop(0)
            print("\n==================================================")
            print("Exiting...")
            print("==================================================")
    except Exception as e:
        print(e)
        print("\n==================================================")
        print('FAILED')
        print("Exiting...")
        print("==================================================")
        
        
if __name__ == '__main__':
    global ip
    global port
    ip = input("Enter your IP: ")
    port = input("Enter your port: ")
    serve()