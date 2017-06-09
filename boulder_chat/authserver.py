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
import requests
import json
from . import crypto as c
from . import store as s

auth_store_path = 'auth_test_1.json'

def get_test_auth_store():
    auth_store = s.AuthStore(file_path=auth_store_path)
    return auth_store

def get_test_stores():
    auth_store = s.AuthStore(file_path=auth_store_path)
    user_store = s.create_test_store(auth_store.public_key())
    return dict(
        auth_store=auth_store,
        user_store=user_store,
    )

def make_auth_token(server_key_pair, sender_public, receiver_public):
    return c.sign_text(server_key_pair,
                c.export_public_key(sender_public) + c.export_public_key(receiver_public))

def check_auth_token(server_public, auth_token, sender_public, receiver_secret):
    s = c.export_public_key(sender_public) + c.export_public_key(receiver_secret)
    return c.verify_sign(server_public, auth_token, s)
    
def make_auth_payload(server_public_key, sender_public_key, receiver_public_key):
    if type(receiver_public_key) is not str and type(receiver_public_key) is not bytes:
        receiver_public_key = c.export_public_key(receiver_public_key)
    return dict(
        receiver=receiver_public_key.decode(),
        sender=c.export_public_key(sender_public_key).decode()
    )

def process_auth_payload(server_key_pair, payload, hook=lambda x: x):
    sender_public_key = c.import_public_key(payload['sender'])
    receiver_public_key = c.import_public_key(payload['receiver'])
    sender_receiver = payload['sender'] + payload['receiver']
    # auth_token is a combination of sender and receiver
    auth_token = c.sign_text(server_key_pair, sender_receiver)
    symetric_key = c.generate_key()
    print(f"Generated key:{symetric_key}")
    symetric_sig = c.sign_text(server_key_pair, symetric_key)
    print(f"Signature key:{symetric_sig}")
    response = dict(
        symetric_key=c.encrypt_RSA(sender_public_key, symetric_key).decode(),
        symetric_signature=symetric_sig,
        auth_token=auth_token
    )
    hook(response)
    return response

def decode_auth_response(server_public, receiver_public, sender_secret, payload):
    unencrypted_sym_key = c.decrypt_RSA(sender_secret, payload['symetric_key'])
    signature = payload['symetric_signature']
    auth_token = payload['auth_token']
    if not c.verify_sign(server_public, signature, unencrypted_sym_key):
        return dict(error="Could not verify the integrity of the symetric key")
    concatenated_key = c.export_public_key(sender_secret) + c.export_public_key(receiver_public)
    if not c.verify_sign(server_public, auth_token, concatenated_key):
        return dict(error="Could not verify the integrity of the authentication token")
    return dict(
        symetric_key=unencrypted_sym_key,
        signature=signature,
        auth_token=auth_token,
    )

def get_auth_store():
    return s.AuthStore(auth_store_path)

def request_symetric_key(store, receiver_public_key):
    host = store.server_host()
    payload = make_auth_payload(
                store.server_public_key(),
                store.public_key(),
                receiver_public_key)
    headers={'Content-Type': 'application/json'}
    auth_payload = requests.post(
        f"http://{host}/get_symetric_key", 
        data=json.dumps(dict(payload=payload)),
        headers=headers,
    )
    if auth_payload.status_code == 200:
        auth_payload_json = auth_payload.json()
        return decode_auth_response(
                    store.server_public_key(),
                    receiver_public_key,
                    store.private_key(),
                    auth_payload_json['payload'],
                )
    else:
        return dict(error="An error occured on the server", error_message=auth_payload.json())

app = Flask(__name__)

auth_store = get_test_auth_store()

@app.route('/get_symetric_key', methods=['POST', 'PUT'])
def get_symetric_key() -> None:
    """
    Generates a symetric key for communication between Alice and Bob
    """
    if req.get_json():
        j = req.get_json()
        load = j['payload']
        print("Received auth request")
        print(json.dumps(load, indent=2, sort_keys=True))
        response = process_auth_payload(auth_store.private_key(), load)
        response = json.dumps(dict(payload=response))
        print(f"Responding with:\n{response}")
        return response, 200
    return json.dumps({'payload': 'error'}), 500


if __name__=="__main__":
    app.run(host='localhost', port=4000, debug=True)

