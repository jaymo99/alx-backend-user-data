#!/usr/bin/env python3
"""Auth module
"""
from uuid import uuid4

from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string and returns a
    salted hash of the input password"""
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Returns a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a User"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if a user exists and password matches
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Takes an email string and returns session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
