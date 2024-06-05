#!/usr/bin/env python3
"""
auth module for the API
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.base import DATA
from models.user import User


class BasicAuth(Auth):
    """
    Basic Auth API Authentication class."""

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """Returns the Base64 part of the Authorization header."""
        if not authorization_header or type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic'):
            return None

        parts = authorization_header.split(' ', 1)
        if len(parts) != 2:
            return None
        return parts[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """Returns the decoded value of a Base64 string."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """Returns the user email and password
        from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string into email and password
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """Returns the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        if not DATA:
            return None

        user_inst = User.search({"email": user_email})
        if not user_inst:
            return None
        if not user_inst[0].is_valid_password(user_pwd):
            return None

        return user_inst[0]
