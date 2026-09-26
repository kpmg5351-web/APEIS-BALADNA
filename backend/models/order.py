from backend.database import db, TimestampMixin, UUIDMixin
from datetime import datetime

class Order(UUIDMixin, TimestampMixin, db.Model):
    """Ride/Transport orders"""
    __tablename__ = 'orders'
    
    # Customer Info
    customer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Pickup & Destination
    pickup_location = db.Column(db.String(500), nullable=False)
    pickup_latitude = db.Column(db.Float)
    pickup_longitude = db.Column(db.Float)
    
    destination_location = db.Column(db.String(500), nullable=False)
    destination_latitude = db.Column(db.Float)
    destination_longitude = db.Column(db.Float)
    
    # Order Details
    order_type = db.Column(db.String(50))  # توك توك, سيارة ملاكي, سيارة نقل / جامبو
    notes = db.Column(db.Text)
    estimated_distance = db.Column(db.Float)
    estimated_time = db.Column(db.Integer)  # in minutes
    estimated_fare = db.Column(db.Float)
    
    # Driver Info
    driver_id = db.Column(db.String(36), db.ForeignKey('drivers.id'), nullable=True, index=True)
    
    # Status
    status = db.Column(db.String(50), default='NEW', index=True)  # NEW, SEARCHING_DRIVER, DRIVER_SELECTED, DRIVER_ACCEPTED, DRIVER_ARRIVING, IN_PROGRESS, COMPLETED, CANCELLED
    
    # Timestamps
    accepted_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Rating
    rating = db.Column(db.Integer)  # 1-5
    review = db.Column(db.Text)
    
    # Relationships
    driver = db.relationship('Driver', backref='orders', foreign_keys=[driver_id])
    status_history = db.relationship('OrderStatusHistory', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id[:8]} - {self.status}>'
    
    def to_dict(self, include_driver=False, include_history=False):
        data = {
            'id': self.id,
            'customer': self.customer.to_dict(),
            'pickup_location': self.pickup_location,
            'pickup_lat': self.pickup_latitude,
            'pickup_lng': self.pickup_longitude,
            'destination_location': self.destination_location,
            'destination_lat': self.destination_latitude,
            'destination_lng': self.destination_longitude,
            'order_type': self.order_type,
            'notes': self.notes,
            'estimated_distance': self.estimated_distance,
            'estimated_time': self.estimated_time,
            'estimated_fare': self.estimated_fare,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'rating': self.rating,
            'review': self.review,
        }
        if include_driver and self.driver:
            data['driver'] = self.driver.to_dict()
        if include_history:
            data['status_history'] = [h.to_dict() for h in self.status_history.all()]
        return data


class OrderStatusHistory(UUIDMixin, TimestampMixin, db.Model):
    """Track order status changes"""
    __tablename__ = 'order_status_history'
    
    # Relations
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False, index=True)
    changed_by_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Status Change
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50), nullable=False)
    
    # Notes
    notes = db.Column(db.Text)
    
    # Relationships
    changed_by = db.relationship('User', backref='order_status_changes')
    
    def __repr__(self):
        return f'<OrderStatusHistory {self.old_status} -> {self.new_status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'changed_by': self.changed_by.to_dict(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
        }
