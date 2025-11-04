import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    RL_LEARNING_RATE = float(os.environ.get('RL_LEARNING_RATE', '0.1'))
    
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'
    RL_EPSILON = 0.3
    
class StagingConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('STAGING_DB_URL', 'sqlite:///staging.db')
    RL_EPSILON = 0.1
    
class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    RL_EPSILON = 0.05
    
config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}