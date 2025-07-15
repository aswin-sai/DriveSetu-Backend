from flask import Blueprint, request, jsonify
from ..db import db
from ..models import ActivityLog

activity_log_bp = Blueprint('activity_log', __name__)

@activity_log_bp.route('/', methods=['GET'])
def list_logs():
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return jsonify([
        {
            'id': log.id,
            'user_id': log.user_id,
            'action_type': log.action_type,
            'target_table': log.target_table,
            'description': log.description,
            'timestamp': log.timestamp.isoformat() if log.timestamp else None
        } for log in logs
    ])

@activity_log_bp.route('/<int:log_id>', methods=['GET'])
def get_log(log_id):
    log = ActivityLog.query.get(log_id)
    if not log:
        return jsonify({'error': 'Log not found'}), 404
    return jsonify({
        'id': log.id,
        'user_id': log.user_id,
        'action_type': log.action_type,
        'target_table': log.target_table,
        'description': log.description,
        'timestamp': log.timestamp.isoformat() if log.timestamp else None
    }) 