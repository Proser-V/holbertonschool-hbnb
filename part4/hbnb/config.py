'''
This module provides the base configuration for the server's application.
'''
import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',
                               'a-string-secret-at-least-256-bits-long')
    LOCATIONIQ_KEY = "pk.84031ba5f6aff806113e746e96348592"
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # False : HTTP / True : HTTPS
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'  # /refresh for security in prod
    JWT_COOKIE_CSRF_PROTECT = False  # True for security in prod

class DevelopmentConfig(Config):
    # Use 'sqlite:///testDB.db' to use automated tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
