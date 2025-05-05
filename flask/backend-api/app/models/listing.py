from datetime import datetime
from app import db

class Listing(db.Model):
    __tablename__ = 'listings'
    
    listing_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # relationships
    # delete-orphan is used to delete the interests when the listing is deleted
    interests = db.relationship('UserInterest', backref='listing', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, property_id, author_id, price, start_date, end_date):
        self.property_id = property_id
        self.author_id = author_id
        self.price = price
        self.start_date = start_date
        self.end_date = end_date
    
    def to_dict(self, include_property=False, include_address=False):
        result = {
            'listing_id': self.listing_id,
            'property_id': self.property_id,
            'author_id': self.author_id,
            'price': float(self.price),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_property and hasattr(self, 'property'):
            result['property'] = self.property.to_dict()
            
            if include_address and hasattr(self.property, 'address'):
                result['address'] = self.property.address.to_dict()
        
        return result 