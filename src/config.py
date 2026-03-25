import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = b'8FmEj>1Sg(KW7g@'
    ALLOWED_EXTENSIONS_UPLOAD = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md'}