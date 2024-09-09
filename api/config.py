import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://arjun:arjun2005@localhost/webauctiondb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
