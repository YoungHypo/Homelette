from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.listing import Listing
from app.models.property import Property, Address
from app.models.user import User
from app import db

listing_bp = Blueprint('listings', __name__)

@listing_bp.route('', methods=['GET'])
def get_listings():
    # get filter parameters
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    city = request.args.get('city')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # build query
    query = Listing.query.join(Property).join(Address)
    
    # apply filter conditions
    if price_min is not None:
        query = query.filter(Listing.price >= price_min)
    if price_max is not None:
        query = query.filter(Listing.price <= price_max)
    if bedrooms is not None:
        query = query.filter(Property.bedrooms == bedrooms)
    if city:
        query = query.filter(Address.city == city)
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Listing.start_date <= start_date_obj)
        except ValueError:
            pass
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Listing.end_date >= end_date_obj)
        except ValueError:
            pass
    
    # execute query
    listings = query.all()
    
    # return results
    result = [listing.to_dict(include_property=True, include_address=True) for listing in listings]
    return jsonify(result), 200

@listing_bp.route('/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    
    # return listing with property and address information
    result = listing.to_dict(include_property=True, include_address=True)
    return jsonify(result), 200

@listing_bp.route('', methods=['POST'])
@jwt_required()
def create_listing():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # verify required fields
    required_fields = {
        'address': ['street_address', 'city', 'state', 'zip_code'],
        'property': ['area', 'bathrooms', 'bedrooms', 'property_type'],
        'listing': ['price', 'start_date', 'end_date']
    }
    
    for category, fields in required_fields.items():
        if category not in data:
            return jsonify({"error": f"Missing {category} information"}), 400
        
        for field in fields:
            if field not in data[category]:
                return jsonify({"error": f"Missing field: {field} in {category}"}), 400
    
    try:
        # create address
        address_data = data['address']
        address = Address(
            street_address=address_data['street_address'],
            city=address_data['city'],
            state=address_data['state'],
            zip_code=address_data['zip_code'],
            apt_number=address_data.get('apt_number')
        )
        db.session.add(address)
        db.session.flush()  # get address_id
        
        # create property
        property_data = data['property']
        property = Property(
            address_id=address.address_id,
            area=property_data['area'],
            bathrooms=property_data['bathrooms'],
            bedrooms=property_data['bedrooms'],
            owner_id=user_id,
            property_type=property_data['property_type'],
            image_url=property_data.get('image_url')
        )
        db.session.add(property)
        db.session.flush()  # get property_id
        
        # create listing
        listing_data = data['listing']
        try:
            start_date = datetime.strptime(listing_data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(listing_data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        listing = Listing(
            property_id=property.property_id,
            author_id=user_id,
            price=listing_data['price'],
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(listing)
        
        # update user's listing_ids (if implemented)
        
        db.session.commit()
        
        return jsonify({
            "message": "Listing created successfully",
            "listing_id": listing.listing_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@listing_bp.route('/<listing_id>', methods=['PUT'])
@jwt_required()
def update_listing(listing_id):
    user_id = get_jwt_identity()
    
    # get listing
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    
    # check permission
    if listing.author_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # update listing information
        if 'listing' in data:
            listing_data = data['listing']
            
            if 'price' in listing_data:
                listing.price = listing_data['price']
            
            if 'start_date' in listing_data:
                try:
                    listing.start_date = datetime.strptime(listing_data['start_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
            
            if 'end_date' in listing_data:
                try:
                    listing.end_date = datetime.strptime(listing_data['end_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
        
        # update property information
        if 'property' in data and listing.property:
            property_data = data['property']
            property = listing.property
            
            updatable_property_fields = ['area', 'bathrooms', 'bedrooms', 'property_type', 'image_url']
            for field in updatable_property_fields:
                if field in property_data:
                    setattr(property, field, property_data[field])
        
        # update address information
        if 'address' in data and listing.property and listing.property.address:
            address_data = data['address']
            address = listing.property.address
            
            updatable_address_fields = ['street_address', 'apt_number', 'city', 'state', 'zip_code']
            for field in updatable_address_fields:
                if field in address_data:
                    setattr(address, field, address_data[field])
        
        db.session.commit()
        
        return jsonify({
            "message": "Listing updated successfully",
            "listing": listing.to_dict(include_property=True, include_address=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@listing_bp.route('/<listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    user_id = get_jwt_identity()
    
    # get listing
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    
    # check permission
    if listing.author_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        property_id = listing.property_id
        
        # delete listing
        db.session.delete(listing)
        
        # get property
        property = Property.query.get(property_id)
        if property:
            address_id = property.address_id

            # TODO: check if the property has any listings, if yes, delete all the listings related to the property
            
            # delete property
            db.session.delete(property)
            
            # get address
            address = Address.query.get(address_id)
            if address:
                # delete address
                db.session.delete(address)
        
        db.session.commit()
        
        return jsonify({"message": "Listing deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@listing_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400
    
    # verify file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        # create unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # save file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # return accessible URL
        image_url = f"/uploads/{unique_filename}"
        
        return jsonify({
            "message": "Image uploaded successfully",
            "image_url": image_url
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500 