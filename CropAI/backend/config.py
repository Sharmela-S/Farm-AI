"""
Configuration settings for AI Crop Recommendation System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ai-crop-recommendation-secret-key-2024'
    DEBUG = True
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # API settings
    API_VERSION = '1.0.0'
    API_TITLE = 'AI Crop Recommendation API'
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Model settings
    MODELS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'models')
    
    # Soil classification settings
    SOIL_TYPES = [
        'Sandy Soil',
        'Clay Soil',
        'Loamy Soil',
        'Silty Soil',
        'Peaty Soil',
        'Red Laterite Soil',
        'Black Soil (Regur)',
        'Alluvial Soil',
        'Chalky Soil',
        'Sandy Loam'
    ]
    
    # Crop database
    SUPPORTED_CROPS = [
        'Rice', 'Wheat', 'Cotton', 'Maize', 'Sugarcane',
        'Groundnut', 'Soybean', 'Bajra', 'Jowar', 'Ragi',
        'Vegetables', 'Pulses', 'Barley', 'Cashew'
    ]
    
    # Indian locations database (major cities/districts)
    INDIAN_LOCATIONS = [
        # Tamil Nadu
        'Chennai, Tamil Nadu', 'Coimbatore, Tamil Nadu', 'Madurai, Tamil Nadu',
        'Tiruchirappalli, Tamil Nadu', 'Salem, Tamil Nadu', 'Tiruppur, Tamil Nadu',
        
        # Karnataka
        'Bangalore, Karnataka', 'Mysore, Karnataka', 'Hubli, Karnataka',
        
        # Maharashtra
        'Mumbai, Maharashtra', 'Pune, Maharashtra', 'Nagpur, Maharashtra',
        
        # Andhra Pradesh & Telangana
        'Hyderabad, Telangana', 'Vijayawada, Andhra Pradesh', 'Visakhapatnam, Andhra Pradesh',
        
        # Kerala
        'Thiruvananthapuram, Kerala', 'Kochi, Kerala', 'Kozhikode, Kerala',
        
        # North India
        'Delhi, Delhi', 'Jaipur, Rajasthan', 'Lucknow, Uttar Pradesh',
        'Chandigarh, Chandigarh', 'Amritsar, Punjab',
        
        # East India
        'Kolkata, West Bengal', 'Patna, Bihar', 'Bhubaneswar, Odisha',
        
        # West India
        'Ahmedabad, Gujarat', 'Surat, Gujarat', 'Indore, Madhya Pradesh'
    ]
    
    # Season options
    SEASONS = ['kharif', 'rabi', 'summer']
    
    # Analysis thresholds
    MIN_CONFIDENCE = 75.0  # Minimum confidence for soil classification
    MIN_SUITABILITY = 70.0  # Minimum suitability for crop recommendation

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
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env='development'):
    """Get configuration based on environment"""
    return config.get(env, config['default'])