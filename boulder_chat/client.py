"""
This module is in charge of communication between two clients. It works
in the following way. We assume that Alice has obtained an auth token from the AuthenticationServer:
    let P_A, P_B be public keys of Alice and Bob
        p_a, p_b be public keys of Alice and Bob
        S_AB be the symetric key between Alice and Bob
        sig be the authentication token between Alice and Bob

"""
from typing import List
from arrow import Arrow
from flask import Flask
from hashlib import sha256
from .message import FirstMessageRequest, FirstMessageResponse, MessageRequest, MessageResponse, AuthServerResponse

Time = Arrow

class ClientState(object):
    private_key: str
    public_key: str
    server_public_key: str
    server_address: str


class KeySet(object):
    our_private_key: str
    our_public_key: str
    symetric_key: str
    reciever_public_key: str

    def __init__(self, our_public_key: str,
                our_private_key: str,
                symetric_key: str,
                reciever_public_key: str):
        self.our_public_key = our_public_key
        self.our_private_key = our_private_key
        self.symetric_key = symetric_key
        self.reciever_public_key = reciever_public_key


class FirstMessageClient(object):
    auth_resp: AuthServerResponse

    def __init__(self, auth_resp: AuthServerResponse):
        self.auth_resp = auth_resp

    def send_message(self, message: str):
        return dumps(payload)

class CommunicationClient(object):
    reciever_end_point: str
    key_set: KeySet

    def __init__(self, reciever_end_point: str, key_set: KeySet) -> None:
        self.reciever_end_point = reciever_end_point
        self.key_set = key_set

    def send_file(self, file_path: str) -> None:
        pass

    def send_message(self, message: str) -> None:
        pass


app = Flask(__name__)

@app.route('/send_file', methods=['POST'])
def send_files():
    pass

@app.route('/send_message', methods=['POST'])

def send_message():
    pass
