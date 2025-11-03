#!/usr/bin/env python3
"""
CrackSmith Backend Application
Flask API server for hash cracking service
"""
import os
from app import create_app, db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create app
app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # IMPORTANT: Set DEBUG=False in production!
    # Debug mode allows arbitrary code execution and should never be enabled in production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
