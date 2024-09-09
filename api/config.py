import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pass@localhost/webauctiondb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
