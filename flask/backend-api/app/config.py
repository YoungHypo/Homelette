import os
from datetime import timedelta

class Config:
    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ensure database migrations are automatically applied
    SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../migrations')
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-app-secret-key'
    
    # file upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'