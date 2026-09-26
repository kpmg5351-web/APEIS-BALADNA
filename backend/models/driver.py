from backend.database import db, TimestampMixin, UUIDMixin
from datetime import datetime

class Driver(UUIDMixin, TimestampMixin, db.Model):
    """Driver profile and information"""
    __tablename__ = 'drivers'
    
    # User Reference
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Vehicle Info
    vehicle_type = db.Column(db.String(50), nullable=False)  # توك توك, سيارة ملاكي, سيارة نقل / جامبو
    vehicle_model = db.Column(db.String(255))
    vehicle_number = db.Column(db.String(50), unique=True)
    vehicle_color = db.Column(db.String(50))
    vehicle_image = db.Column(db.String(500))
    
    # License Info
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    license_expiry = db.Column(db.Date)
    license_image = db.Column(db.String(500))
    
    # Village
    village_id = db.Column(db.String(36), db.ForeignKey('villages.id'), nullable=True, index=True)
    
    # Status
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_online = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=False)
    
    # Current Location
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Stats
    total_trips = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=5.0)
    total_ratings = db.Column(db.Integer, default=0)
    
    # Timestamps
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='driver_profile', uselist=False)
    availability = db.relationship('DriverAvailability', backref='driver', lazy='dynamic', cascade='all, delete-orphan')
    locations = db.relationship('DriverLocation', backref='driver', lazy='dynamic', cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='driver', lazy='dynamic', foreign_keys='Rating.driver_id')
    
    def __repr__(self):
        return f'<Driver {self.user.name} ({self.vehicle_type})>'
    
    def to_dict(self, include_location=False):
        data = {
            'id': self.id,
            'user': self.user.to_dict(),
            'vehicle_type': self.vehicle_type,
            'vehicle_model': self.vehicle_model,
            'vehicle_number': self.vehicle_number,
            'vehicle_color': self.vehicle_color,
            'vehicle_image': self.vehicle_image,
            'village_id': self.village_id,
            'village_name': self.user.village.name if self.user.village else None,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'is_online': self.is_online,
            'is_available': self.is_available,
            'total_trips': self.total_trips,
            'rating': self.rating,
            'total_ratings': self.total_ratings,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
        }
        if include_location:
            data['latitude'] = self.latitude
            data['longitude'] = self.longitude
        return data


class DriverAvailability(UUIDMixin, TimestampMixin, db.Model):
    """Driver availability schedule"""
    __tablename__ = 'driver_availability'
    
    # Driver
    driver_id = db.Column(db.String(36), db.ForeignKey('drivers.id'), nullable=False, index=True)
    
    # Schedule
    day_of_week = db.Column(db.Integer)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return f'<DriverAvailability {days[self.day_of_week] if self.day_of_week is not None else "All"}>
    
    def to_dict(self):
        days = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'day_of_week': self.day_of_week,
            'day_name': days[self.day_of_week] if self.day_of_week is not None else 'كل يوم',
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_available': self.is_available,
        }


class DriverLocation(UUIDMixin, TimestampMixin, db.Model):
    """Real-time driver location tracking"""
    __tablename__ = 'driver_locations'
    
    # Driver
    driver_id = db.Column(db.String(36), db.ForeignKey('drivers.id'), nullable=False, index=True)
    
    # Location
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float)  # GPS accuracy in meters
    
    # Related Order
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=True, index=True)
    
    # Indexes for efficient querying
    __table_args__ = (
        db.Index('idx_driver_location_time', 'driver_id', 'created_at'),
        db.Index('idx_order_location', 'order_id', 'created_at'),
    )
    
    def __repr__(self):
        return f'<DriverLocation {self.driver_id} at ({self.latitude}, {self.longitude})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'accuracy': self.accuracy,
            'order_id': self.order_id,
            'created_at': self.created_at.isoformat(),
        }
