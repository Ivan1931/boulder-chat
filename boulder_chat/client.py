"""
The code for the python client will reside over here
"""
from typing import List
from arrow import Arrow

Time = Arrow

class LocalMessage(object):
    message: str
    timestamp: Time
    sent: bool # True if we sent this message

    def __lt__(self, other):
        """
        Messages are ordered by timestamp so that
        we can order them in chronological order
        """
        self.timestamp < other.timestamp

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class Friend(object):
    symetric_key: str
    public_key: str
    messages: List[LocalMessages] = []


class ClientState(object):
    address_book: List[Friend]
    private_key: str
    public_key: str
    server_public_key: str
    server_address: str
