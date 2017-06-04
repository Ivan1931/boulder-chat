from . import crypto as c
import json
import base64

def save_json(file_path, json_dict):
    pass

def load_json(file_path):
    pass

class AuthStore(object):
    """
    This object keeps track of the authentication server state.
    So basically - "What is the authentication servers
    public key"?
    """
    def __init__(self, file_path):
        material_json = load_json(file_path)
        self.store_path = file_path
        self.store = dict(
            material= c.import_private_key(material_json['material'])
        )

    def public_key(self):
        return self.store['material'].publickey()

    def private_key(self):
        return self.store['material']

class ClientStore(object):
    def __init__(self, file_path='chat_data.json'):
        data = load_json(file_path)
        self.store_path = file_path
        self.server = data['server']
        self.server['public_key'] = c.import_public_key(data['server']['public_key'])
        self.users = {}
        for user_pk, u_data in data['users'].items():
            key_object = c.import_public_key(u_data['public_key'])
            u_data['public_key'] = key_object
            u_data['symetric_key'] = base64.b64decode(u_data['symetric_key'])
            self.users[user_pk] = u_data
        self.material = c.import_private_key(data['material'])

    def get_user_data(self, user_pk):
        """
        Returns public key, last known user host, symetric key and messages.
        Or None if the user does not exist.
        """
        if not (type(user_pk) is str or type(user_pk) is bytes):
            user_pk = c.export_public_key(user_pk)
        return self.users.get(user_pk)

    def public_key(self):
        return self.material.publickey()

    def private_key(self):
        return self.material

    def server_data(self):
        return self.server

    def server_host(self):
        """
        Server data
        """
        return self.server['host']

    def server_public_key(self):
        return self.server['public_key']

    def add_message(self, user_public_key, message, sender=False):
        user = self.get_user_data(user_public_key)
        user['conversation'].append(dict(message=message, sender=sender, is_file=False))

    def all_user_data(self):
        """
        Gets all data stored on users
        """
        return self.users

    def save(self):
        pass
