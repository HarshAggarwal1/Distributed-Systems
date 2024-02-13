import pika
import json
import sys

class User:
    def __init__(self, name):
        self.name = name
        print(f"User {self.name} created")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue=self.name, durable=True)
        self.subscriptions = []
        
    def login(self):
        request = {
            'action': 'login',
            'user': self.name
        }
        self.channel.basic_publish(exchange='',
                                   routing_key='user_requests',
                                   body=json.dumps(request))
        print("SUCCESS")

    def update_subscription(self, youtuber, subscribe):
        if (subscribe == 'subscribed'):
            self.subscriptions.append(youtuber)
        else:
            self.subscriptions.remove(youtuber)
            
        request = {
            'action': 'subscription',
            'user': self.name,
            'youtuber': youtuber,
            'subscribe': subscribe
        }
        self.channel.basic_publish(exchange='',
                                   routing_key='user_requests',
                                   body=json.dumps(request))

        print("SUCCESS")

    def receive_notifications(self, ch, method, properties, body):
        notification = json.loads(body)
        print(f"Notification from {notification['youtuber']}: {notification['video']} video uploaded")
       
    
    def start_consuming(self):
        self.channel.basic_consume(queue=self.name, on_message_callback=self.receive_notifications, auto_ack=True)
        self.channel.start_consuming()

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python User.py <username> [<s/u> <YouTuberName>]")
        sys.exit(1)

    user_name = sys.argv[1]
    user = User(user_name)
    
    user.login()

    if len(sys.argv) == 4:
        action = sys.argv[2]
        youtuber_name = sys.argv[3]
        if action not in ['s', 'u']:
            print("Invalid action. Use 's' to subscribe or 'u' to unsubscribe")
            sys.exit(1)
        if action == 's':
            action = 'subscribed'
        else:
            action = 'unsubscribed'
        user.update_subscription(youtuber_name, action)
    
    user.start_consuming()
