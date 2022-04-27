from datetime import timedelta
import os

basedir = os.path.dirname(__file__)
path = os.path.join(basedir, '..', 'webapp.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{path}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'erb56jh3ger'
REMEMBER_COOKIE_DURATION = timedelta(days=30)
