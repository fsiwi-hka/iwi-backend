import os
from functools import wraps
from flask import request, jsonify

API_KEY = os.environ.get("API_KEY")

def require_api_key(f):
    """Prüft, ob der X-API-Key dem in der .env entspricht."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({"error": "API Key fehlt (X-API-Key Header)."}), 401

        if api_key != API_KEY:
            return jsonify({"error": "Ungültiger API Key."}), 403

        return f(*args, **kwargs)

    return decorated_function