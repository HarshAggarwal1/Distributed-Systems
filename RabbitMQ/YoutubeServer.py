import pika
import json

subscribers = {}

class YouTubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_requests')

    def consume_user_requests(self, ch, method, properties, body):
        request = json.loads(body)
        if request['action'] == 'login':
            print(f"{request['user']} logged in")
            
        elif request['action'] == 'subscription':
            
            if request['subscribe'] == 'subscribed':
                if request['youtuber'] not in subscribers:
                    subscribers[request['youtuber']] = []
                    subscribers[request['youtuber']].append(request['user'])
                else:
                    subscribers[request['youtuber']].append(request['user'])
            else:
                if request['youtuber'] in subscribers:
                    subscribers[request['youtuber']].remove(request['user'])
            
            print(f"{request['user']} {request['subscribe']} to {request['youtuber']}")

    def consume_youtuber_requests(self, ch, method, properties, body):
        request = json.loads(body)      
        
        if request['youtuber'] not in subscribers:
            subscribers[request['youtuber']] = []
        
        print(f"{request['youtuber']} uploaded {request['video']}")
        
        self.notify_users(request['youtuber'], request['video'])
    
    def notify_users(self, youtuber, video):
        
        for user in subscribers[youtuber]:
            self.channel.queue_declare(queue=user, durable=True)
            self.channel.basic_publish(exchange='',
                                       routing_key=user,
                                       body=json.dumps({'youtuber': youtuber, 'video': video}))
    
    def start_consuming(self):
        self.channel.basic_consume(queue='user_requests', on_message_callback=self.consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=self.consume_youtuber_requests, auto_ack=True)

        print('Server is waiting for requests. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    youtube_server = YouTubeServer()
    youtube_server.start_consuming()
