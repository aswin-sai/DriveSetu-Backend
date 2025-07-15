from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Instructor
from sqlalchemy.exc import IntegrityError

instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/', methods=['GET'])
def list_instructors():
    instructors = Instructor.query.all()
    return jsonify([
        {
            'id': i.id,
            'name': i.name,
            'email': i.email,
            'phone': i.phone,
            'created_at': i.created_at.isoformat() if i.created_at else None
        } for i in instructors
    ])

@instructors_bp.route('/<instructor_id>', methods=['GET'])
def get_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404
    return jsonify({
        'id': instructor.id,
        'name': instructor.name,
        'email': instructor.email,
        'phone': instructor.phone,
        'created_at': instructor.created_at.isoformat() if instructor.created_at else None
    })

@instructors_bp.route('/', methods=['POST'])
def create_instructor():
    data = request.get_json()
    try:
        instructor = Instructor(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            phone=data.get('phone')
        )
        db.session.add(instructor)
        db.session.commit()
        return jsonify({'id': instructor.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email or ID already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@instructors_bp.route('/<instructor_id>', methods=['PUT'])
def update_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404
    data = request.get_json()
    instructor.name = data.get('name', instructor.name)
    instructor.email = data.get('email', instructor.email)
    instructor.phone = data.get('phone', instructor.phone)
    try:
        db.session.commit()
        return jsonify({'message': 'Instructor updated'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email or ID already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@instructors_bp.route('/<instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted'}) 