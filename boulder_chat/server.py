"""
The code to construct the server will be here
"""

class User(object):
    public_key: str
    user_name: str
    user_status: str
    messages: List[Messages] # this may change to a queue in future

class Server(object):
    private_key: str
    users: List[User]

