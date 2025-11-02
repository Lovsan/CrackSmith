from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models import db, User, UserStatistics, Installation
from app.utils.errors import safe_error_response
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        # Set PIN if provided
        if data.get('pin'):
            user.set_pin(data['pin'])
        
        db.session.add(user)
        db.session.flush()
        
        # Create user statistics
        stats = UserStatistics(user_id=user.id)
        db.session.add(stats)
        
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check PIN if user has one set
        if user.pin_code and data.get('pin'):
            if not user.check_pin(data['pin']):
                return jsonify({'error': 'Invalid PIN code'}), 401
        elif user.pin_code and not data.get('pin'):
            return jsonify({'error': 'PIN code required', 'pin_required': True}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'statistics': user.statistics.to_dict() if user.statistics else {}
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/set-pin', methods=['POST'])
@jwt_required()
def set_pin():
    """Set or update user PIN"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data.get('pin'):
            return jsonify({'error': 'PIN code is required'}), 400
        
        # Verify current PIN if one exists
        if user.pin_code and not data.get('current_pin'):
            return jsonify({'error': 'Current PIN required'}), 400
        
        if user.pin_code and not user.check_pin(data['current_pin']):
            return jsonify({'error': 'Invalid current PIN'}), 401
        
        user.set_pin(data['pin'])
        db.session.commit()
        
        return jsonify({'message': 'PIN code updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/installation', methods=['POST'])
@jwt_required()
def track_installation():
    """Track app installation"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        device_id = data.get('device_id')
        if not device_id:
            return jsonify({'error': 'Device ID is required'}), 400
        
        # Check if installation exists
        installation = Installation.query.filter_by(device_id=device_id).first()
        
        if installation:
            # Update existing installation
            installation.user_id = current_user_id
            installation.last_active = datetime.utcnow()
            if data.get('platform'):
                installation.platform = data['platform']
            if data.get('version'):
                installation.version = data['version']
        else:
            # Create new installation
            installation = Installation(
                device_id=device_id,
                user_id=current_user_id,
                platform=data.get('platform'),
                version=data.get('version')
            )
            db.session.add(installation)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Installation tracked successfully',
            'installation': installation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
