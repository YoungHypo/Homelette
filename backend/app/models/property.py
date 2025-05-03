from app import db

class Address(db.Model):
    __tablename__ = 'addresses'
    
    address_id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(200), nullable=False)
    apt_number = db.Column(db.String(20))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    
    # relationships
    properties = db.relationship('Property', backref='address', lazy='dynamic')
    
    def __init__(self, street_address, city, state, zip_code, apt_number=None):
        self.street_address = street_address
        self.apt_number = apt_number
        self.city = city
        self.state = state
        self.zip_code = zip_code
    
    def to_dict(self):
        return {
            'address_id': self.address_id,
            'street_address': self.street_address,
            'apt_number': self.apt_number,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'full_address': self.get_full_address()
        }
    
    def get_full_address(self):
        address = f"{self.street_address}"
        if self.apt_number:
            address += f" Apt {self.apt_number}"
        address += f", {self.city}, {self.state} {self.zip_code}"
        return address

class Property(db.Model):
    __tablename__ = 'properties'
    
    property_id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=False)
    area = db.Column(db.Numeric(10, 2), nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    owner_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    
    # relationships
    listings = db.relationship('Listing', backref='property', lazy='dynamic')
    
    def __init__(self, address_id, area, bathrooms, bedrooms, owner_id, property_type, image_url=None):
        self.address_id = address_id
        self.area = area
        self.bathrooms = bathrooms
        self.bedrooms = bedrooms
        self.owner_id = owner_id
        self.property_type = property_type
        self.image_url = image_url
    
    def to_dict(self):
        return {
            'property_id': self.property_id,
            'address_id': self.address_id,
            'area': float(self.area),
            'bathrooms': self.bathrooms,
            'bedrooms': self.bedrooms,
            'image_url': self.image_url,
            'owner_id': self.owner_id,
            'property_type': self.property_type
        } 