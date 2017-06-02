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
from typing import Dict, Any
from requests import request
from json import dumps
import arrow

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class AuthenticationClient(object):
    end_point: str
    reciever: str
    public_key: str
    encyption_client: Any
    def __init__(self, reciever: str, end_point: str, public_key: str) -> None:
        self.reciever = reciever
        self.end_point = end_point
    
    def get_symetric_key(self) -> Dict[str, str]:
        payload = dict(public_key=self.public_key,
                       reciever=self.reciever,
                       signature='')
        key_result = request.post(self.end_point, data=payload)
        return key_result

    def is_alive(self):
        pass

def generate_symetric_key() -> str:
    raise NotImplementedError()

def generate_signature(alice_public_key: str, bob_public_key: str, signature: str, time_stamp: int) -> str:
    raise NotImplementedError()

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
    raise NotImplementedError()

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
    alice, bob = decrypt_payload(payload)
    logger.info(f"alice: ${alice}\nbob: ${bob}")
    time = arrow.now()
    logger.info(f"time_stamp: ${time}")
    time_stamp = time.timestamp
    s_ab = generate_symetric_key()
    signature = generate_signature(alice, bob, s_ab, time_stamp)
    logger.info("signature:\n${signature}")
    authentication_payload = dumps(dict(signature=signature, time_stamp=time_stamp))
    logger.info("authentication_payload:\n${authentication_payload}")
    return authentication_payload

@app.route('/get_symetric_key', methods=['POST'])
def gey_key() -> None:
    if req.json:
        j = req.json
        payload = j['payload']
        response = process_payload(payload)
        return dict(payload=response)
