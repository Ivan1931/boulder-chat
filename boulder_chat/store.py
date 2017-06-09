from . import crypto as c
import json
import base64
import random

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

class AuthStore(object):
    """
    This object keeps track of the authentication server state.
    So basically - "What is the authentication servers
    public key"?
    """
    def __init__(self, file_path, materials=None):
        self.store_path = file_path
        if materials:
            self.store = dict(material=materials)
        else:
            material_json = load_json(file_path)
            self.store = dict(
                material=c.import_private_key(material_json['material'])
            )

    def public_key(self):
        return self.store['material'].publickey()

    def private_key(self):
        return self.store['material']

    def toSerializableDict(self):
        return dict(material=c.export_private_key(self.private_key()).decode('utf-8'))

    def save(self):
        with open(self.store_path, 'w') as f:
            data = self.toSerializableDict()
            json.dump(data, f, indent=2, sort_keys=True)


class ClientStore(object):
    def __init__(self, file_path='chat_data.json', data=None):
        if data == None:
            data = load_json(file_path)
        self.from_data(data, file_path=file_path)

    def from_data(self, data, file_path=None):
        self.store_path = file_path
        self.server = {}
        self.server['public_key'] = c.import_public_key(data['server']['public_key'])
        self.server['host'] = data['server']['host']
        self.users = {}
        for user_pk, u_data in data['users'].items():
            key_object = c.import_public_key(u_data['public_key'])
            user_data = {}
            user_data['public_key'] = key_object
            user_data['symetric_key'] = base64.b64decode(u_data['symetric_key'])
            user_data['conversation'] = u_data['conversation']
            user_data['host'] = u_data['host']
            self.users[user_pk.encode()] = user_data
        self.material = c.import_private_key(data['material'])


    def get_user_data(self, user_pk):
        """
        Returns public key, last known user host, symetric key and messages.
        Or None if the user does not exist.
        """
        if not (type(user_pk) is str or type(user_pk) is bytes):
            user_pk = c.export_public_key(user_pk)
        if type(user_pk) is str:
            user_pk = user_pk.encode()
        return self.users.get(user_pk)

    def public_key(self):
        return self.material.publickey()

    def private_key(self):
        return self.material

    def server_data(self):
        return self.server

    def server_host(self):
        """
        Gets the host of the server
        """
        return self.server['host']

    def server_public_key(self):
        return self.server['public_key']

    def add_message(self, user_public_key, message, sender=False):
        user = self.get_user_data(user_public_key)
        user['conversation'].append(dict(message=message, sender=sender, is_file=False))

    def add_file(self, user_public_key, message, sender=False):
        file_name = [random.choice("1234567abcdefghijklmnop") for _ in range(8)]
        with open(file_name, 'w') as f:
            f.writelines(message)
        file_message = dict(is_file=True, file_path=file_name, sender=sender)
        user['conversation'].append(file_message)

    def get_user_host(self, user_public_key):
        user = self.get_user_data(user_public_key)
        if user:
            return user['host']
        else:
            return None

    def get_user_conversation(self, user_public_key):
        return self.get_user_data(user_public_key)['conversation']

    def add_user(self, public_key, symetric_key, first_message, is_sender=True, host='localhost:3000'):
        if type(public_key) is str:
            public_key = public_key.encode()
        if type(public_key) is not bytes:
            public_key = c.export_public_key(public_key)
        self.users[public_key] = dict(public_key=public_key, 
                                      conversation=[], 
                                      symetric_key=symetric_key, 
                                      host=host)
        self.add_message(public_key, first_message, sender=is_sender)

    def all_user_data(self):
        """
        Gets all data stored on users
        """
        return self.users

    def toSerializableDict(self):
        user_data = {}
        for user_key, user in self.users.items():
            user_data[user_key.decode('utf-8')] = dict(
                conversation=user['conversation'],
                symetric_key=base64.b64encode(user['symetric_key']).decode('utf-8'),
                public_key=user_key.decode('utf-8'),
                host=user['host'],
            )
        server_data = {}
        server_data['public_key'] = c.export_public_key(self.server_public_key()).decode('utf-8')
        server_data['host'] = self.server_host()
        material = c.export_private_key(self.material).decode('utf-8')
        result = dict(material=material, server=server_data, users=user_data)
        return result


    def save(self):
        data = self.toSerializableDict()
        with open(self.store_path, 'w') as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def get_user_symetric_key(self, user):
        symetric_key = self.get_user_data(user)
        if symetric_key:
            return symetric_key['symetric_key']

    def save_public_key(self, file_path):
        pk = self.public_key()
        with open(file_path, 'wb') as f:
            f.write(c.export_public_key(pk))

    def reload(self):
        with open(self.store_path, 'r') as f:
            data = json.load(f)
            self.from_data(data, self.store_path)

def create_test_store(server_materials=None):
    test_material = c.gen_key_RSA()
    user_material = c.gen_key_RSA()
    if server_materials:
        pass
    else:
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
    return ClientStore(file_path='user_test_1.json', data=test_store)
    
