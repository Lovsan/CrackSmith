# CrackSmith Backend

Flask-based REST API for the CrackSmith hash cracking service.

## Features

- User authentication with JWT tokens
- PIN code security
- Hash cracking for MD5, SHA1, SHA256, and Bcrypt
- Job queue system with priority for paid users
- Statistics tracking
- Admin panel
- Installation tracking
- Anti-abuse measures

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/set-pin` - Set/update PIN code
- `POST /api/auth/installation` - Track installation

### Jobs
- `POST /api/jobs/` - Submit new cracking job
- `GET /api/jobs/` - Get user's jobs
- `GET /api/jobs/<id>` - Get specific job
- `DELETE /api/jobs/<id>` - Delete job

### Statistics
- `GET /api/stats/user` - Get user statistics
- `GET /api/stats/dashboard` - Get dashboard statistics

### Admin (Admin only)
- `GET /api/admin/stats` - Get platform statistics
- `GET /api/admin/users` - Get all users
- `POST /api/admin/users/<id>/upgrade` - Upgrade user to paid
- `POST /api/admin/users/<id>/admin` - Grant admin access
- `GET /api/admin/installations` - Get all installations
- `GET /api/admin/jobs` - Get all jobs
- `GET /api/admin/settings` - Get app settings
- `POST /api/admin/settings` - Update app settings

## Configuration

Key environment variables in `.env`:

- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string
- `ADMIN_PIN` - Admin PIN for granting admin access
- `MAX_FREE_THREADS` - Max threads for free users (default: 2)
- `MAX_PAID_THREADS` - Max threads for paid users (default: 8)

## Development

Run in development mode:
```bash
export FLASK_ENV=development
python run.py
```

## Production

Use gunicorn for production:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Database Migrations

Initialize migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## License

MIT License - See LICENSE file
