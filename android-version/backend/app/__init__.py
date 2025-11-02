from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.models import db
from config import config
import os

def create_app(config_name=None):
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.admin import admin_bp
    from app.routes.stats import stats_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(stats_bp)
    
    # Health check endpoint
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'healthy', 'message': 'CrackSmith API is running'}), 200
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'CrackSmith API',
            'version': '1.0.0',
            'description': 'Hash cracking service with React frontend and Flask backend'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app
