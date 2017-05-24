# producer.py
import pika, os, logging

# Parse CLODUAMQP_URL (fallback to localhost)
# set up parameters for connection
url = os.environ.get('CLODUAMQP_URL', 'amqp://test:test@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5 # default timeout is 0.25 but we make it longer to avoid connection timeout

# create connection
connection = pika.BlockingConnection(params) # connects with RabbitMQ server

# create channel
channel = connection.channel()

# declare a queue
channel.queue_declare(queue='chat')

# publish a message
def send_msg(msg):
    # uses the default exhange which is the direct exchange with no name
    # routing key refers to the queue we want
    channel.basic_publish(exchange='', routing_key='chat', body=msg)
    print "[x] msg sent to consumer"


#using main because I want to create a quit command
def main():
    print "...Welcome to Boulder_Chat..."
    print "type = producer"
    print "use ^C to close"

    try:
        # consume messages from queue
        channel.start_consuming()
        # get message input
        while(True):
            msg_input = raw_input("Enter message: ")
            send_msg(msg_input)
    except KeyboardInterrupt:
        # close connection
        connection.close()
        print ""
        print "\nLogged Out"

if (__name__ == '__main__'):
    main()