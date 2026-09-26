import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///abees_baladna.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # JWT
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY', 
        'dev-secret-key-change-in-production'
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=90)
    
    # Security
    SECURITY_PASSWORD_SALT = os.getenv(
        'SECURITY_PASSWORD_SALT',
        'dev-salt-change-in-production'
    )
    
    # OTP
    OTP_EXPIRY_MINUTES = 10
    OTP_LENGTH = 6
    
    # CORS
    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:8000,http://localhost:3000'
    ).split(',')
    
    # SocketIO
    SOCKETIO_MESSAGE_QUEUE = os.getenv(
        'SOCKETIO_MESSAGE_QUEUE',
        'redis://localhost:6379'
    )
    
    # File Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Villages (مركزي)
    VILLAGES = [
        {'id': 1, 'name': 'أبيس القرية الأولى', 'code': 'ABEES_1'},
        {'id': 2, 'name': 'أبيس القرية الثانية', 'code': 'ABEES_2'},
        {'id': 3, 'name': 'أبيس القرية السابعة', 'code': 'ABEES_7'},
        {'id': 4, 'name': 'أبيس القرية الثامنة', 'code': 'ABEES_8'},
        {'id': 5, 'name': 'عزبة القلعة / أبيس', 'code': 'ABEES_QLA'},
    ]
    
    # User Roles
    USER_ROLES = {
        'USER': 'مستخدم',
        'DRIVER': 'سائق',
        'SHOP': 'صاحب محل',
        'CRAFTSMAN': 'حرفي',
        'PHARMACY': 'صيدلية',
        'HOSPITAL': 'مستشفى',
        'ADMIN': 'إدارة'
    }
    
    # Service Categories
    CRAFTSMAN_SPECIALTIES = [
        'سباكة',
        'كهرباء',
        'نجارة',
        'نقاشة',
        'تكييف',
        'حدادة'
    ]
    
    VEHICLE_TYPES = [
        'توك توك',
        'سيارة ملاكي',
        'سيارة نقل / جامبو'
    ]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
