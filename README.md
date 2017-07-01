# Disclaimer
This is not meant to be taken seriously - it's a university project. This was undertaken for the Network and Information Security module at UCT CS honours.

# About
In this project we were instructed to create a secure file and message sending protocol that performs the following functions

* prevents interception - confidentiality
* prevents tampering
* prevents impersonation

The design of the program is based on GNU PGP with a twist - an authentication server (that actually does not authenticate but could be enabled to do so).
We assumed the following things about the auth server - all clients had it's public key so that it could be trusted. 

We had to write a brief document about this application as a requirement for the project. It is on this repository under the file `nis-part-ii.pdf`


# Building Instructions
To install dependencies and run tests the following instructions should be followed

## Installing Dependencies

```
make deps
```

## Running Tests

```
make test
```

## Running Type Checker and Linter

```
make -k check
```

The `-k` option instructs make to keep going even if the
linter and type checker fails. Need this to run all checks.

Alternatively, the linter can be run separately using:

```
make lint
```

The type checker can be run separately using:

```
make type_check
```

# Demo
Running the demo - open 5 terminal windows. In each window do the following:

1. `start_auth` - this starts the authentication server
2. `start_sender` - this starts the senders server
3. `start_receiver` - this starts the receivers server
4. `start_sender_ui` - this starts a simple command line interface too the sender
5. `start_receiver_ui` - this starts the receiver ui

Now follow the following instructions:

* In the `start_sender_ui` screen type in the `first` option - this will allow you to send the first message to the receiver instance of the chat. 
* You should be prompted to provide a public key file - use `receiver.pem`
* Next you will need to give your address and that of the receiver - use `localhost:4000` for the person you're sending too (this is the first thing you need to enter) and then `localhost:3000` for your return address
* Type a message and chat

# Future Work
Actually building a more sensible messaging system
