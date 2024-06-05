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
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path = "{}/".format(path)
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header from request object
        """
        if not request:
            return None
        auth = request.headers.get('Authorization')
        if not auth:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a User"""
        return None
