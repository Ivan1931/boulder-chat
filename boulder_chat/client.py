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
import requests
from . import crypto as c
from . import authserver as a
from . import store as s
import json

def create_message_payload(key_pair, symetric_key, message, is_file=False):
    message_hash = c.create_key(message)
    encrypted_message = c.encrypt_AES(symetric_key, message)
    signature = c.sign_text(key_pair, message_hash)
    return dict(signature=signature, 
                public_key=c.export_public_key(key_pair).decode(), 
                message=encrypted_message)

def create_first_message_payload(sender_key_pair, reciever_key_pair, symetric_key, authentication_token, sender_host, message):
    encrypted_symetric_key = c.encrypt_RSA(reciever_key_pair.publickey(), symetric_key)
    message_hash = c.create_key(message)
    signature = c.sign_text(sender_key_pair, message_hash)
    encrypted_message = c.encrypt_AES(symetric_key, message)
    payload_dict = dict( 
        signature=signature,
        symetric_key=encrypted_symetric_key.decode(),
        message=encrypted_message,
        public_key=c.export_public_key(sender_key_pair).decode(),
        auth_token=authentication_token,
        host=sender_host,
    )
    print("First messagepayload created:\n")
    print(payload_dict)
    return payload_dict

def process_message_payload(symetric_key, payload, hook=lambda x: x):
    encrypted_message = payload['message']
    signature = payload['signature']
    public_key = payload['public_key']
    is_file = False
    if 'is_file' in payload and payload['is_file']:
        is_file=True
    # Crash violently if we cannot verify someones sign for now
    message = c.decrypt_AES(symetric_key, encrypted_message)
    print(f"Unencrypted message:\n{message}")
    if not c.verify_sign(c.import_public_key(public_key), signature, c.create_key(message)):
        return dict(error="it appears that the message sent to you has been tampered with")
    result = dict(sender=public_key, 
                  message=message, 
                  is_file=is_file)
    hook(result)
    return result

def process_first_message_payload(secret_key, server_public, payload, hook=lambda x: x):
    signature = payload['signature']
    public_key = c.import_public_key(payload['public_key']) # need this to verify signature
    encrypted_symetric_key = payload['symetric_key']
    encrypted_message = payload['message']
    auth_token = payload['auth_token']
    symetric_key = c.decrypt_RSA(secret_key, encrypted_symetric_key)
    try:
        message = c.decrypt_AES(symetric_key, encrypted_message)
    except ValueError:
        return dict(error="It seems like someone has tampered with the symetric key in transit")
    if not c.verify_sign(public_key, signature, c.create_key(message)):
        return dict(error="It seems that the message has been tampered with. Be careful")
    if not a.check_auth_token(server_public, auth_token, public_key, secret_key):
        return dict(error="It seems that the user you're trying to chat to is unauthorized. Be careful")
    result = dict(
        sender=public_key, 
        message=message, 
        symetric_key=symetric_key,
        host=payload['host'],
    )
    hook(result)
    return result

def deliver_message(store, user_public_key, message, is_file=False):
    sender_private_key = store.private_key()
    symetric_key = store.get_user_symetric_key(user_public_key)
    print(f"Sending message")
    print(f"sender:\n{sender_private_key}")
    print(f"reciever:\n{user_public_key}")
    print(f"symetric_key:{symetric_key}")
    print(f"message:{message}")
    payload = create_message_payload(sender_private_key, store.get_user_symetric_key(user_public_key), message, is_file)
    host = store.get_user_host(user_public_key)
    headers={'Content-Type': 'application/json'}
    message_respone = requests.post(
            f"http://{host}/send_message", 
            data=json.dumps(dict(payload=payload)),
            headers=headers,
        )
    if message_respone.status_code == 200:
        store.add_message(user_public_key, message, sender=True)
        store.save()
        return message_respone

def deliver_first_message(store, user_host, user_public_key, sender_host, message):
    auth_payload = a.request_symetric_key(store, user_public_key)
    if type(user_public_key) is bytes:
        user_public_key = c.import_public_key(user_public_key)
    if type(user_public_key) is str:
        user_public_key = c.import_public_key(user_public_key.encode())
    if auth_payload:
        symetric_key = auth_payload['symetric_key']
        auth_token = auth_payload['auth_token']
        first_payload = create_first_message_payload(
                    store.private_key(),
                    user_public_key,
                    symetric_key,
                    auth_token,
                    sender_host,
                    message)
        headers={'Content-Type': 'application/json'}
        message_respone = requests.post(
                f"http://{user_host}/send_first_message", 
                data=json.dumps(dict(payload=first_payload)),
                headers=headers,
            )
        if message_respone.status_code == 200:
            print(f"Succesfully sent first message to {user_public_key}")
            print(f"Generated symetric_key: {symetric_key}")
            print(f"User is at host: {user_host}")
            print(f"We sent the message:\n{message}")
            store.add_user(user_public_key, 
                           symetric_key,
                           message,
                           host=user_host,
                           is_sender=True)
            store.save()
            return dict(ok=True)
        else:
            return message_respone.json()
    else:
        print("Error requesting symetric key:")
        print(auth_payload)

def send_file(store, user, file_path):
    text = ''
    with open(file_path, 'r') as f:
        for line in f:
            text += line
    deliver_message(store, user, text, True)


def recieve_first_message(store, message):
    sender = message['sender']
    print(f"Adding user:\n{sender}")
    store.add_user(
            message['sender'], 
            message['symetric_key'], 
            message['message'], 
            is_sender=False, 
            host=message['host'])
    store.save()

def recieve_message(store, message):
    store.add_message(message['sender'], message['message'])
    store.save()


def create_test_users(save=False):
    stores = a.get_test_stores()
    sender = stores['user_store']
    auth = stores['auth_store']
    receiver = s.create_test_store(auth.public_key())
    sender.store_path = 'sender.json'
    sender_pk_path = 'sender.pem'
    receiver.users = {}
    receiver.store_path = 'receiver.json'
    receiver_pk_path = 'receiver.pem'
    sender.users = {}
    if save:
        sender.save()
        sender.save_public_key(sender_pk_path)
        receiver.save()
        receiver.save_public_key(receiver_pk_path)

def get_receiver():
    return s.ClientStore('receiver.json')

def get_sender():
    return s.ClientStore('sender.json')

app = Flask(__name__)

@app.route('/send_first_message', methods=['POST'])
def send_first_message():
    if req.get_json():
        first_message = process_first_message_payload(
                store.private_key(),
                store.server_public_key(),
                req.get_json()['payload'], 
                hook=lambda message: recieve_first_message(store, message)
            )
        print("Sucessfully processed first message")
        print("Payload was:\n")
        print(req.get_json()['payload'])
        print("Which was processed too")
        print(first_message)
        if 'error' in first_message:
            return first_message, 400
        else:
            return "{'recieved': 'ok'}", 200

@app.route('/send_message', methods=['POST'])
def send_message():
    if req.get_json():
        payload = req.get_json()['payload']
        print("Message recieved:")
        print(json.dumps(payload, indent=2))
        sender_public_key = payload['public_key']
        store.reload()
        symetric_key = store.get_user_symetric_key(sender_public_key) 
        # print(store.all_user_data())
        print(f"sender public key:{sender_public_key}")
        if symetric_key:
            print(f"sender symetric_key:{symetric_key}")
            first_message = process_message_payload(
                        symetric_key,
                        payload,
                        hook=lambda message: recieve_message(store, message)
                    )
        else:
            print(f"User not found")
            return "{'error': 'no symetric key'}", 400
        if 'error' in first_message:
            return first_message, 400
        else:
            return "{'recieved': 'ok'}", 200

# Supress flask logging
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import os

try:
    file_path = os.environ['FILE_PATH']
    store = s.ClientStore(file_path)
except FileNotFoundError:
    print("Not found Bah")

def run_flask():
    sender_port = os.environ['PORT']
    file_path = os.environ['FILE_PATH']
    print("Starting flask")
    app.run('127.0.0.1', port=int(sender_port))
