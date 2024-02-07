import grpc
from concurrent import futures

import protos_pb2 as protos_pb2
import protos_pb2_grpc as protos_pb2_grpc
import notify_pb2 as notify_pb2
import notify_pb2_grpc as notify_pb2_grpc

import datetime
import time
import json
import os

class MarketServicer(protos_pb2_grpc.MarketServiceServicer):
    
    def RegisterBuyer(self, request, context):
        """
            This function is called when a buyer wants to register with the market.
            
            Args:
                request: The request object containing the buyer's IP and port.
                context: The context object to send the response.
            
            Returns:
                The response object containing the status of the registration.
        """
        
        print(f"{datetime.datetime.now()}: Buyer join request from {request.ip}:{request.port}")
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.RegisterBuyerResponse(status="SUCCESS")
    
    def RegisterSeller(self, request, context):
        """
            This function is called when a seller wants to register with the market.
            
            Args:
                request: The request object containing the seller's IP and port.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the registration.
        """
        
        print(f"{datetime.datetime.now()}: Seller register request from {request.ip}:{request.port}, uuid = {request.uuid}")
        
        context.set_code(grpc.StatusCode.OK)
        return protos_pb2.RegisterSellerResponse(status="SUCCESS")

    def SellItem(self, request, context):
        """
            This function is called when a seller wants to sell an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the item addition.
        """
        
        print(f"{datetime.datetime.now()}: Sell Item request from {request.ip}:{request.port}")
        
        try:
            if not os.path.exists('seller/'+ request.uuid + '.json'):
                with open(f'seller/{request.uuid}.json', 'w', encoding="utf-8") as f:
                    json.dump({"address": f'{request.ip}:{request.port}', "uuid": request.uuid , "items": []}, f)
                f.close()  
                
            with open(f'seller/{request.uuid}.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
                f.close()  
                
            for item in data["items"]:
                if item["item_id"] == request.item.itemId:
                    context.set_code(grpc.StatusCode.OK)
                    return protos_pb2.SellItemResponse(status="FAILURE")   
            
            data["items"].append({
                "item_id": request.item.itemId, 
                "name": request.item.name,
                "category": request.item.category, 
                "description": request.item.description, 
                "price": request.item.price, 
                "quantity": request.item.quantity, 
                "rating": request.item.rating,
                "wishlist": []
                })                        
            
            with open(f'seller/{request.uuid}.json', 'w', encoding="utf-8") as f:
                json.dump(data, f)
                f.close()                               
            
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.SellItemResponse(status="SUCCESS")
        
        except Exception as e:
            print("Sell Item Call Error: ", e)
            
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.SellItemResponse(status="FAILURE")

    def UpdateItem(self, request, context):
        """
            This function is called when a seller wants to update an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the item update.
        """
        print(f"{datetime.datetime.now()}: Update Item {request.itemId}[id] request from {request.ip}:{request.port}")
        
        try:
            if not os.path.exists('seller/'+ request.uuid + '.json'):
                context.set_code(grpc.StatusCode.OK)
                return protos_pb2.UpdateItemResponse(status="FAILURE")
            
            with open(f'seller/{request.uuid}.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
                f.close()
            
            exists = False
            
            for item in data["items"]:
                if item["item_id"] == request.itemId:
                    exists = True
                    break
            
            if not exists:
                context.set_code(grpc.StatusCode.OK)
                return protos_pb2.UpdateItemResponse(status="FAILURE")
            
            item_notify = notify_pb2.Item()
            
            wishlist = []
            
            for item in data["items"]:
                if item["item_id"] == request.itemId:
                    item["price"] = request.newPrice
                    item["quantity"] = request.newQuantity
                    
                    item_notify.itemId = item["item_id"]
                    item_notify.price = item["price"]
                    item_notify.name = item["name"]
                    item_notify.category = item["category"]
                    item_notify.description = item["description"]
                    item_notify.quantity = item["quantity"]
                    item_notify.rating = item["rating"]
                    
                    wishlist = item["wishlist"]
                    
                    break
            
            with open(f'seller/{request.uuid}.json', 'w', encoding="utf-8") as f:
                json.dump(data, f)
                f.close()
            
            context.set_code(grpc.StatusCode.OK)    
            
            for address in wishlist:
                with grpc.insecure_channel(address) as channel:
                    stub = notify_pb2_grpc.NotifyServiceStub(channel)
                    stub.Notify(notify_pb2.NotifyRequest(item=item_notify, ip=request.ip, port=request.port))
                    channel.close()
            
            return protos_pb2.UpdateItemResponse(status="SUCCESS")
        
        except Exception as e:
            print("Update Item Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.UpdateItemResponse(status="FAILURE")
            

    def DeleteItem(self, request, context):
        """
            This function is called when a seller wants to delete an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
            
            Returns:
                The response object containing the status of the item deletion.
        """
        print(f"{datetime.datetime.now()}: Delete Item {request.itemId}[id] request from {request.ip}:{request.port}")
        
        try:
            if not os.path.exists('seller/'+ request.uuid + '.json'):
                context.set_code(grpc.StatusCode.OK)
                return protos_pb2.DeleteItemResponse(status="FAILURE")
            
            with open(f'seller/{request.uuid}.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
                f.close()
            
            exists = False
            
            for item in data["items"]:
                if item["item_id"] == request.itemId:
                    exists = True
                    data["items"].remove(item)
                    break
            
            if not exists:
                context.set_code(grpc.StatusCode.OK)
                return protos_pb2.DeleteItemResponse(status="FAILURE")
            
            with open(f'seller/{request.uuid}.json', 'w', encoding="utf-8") as f:
                json.dump(data, f)
                f.close()
            
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.DeleteItemResponse(status="SUCCESS")
        
        except Exception as e:
            print("Delete Item Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.DeleteItemResponse(status="FAILURE")

    def DisplaySellerItems(self, request, context):
        """
            This function is called when a buyer wants to display the items of a seller.
            
            Args:
                request: The request object containing the seller's IP and port.
                context: The context object to send the response.
                
            Returns:
                The response object containing the items of the seller.
        """
        print(f"{datetime.datetime.now()}: Display Items request from {request.ip}:{request.port}")
        
        try:
            if not os.path.exists('seller/'+ request.uuid + '.json'):
                context.set_code(grpc.StatusCode.OK)
                return protos_pb2.DisplaySellerItemsResponse()
            
            with open(f'seller/{request.uuid}.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
                f.close()
                
            items = []
            
            for item in data["items"]:
                item_ = protos_pb2.Item()
                item_.itemId = item["item_id"]
                item_.price = item["price"]
                item_.name = item["name"]
                item_.category = item["category"]
                item_.description = item["description"]
                item_.quantity = item["quantity"]
                item_.rating = item["rating"]
                items.append(item_)
                
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.DisplaySellerItemsResponse(item=items)
            
        except Exception as e:
            print("Display Seller Items Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.DisplaySellerItemsResponse()
        

    def SearchItem(self, request, context):
        """
            This function is called when a buyer wants to search for an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the items matching the search.
        """
        print(f"{datetime.datetime.now()}: Search request for Item name: {request.name}, Category: {request.category}")
        
        try:
            items = []
            
            for filename in os.listdir('seller'):
                with open(f'seller/{filename}', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()
                    
                for item in data["items"]:
                    if (request.name == ""):
                        if request.category == "ANY":
                            item_ = protos_pb2.Item()
                            item_.itemId = item["item_id"]
                            item_.price = item["price"]
                            item_.name = item["name"]
                            item_.category = item["category"]
                            item_.description = item["description"]
                            item_.quantity = item["quantity"]
                            item_.rating = item["rating"]
                            items.append(item_)
                        else:
                            if request.category in item["category"]:
                                item_ = protos_pb2.Item()
                                item_.itemId = item["item_id"]
                                item_.price = item["price"]
                                item_.name = item["name"]
                                item_.category = item["category"]
                                item_.description = item["description"]
                                item_.quantity = item["quantity"]
                                item_.rating = item["rating"]
                                items.append(item_)
                    else:  
                        if request.category == "ANY":
                            if request.name in item["name"]:
                                item_ = protos_pb2.Item()
                                item_.itemId = item["item_id"]
                                item_.price = item["price"]
                                item_.name = item["name"]
                                item_.category = item["category"]
                                item_.description = item["description"]
                                item_.quantity = item["quantity"]
                                item_.rating = item["rating"]
                                items.append(item_)
                        else:
                            if request.name in item["name"] and request.category in item["category"]:
                                item_ = protos_pb2.Item()
                                item_.itemId = item["item_id"]
                                item_.price = item["price"]
                                item_.name = item["name"]
                                item_.category = item["category"]
                                item_.description = item["description"]
                                item_.quantity = item["quantity"]
                                item_.rating = item["rating"]
                                items.append(item_)
            
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.SearchItemResponse(item=items)
        
        except Exception as e:
            print("Search Item Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.SearchItemResponse()

    def BuyItem(self, request, context):
        """
            This function is called when a buyer wants to buy an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the purchase.
        """
        print(f"{datetime.datetime.now()}: Buy request {request.quantity}[quantity] of item {request.itemId}[id], from {request.ip}:{request.port}")
        
        try:
            for filename in os.listdir('seller'):
                with open(f'seller/{filename}', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()
                    
                for item in data["items"]:
                    if item["item_id"] == request.itemId:
                        if item["quantity"] >= request.quantity:
                            item["quantity"] -= request.quantity
                            
                            with open(f'seller/{filename}', 'w', encoding="utf-8") as f:
                                json.dump(data, f)
                                f.close()
                                
                            seller_ip = data["address"].split(":")[0]
                            seller_port = data["address"].split(":")[1]
                            
                            item_notify = notify_pb2.Item()
                            item_notify.itemId = item["item_id"]
                            
                            with grpc.insecure_channel(f'{seller_ip}:{seller_port}') as channel:
                                stub = notify_pb2_grpc.NotifyServiceStub(channel)
                                stub.Notify(notify_pb2.NotifyRequest(item=item_notify, ip=request.ip, port=request.port))
                                channel.close()
                            
                            context.set_code(grpc.StatusCode.OK)
                            return protos_pb2.BuyItemResponse(status="SUCCESS")
                        else:
                            context.set_code(grpc.StatusCode.OK)
                            return protos_pb2.BuyItemResponse(status="FAILURE")
                        
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.BuyItemResponse(status="FAILURE")
        
        except Exception as e:
            print("Buy Item Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.BuyItemResponse(status="FAILURE")

    def AddToWishList(self, request, context):
        """
            This function is called when a buyer wants to add an item to his wishlist.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the addition.
        """
        print(f"{datetime.datetime.now()}: Wishlist request of item {request.itemId}, from {request.ip}:{request.port}")
        
        try:
            for filename in os.listdir('seller'):
                with open(f'seller/{filename}', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()
                
                for item in data["items"]:
                    if item["item_id"] == request.itemId:
                        item["wishlist"].append(f'{request.ip}:{request.port}')
                        
                        with open(f'seller/{filename}', 'w', encoding="utf-8") as f:
                            json.dump(data, f)
                            f.close()
                        
                        context.set_code(grpc.StatusCode.OK)
                        return protos_pb2.AddToWishListResponse(status="SUCCESS")
                    
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.AddToWishListResponse(status="FAILURE")
        
        except Exception as e:
            print("Add To Wishlist Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.AddToWishListResponse(status="FAILURE")

    def RateItem(self, request, context):
        """
            This function is called when a buyer wants to rate an item.
            
            Args:
                request: The request object containing the item details.
                context: The context object to send the response.
                
            Returns:
                The response object containing the status of the rating.
        """
        print(f"{datetime.datetime.now()}: {request.ip}:{request.port} rated item {request.itemId} with {request.rating} stars.")

        try:
            for filename in os.listdir('seller'):
                with open(f'seller/{filename}', 'r', encoding="utf-8") as f:
                    data = json.load(f)
                    f.close()
                
                for item in data["items"]:
                    if item["item_id"] == request.itemId:
                        if (item["rating"] <= 0.0):
                            item["rating"] += request.rating
                        else:
                            item["rating"] += request.rating
                            item["rating"] /= 2.0
                        
                        with open(f'seller/{filename}', 'w', encoding="utf-8") as f:
                            json.dump(data, f)
                            f.close()
                        
                        context.set_code(grpc.StatusCode.OK)
                        return protos_pb2.RateItemResponse(status="SUCCESS")
                    
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.RateItemResponse(status="FAILURE")
        
        except Exception as e:
            print("Rate Item Call Error: ", e)
            context.set_code(grpc.StatusCode.OK)
            return protos_pb2.RateItemResponse(status="FAILURE")

if __name__ == '__main__':

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) 
    protos_pb2_grpc.add_MarketServiceServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('localhost:50051') # Adding the custom "localhost:50051" address for the market to run on it
    server.start()

    """
        Running the market until the user stops it
    """
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0) 