from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Student, User
from sqlalchemy.exc import IntegrityError

students_bp = Blueprint('students', __name__)

VALID_LEVELS = {'Beginner', 'Intermediate', 'Advanced', 'Test Ready'}

@students_bp.route('/', methods=['POST'])
def create_student():
    data = request.get_json()
    user_id = data.get('id')
    user = User.query.get(user_id)
    if not user or user.role != 'student':
        return jsonify({'error': 'User must exist and be a student'}), 400
    if data.get('level') not in VALID_LEVELS:
        return jsonify({'error': 'Invalid level'}), 400
    try:
        student = Student(
            id=user_id,
            phone=data.get('phone'),
            join_date=data.get('join_date'),
            level=data.get('level'),
            total_sessions=data.get('total_sessions', 0),
            total_distance=data.get('total_distance', 0),
            license_category=data.get('license_category'),
            address=data.get('address')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({'id': student.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Student already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@students_bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([
        {
            'id': s.id,
            'name': (User.query.get(s.id).name if User.query.get(s.id) else ''),
            'email': (User.query.get(s.id).email if User.query.get(s.id) else ''),
            'phone': s.phone,
            'join_date': s.join_date.isoformat() if s.join_date else None,
            'level': s.level,
            'total_sessions': s.total_sessions,
            'total_distance': s.total_distance,
            'license_category': s.license_category,
            'address': s.address
        } for s in students
    ])

@students_bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
    print('Fetching student with id:', student_id)
    student = Student.query.get(student_id)
    print('Student found:', student)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({
        'id': student.id,
        'phone': student.phone,
        'join_date': student.join_date.isoformat() if student.join_date else None,
        'level': student.level,
        'total_sessions': student.total_sessions,
        'total_distance': student.total_distance,
        'license_category': student.license_category,
        'address': student.address
    })

@students_bp.route('/<student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.get_json()
    if 'level' in data and data['level'] not in VALID_LEVELS:
        return jsonify({'error': 'Invalid level'}), 400
    student.phone = data.get('phone', student.phone)
    student.join_date = data.get('join_date', student.join_date)
    student.level = data.get('level', student.level)
    student.total_sessions = data.get('total_sessions', student.total_sessions)
    student.total_distance = data.get('total_distance', student.total_distance)
    student.license_category = data.get('license_category', student.license_category)
    student.address = data.get('address', student.address)
    try:
        db.session.commit()
        return jsonify({'message': 'Student updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@students_bp.route('/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'}) 