import os
import environ


env = environ.Env()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess"
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FOLDER = os.path.join(os.path.join("/var/log", "gridscale"))


class DevelopmentConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


CONFIG_MAP = {"development": DevelopmentConfig, "production": ProductionConfig}
