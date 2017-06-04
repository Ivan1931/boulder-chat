from boulder_chat import store
from boulder_chat import crypto as c
from mock import patch
import base64
import json

def test_authentication_store():
    test_material = c.gen_key_RSA()
    test_store = dict(
        material=c.export_private_key(test_material).decode('utf-8')
    )
    with patch('boulder_chat.store.load_json', return_value=test_store):
        auth_store = store.AuthStore('fake_file_path.json')
        assert(auth_store.public_key() == test_material.publickey())
        assert(auth_store.private_key() == test_material)

def test_client_store():
    test_material = c.gen_key_RSA()
    user_material = c.gen_key_RSA()
    server_materials = c.gen_key_RSA()
    user_public_key = c.export_public_key(user_material)
    user_symetric_key = c.generate_key()
    test_user = dict(
        public_key=c.export_public_key(user_material).decode('utf-8'),
        conversation=[
            dict(is_file=False, sender=True, message='Hello! How are you?'),
            dict(is_file=False, sender=False, message='Fine thanks, how goes it with you?'),
            dict(is_file=False, sender=True, message='Great thanks!'),
            dict(is_file=True, sender=False, file_path='file1.txt'),
        ],
        symetric_key=base64.b64encode(user_symetric_key).decode('utf-8'),
        host='localhost:4000',
    )
    test_server = dict(
            host='localhost:5000',
            public_key=c.export_public_key(server_materials).decode('utf-8'),
    )
    test_store = dict(
        material=c.export_private_key(test_material).decode('utf-8'),
        server=test_server,
        users={}, # defined bellow this
    )
    test_store['users'][user_public_key.decode('utf-8')] = test_user
    with patch('boulder_chat.store.load_json', return_value=test_store):
        client_store = store.ClientStore('fake_file_path.json')
        assert(client_store.get_user_data(user_public_key)['conversation'] == test_user['conversation'])
        assert(client_store.get_user_data(c.import_public_key(user_public_key))['conversation'] == test_user['conversation'])
        assert(client_store.public_key() == test_material.publickey())
        assert(client_store.private_key() == test_material)
        assert(client_store.server_data()['public_key'] == server_materials.publickey())
        test_message = "Are you still there?"
        client_store.add_message(user_public_key, test_message, sender=True)
        test_user["conversation"].append(dict(is_file=False, message=test_message, sender=True))
        assert(client_store.get_user_data(user_public_key)['conversation'] == test_user['conversation'])
        reserialized_store = json.loads(json.dumps(client_store.toSerializableDict())) 
        print(reserialized_store)
        print(test_store)
        assert(reserialized_store == test_store)
