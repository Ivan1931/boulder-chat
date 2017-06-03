"""
Description of authentication server:
    let Alice(A) and Bob(B) be two parties that want to communicate
        AS be the symetric key generating Authentication Server
        P_A, P_B, P_AS be the public keys of Alice, Bob and the Auth Server Respectively
        p_A, p_B, p_AS be the private keys of Alice, Bob and Auth Server
        S_AB be the symetric key for Alice and Bob
If Alice wants to send a secure message with Bob for the first time, the following process is follows
    Alice --> AS: GET matierial for Bob
        - public key of Alice (P_AS)
        - encrypted using P_AS
        - P_B
    AS -->  Alice: Material for communication between Alice and Bob
        - payload encrypted with P_A
        - time_stamp
        - contains a signature
            - signature <- encrypt(P_A || P_B || time_stamp, | S_AB, p_AS)
            - verifies that Alice and Bob can communicate using S_AB
            - allows Alice to derive S_AB
"""

from flask import Flask
from flask import request as req
from typing import Dict
from requests import request
from json import dumps, loads
from .crypto import AuthServerPayload, public_key_encrypt, private_key_decrypt
import arrow

def get_server_secret():
    raise NotImplementedError()

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AuthenticationClient(object):
    end_point: str
    reciever_key: str # Bob public key
    sender_key: str # Alice public key
    sender_secret: str # Alice private key
    as_key: str # Authentication server public key
    def __init__(self, reciever_key: str, sender_key: str, sender_secret: str, as_key: str) -> None:
        self.reciever_key = reciever_key
        self.sender_key = sender_key
        self.sender_secret = sender_secret
        self.as_key = as_key
    
    def get_symetric_key(self) -> AuthServerPayload:
        logger.log(f"encrypting using: ${self.sender_key}")
        payload = public_key_encrypt(self.as_key, dumps(dict(sender_key=self.sender_key, reciever_key=self.reciever_key)))
        result = request.post(self.end_point, data=payload)
        assert('signature' in result)
        return AuthServerPayload.decrypt(self.sender_secret, result['signature'])

    def is_alive(self):
        pass

def generate_symetric_key() -> str:
    raise NotImplementedError()

def generate_signature(alice_public_key: str, bob_public_key: str, time_stamp: int) -> str:
    payload = AuthServerPayload(alice_public_key, bob_public_key, time_stamp)
    return payload.encrypt()

def is_authorized(user_public_key) -> bool:
    """
    This is a stub method that can be expanded upon later
    It's here for completeness
    """
    return True

def decrypt_payload(payload: str) -> Dict[str, str]:
    """
    Takes string payload and returns 
    the public keys of both the sender and
    recievers
    """
    return loads(private_key_decrypt(server_secret, payload))

def encrypt(signature: str, time_stamp: int) -> str:
    raise NotImplementedError()

def process_payload(payload: str) -> str:
    """
    Takes a payload from Alice as input
    Payload is an encrypted json blob with the following inputs:
        [P_A, P_B]
    Method will generate S_AB and a signature to verify the
    that uniquely verifies that the AS is allowed to verfify that
    Alice and Bob can communicate

    Returns: An encrypted json string containing
        {
            "signature": str
            "time_stamp": str
        }
    Throws: (not implemented yet)
        AuthorizationError if Alice or Bob are not authorized
        DecryptionError if we can't decrypt the payload
    """
    logger.info("Starting payload processing for payload:\n${payload}")
    logger.info(payload)
    public_keys = decrypt_payload(payload)
    alice = public_keys['sender_key']
    bob = public_keys['reciever_key']
    logger.info(f"alice: ${alice}\nbob: ${bob}")
    time = arrow.now()
    logger.info(f"time_stamp: ${time}")
    time_stamp = time.timestamp
    signature = generate_signature(alice, bob, time_stamp)
    logger.info(f"signature:\n${signature}")
    response_payload = dumps(dict(signature=signature, time_stamp=time_stamp))
    logger.info(f"response_payload:\n${response_payload}")
    return response_payload

@app.route('/get_symetric_key', methods=['POST'])
def gey_key() -> None:
    if req.json:
        j = req.json
        payload = j['payload']
        response = process_payload(payload)
        return dict(payload=response)

if __name__=="__main__":
    global server_secret
    server_secret = get_server_secret()
    app.run(host='localhost', port=4000, debug=True)
