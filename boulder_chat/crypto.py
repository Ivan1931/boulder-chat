from typing import Dict
from json import dumps

def public_key_encrypt(public_key: str, payload: str) -> str:
    """
    This method must encrypt paload using public_key
    """
    raise NotImplementedError()

def private_key_encrypt(private_key: str, payload: str) -> str:
    """
    Implement private key encryption here
    """
    raise NotImplementedError()

def private_key_decrypt(private_key: str, payload: str) -> str:
    """
    Decrypt something using a private key
    """
    raise NotImplementedError()

def public_key_decrypt(public_key: str, payload: str) -> str:
    """
    Decrypt something using a public key
    """
    raise NotImplementedError()

def symetric_key_encrypt(symetric_key: str, payload: str) -> str:
    """
    This method should encrypt and arbitrary string
    using a symetric key
    """
    raise NotImplementedError()
