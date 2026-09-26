from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

def generate_id():
    """Generate UUID for database records"""
    return str(uuid.uuid4())

class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class UUIDMixin:
    """Mixin for UUID primary key"""
    id = db.Column(db.String(36), primary_key=True, default=generate_id)
