from decouple import config

ENV = config('FLASK_ENV', default='production')
DEBUG = ENV
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
