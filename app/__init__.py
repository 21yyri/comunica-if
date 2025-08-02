from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db = SQLAlchemy()
db.init_app(app)

jwt = JWTManager(app)

migrate = Migrate(app, db)

from . import routes

with app.app_context():
    db.create_all()
