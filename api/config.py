class Config(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'super-secret'
    CROSS_ORIGIN = 'Content-Type'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/lps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'