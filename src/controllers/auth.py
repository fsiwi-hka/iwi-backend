import secrets
from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from src.db import db
from src.middleware.auth import require_api_key
from src.models.user import UserEntity

auth = Blueprint('auth', __name__)

@auth.post('/users')
@require_api_key
def create_user():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "password", "name")):
        return jsonify({"error": "Fehlende Felder: email, password und name sind erforderlich."}), 400

    existing_user = db.session.execute(
        db.select(UserEntity).where(UserEntity.email == data['email'])
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({"error": "Ein Nutzer mit dieser Email existiert bereits."}), 409

    try:
        hashed_password = generate_password_hash(data['password'])

        new_user = UserEntity(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            api_key=secrets.token_urlsafe(32)
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Nutzer erfolgreich erstellt.",
            "created_by": g.user.name,
            "user": {
                "id": str(new_user.id),
                "name": new_user.name,
                "email": new_user.email,
                "api_key": new_user.api_key
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Datenbankfehler: {str(e)}"}), 500


@auth.post('/login')
def login():
    """
    Prüft Email und Passwort und gibt den API-Key zurück.
    """
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email und Passwort benötigt"}), 400

    user = db.session.execute(
        db.select(UserEntity).where(UserEntity.email == data['email'])
    ).scalar_one_or_none()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({
            "message": "Login erfolgreich",
            "api_key": user.api_key,
            "name": user.name
        }), 200

    return jsonify({"error": "Ungültige Email oder Passwort"}), 401