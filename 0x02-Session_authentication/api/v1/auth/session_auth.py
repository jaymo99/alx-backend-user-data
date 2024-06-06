#!/usr/bin/env python3
"""
auth module for the API
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session Auth API Authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a `user_id`"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
