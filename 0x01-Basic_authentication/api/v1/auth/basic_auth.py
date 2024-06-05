#!/usr/bin/env python3
"""
auth module for the API
"""
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
