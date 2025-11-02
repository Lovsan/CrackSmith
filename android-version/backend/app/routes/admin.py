from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, CrackingJob, UserStatistics, Installation, AppSettings
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    
    return decorated_function


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_admin_stats():
    """Get overall platform statistics"""
    try:
        # User statistics
        total_users = User.query.count()
        paid_users = User.query.filter_by(is_paid=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        # Job statistics
        total_jobs = CrackingJob.query.count()
        completed_jobs = CrackingJob.query.filter_by(status='completed').count()
        failed_jobs = CrackingJob.query.filter_by(status='failed').count()
        queued_jobs = CrackingJob.query.filter_by(status='queued').count()
        processing_jobs = CrackingJob.query.filter_by(status='processing').count()
        
        # Installation statistics
        total_installations = Installation.query.count()
        active_installations = Installation.query.filter(
            Installation.last_active >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_users_week = User.query.filter(User.created_at >= week_ago).count()
        jobs_week = CrackingJob.query.filter(CrackingJob.created_at >= week_ago).count()
        
        return jsonify({
            'users': {
                'total': total_users,
                'paid': paid_users,
                'admin': admin_users,
                'new_this_week': new_users_week
            },
            'jobs': {
                'total': total_jobs,
                'completed': completed_jobs,
                'failed': failed_jobs,
                'queued': queued_jobs,
                'processing': processing_jobs,
                'this_week': jobs_week
            },
            'installations': {
                'total': total_installations,
                'active': active_installations
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/upgrade', methods=['POST'])
@admin_required
def upgrade_user(user_id):
    """Upgrade user to paid"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_paid = True
        db.session.commit()
        
        return jsonify({
            'message': 'User upgraded to paid',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/admin', methods=['POST'])
@admin_required
def make_admin(user_id):
    """Make user an admin"""
    try:
        # Verify admin PIN
        data = request.get_json()
        admin_pin = data.get('admin_pin')
        
        if admin_pin != current_app.config['ADMIN_PIN']:
            return jsonify({'error': 'Invalid admin PIN'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_admin = True
        db.session.commit()
        
        return jsonify({
            'message': 'User granted admin access',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/installations', methods=['GET'])
@admin_required
def get_installations():
    """Get all installations"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Installation.query.order_by(Installation.installed_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'installations': [inst.to_dict() for inst in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/jobs', methods=['GET'])
@admin_required
def get_all_jobs():
    """Get all jobs"""
    try:
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = CrackingJob.query
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(CrackingJob.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'jobs': [job.to_dict() for job in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/settings', methods=['GET'])
@admin_required
def get_settings():
    """Get all app settings"""
    try:
        settings = AppSettings.query.all()
        
        return jsonify({
            'settings': {s.key: s.value for s in settings}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/settings', methods=['POST'])
@admin_required
def update_settings():
    """Update app settings"""
    try:
        data = request.get_json()
        
        for key, value in data.items():
            setting = AppSettings.query.filter_by(key=key).first()
            
            if setting:
                setting.value = str(value)
                setting.updated_at = datetime.utcnow()
            else:
                setting = AppSettings(key=key, value=str(value))
                db.session.add(setting)
        
        db.session.commit()
        
        return jsonify({'message': 'Settings updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
