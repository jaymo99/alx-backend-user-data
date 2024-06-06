#!/usr/bin/env python3
""" Module of Session views
"""
from os import getenv

from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """Handles session authentication"""
    from api.v1.app import auth

    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    sess_id = auth.create_session(user[0].id)
    resp = jsonify(user[0].to_json())
    resp.set_cookie(getenv('SESSION_NAME', 'None'), sess_id)
    return resp
