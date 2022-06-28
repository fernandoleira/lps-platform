class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'super-secret'
    SEED_PATH = 'services/db/seeds'
    CROSS_ORIGIN = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_ENABLED = False
    REDIS_PASSWORD = None
