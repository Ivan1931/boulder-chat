import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES
from typing import Dict
from json import dumps

block_size = 16
IV = block_size * '\x00'
mode = AES.MODE_CBC
message = 'bitches'
password = 'abcdefghijklmnopqrstuvwxyz'
test_key = hashlib.sha256(password.encode()).digest()

# padding methods
pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]
# generic encryption method
def encrypt(key, payload):
    payload = payload.encode();
    raw_payload = pad(payload)
    # generate the cipher for encryption and encrypt
    cipher = AES.new(key, mode, IV=IV)
    encoded_payload = cipher.encrypt(raw_payload)
    # decode back into plain text and return
    return base64.b64encode(encoded_payload).decode('utf-8')

# generic decryption method
def decrypt(key, ecrypted_payload):
    ecrypted_payload = base64.b64decode(ecrypted_payload)
    # generate the cipher for decryption and decrypt
    cipher = AES.new(key, mode, IV=IV)
    decrypted_payload = cipher.decrypt(ecrypted_payload)
    # decode back into plain text, unpad and return
    return unpad(decrypted_payload).decode('utf-8')

# def public_key_encrypt(public_key: str, payload: str) -> str:
#     """
#     This method must encrypt paload using public_key
#     """
#     raise NotImplementedError()
#
def private_key_encrypt(private_key, payload):
    result = encrypt(private_key, payload)
    return result

def private_key_decrypt(private_key, payload):
    result = decrypt(private_key, payload)
    return result
#
# def public_key_decrypt(public_key: str, payload: str) -> str:
#     """
#     Decrypt something using a public key
#     """
#     raise NotImplementedError()
#
# def symetric_key_encrypt(symetric_key: str, payload: str) -> str:
#     """
#     This method should encrypt and arbitrary string
#     using a symetric key
#     """
#     raise NotImplementedError()
#
# class AuthServerPayload(object):
#     """
#     This is a data structure that contains the results of sending
#     a request from the server to the client.
#     """
#     sender_public: str
#     reciever_public: str
#     time_stamp: int
#     signature: str
#
#     def __init__(self, sender_public: str, reciever_public: str, time_stamp: int) -> None:
#         self.sender_public = sender_public
#         self.reciever_public = reciever_public
#         self.time_stamp = time_stamp
#
#     def toJSON(self):
#         return dumps(dict(sender_public=self.sender_public,
#                           reciever_public=self.reciever_public,
#                           time_stamp=self.time_stamp))
#
#     def encrypt(self) -> str:
#         raise NotImplementedError()
#
#     @staticmethod
#     def decrypt(secret: str, payload: str) -> AuthServerPayload:
#         """
#         This method takes the sender (Alice) secret key
#         and a payload she has recieved from the server
#         and decrypts it into a AuthServerPayload objectr
#         """
#         raise NotImplementedError()
enc_message = private_key_encrypt(test_key, message)
dec_message = private_key_decrypt(test_key, enc_message)

print(message)
print(enc_message)
print(dec_message)
print(message == dec_message)