class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/lps'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
