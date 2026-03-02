import asyncio
import sys

from flask_cors import CORS
from flask import Flask
from src.config import Config
import auth
import content
from loguru import logger

from src.db import db

logger.add(sys.stderr)
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173"])
db.init_app(app)

with app.app_context() as ctx:
    try:
        print("Creating all tables...")
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    app.run(debug=True)