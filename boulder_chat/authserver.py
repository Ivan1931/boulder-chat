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

"""
@todo:
    * implement crypto methods
    * implement tests for auth server
    * implement tests for AuthenticationClient
"""

from flask import Flask
from flask import request as req
from . import crypto as c

def make_auth_payload(server_public_key, sender_public_key, reciever_public_key):
    if type(reciever_public_key) is not str and type(reciever_public_key) is not bytes:
        reciever_public_key = c.export_public_key(reciever_public_key)
    return dict(
        reciever=reciever_public_key.decode(),
        sender=c.export_public_key(sender_public_key).decode()
    )

def process_auth_payload(server_key_pair, payload, hook=lambda x: x):
    sender_public_key = c.import_public_key(payload['sender'])
    symetric_key = c.generate_key()
    symetric_signature = c.sign_text(server_key_pair, symetric_key)
    response = dict(
        symetric_key=c.encrypt_RSA(sender_public_key, symetric_key).decode(),
        symetric_signature=symetric_signature
    )
    hook(response)
    return response

def decode_auth_response(server_public, sender_secret, payload):
    unencrypted_sym_key = c.decrypt_RSA(sender_secret, payload['symetric_key'])
    unencrypted_signature = payload['symetric_signature']
    assert(c.verify_sign(server_public, unencrypted_signature, unencrypted_sym_key))
    return dict(
        symetric_key=unencrypted_sym_key,
        signature=unencrypted_signature
    )


app = Flask(__name__)

@app.route('/get_symetric_key', methods=['POST'])
def get_symetric_key() -> None:
    """
    Generates a symetric key for communication between Alice and Bob
    """
    if req.json:
        j = req.json
        payload = j['payload']
        response = process_auth_payload(payload)
        return dict(payload=response)


if __name__=="__main__":
    app.run(host='localhost', port=4000, debug=True)

