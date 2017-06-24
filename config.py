import os

# import redis

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fitme:fitme9920@fitme.czefvwpajvgh.eu-west-1.rds.amazonaws.com:3306/fitmedb'
USE_TOKEN_AUTH = True

# enable rate limits only if redis is running
# try:
#     r = redis.Redis()
#     r.ping()
#     USE_RATE_LIMITS = True
# except redis.ConnectionError:
#     USE_RATE_LIMITS = False
