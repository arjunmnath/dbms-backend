from flask import request, jsonify
from api.models import db, User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from api.routes import appbp

# Register a user
@appbp.route('/api/register', methods=['POST']) #working fine
def create_user():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        username=data['username']
        email=data['email']
        password = data['password']
        
        # Check if the username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'error': 'Username or email already exists'}), 400
        
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create a new user instance
        new_user = User(
            username=username,
            phone=data['phone'],
            email=email,
            passwdHash=hashed_password,
            firstName=data['firstName'],
            lastName=data['lastName'],
            house_flatNo=data['house_flatNo'],
            street=data['street'],
            city=data['city'],
            pincode=data['pincode'],
            dateJoined=data['dateJoined'],
            isVerified=data['isVerified']
        )
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Return success response
        return jsonify({'message': 'User registered successfully', 'userId': new_user.userId}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error creating product'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Login user
@appbp.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwdHash, password):
            return jsonify({'message': 'Login successful', 'userId': user.userId}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get user details
@appbp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    try:
        # Fetch the user by ID
        user = User.query.get_or_404(user_id)
        
        # Prepare response data
        user_details = {
            'userId': user.userId,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'houseFlatNo': user.houseFlatNo,
            'street': user.street,
            'city': user.city,
            'pincode': user.pincode,
            'dateJoined': user.dateJoined.isoformat(),
            'isVerified': user.isVerified
        }
        
        return jsonify(user_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update user details
@appbp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        
        # Update user details
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.firstName = data.get('firstName', user.firstName)
        user.lastName = data.get('lastName', user.lastName)
        user.house_flatNo = data.get('house_flatNo', user.house_flatNo)
        user.street = data.get('street', user.street)
        user.city = data.get('city', user.city)
        user.pincode = data.get('pincode', user.pincode)
        user.dateJoined = data.get('dateJoined', user.dateJoined)
        user.isVerified = data.get('isVerified', user.isVerified)
        
        db.session.commit()
        
        return jsonify({'message': 'User details updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Delete user
@appbp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
