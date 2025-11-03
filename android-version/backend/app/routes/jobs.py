from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, CrackingJob, UserStatistics
from datetime import datetime
from app.services.cracker import submit_cracking_job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    """Submit a new cracking job"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('hash_value'):
            return jsonify({'error': 'Hash value is required'}), 400
        
        # Detect hash type
        hash_value = data['hash_value']
        hash_type = data.get('hash_type', detect_hash_type(hash_value))
        
        # Set priority based on user type
        priority = 10 if user.is_paid else 0
        
        # Create job
        job = CrackingJob(
            user_id=user.id,
            hash_value=hash_value,
            hash_type=hash_type,
            priority=priority,
            status='queued'
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Submit job to queue
        submit_cracking_job(job.id)
        
        # Update user statistics
        if user.statistics:
            user.statistics.total_jobs += 1
            user.statistics.last_job_date = datetime.utcnow()
            db.session.commit()
        
        return jsonify({
            'message': 'Job submitted successfully',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get user's cracking jobs"""
    try:
        current_user_id = get_jwt_identity()
        
        # Query parameters
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = CrackingJob.query.filter_by(user_id=current_user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by creation date (newest first)
        query = query.order_by(CrackingJob.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'jobs': [job.to_dict() for job in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get specific job details"""
    try:
        current_user_id = get_jwt_identity()
        
        job = CrackingJob.query.filter_by(
            id=job_id,
            user_id=current_user_id
        ).first()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete a job"""
    try:
        current_user_id = get_jwt_identity()
        
        job = CrackingJob.query.filter_by(
            id=job_id,
            user_id=current_user_id
        ).first()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Only allow deletion of queued or failed jobs
        if job.status not in ['queued', 'failed']:
            return jsonify({'error': 'Cannot delete job in current status'}), 400
        
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def detect_hash_type(hash_value):
    """Detect hash type from hash value"""
    if hash_value.startswith("$2y$") or hash_value.startswith("$2b$"):
        return "bcrypt"
    elif len(hash_value) == 32:
        return "md5"
    elif len(hash_value) == 40:
        return "sha1"
    elif len(hash_value) == 64:
        return "sha256"
    else:
        return "unknown"
