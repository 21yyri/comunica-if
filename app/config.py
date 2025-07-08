import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "18102007"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:labinfo@localhost:3306/comunica"
