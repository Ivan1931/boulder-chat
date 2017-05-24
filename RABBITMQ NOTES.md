# RABBITMQ NOTES
## Setting up a user to login
Once you have installed rabbitmq the default login info is guest with password guest but I couldn't log in with that so I had to create a new user with admin permissions.

```bash
rabbitmqctl add_user test test
rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
```

## PUBLISH AND SUBSCRIBE MESSAGES

RabbitMQ speaks a protocol called AMQP by default. To be able to communicate with RabbitMQ you need a library that understands the same protocol as RabbitMQ. You need to download the client-library for the programming language that you intend to use for your applications. A client-library is an applications programming interface (API) for use in writing client applications. A client library has several methods that can be used, in this case to communicate with RabbitMQ. The methods should be used when you, for example, connect to the RabbitMQ broker (using the given parameters, host name, port number, etc) or when you declare a queue or an exchange. There is a choice of libraries for almost every programming language.

Steps to follow when setting up a connection and publishing a message/consuming a message:

1. First of all, we need to set up/create a connection object. Here, the username, password, connection URL, port etc, will be specified. A TCP connection will be set up between the application and RabbitMQ when the start method is called.

2. Secondly a channel needs to be opened. A channel needs to be created in the TCP connection. The connection interface can be used to open a channel and when the channel is opened it can be used to send and receive messages.

3. Declare/create a queue. Declaring a queue will cause it to be created if it does not already exist. All queues needs to be declared before they can be used.

4. In subscriber/consumer: Set up exchanges and bind a queue to an exchange. All exchanges needs to be declared before they can be used. An exchange accepts messages from a producer application and routes them to message queues. For messages to be routed to queues, queues need to be bound to an exchange.

5. In publisher: Publish a message to an exchange

6. In subscriber/consumer: Consume a message from a queue.
   Close the channel and the connection.