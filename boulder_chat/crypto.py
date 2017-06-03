from typing import Dict
from json import dumps

def public_key_encrypt(public_key: str, payload: str) -> str:
    """
    This method must encrypt paload using public_key
    """
    raise NotImplementedError()

def private_key_encrypt(private_key: str, payload: str) -> str:
    """
    Implement private key encryption here
    """
    raise NotImplementedError()

def private_key_decrypt(private_key: str, payload: str) -> str:
    """
    Decrypt something using a private key
    """
    raise NotImplementedError()

def public_key_decrypt(public_key: str, payload: str) -> str:
    """
    Decrypt something using a public key
    """
    raise NotImplementedError()

def symetric_key_encrypt(symetric_key: str, payload: str) -> str:
    """
    This method should encrypt and arbitrary string
    using a symetric key
    """
    raise NotImplementedError()

class AuthServerPayload(object):
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

    def toJSON(self):
        return dumps(dict(sender_public=self.sender_public, 
                          reciever_public=self.reciever_public, 
                          time_stamp=self.time_stamp))

    def encrypt(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def decrypt(secret: str, payload: str) -> AuthServerPayload:
        """
        This method takes the sender (Alice) secret key
        and a payload she has recieved from the server
        and decrypts it into a AuthServerPayload objectr
        """
        raise NotImplementedError()
