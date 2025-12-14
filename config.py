class Config:
    """Config settings for the Flask application"""
    
    # Security
    SECRET_KEY = 'dian1612102703'
    
    # MySQL Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'mlbbdb'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # JWT Settings
    JWT_EXPIRATION_HOURS = 24
    
    # API Settings
    DEBUG = True
    PORT = 5000