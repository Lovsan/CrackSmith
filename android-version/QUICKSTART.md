# CrackSmith Android Version - Quick Start Guide

Welcome to CrackSmith! This guide will help you get started in 5 minutes.

## What is CrackSmith?

CrackSmith is a modern hash cracking service with a beautiful mobile-friendly interface. It supports MD5, SHA1, SHA256, and Bcrypt hashes, with features like:

- 🔐 Secure user authentication with optional PIN
- 📊 Statistics dashboard with charts
- 👥 Admin panel for platform management
- 🚀 Queue system with priority for premium users
- 💻 Run locally (free) or on fast servers (premium)

## Quick Setup (5 minutes)

### Step 1: Install Prerequisites

Make sure you have:
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Node.js 16+ ([Download](https://nodejs.org/))

### Step 2: Clone and Setup Backend

```bash
# Clone repository
git clone https://github.com/Lovsan/CrackSmith.git
cd CrackSmith/android-version/backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Start backend
python run.py
```

✅ Backend running at http://localhost:5000

### Step 3: Setup Frontend (New Terminal)

```bash
cd CrackSmith/android-version/frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

✅ Frontend running at http://localhost:3000

### Step 4: Use the App

1. Open http://localhost:3000 in your browser
2. Click **"Register here"**
3. Create your account
4. Start cracking hashes!

## Your First Hash Crack

Try these example hashes:

### MD5 Hash (password = "password")
```
5f4dcc3b5aa765d61d8327deb882cf99
```

### SHA256 Hash (password = "123456")
```
8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

### How to Submit a Job

1. Go to **Dashboard**
2. Paste the hash in the "Hash Value" field
3. Select hash type (or use Auto-detect)
4. Click **Submit**
5. View results in the **Jobs** page

## Features Overview

### 🏠 Dashboard
- Submit new hashing jobs
- View quick statistics
- See recent jobs

### 💼 Jobs
- View all your jobs
- Check cracking status
- Delete failed jobs
- See cracked passwords

### 📊 Statistics
- Job status distribution
- Hash type breakdown
- Activity over time
- Success rate metrics

### ⚙️ Settings
- Update PIN code
- View account info
- Manage preferences

### ℹ️ About
- Learn about features
- Supported hash types
- Why choose CrackSmith

### 👑 Admin Panel (Admins Only)
- Platform statistics
- User management
- Installation tracking
- Job monitoring

## Free vs Premium

### Free Account
- ✅ Run locally on your device
- ✅ 2 threads
- ✅ 10 jobs per day
- ✅ Basic wordlist
- ✅ All core features

### Premium Account
- ⭐ Run on fast servers
- ⭐ 8 threads
- ⭐ 100 jobs per day
- ⭐ Priority queue access
- ⭐ Expanded wordlists

## Security Features

### PIN Protection
Set up a PIN for extra security:
1. Go to **Settings**
2. Scroll to "Security Settings"
3. Enter new PIN (4+ characters)
4. Click "Update PIN"

Now you'll need this PIN to login!

### Anti-Abuse Protection
- Rate limiting prevents spam
- Job queue prevents system overload
- Secure password storage with bcrypt
- JWT token-based authentication

## Mobile Usage

CrackSmith is fully optimized for mobile:

1. **On Desktop**: Sidebar is always visible
2. **On Mobile**: Tap menu icon (☰) to open navigation
3. **Responsive**: All features work on any screen size
4. **Touch-friendly**: Large buttons and easy navigation

## Common Tasks

### Change Your PIN
Settings → Security Settings → Update PIN

### View Statistics
Statistics → See charts and metrics

### Delete a Job
Jobs → Find job → Click delete icon (trash)

### Become Admin
See [DEPLOYMENT.md](DEPLOYMENT.md#setting-up-first-admin-user)

## Troubleshooting

### Backend won't start
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear and reinstall
rm -rf node_modules
npm install
```

### Can't login
- Check username/password
- If PIN is set, enter it correctly
- Make sure backend is running

### Job stuck in "queued"
- Backend processes jobs in background
- Free users: max 2 threads
- Check backend console for errors

## API Testing

Test the API directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Register (save the access_token from response)
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Submit job (replace YOUR_TOKEN with access_token)
curl -X POST http://localhost:5000/api/jobs/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hash_value":"5f4dcc3b5aa765d61d8327deb882cf99","hash_type":"md5"}'
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- See [TESTING.md](TESTING.md) for testing guide
- Explore the code in `backend/` and `frontend/`

## Getting Help

- **Documentation**: Check README files in each directory
- **Issues**: https://github.com/Lovsan/CrackSmith/issues
- **Testing**: See TESTING.md for test procedures

## Legal Notice

⚠️ **Important**: This tool is for authorized use only. You must have permission to crack any hashes you submit. Unauthorized use is prohibited.

## Tips

1. **Start simple**: Try the example hashes first
2. **Use auto-detect**: Let the system detect hash types
3. **Check statistics**: Monitor your success rate
4. **Set a PIN**: Add extra security to your account
5. **Mobile-friendly**: Use it on any device

---

Enjoy using CrackSmith! 🔐✨
