#!/usr/bin/env python3
"""Auth module
"""
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string and returns a
    salted hash of the input password"""
    return hashpw(password.encode('utf-8'), gensalt())
