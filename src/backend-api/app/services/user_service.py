from app.models.user import User
from app import db

def create_user(data):
    user = User(
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        major=data.get('major'),
        graduation_year=data.get('graduation_year'),
        about_me=data.get('about_me'),
        profile_picture_url=data.get('profile_picture_url')
    )
    
    db.session.add(user)
    db.session.commit()
    return user

def validate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user_profile(user_id, update_data):
    user = User.query.get(user_id)
    if not user:
        return None
    
    allowed_fields = ['first_name', 'last_name', 'major', 'graduation_year', 
                      'about_me', 'profile_picture_url']
    
    # apply update
    for field in allowed_fields:
        if field in update_data:
            setattr(user, field, update_data[field])
    
    db.session.commit()
    return user 