"""
This module contains all possible messages that can be sent between the client
and the server. There are currently 3 interactions that take place in the whole system
* GET authentication
** Gets an authentication signature for the requester
* POST first_message
** Sends a special first message to the user at the end point
* POST message
** Sends a message to a user using a symetric key after
** symetric key exchange occurs
"""

from arrow import Arrow
from json import dumps

class AuthServerResponse(object):
    """
    This is a data structure that contains the results of sending
    a request from the server to the client.
    """
    sender_public: str
    reciever_public: str
    time_stamp: int
    signature: str

    def __init__(self, sender_public: str, reciever_public: str, time_stamp: int) -> None:
        self.sender_public = sender_public
        self.reciever_public = reciever_public
        self.time_stamp = time_stamp

    def toJSON(self) -> str:
        return dumps(dict(sender_public=self.sender_public, 
                          reciever_public=self.reciever_public, 
                          time_stamp=self.time_stamp))

    def encrypt(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def decrypt(secret: str, payload: str) -> AuthServerResponse:
        """
        This method takes the sender (Alice) secret key
        and a payload she has recieved from the server
        and decrypts it into a AuthServerResponse objectr
        """
        raise NotImplementedError()

class AuthServerRequest(object):

    sender_public: str
    reciever_public: str

    def __init__(self, sender_public: str, reciever_public: str) -> None:
        self.sender_public = sender_public
        self.reciever_public = reciever_public


    def toJSON(self) -> str:
        return dumps(dict(
                    sender_public=self.sender_public, 
                    reciever_public=self.reciever_public
                ))

    def encrypt(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def decrypt(secret: str, payload: str) -> AuthServerRequest:
        raise NotImplementedError()
                        

class FirstMessageRequest(object):
    authentication_signature: AuthServerResponse
    first_message: str
    
    def __init__(self, authentication_signature, first_message) -> None:
        self.authentication_signature = authentication_signature
        self.first_message = first_message


class FirstMessageResponse(object):
    ok: bool

    def __init__(self, ok: bool) -> None:
        self.ok = ok


class MessageRequest(object):
    symetric_key: str
    message: str

    def __init__(self, symetric_key: str, message: str) -> None:
        self.symetric_key = symetric_key
        self.message = message

    def encrypt(self) -> str:
        """
        Encrypts the message using the symetric key
        """
        raise NotImplementedError()

    @staticmethod
    def decrypt(self, symetric_key: str, payload: str) -> MessageRequest:
        """
        Decrypts a message request using the symetric key for that user
        """
        raise NotImplementedError()


class MessageResponse(object):
    ok: bool

    def __init__(ok: bool) -> None:
        self.ok = ok
