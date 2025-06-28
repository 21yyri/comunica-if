from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

from . import routes

with app.app_context():
    db.create_all()
