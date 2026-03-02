import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS_UPLOAD = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads')