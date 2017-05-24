# consumer.py

import pika, os, logging, time

# worker function
def chat_function(msg):
    print "New Message!"
    time.sleep(5) # waits for 5 seconds
    print msg
    return

# Parse CLODUAMQP_URL (fallback to localhost)
# set up parameters for connection
url = os.environ.get('CLODUAMQP_URL', 'amqp://test:test@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5 # default timeout is 0.25 but we make it longer to avoid connection timeout

# create connection
connection = pika.BlockingConnection(params) # connects with RabbitMQ server

# create channel
channel = connection.channel()

# function that is called for incoming messages
# called for every message on the queue
def callback(ch, method, properties, body):
    chat_function(body)

# subscribe to queue
# basic consume binds messages to the callback function
channel.basic_consume(callback, queue='chat', no_ack=True)

#using main because I want to create a quit command
def main():
    print "...Welcome to Boulder_Chat..."
    print "type = consumer"
    print "use ^C to close"

    try:
        # consume messages from queue
        channel.start_consuming()
    except KeyboardInterrupt:
        # stop consuming messages
        channel.stop_consuming()

    # close connection
    connection.close()
    print "\nLogged Out"
    exit()

if (__name__ == '__main__'):
    main()
