from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, CrackingJob, UserStatistics
from datetime import datetime, timedelta
from sqlalchemy import func

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get current user's statistics"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user statistics
        stats = user.statistics
        
        if not stats:
            stats = UserStatistics(user_id=user.id)
            db.session.add(stats)
            db.session.commit()
        
        # Get recent jobs for chart data
        jobs = CrackingJob.query.filter_by(user_id=user.id).order_by(
            CrackingJob.created_at.desc()
        ).limit(10).all()
        
        # Calculate success rate
        total_jobs = stats.total_jobs
        success_rate = (stats.successful_cracks / total_jobs * 100) if total_jobs > 0 else 0
        
        return jsonify({
            'statistics': stats.to_dict(),
            'success_rate': round(success_rate, 2),
            'recent_jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stats_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics with charts data"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get statistics
        stats = user.statistics
        
        if not stats:
            stats = UserStatistics(user_id=user.id)
            db.session.add(stats)
            db.session.commit()
        
        # Get jobs by status
        status_counts = db.session.query(
            CrackingJob.status,
            func.count(CrackingJob.id)
        ).filter_by(user_id=user.id).group_by(CrackingJob.status).all()
        
        status_data = {status: count for status, count in status_counts}
        
        # Get jobs over time (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        daily_jobs = db.session.query(
            func.date(CrackingJob.created_at).label('date'),
            func.count(CrackingJob.id).label('count')
        ).filter(
            CrackingJob.user_id == user.id,
            CrackingJob.created_at >= thirty_days_ago
        ).group_by(func.date(CrackingJob.created_at)).all()
        
        # Format daily jobs data
        jobs_over_time = [
            {
                'date': str(date),
                'count': count
            }
            for date, count in daily_jobs
        ]
        
        # Get hash type distribution
        hash_type_counts = db.session.query(
            CrackingJob.hash_type,
            func.count(CrackingJob.id)
        ).filter_by(user_id=user.id).group_by(CrackingJob.hash_type).all()
        
        hash_type_data = {hash_type: count for hash_type, count in hash_type_counts}
        
        return jsonify({
            'statistics': stats.to_dict(),
            'status_distribution': status_data,
            'jobs_over_time': jobs_over_time,
            'hash_type_distribution': hash_type_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
