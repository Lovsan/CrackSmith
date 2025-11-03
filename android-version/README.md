# CrackSmith Android Version

Full-stack hash cracking application with React frontend and Flask backend, designed for mobile-friendly use with both local and server-based execution.

## Overview

This is the Android/mobile version of CrackSmith, featuring:

- **React Frontend**: Beautiful, mobile-friendly UI with Material-UI
- **Flask Backend**: RESTful API with user authentication and job queue system
- **User Authentication**: JWT-based auth with optional PIN code security
- **Statistics Dashboard**: Track cracking success with charts and metrics
- **Admin Panel**: Comprehensive platform management
- **Dual Deployment**: Run locally for free or on fast servers for paid users
- **Queue System**: Priority processing for premium users

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the server:
```bash
python run.py
```

Backend will run at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run at `http://localhost:3000`

## Features

### User Features

- **Authentication System**
  - User registration and login
  - JWT token-based authentication
  - Optional PIN code protection
  - Secure password hashing

- **Hash Cracking**
  - Support for MD5, SHA1, SHA256, and Bcrypt
  - Auto-detection of hash types
  - Job queue with status tracking
  - Results display with attempt counts

- **Statistics Dashboard**
  - Total jobs and success rate
  - Job status distribution (pie chart)
  - Hash type distribution (pie chart)
  - Jobs over time (line chart)
  - Recent job history

- **Settings**
  - PIN code management
  - Account information
  - App preferences
  - Security settings

### Admin Features

- **Platform Statistics**
  - Total users (free vs paid)
  - Total jobs and completion rates
  - Installation tracking
  - Weekly activity metrics

- **User Management**
  - View all users
  - Upgrade users to paid
  - Grant admin access
  - User activity monitoring

- **Installation Tracking**
  - Device ID tracking
  - Platform and version info
  - Last active timestamps

- **Job Monitoring**
  - View all jobs across platform
  - Filter by status
  - Job statistics

### Security Features

- **PIN Code Protection**: Optional PIN for account access
- **Anti-Abuse Checks**: Rate limiting and resource checks
- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: Bcrypt for password storage
- **Installation Tracking**: Monitor app installations

### Deployment Options

#### Free (Local)
- Run on user's device
- Limited to 2 threads
- 10 jobs per day rate limit
- Basic wordlist

#### Premium (Server)
- Run on fast servers
- Up to 8 threads
- 100 jobs per day rate limit
- Priority queue access
- Expanded wordlists

## Architecture

```
android-version/
├── backend/              # Flask API
│   ├── app/
│   │   ├── models.py     # Database models
│   │   ├── routes/       # API routes
│   │   │   ├── auth.py
│   │   │   ├── jobs.py
│   │   │   ├── admin.py
│   │   │   └── stats.py
│   │   └── services/     # Business logic
│   │       └── cracker.py
│   ├── config.py         # Configuration
│   ├── run.py            # Entry point
│   └── requirements.txt
│
└── frontend/             # React app
    ├── src/
    │   ├── components/   # Reusable components
    │   ├── context/      # React context
    │   ├── pages/        # Page components
    │   ├── services/     # API services
    │   └── App.jsx
    ├── package.json
    └── vite.config.js
```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/set-pin` - Set/update PIN

### Job Endpoints
- `POST /api/jobs/` - Submit new job
- `GET /api/jobs/` - Get user's jobs
- `GET /api/jobs/<id>` - Get specific job
- `DELETE /api/jobs/<id>` - Delete job

### Statistics Endpoints
- `GET /api/stats/user` - User statistics
- `GET /api/stats/dashboard` - Dashboard data

### Admin Endpoints (Admin only)
- `GET /api/admin/stats` - Platform statistics
- `GET /api/admin/users` - All users
- `POST /api/admin/users/<id>/upgrade` - Upgrade user
- `GET /api/admin/installations` - All installations

## Technologies

### Backend
- Flask 3.0
- Flask-JWT-Extended (authentication)
- Flask-SQLAlchemy (ORM)
- Bcrypt (password hashing)
- SQLite (database)

### Frontend
- React 18
- Material-UI 5
- React Router 6
- Recharts (charts)
- Axios (HTTP client)
- Vite (build tool)

## Mobile Optimization

The frontend is fully optimized for mobile:
- Responsive layouts
- Touch-friendly interface
- Mobile-first design
- Fast performance
- PWA-ready

## Development

### Backend Development
```bash
cd backend
export FLASK_ENV=development
python run.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Production Build

Backend:
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Frontend:
```bash
cd frontend
npm run build
```

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///cracksmith.db
ADMIN_PIN=1234
MAX_FREE_THREADS=2
MAX_PAID_THREADS=8
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file

## Support

For issues and questions:
- GitHub Issues: https://github.com/Lovsan/CrackSmith/issues
- Email: [Your contact email]

## Legal Notice

This tool is for authorized security testing and password recovery only. Users must have explicit permission to crack any hashes they submit. Misuse is prohibited.
