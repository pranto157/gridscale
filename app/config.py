import os
import environ


env = environ.Env()


class Config(object):
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess"
    SQLALCHEMY_DATABASE_URI = env("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FOLDER = os.path.join(os.path.join("/var/log", "gridscale"))


class DevelopmentConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


CONFIG_MAP = {"development": DevelopmentConfig, "production": ProductionConfig}
