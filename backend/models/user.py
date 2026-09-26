from backend.database import db, TimestampMixin, UUIDMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Village(UUIDMixin, db.Model):
    """Village model - مركزي"""
    __tablename__ = 'villages'
    
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    users = db.relationship('User', backref='village', lazy='dynamic')
    posts = db.relationship('Post', backref='village', lazy='dynamic')
    services = db.relationship('Service', backref='village', lazy='dynamic')
    drivers = db.relationship('Driver', backref='village', lazy='dynamic')
    
    def __repr__(self):
        return f'<Village {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description
        }


class User(UUIDMixin, TimestampMixin, db.Model):
    """User model - الحساب الأساسي"""
    __tablename__ = 'users'
    
    # Basic Info
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True, index=True)
    
    # Authentication
    password_hash = db.Column(db.String(255))
    otp = db.Column(db.String(6))
    otp_attempts = db.Column(db.Integer, default=0)
    otp_created_at = db.Column(db.DateTime)
    otp_verified = db.Column(db.Boolean, default=False)
    
    # Profile
    avatar = db.Column(db.String(500))
    bio = db.Column(db.Text)
    village_id = db.Column(db.String(36), db.ForeignKey('villages.id'), nullable=True)
    
    # Status
    role = db.Column(db.String(50), default='USER', nullable=False)  # USER, DRIVER, SHOP, CRAFTSMAN, etc
    status = db.Column(db.String(50), default='ACTIVE')  # ACTIVE, BANNED, DELETED
    is_verified = db.Column(db.Boolean, default=False)
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy='dynamic', foreign_keys='Order.customer_id', cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', foreign_keys='Conversation.user_id', backref='user', lazy='dynamic')
    messages_sent = db.relationship('Message', backref='sender', lazy='dynamic', foreign_keys='Message.sender_id', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    ratings_given = db.relationship('Rating', backref='rater', lazy='dynamic', foreign_keys='Rating.rater_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password) if self.password_hash else False
    
    def __repr__(self):
        return f'<User {self.name} ({self.phone})>'
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone if include_sensitive else self.phone[-4:],
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'village_id': self.village_id,
            'village_name': self.village.name if self.village else None,
            'role': self.role,
            'status': self.status,
            'is_verified': self.is_verified,
            'is_online': self.is_online,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat(),
        }
        if include_sensitive:
            data['otp_verified'] = self.otp_verified
            data['email'] = self.email
        return data


class UserProfile(UUIDMixin, TimestampMixin, db.Model):
    """Extended user profile information"""
    __tablename__ = 'user_profiles'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Additional Info
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))  # MALE, FEMALE, OTHER
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Stats
    posts_count = db.Column(db.Integer, default=0)
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=5.0)
    total_ratings = db.Column(db.Integer, default=0)
    
    # Preferences
    notifications_enabled = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<UserProfile {self.user.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'posts_count': self.posts_count,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'rating': self.rating,
            'total_ratings': self.total_ratings,
        }
