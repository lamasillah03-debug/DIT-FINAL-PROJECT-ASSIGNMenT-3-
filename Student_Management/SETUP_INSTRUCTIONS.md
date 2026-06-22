# Student Management System - Complete Setup Instructions

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Pre-Installation Checklist](#pre-installation-checklist)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Database Configuration](#database-configuration)
5. [Running the Application](#running-the-application)
6. [Verification & Testing](#verification--testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum
- **OS**: Windows 10+, macOS 10.12+, or Linux (Ubuntu 18.04+)
- **RAM**: 4 GB
- **Disk Space**: 500 MB
- **Python**: 3.8 or higher

### Recommended
- **RAM**: 8 GB+
- **Python**: 3.10+
- **Internet**: Stable connection (for Supabase)
- **Browser**: For Supabase dashboard access

### Software
- Python 3.8+
- Pip (Python package manager)
- Git (optional but recommended)
- Text editor (VSCode recommended)

---

## Pre-Installation Checklist

### Check Python Installation
```bash
python --version          # Should show Python 3.8+
python -m pip --version   # Should show pip version
```

### Check Tkinter (GUI Library)

**Windows:**
- Usually installed with Python. If missing, run Python installer and check "tcl/tk and IDLE"

**macOS:**
```bash
python3 -m tkinter
# A small window should appear
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

### Create Supabase Account
1. Visit [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub or email
4. Create a new project
5. Wait for PostgreSQL database initialization (5-10 minutes)

---

## Step-by-Step Installation

### Step 1: Prepare Project Folder (2 minutes)

**Windows (PowerShell/Command Prompt):**
```bash
cd Desktop
# If folder doesn't exist:
mkdir Student_Management
cd Student_Management
```

**macOS/Linux (Terminal):**
```bash
cd ~/Desktop
mkdir Student_Management
cd Student_Management
```

### Step 2: Create Python Virtual Environment (2 minutes)

Virtual environment isolates project dependencies.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of terminal line.

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Copy Project Files (1 minute)

If you downloaded the project as ZIP:
1. Extract to the Student_Management folder
2. Verify you can see: main.py, requirements.txt, .env, config/, database/, etc.

### Step 4: Install Python Dependencies (3 minutes)

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `supabase` - Database connection library
- `python-dotenv` - Environment variable management
- `requests` - HTTP library
- `Pillow` - Image processing

Verify installation:
```bash
pip list
```

### Step 5: Configure Supabase Credentials (3 minutes)

#### Get Supabase Credentials:

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project
3. Click **Settings** → **API**
4. You'll see:
   - **Project URL** (SUPABASE_URL)
   - **anon public** key (SUPABASE_KEY)
   - **service_role** key (SUPABASE_SERVICE_ROLE_KEY)

#### Update .env File:

1. Open `.env` file with text editor
2. Replace values:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

APP_NAME=Student Management System
APP_VERSION=1.0.0
DEBUG=True
```

3. Save file

**⚠️ IMPORTANT**: Never commit .env with real credentials to GitHub!

---

## Database Configuration

### Option A: Using Supabase Web Console (Recommended)

#### Step 1: Access SQL Editor
1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project
3. Click **SQL Editor** (left sidebar)
4. Click **New Query**

#### Step 2: Execute Database Schema

1. Open `database/schema.sql` in text editor
2. Copy **entire content** (Ctrl+A, Ctrl+C)
3. Paste into Supabase SQL Editor
4. Click **Run** button
5. Wait for completion (should see green checkmark)

#### Step 3: Verify Tables Created

In SQL Editor, run:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

Should see these tables:
- attendance
- courses
- enrollments
- lecturers
- students
- users

### Option B: Using Supabase CLI (Advanced)

```bash
# Install Supabase CLI
npm install -g supabase

# Or use Homebrew (macOS)
brew install supabase/tap/supabase

# Link to your project
supabase link --project-ref your-project-id

# Run migrations
supabase db push database/schema.sql
```

---

## Running the Application

### Start Application

**Windows:**
```bash
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

### Expected Behavior

1. **Splash Screen** (2-3 seconds)
   - Shows application name and version
   - Loading animation

2. **Login Screen**
   - Email and password fields
   - "Sign Up" link if no account
   - "Forgot Password" link

### First Time Setup

#### Create Account:
1. Click **"Sign Up"** link
2. Fill form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Password: Test@1234567 (must have uppercase, lowercase, number)
3. Click **"Create Account"**
4. Check email inbox for OTP code
5. Enter OTP when prompted
6. You're now registered!

#### First Login:
1. Enter email and password
2. Click **"Sign In"**
3. Dashboard appears with sidebar

---

## Verification & Testing

### Test Database Connection

1. In application, go to Profile page
2. You should see your email address
3. This confirms database is working

### Test Authentication

1. Create test account
2. Logout
3. Login with test account
4. Should access dashboard

### Test Database Schema

In Supabase SQL Editor:

```sql
-- Count tables
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'public';
-- Should return 6

-- Check RLS enabled
SELECT tablename 
FROM pg_tables 
WHERE tablename IN ('users', 'students', 'courses', 'lecturers', 'enrollments', 'attendance');
```

---

## Troubleshooting

### Issue: Python not found
```
'python' is not recognized as an internal or external command
```
**Solution:**
- Install Python from [python.org](https://python.org)
- Make sure "Add Python to PATH" is checked during installation

### Issue: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'supabase'
```
**Solution:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### Issue: Tkinter not found
```
ModuleNotFoundError: No module named 'tkinter'
```
**Solution:**

**Windows:**
- Run Python installer
- Choose "Modify"
- Check "tcl/tk and IDLE"
- Click Install

**macOS:**
```bash
brew install python-tk
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Issue: .env file not found
```
KeyError: 'SUPABASE_URL'
```
**Solution:**
- Ensure .env file exists in project root
- File must be named exactly: `.env`
- Verify it contains SUPABASE_URL, SUPABASE_KEY values

### Issue: Cannot connect to Supabase
```
ConnectionError: Failed to connect to Supabase
```
**Solution:**
1. Check internet connection
2. Verify SUPABASE_URL is correct
3. Check SUPABASE_KEY is correct
4. Verify Supabase project exists and is active
5. Try disabling VPN if using one

### Issue: OTP Not Received
**Solution:**
1. Check spam/junk folder
2. Wait 2-3 minutes (sometimes delayed)
3. Use "Resend Code" button
4. Check Supabase email configuration
5. Verify email is not already registered

### Issue: Can't create account (email already exists)
**Solution:**
1. Try different email
2. Or use forgot password to reset existing account
3. Check Supabase Users in Auth section

### Issue: Application crashes on startup
**Solution:**
1. Check `logs/app.log` for error details
2. Set DEBUG=True in .env for more info
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Try restarting application

### Issue: GUI freezes
**Solution:**
1. Don't perform long operations (use threading for production)
2. Restart application
3. Check logs for errors
4. Verify system resources (RAM, CPU)

### Issue: Database schema not created
**Solution:**
1. Verify SQL was copied completely
2. Check for error messages in Supabase
3. Try creating tables manually one at a time
4. Ensure you have database permissions

---

## Post-Installation Steps

### 1. Create Backup
```bash
# In Supabase Dashboard → Database → Backups
# Click "Save a backup now"
```

### 2. Enable Two-Factor Authentication (2FA)
1. Go to Supabase Dashboard → Auth Settings
2. Enable 2FA for admin account
3. Save recovery codes securely

### 3. Set Up Email Templates (Optional)
1. Supabase → Auth → Email Templates
2. Customize email messages

### 4. Test All Features
- [ ] Create account
- [ ] Verify email with OTP
- [ ] Login
- [ ] Logout
- [ ] Forgot password
- [ ] Edit profile
- [ ] Change password

### 5. Performance Tuning
1. Monitor database performance
2. Add indexes if needed
3. Set up query logging
4. Regular backups

---

## Development Setup

### Using Git
```bash
# Initialize git
git init

# Create .gitignore (already provided)
# Add files
git add .

# Commit
git commit -m "Initial commit"
```

### IDE Setup (VSCode Recommended)

**Extensions to Install:**
- Python (Microsoft)
- Pylance
- Python Docstring Generator

**Settings (.vscode/settings.json):**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true
    }
}
```

---

## File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `.env` | Configuration and secrets |
| `requirements.txt` | Python dependencies |
| `config/settings.py` | Global configuration |
| `database/schema.sql` | Database schema |
| `database/connection.py` | Database connection |
| `auth/auth_manager.py` | Authentication logic |
| `pages/*.py` | UI pages and screens |
| `widgets/custom_widgets.py` | Custom UI components |
| `utils/*.py` | Utility functions |

---

## Security Checklist

- [ ] .env file added to .gitignore
- [ ] Real credentials in .env file
- [ ] SUPABASE_SERVICE_ROLE_KEY kept private
- [ ] Strong password for admin account
- [ ] RLS enabled on all tables
- [ ] Regular database backups
- [ ] Keep Python packages updated
- [ ] Monitor application logs

---

## Support & Resources

### Documentation
- 📖 [README.md](README.md) - Full project guide
- 📖 [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Developer reference
- 📖 [DATABASE_SETUP.md](DATABASE_SETUP.md) - Database guide
- 📖 [QUICKSTART.md](QUICKSTART.md) - 5-minute setup

### External Resources
- 🔗 [Supabase Documentation](https://supabase.com/docs)
- 🔗 [Python Documentation](https://docs.python.org/3/)
- 🔗 [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

### Getting Help
1. Check error logs: `logs/app.log`
2. Review documentation files
3. Enable DEBUG mode in .env
4. Check Supabase logs and metrics

---

## Next Steps

1. **Complete Installation** using steps above
2. **Read README.md** for feature overview
3. **Explore Code** to understand architecture
4. **Create Test Data** using Supabase console
5. **Customize** application for your needs

---

**Installation Complete! 🎉**

The Student Management System is now ready to use. Start by running:
```bash
python main.py
```

For questions or issues, refer to troubleshooting section or check documentation files.

**Happy coding! 🚀**
