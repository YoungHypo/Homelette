from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.services.user_service import create_user, validate_user
from app import db
import email_validator

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # verify required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # check if email already exists
    # SELECT * FROM users WHERE email = 'user@example.com' LIMIT 1;
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409
    
    # create user
    try:
        user = create_user(data)
        return jsonify({
            "message": "User registered successfully",
            "user_id": user.user_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400
    
    # validate user
    user = validate_user(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # create access token
    access_token = create_access_token(identity=user.user_id)
    
    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    }), 200 