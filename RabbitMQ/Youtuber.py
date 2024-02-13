import pika
import json
import sys

class Youtuber:
    def __init__(self, name):
        self.name = name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='notifications')
        self.channel.queue_declare(queue='youtuber_requests')

    def publish_video(self, video_name):
        request = {
            'youtuber': self.name,
            'video': video_name
        }
        self.channel.basic_publish(exchange='',
                                   routing_key='youtuber_requests',
                                   body=json.dumps(request))

        print("SUCCESS")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])

    youtuber = Youtuber(youtuber_name)
    youtuber.publish_video(video_name)
