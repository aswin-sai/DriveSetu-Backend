from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from ..db import db
from ..models import User

users_bp = Blueprint('users', __name__)

VALID_ROLES = {'student', 'admin'}

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if data['role'] not in VALID_ROLES:
        return jsonify({'error': 'Invalid role'}), 400
    try:
        user = User(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            role=data['role'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email or ID already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users
    ])

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role})

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if 'role' in data and data['role'] not in VALID_ROLES:
        return jsonify({'error': 'Invalid role'}), 400
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if 'role' in data:
        user.role = data['role']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    try:
        db.session.commit()
        return jsonify({'message': 'User updated'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email or ID already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    print('Login attempt for:', email)
    print('User found:', user)
    if user:
        print('Password hash in DB:', user.password)
        print('Password check:', check_password_hash(user.password, password))
    if user and check_password_hash(user.password, password):
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401 