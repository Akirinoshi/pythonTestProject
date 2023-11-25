import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    APP_NAME = os.environ.get('APP_NAME')
    DOMAIN = os.environ.get('FLASK_RUN_HOST')
    PORT = os.environ.get('FLASK_RUN_PORT')
    DEBUG = os.environ.get('FLASK_DEBUG')
    TESTING = False
    CSRF_ENABLED = True
    ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    JWT_PROJECT_KEY = os.environ.get('JWT_PROJECT_KEY')


