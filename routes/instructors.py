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
            'phone': i.phone,
            'email': i.email,
            'experience': i.experience,
            'specialty': i.specialty
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
        'phone': instructor.phone,
        'email': instructor.email,
        'experience': instructor.experience,
        'specialty': instructor.specialty
    })

@instructors_bp.route('/', methods=['POST'])
def create_instructor():
    data = request.get_json()
    try:
        instructor = Instructor(
            id=data['id'],
            name=data['name'],
            phone=data.get('phone'),
            email=data.get('email'),
            experience=data.get('experience'),
            specialty=data.get('specialty')
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
    instructor.phone = data.get('phone', instructor.phone)
    instructor.email = data.get('email', instructor.email)
    instructor.experience = data.get('experience', instructor.experience)
    instructor.specialty = data.get('specialty', instructor.specialty)
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