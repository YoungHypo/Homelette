from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, UserInterest
from app.models.listing import Listing
from app import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # protected fields
    protected_fields = ['user_id', 'email', 'password', 'join_date']
    update_fields = {k: v for k, v in data.items() if k not in protected_fields}
    
    try:
        for key, value in update_fields.items():
            setattr(user, key, value)
        
        db.session.commit()
        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/interests', methods=['GET'])
@jwt_required()
def get_user_interests(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # get all interests of the user
        interests = UserInterest.query.filter_by(user_id=user_id).all()
        listing_ids = [interest.listing_id for interest in interests]
        
        # get detailed information of these listings
        listings = Listing.query.filter(Listing.listing_id.in_(listing_ids)).all()
        
        # return listings with property and address information
        result = [listing.to_dict(include_property=True, include_address=True) for listing in listings]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/interests/<listing_id>', methods=['POST'])
@jwt_required()
def add_interest(user_id, listing_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # check if user and listing exist
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    
    # check if the listing is already marked as interested
    existing_interest = UserInterest.query.filter_by(
        user_id=user_id, listing_id=listing_id).first()
    if existing_interest:
        return jsonify({"message": "Listing already marked as interested"}), 200
    
    try:
        # create new interest record
        interest = UserInterest(user_id=user_id, listing_id=listing_id)
        db.session.add(interest)
        db.session.commit()
        
        return jsonify({"message": "Interest added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>/interests/<listing_id>', methods=['DELETE'])
@jwt_required()
def remove_interest(user_id, listing_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # find interest record
    interest = UserInterest.query.filter_by(
        user_id=user_id, listing_id=listing_id).first()
    
    if not interest:
        return jsonify({"error": "Interest not found"}), 404
    
    try:
        # delete interest record
        db.session.delete(interest)
        db.session.commit()
        
        return jsonify({"message": "Interest removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500 