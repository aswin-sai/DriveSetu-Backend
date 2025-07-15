from datetime import datetime
from .db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    student = db.relationship('Student', back_populates='user', uselist=False, cascade='all, delete')

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(50), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    phone = db.Column(db.String(20))
    join_date = db.Column(db.Date, default=datetime.utcnow)
    level = db.Column(db.String(20), nullable=False)
    total_sessions = db.Column(db.Integer, default=0)
    total_distance = db.Column(db.Integer, default=0)
    license_category = db.Column(db.String(50))
    address = db.Column(db.String(200))
    user = db.relationship('User', back_populates='student')
    sessions = db.relationship('Session', back_populates='student', cascade='all, delete-orphan')

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    distance = db.Column(db.Integer)
    instructor_id = db.Column(db.String(50), db.ForeignKey('instructors.id', ondelete='SET NULL'))
    session_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    location = db.Column(db.String(100))
    student = db.relationship('Student', back_populates='sessions')
    instructor = db.relationship('Instructor', back_populates='sessions')

    __table_args__ = (
        db.Index('idx_sessions_student_id', 'student_id'),
        db.Index('idx_sessions_instructor_id', 'instructor_id'),
        db.Index('idx_sessions_date', 'date'),
    )

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    experience = db.Column(db.Integer)  # in years
    specialty = db.Column(db.String(100))
    sessions = db.relationship('Session', back_populates='instructor', cascade='all, delete-orphan')

class ActivityLog(db.Model):
    __tablename__ = 'activity_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id', ondelete='SET NULL'))
    action_type = db.Column(db.String(20), nullable=False)
    target_table = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint(
            action_type.in_(['INSERT', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT']),
            name='check_action_type_valid'
        ),
    ) 