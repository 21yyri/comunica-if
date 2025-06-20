from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

from app import routes

with app.app_context():
    db.create_all()
