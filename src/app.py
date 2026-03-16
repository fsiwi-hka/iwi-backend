import os
import sys
from flask_cors import CORS
from flask import Flask
from src.config import Config
from loguru import logger
from src.controllers.content import content_bp

logger.add(sys.stderr)

app = Flask(__name__)

MARKDOWN_DIR = os.environ.get("MARKDOWN_DIR", "./data/uploads")
os.makedirs(MARKDOWN_DIR, exist_ok=True)

app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False
)

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173"])

app.register_blueprint(content_bp, url_prefix='/api/content')

if __name__ == "__main__":
    app.run(debug=True)