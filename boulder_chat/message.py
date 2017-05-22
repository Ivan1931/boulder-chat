"""
This module contains the message class object and utilities to construct messages
"""

from arrow import Arrow

Time = Arrow

class Message(object):
    message_id: str
    checksum: int
    send_public_key: str
    reciever_public_key: str
    timestamp: Time
