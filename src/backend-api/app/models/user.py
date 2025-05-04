import uuid
from datetime import datetime
import bcrypt
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile_picture_url = db.Column(db.String(255))
    major = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    about_me = db.Column(db.Text)
    
    # relationships
    properties = db.relationship('Property', backref='owner', lazy='dynamic')
    listings = db.relationship('Listing', backref='author', lazy='dynamic')
    interests = db.relationship('UserInterest', backref='user', lazy='dynamic')
    
    def __init__(self, email, password, first_name, last_name, **kwargs):
        self.user_id = str(uuid.uuid4())
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.user_id,
            'email': self.email,
            'first_name': self.first_name, 
            'last_name': self.last_name,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'profile_picture_url': self.profile_picture_url,
            'major': self.major,
            'graduation_year': self.graduation_year,
            'about_me': self.about_me
        }

class UserInterest(db.Model):
    __tablename__ = 'user_interests'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), primary_key=True)
    interest_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, user_id, listing_id):
        self.user_id = user_id
        self.listing_id = listing_id
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'listing_id': self.listing_id,
            'interest_date': self.interest_date.isoformat() if self.interest_date else None
        } 