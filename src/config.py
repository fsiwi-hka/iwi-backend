import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/backend-db"

class Config:
    SECRET_KEY = b'8FmEj>1Sg(KW7g@'
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS_UPLOAD = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads')