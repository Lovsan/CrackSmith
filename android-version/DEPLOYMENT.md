# CrackSmith Android Version - Deployment Guide

## Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Lovsan/CrackSmith.git
cd CrackSmith/android-version
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run the backend
python run.py
```

Backend will run at `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# Run the frontend
npm run dev
```

Frontend will run at `http://localhost:3000`

### 4. Access the Application

Open your browser and navigate to `http://localhost:3000`

1. Register a new account
2. Login with your credentials
3. Start cracking hashes!

## Production Deployment

### Backend Deployment (Flask)

#### Option 1: Gunicorn (Recommended)

```bash
# Install gunicorn (already in requirements.txt)
cd backend
source venv/bin/activate

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

#### Option 2: Docker

Create `Dockerfile` in backend directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

Build and run:

```bash
docker build -t cracksmith-backend .
docker run -p 5000:5000 -e DATABASE_URL=sqlite:///data/cracksmith.db cracksmith-backend
```

### Frontend Deployment

#### Option 1: Build and Serve Statically

```bash
cd frontend

# Build for production
npm run build

# Serve with any static file server
# Example with serve:
npx serve -s build -l 3000
```

#### Option 2: Deploy to Vercel/Netlify

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel
```

#### Option 3: Docker

Create `Dockerfile` in frontend directory:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:

```bash
docker build -t cracksmith-frontend .
docker run -p 80:80 cracksmith-frontend
```

## Environment Variables

### Backend (.env)

Required:
- `SECRET_KEY` - Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `JWT_SECRET_KEY` - JWT secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

Optional:
- `DATABASE_URL` - Database connection string (default: sqlite:///cracksmith.db)
- `ADMIN_PIN` - PIN for granting admin access (default: 1234)
- `MAX_FREE_THREADS` - Max threads for free users (default: 2)
- `MAX_PAID_THREADS` - Max threads for paid users (default: 8)
- `FREE_RATE_LIMIT` - Rate limit for free users (default: 10)
- `PAID_RATE_LIMIT` - Rate limit for paid users (default: 100)

### Frontend (.env)

Required:
- `VITE_API_URL` - Backend API URL (e.g., http://localhost:5000/api or https://api.yourserver.com/api)

## Database Setup

The application uses SQLite by default. For production, consider using PostgreSQL:

1. Install PostgreSQL
2. Create database: `createdb cracksmith`
3. Update DATABASE_URL in .env: `postgresql://user:password@localhost/cracksmith`
4. Install psycopg2: `pip install psycopg2-binary`

## Setting up First Admin User

1. Register a normal user through the app
2. Use Python to grant admin access:

```bash
cd backend
source venv/bin/activate
python

>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='your_username').first()
...     user.is_admin = True
...     db.session.commit()
```

Or use the API with admin PIN:
```bash
curl -X POST http://localhost:5000/api/admin/users/1/admin \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"admin_pin": "1234"}'
```

## Reverse Proxy Setup (Nginx)

Create nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL/HTTPS Setup

Use Let's Encrypt with certbot:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Mobile App Deployment

### Android APK

For building an Android app, consider using:
1. **React Native** - Convert the React app to React Native
2. **Capacitor** - Wrap the web app in a native container
3. **PWA** - Make it a Progressive Web App

Example with Capacitor:

```bash
cd frontend
npm install @capacitor/core @capacitor/cli
npx cap init
npx cap add android
npm run build
npx cap copy
npx cap open android
```

### iOS App

Similar process with Capacitor:

```bash
npx cap add ios
npx cap copy
npx cap open ios
```

## Monitoring and Logging

### Backend Logging

Add to `run.py`:

```python
import logging
logging.basicConfig(
    filename='cracksmith.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

### Production Monitoring

Consider using:
- **Sentry** for error tracking
- **Prometheus** + **Grafana** for metrics
- **ELK Stack** for log aggregation

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx, HAProxy)
- Multiple backend instances
- Shared database (PostgreSQL, MySQL)
- Redis for session storage

### Celery for Background Jobs

Enable Celery for async hash cracking:

```bash
# Install Redis
sudo apt install redis-server

# Start Celery worker
cd backend
celery -A app.celery worker --loglevel=info
```

## Security Checklist

- [ ] Change default SECRET_KEY and JWT_SECRET_KEY
- [ ] Change default ADMIN_PIN
- [ ] Use HTTPS in production
- [ ] Set strong database password
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable firewall
- [ ] Regular backups

## Backup and Restore

### Backup Database

```bash
# SQLite
cp cracksmith.db cracksmith_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump cracksmith > cracksmith_backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# SQLite
cp cracksmith_backup_20231102.db cracksmith.db

# PostgreSQL
psql cracksmith < cracksmith_backup_20231102.sql
```

## Troubleshooting

### Backend won't start

- Check virtual environment is activated
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check .env file exists and has valid values
- Check port 5000 is not in use

### Frontend won't start

- Check Node.js version: `node --version` (should be 16+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check .env file has correct VITE_API_URL
- Check port 3000 is not in use

### CORS errors

- Ensure backend has Flask-CORS installed
- Check VITE_API_URL matches backend URL
- In production, configure CORS origins properly

### Database errors

- Check DATABASE_URL is correct
- Ensure database exists
- Run migrations if using PostgreSQL

## Support

For issues and questions:
- GitHub Issues: https://github.com/Lovsan/CrackSmith/issues
- Documentation: Check README files in backend/ and frontend/ directories
