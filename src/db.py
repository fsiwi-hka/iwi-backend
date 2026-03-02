from flask_sqlalchemy import SQLAlchemy
from src.models import *  # noqa

db = SQLAlchemy(model_class=Base)