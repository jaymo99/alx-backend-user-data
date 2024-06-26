#!/usr/bin/env python3
"""
auth module for the API
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session Auth API Authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a `user_id`
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a `User ID` based on a `Session ID`.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Returns a `User` based on cookie value
        """
        user_id = self.user_id_for_session_id(
            self.session_cookie(request)
        )
        if not user_id:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session. Logout
        """
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        try:
            del self.user_id_by_session_id[sess_id]
        except KeyError:
            return False
        return True
