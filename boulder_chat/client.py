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

Time = Arrow

class LocalMessage(object):
    message: str
    timestamp: Time
    sent: bool # True if we sent this message

    def __lt__(self, other):
        """
        Messages are ordered by timestamp so that
        we can order them in chronological order
        """
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class Friend(object):
    symetric_key: str
    public_key: str
    messages: List[LocalMessages] = []


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
