import os
from datetime import timedelta

class Config:
    # database configuration
    MARIADB_IP = os.environ.get('MARIADB_IP')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://homelette_user:123aaa@{MARIADB_IP}/homelette'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ensure database migrations are automatically applied
    SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../migrations')
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-app-secret-key'
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Redis configuration
    REDIS_IP = os.environ.get('REDIS_IP')
    REDIS_URL = f'redis://{REDIS_IP}:6379/0'
    
    # Debug mode
    DEBUG = True