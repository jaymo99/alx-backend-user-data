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
    pass
