"""
This module is in charge of communication between two clients. It works
in the following way. We assume that Alice has obtained an auth token from the AuthenticationServer:
    let P_A, P_B be public keys of Alice and Bob
        p_a, p_b be public keys of Alice and Bob
        S_AB be the symetric key between Alice and Bob
        sig be the authentication token between Alice and Bob

"""
from flask import Flask
from flask import request as req
from . import crypto as c

# Setup logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

def create_message_payload(key_pair, symetric_key, message):
    message_hash = c.create_key(message)
    encrypted_message = c.encrypt_AES(key_pair, message)
    signature = c.sign_text(key_pair, message_hash)
    return dict(signature=signature, 
                public_key=c.export_public_key(key_pair), 
                message=encrypted_message)

def create_first_message_payload(sender_key_pair, reciever_key_pair, symetric_key, message):
    encrypted_symetric_key = c.encrypt_RSA(reciever_key_pair.publickey(), symetric_key)
    message_hash = c.create_key(message)
    signature = c.sign_text(sender_key_pair, message_hash)
    encrypted_message = c.encrypt_AES(symetric_key, message)
    return dict( 
        signature=signature,
        symetric_key=encrypted_symetric_key.decode(),
        message=encrypted_message,
        public_key=c.export_public_key(sender_key_pair).decode(),
    )

def process_first_message_payload(secret_key, payload, hook=lambda x: x):
    signature = payload['signature']
    public_key = c.import_public_key(payload['public_key']) # need this to verify signature
    encrypted_symetric_key = payload['symetric_key']
    encrypted_message = payload['message']
    symetric_key = c.decrypt_RSA(secret_key, encrypted_symetric_key)
    message = c.decrypt_AES(symetric_key, encrypted_message)
    assert(c.verify_sign(public_key, signature, c.create_key(message)))
    result = dict(
        sender=public_key, 
        message=message, 
        symetric_key=symetric_key
    )
    hook(result)
    return result

def process_message_payload(symetric_key, payload, hook=lambda x: x):
    encrypted_message = payload['message']
    signature = payload['signature']
    public_key = payload['public_key']
    # Crash violently if we cannot verify someones sign for now
    message = c.decrypt_AES(symetric_key, encrypted_message)
    assert(c.verify_sign(c.import_public_key(public_key), signature, message))
    result = dict(sender=public_key, message=message)
    hook(result)
    return result

@app.route('/send_file', methods=['POST'])
def send_files():
    return 'hello'

@app.route('/send_first_message', methods=['POST'])
def send_first_message():
    if req.json:
        return process_first_message_payload(req.json)

@app.route('/send_message', methods=['POST'])
def send_message():
    if req.json:
        return process_message_payload(req.json)
