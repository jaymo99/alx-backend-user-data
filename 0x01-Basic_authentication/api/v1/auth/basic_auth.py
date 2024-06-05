#!/usr/bin/env python3
"""
auth module for the API
"""
import base64
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


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
