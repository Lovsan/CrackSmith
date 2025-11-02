import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Validate required secrets in production
    if not SECRET_KEY or not JWT_SECRET_KEY:
        raise ValueError("SECRET_KEY and JWT_SECRET_KEY must be set in environment variables")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cracksmith.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # App specific settings
    ADMIN_PIN = os.environ.get('ADMIN_PIN') or '1234'
    MAX_FREE_THREADS = int(os.environ.get('MAX_FREE_THREADS', 2))
    MAX_PAID_THREADS = int(os.environ.get('MAX_PAID_THREADS', 8))
    FREE_RATE_LIMIT = int(os.environ.get('FREE_RATE_LIMIT', 10))
    PAID_RATE_LIMIT = int(os.environ.get('PAID_RATE_LIMIT', 100))
    
    # Celery configuration
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
    # Allow default secrets in development only
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret-key-change-in-production'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Ensure secrets are set in production
    if not os.environ.get('SECRET_KEY') or not os.environ.get('JWT_SECRET_KEY'):
        raise ValueError("SECRET_KEY and JWT_SECRET_KEY must be set in production!")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
