# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email the maintainers or create a private security advisory on GitHub.

## Security Considerations

### Production Deployment

When deploying to production, ensure the following security measures are in place:

#### 1. Debug Mode
**CRITICAL**: Never run with `debug=True` in production!

```python
# In run.py, ensure debug is False in production
debug_mode = os.environ.get('FLASK_ENV') == 'development'
app.run(host='0.0.0.0', port=port, debug=debug_mode)
```

Set environment variable:
```bash
export FLASK_ENV=production
```

#### 2. Secret Keys
Always use strong, random secret keys in production:

```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_hex(32))"

# Set in environment
export SECRET_KEY="your-generated-secret-key"
export JWT_SECRET_KEY="your-generated-jwt-secret-key"
```

Never use the default development keys in production!

#### 3. Error Handling
The current implementation exposes stack traces in error responses for development debugging. In production:

**Option A**: Implement custom error handlers in `app/__init__.py`:

```python
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}", exc_info=True)
    return jsonify({'error': 'An internal error occurred'}), 500
```

**Option B**: Use a production WSGI server (gunicorn) that handles errors properly:

```bash
gunicorn -w 4 --error-logfile error.log run:app
```

#### 4. HTTPS/SSL
Always use HTTPS in production:
- Use a reverse proxy (Nginx, Apache) with SSL certificates
- Use Let's Encrypt for free SSL certificates
- Redirect all HTTP traffic to HTTPS

#### 5. CORS Configuration
Update CORS settings for production in `app/__init__.py`:

```python
CORS(app, origins=['https://yourdomain.com'])
```

#### 6. Database
- Use PostgreSQL or MySQL instead of SQLite in production
- Use strong database passwords
- Enable database backups
- Restrict database access to localhost only

#### 7. Rate Limiting
Implement rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

#### 8. Admin Access
- Change the default `ADMIN_PIN` immediately
- Use a strong PIN (8+ characters)
- Limit admin access to specific IP addresses if possible

#### 9. File Permissions
Ensure proper file permissions:

```bash
chmod 600 .env
chmod 755 run.py
```

#### 10. Logging
- Enable comprehensive logging
- Log to files, not just console
- Monitor logs for suspicious activity
- Rotate logs regularly

```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

## Known Security Considerations

### Hash Cracking Algorithms
The application intentionally uses "weak" hashing algorithms (MD5, SHA1, SHA256) for **password cracking purposes**. These are NOT used for storing user passwords (which use bcrypt). This is expected behavior.

### Thread Management
The current implementation uses threading for job processing. For production, consider:
- Using Celery with Redis for proper task queuing
- Implementing job timeouts
- Monitoring resource usage

### PIN Code Security
- PIN codes are hashed using werkzeug's password hashing (bcrypt)
- PINs should be at least 4 characters
- Consider enforcing stronger PIN requirements

## Security Checklist for Production

- [ ] `FLASK_ENV=production` is set
- [ ] `debug=False` in run.py
- [ ] Strong SECRET_KEY and JWT_SECRET_KEY set
- [ ] ADMIN_PIN changed from default
- [ ] HTTPS/SSL enabled
- [ ] CORS configured for specific domains
- [ ] Production database (PostgreSQL/MySQL) configured
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] File permissions set correctly
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] Database backups enabled

## Dependencies

Run regular security audits:

```bash
# Python
pip install safety
safety check

# Check for outdated packages
pip list --outdated
```

## Updates

Keep all dependencies up to date:

```bash
pip install --upgrade -r requirements.txt
npm audit fix  # For frontend
```

## Contact

For security concerns, please contact the repository maintainers.
