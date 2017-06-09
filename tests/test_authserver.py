import boulder_chat.crypto as c
import boulder_chat.authserver as a
import json
from mock import patch

def test_process_auth_payload():
    a_key = c.gen_key_RSA()
    s_key = c.gen_key_RSA()
    r_key = c.gen_key_RSA()
    test_key = c.generate_key()
    payload = a.make_auth_payload(a_key.publickey(), s_key.publickey(), r_key.publickey())
    payload_json = json.dumps(payload)
    with patch('boulder_chat.crypto.generate_key', return_value=test_key):
        auth_payload = a.process_auth_payload(a_key, json.loads(payload_json))
        # simulate convertion too and from json
        auth_payload_json = json.dumps(auth_payload)
        auth_load = a.decode_auth_response(a_key.publickey(), r_key.publickey(), s_key, json.loads(auth_payload_json))
        assert(test_key == auth_load['symetric_key'])
        assert(c.verify_sign(a_key.publickey(), auth_load['signature'], auth_load['symetric_key']))

