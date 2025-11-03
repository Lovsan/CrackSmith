# CrackSmith Android Version - Testing Guide

## Manual Testing Checklist

### Backend API Testing

#### 1. Health Check
```bash
curl http://localhost:5000/api/health
```
Expected: `{"status": "healthy", "message": "CrackSmith API is running"}`

#### 2. User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "pin": "1234"
  }'
```
Expected: User created with access_token and refresh_token

#### 3. User Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123",
    "pin": "1234"
  }'
```
Expected: Login successful with tokens

#### 4. Get Current User
```bash
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Expected: User profile and statistics

#### 5. Submit Cracking Job
```bash
# MD5 hash of "password"
curl -X POST http://localhost:5000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hash_value": "5f4dcc3b5aa765d61d8327deb882cf99",
    "hash_type": "md5"
  }'
```
Expected: Job created and queued

#### 6. Get User Jobs
```bash
curl http://localhost:5000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Expected: List of user's jobs

#### 7. Get User Statistics
```bash
curl http://localhost:5000/api/stats/user \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Expected: User statistics

### Frontend Testing

#### 1. Registration Flow
1. Navigate to http://localhost:3000
2. Click "Register here"
3. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
   - PIN: 1234 (optional)
4. Click "Register"
5. Should redirect to Dashboard

#### 2. Login Flow
1. Navigate to http://localhost:3000/login
2. Enter username: testuser
3. Enter password: password123
4. If PIN set, enter PIN: 1234
5. Click "Login"
6. Should redirect to Dashboard

#### 3. Dashboard - Job Submission
1. On Dashboard
2. Enter hash value: `5f4dcc3b5aa765d61d8327deb882cf99`
3. Select hash type: MD5 (or Auto-detect)
4. Click "Submit"
5. Should show success message
6. Check Recent Jobs section for new job

#### 4. Jobs Page
1. Click "Jobs" in sidebar
2. Should see list of submitted jobs
3. Check job status (queued, processing, completed, failed)
4. For completed jobs, verify password is shown
5. Try deleting a queued/failed job

#### 5. Statistics Page
1. Click "Statistics" in sidebar
2. Verify charts are displayed:
   - Job Status Distribution (pie chart)
   - Hash Type Distribution (pie chart)
   - Jobs Over Time (line chart)

#### 6. Settings Page
1. Click "Settings" in sidebar
2. Verify account information is correct
3. Try updating PIN code:
   - Enter current PIN (if set)
   - Enter new PIN
   - Confirm new PIN
   - Click "Update PIN"
4. Verify success message

#### 7. About Page
1. Click "About" in sidebar
2. Verify all sections display correctly:
   - Welcome message
   - Feature cards
   - Supported hash types
   - Why Choose Us section

#### 8. Admin Panel (Admin Only)
1. First, make user an admin (see DEPLOYMENT.md)
2. Click "Admin" in sidebar
3. Verify statistics cards show correct data
4. Switch between tabs:
   - Users
   - Installations
   - Jobs
5. Verify data displays correctly

### Mobile Responsiveness Testing

Test on different screen sizes:

#### Desktop (1920x1080)
- Sidebar should be permanently visible
- All components should use full width
- Charts should be large and readable

#### Tablet (768x1024)
- Sidebar should be permanently visible
- Layout should adjust to smaller width
- Charts should remain readable

#### Mobile (375x667)
- Sidebar should be hidden by default
- Menu icon should appear in header
- Clicking menu opens drawer
- All forms should be single column
- Charts should be scrollable if needed

### Hash Cracking Testing

Test different hash types:

#### MD5
```bash
# Hash of "password"
5f4dcc3b5aa765d61d8327deb882cf99

# Hash of "123456"
e10adc3949ba59abbe56e057f20f883e

# Hash of "admin"
21232f297a57a5a743894a0e4a801fc3
```

#### SHA1
```bash
# Hash of "password"
5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8

# Hash of "123456"
7c4a8d09ca3762af61e59520943dc26494f8941b
```

#### SHA256
```bash
# Hash of "password"
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

# Hash of "123456"
8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

#### Bcrypt
Generate with Python:
```python
import bcrypt
password = b"password123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())
```

### Security Testing

#### 1. PIN Protection
1. Set a PIN in Settings
2. Logout
3. Try to login without PIN
4. Should require PIN

#### 2. JWT Token Expiry
1. Login and copy access token
2. Wait for token to expire (24 hours by default, or modify JWT_ACCESS_TOKEN_EXPIRES for testing)
3. Try to access protected endpoint
4. Should auto-refresh or redirect to login

#### 3. Authorization
1. Try to access admin endpoint as non-admin user
2. Should receive 403 Forbidden

#### 4. Rate Limiting
1. Submit many jobs quickly as free user
2. Should respect rate limits

### Performance Testing

#### 1. Multiple Jobs
Submit 10+ jobs and verify:
- Jobs are queued properly
- Processing happens in background
- UI remains responsive
- Jobs complete successfully

#### 2. Large Dataset
- Submit multiple jobs simultaneously
- Check server resource usage
- Verify queue processes jobs in order (priority for paid users)

### Error Handling Testing

#### 1. Invalid Hash
Submit invalid hash value:
- Should show appropriate error
- Should not crash app

#### 2. Network Error
1. Stop backend server
2. Try to submit job from frontend
3. Should show connection error
4. Restart backend
5. Should reconnect automatically

#### 3. Invalid Credentials
Try to login with:
- Wrong username
- Wrong password
- Wrong PIN
Should show appropriate error messages

### Browser Compatibility

Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

### Accessibility Testing

- [ ] Can navigate with keyboard only
- [ ] Screen reader compatible
- [ ] Proper ARIA labels
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible

## Automated Testing

### Backend Unit Tests

Create `tests/test_api.py`:

```python
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'access_token' in response.data

def test_login(client):
    # First register
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Then login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'access_token' in response.data
```

Run tests:
```bash
cd backend
pip install pytest
pytest tests/
```

### Frontend Testing

Create `src/tests/App.test.jsx`:

```javascript
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders login page', () => {
  render(<App />);
  const loginElement = screen.getByText(/login/i);
  expect(loginElement).toBeInTheDocument();
});
```

Run tests:
```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom
npm test
```

## Load Testing

Use Apache Bench or similar:

```bash
# Test 100 requests with 10 concurrent
ab -n 100 -c 10 http://localhost:5000/api/health

# Test with authentication
ab -n 100 -c 10 -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/jobs/
```

## Continuous Integration

Example GitHub Actions workflow (`.github/workflows/test.yml`):

```yaml
name: Test

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: |
          cd android-version/backend
          pip install -r requirements.txt
          pytest

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: |
          cd android-version/frontend
          npm install
          npm test
```

## Test Coverage

Generate coverage reports:

### Backend
```bash
cd backend
pip install pytest-cov
pytest --cov=app tests/
```

### Frontend
```bash
cd frontend
npm test -- --coverage
```

## Reporting Issues

When reporting bugs, include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Screenshots (if UI issue)
5. Browser/OS information
6. Error messages from console
