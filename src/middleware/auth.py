from functools import wraps
from flask import request, jsonify, g
from sqlalchemy import select

from src.db import db
from src.models.user import UserEntity

def require_api_key(f):
    """Prüft, ob der X-API-Key in der User-Tabelle existiert."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({"error": "API Key fehlt (X-API-Key Header)."}), 401

        user = db.session.execute(
            select(UserEntity).where(UserEntity.api_key == api_key)
        ).scalar_one_or_none()

        if user is None:
            return jsonify({"error": "Ungültiger API Key."}), 403

        g.user = user
        return f(*args, **kwargs)

    return decorated_function