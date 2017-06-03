from typing import Dict
from json import dumps

import ast
import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

block_size = 16
IV = block_size * '\x00'
mode = AES.MODE_CBC

message = 'bitches'
password = 'abcdefghijklmnopqrstuvwxyz'
test_key = hashlib.sha256(password.encode()).digest()

# padding methods for blocks
pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

# AES Code

# generic encryption method for AES
def encryptAES(key, payload):
    payload = payload.encode();
    raw_payload = pad(payload)
    # generate the cipher for encryption and encrypt
    cipher = AES.new(key, mode, IV=IV)
    encoded_payload = cipher.encrypt(raw_payload)
    # decode back into plain text and return
    return base64.b64encode(encoded_payload).decode('utf-8')

# generic decryption method of AES
def decryptAES(key, ecrypted_payload):
    ecrypted_payload = base64.b64decode(ecrypted_payload)
    # generate the cipher for decryption and decrypt
    cipher = AES.new(key, mode, IV=IV)
    decrypted_payload = cipher.decrypt(ecrypted_payload)
    # decode back into plain text, unpad and return
    return unpad(decrypted_payload).decode('utf-8')

# RSA Code
# this will generate the key object which is the private key
# to get the public key once the object is returned just go
# public_key = key.publickey()
def genKeyRSA():
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator) #generate pub and priv key
    return key

def encryptRSA(public_key, payload):
    payload = payload.encode();
    #dont worry about the 32 it is just a random number for compatibility
    encrypted_payload = public_key.encrypt(payload, 32)
    return encrypted_payload

def decryptRSA(private_key, payload):
    decrypted_payload = private_key.decrypt(payload)
    return decrypted_payload.decode('utf-8')

# def private_key_encrypt(private_key, payload):
#
# def private_key_decrypt(private_key, payload):
#
# def public_key_decrypt(public_key, payload):

# class AuthServerPayload(object):
    # """
    # This is a data structure that contains the results of sending
    # a request from the server to the client.
    # """
    # sender_public: str
    # reciever_public: str
    # time_stamp: int
    # signature: str
    #
    # def __init__(self, sender_public: str, reciever_public: str, time_stamp: int) -> None:
    #     self.sender_public = sender_public
    #     self.reciever_public = reciever_public
    #     self.time_stamp = time_stamp
    #
    # def toJSON(self):
    #     return dumps(dict(sender_public=self.sender_public,
    #                       reciever_public=self.reciever_public,
    #                       time_stamp=self.time_stamp))
    #
    # def encrypt(self) -> str:
    #     raise NotImplementedError()
    #
    # @staticmethod
    # def decrypt(secret: str, payload: str) -> AuthServerPayload:
    #     """
    #     This method takes the sender (Alice) secret key
    #     and a payload she has recieved from the server
    #     and decrypts it into a AuthServerPayload objectr
    #     """
    #     raise NotImplementedError()

# print tests
# print (decryptAES(test_key, encryptAES(test_key, message)) == message)
# private_key = genKeyRSA()
# public_key = private_key.publickey()
# print ("private key = " + str(private_key))
# print ("public key = " + str(public_key))
# enc_message =  encryptRSA(public_key, message)
# dec_message = decryptRSA(private_key,enc_message)
# print(dec_message)
# print (message)