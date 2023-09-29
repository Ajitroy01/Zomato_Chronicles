from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, db
from app.hashing import hash_password, check_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/customer-signup', methods=['POST'])
def customer_signup():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        customer_name = data['customer_name']
        address = data['address']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists. Please choose another username.', 'success': False}), 400

        # Create a new customer user with hashed password
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password, role='customer', customer_name=customer_name, address=address)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully', 'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/staff-signup', methods=['POST'])
def staff_signup():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists. Please choose another username.', 'success': False}), 400

        # Create a new staff user with hashed password
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password, role='staff')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Staff account created successfully', 'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/customer-login', methods=['POST'])
def customer_login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username, role='customer').first()

        if user and check_password(user.password, password):
            login_user(user)
            return jsonify({'message': 'Logged in successfully', 'success': True}), 200
        else:
            return jsonify({'message': 'Login failed. Please check your credentials.', 'success': False}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/staff-login', methods=['POST'])
def staff_login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username, role='staff').first()

        if user and check_password(user.password, password):
            login_user(user)
            return jsonify({'message': 'Staff logged in successfully', 'success': True}), 200
        else:
            return jsonify({'message': 'Staff login failed. Please check your credentials.', 'success': False}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully', 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
