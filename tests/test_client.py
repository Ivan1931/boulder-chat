import boulder_chat.client as client
import boulder_chat.crypto as c
import boulder_chat.authserver as a
import json

def test_process_message_payload():
    message = 'Hello, my name is actually Jonah. Not just public key'
    message_hash = c.create_key(message)
    key = c.create_key('this is a password')
    key_pair = c.gen_key_RSA()
    public_key = c.export_public_key(key_pair)
    payload = client.create_message_payload(key_pair, key, message)
    payload_json = json.dumps(payload)
    result = client.process_message_payload(key, json.loads(payload_json))
    assert('error' not in result)
    assert(result['message'] == message)


def test_process_first_message_payload():
    message = "Hi there, I'm Jonah. This is my first message. Cool"
    key = c.create_key('this is password')
    r_key_pair = c.gen_key_RSA()
    s_key_pair = c.gen_key_RSA()
    server_key_pair = c.gen_key_RSA()
    auth_token = a.make_auth_token(server_key_pair, s_key_pair, r_key_pair)
    payload = client.create_first_message_payload(s_key_pair, r_key_pair.publickey(), key, auth_token, 'localhost:3000', message)
    payload_json = json.dumps(payload)
    result = client.process_first_message_payload(r_key_pair, server_key_pair.publickey(), json.loads(payload_json))
    assert('error' not in result)
    assert(result['message'] == message)
