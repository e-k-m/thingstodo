import os

import environs

env = environs.Env()
env.read_env()


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = False
    CORS_ORIGIN_WHITELIST = "*"
    SQLALCHEMY_DATABASE_URI = env.str("THINGS_TODO_DATABASE")
    JWT_SECRET_KEY = env.str("THINGS_TODO_SECRET")
    LOG_LEVEL = env.log_level("THINGS_TODO_LOG_LEVEL", "WARNING")


class ProdConfig(Config):
    ENV = "production"


class DevConfig(Config):
    ENV = "development"
    LOG_LEVEL = env.log_level("THINGS_TODO_LOG_LEVEL", "DEBUG")


class TestConfig(Config):
    ENV = "development"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
