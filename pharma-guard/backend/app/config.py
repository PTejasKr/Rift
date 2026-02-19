"""
PharmaGuard Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///pharmaguard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Blockchain Configuration
    ALGORAND_NODE_URL = os.getenv('ALGORAND_NODE_URL', 'https://testnet-api.algorand.network')
    ALGORAND_INDEXER_URL = os.getenv('ALGORAND_INDEXER_URL', 'https://testnet-idx.algorand.network')
    ALGORAND_WALLET_MNEMONIC = os.getenv('ALGORAND_WALLET_MNEMONIC', '')
    CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS', '')
    
    # AI Service Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-4')
    
    # Application Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_BLOCKCHAIN_VERIFICATION = os.getenv('ENABLE_BLOCKCHAIN_VERIFICATION', 'true').lower() == 'true'
    MERKLE_TREE_DEPTH = int(os.getenv('MERKLE_TREE_DEPTH', '20'))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, DevelopmentConfig)
