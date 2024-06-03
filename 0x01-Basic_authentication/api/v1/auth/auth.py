#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    API Authentication class."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header from request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a User"""
        return None
