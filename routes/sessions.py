from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Session, Student
from sqlalchemy.exc import IntegrityError
from datetime import datetime

sessions_bp = Blueprint('sessions', __name__)

VALID_SESSION_TYPES = {
    'Theory Class',
    'Practical - City Roads',
    'Highway Practice',
    'Parking Practice',
    'Test Preparation'
}

@sessions_bp.route('/', methods=['POST'])
def create_session():
    data = request.get_json()
    if 'session_type' not in data or data['session_type'] not in VALID_SESSION_TYPES:
        return jsonify({'error': 'Invalid or missing session_type'}), 400
    try:
        session = Session(
            id=data['id'],
            student_id=data['student_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M').time() if data.get('start_time') else None,
            end_time=datetime.strptime(data['end_time'], '%H:%M').time() if data.get('end_time') else None,
            distance=data.get('distance'),
            instructor=data.get('instructor'),
            session_type=data['session_type'],
            notes=data.get('notes'),
            location=data.get('location')
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({'id': session.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Session already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@sessions_bp.route('/', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    return jsonify([
        {
            'id': s.id,
            'student_id': s.student_id,
            'date': s.date.isoformat(),
            'start_time': s.start_time.strftime('%H:%M') if s.start_time else None,
            'end_time': s.end_time.strftime('%H:%M') if s.end_time else None,
            'distance': s.distance,
            'instructor': s.instructor,
            'session_type': s.session_type,
            'notes': s.notes,
            'location': s.location
        } for s in sessions
    ])

@sessions_bp.route('/<session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify({
        'id': session.id,
        'student_id': session.student_id,
        'date': session.date.isoformat(),
        'start_time': session.start_time.strftime('%H:%M') if session.start_time else None,
        'end_time': session.end_time.strftime('%H:%M') if session.end_time else None,
        'distance': session.distance,
        'instructor': session.instructor,
        'session_type': session.session_type,
        'notes': session.notes,
        'location': session.location
    })

@sessions_bp.route('/<session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    data = request.get_json()
    if 'session_type' in data and data['session_type'] not in VALID_SESSION_TYPES:
        return jsonify({'error': 'Invalid session_type'}), 400
    if 'date' in data:
        session.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'start_time' in data:
        session.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
    if 'end_time' in data:
        session.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    session.distance = data.get('distance', session.distance)
    session.instructor = data.get('instructor', session.instructor)
    if 'session_type' in data:
        session.session_type = data['session_type']
    session.notes = data.get('notes', session.notes)
    session.location = data.get('location', session.location)
    try:
        db.session.commit()
        return jsonify({'message': 'Session updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@sessions_bp.route('/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'})

# Extra: Get all sessions for a student
@sessions_bp.route('/student/<student_id>', methods=['GET'])
def get_sessions_for_student(student_id):
    sessions = Session.query.filter_by(student_id=student_id).all()
    return jsonify([
        {
            'id': s.id,
            'student_id': s.student_id,
            'date': s.date.isoformat(),
            'start_time': s.start_time.strftime('%H:%M') if s.start_time else None,
            'end_time': s.end_time.strftime('%H:%M') if s.end_time else None,
            'distance': s.distance,
            'instructor': s.instructor,
            'session_type': s.session_type,
            'notes': s.notes,
            'location': s.location
        } for s in sessions
    ]) 