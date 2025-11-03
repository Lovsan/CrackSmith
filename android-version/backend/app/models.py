from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(255), nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    cracking_jobs = db.relationship('CrackingJob', backref='user', lazy='dynamic')
    statistics = db.relationship('UserStatistics', backref='user', uselist=False)
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify user password"""
        return check_password_hash(self.password_hash, password)
    
    def set_pin(self, pin):
        """Hash and set PIN code"""
        self.pin_code = generate_password_hash(pin)
    
    def check_pin(self, pin):
        """Verify PIN code"""
        if not self.pin_code:
            return False
        return check_password_hash(self.pin_code, pin)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_paid': self.is_paid,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class CrackingJob(db.Model):
    """Model for hash cracking jobs"""
    __tablename__ = 'cracking_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hash_value = db.Column(db.String(255), nullable=False)
    hash_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='queued')  # queued, processing, completed, failed
    priority = db.Column(db.Integer, default=0)  # Higher for paid users
    result = db.Column(db.String(255), nullable=True)
    attempts = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'hash_value': self.hash_value,
            'hash_type': self.hash_type,
            'status': self.status,
            'priority': self.priority,
            'result': self.result,
            'attempts': self.attempts,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserStatistics(db.Model):
    """Model for tracking user statistics"""
    __tablename__ = 'user_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    total_jobs = db.Column(db.Integer, default=0)
    successful_cracks = db.Column(db.Integer, default=0)
    failed_attempts = db.Column(db.Integer, default=0)
    total_hashes_cracked = db.Column(db.Integer, default=0)
    total_attempts = db.Column(db.Integer, default=0)
    last_job_date = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """Convert statistics to dictionary"""
        return {
            'total_jobs': self.total_jobs,
            'successful_cracks': self.successful_cracks,
            'failed_attempts': self.failed_attempts,
            'total_hashes_cracked': self.total_hashes_cracked,
            'total_attempts': self.total_attempts,
            'last_job_date': self.last_job_date.isoformat() if self.last_job_date else None
        }


class Installation(db.Model):
    """Model for tracking app installations"""
    __tablename__ = 'installations'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    platform = db.Column(db.String(50), nullable=True)
    version = db.Column(db.String(50), nullable=True)
    installed_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert installation to dictionary"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'user_id': self.user_id,
            'platform': self.platform,
            'version': self.version,
            'installed_at': self.installed_at.isoformat() if self.installed_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }


class AppSettings(db.Model):
    """Model for global app settings"""
    __tablename__ = 'app_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert setting to dictionary"""
        return {
            'key': self.key,
            'value': self.value,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
