# Quick Start Guide

## 5-Minute Setup

Follow these steps to get the Student Management System running.

### Prerequisites
- Python 3.8+ installed
- Supabase account (free tier works)
- Git (optional)

### Step 1: Install Dependencies (1 minute)

```bash
# Navigate to project folder
cd Student_Management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```


3. Save file

### Step 4: Setup Database (1 minute)

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project
3. Click **SQL Editor** → **New Query**
4. Copy all content from `database/schema.sql`
5. Paste into SQL editor
6. Click **Run**
7. Wait for completion (should see "Success" message)

### Step 5: Run Application (1 minute)

```bash
python main.py
```

Done! Application should open.

## First Use

### Create Account
1. Click "Sign Up" link
2. Fill in details:
   - First Name: Your first name
   - Last Name: Your last name
   - Email: Your email
   - Password: Min 8 chars, uppercase, lowercase, number
3. Click "Create Account"
4. Check email for OTP code
5. Enter OTP and verify
6. Login with your credentials

### First Login
1. Enter email and password
2. Click "Sign In"
3. You'll see the Dashboard

## Dashboard Overview

### Left Sidebar
- **Dashboard**: Home page with statistics
- **Students**: Manage student records
- **Attendance**: Track attendance
- **Courses**: Manage courses
- **Lecturers**: Manage lecturers
- **Profile**: Your profile
- **Settings**: App settings
- **Logout**: Sign out

### Main Area
- Statistics cards showing key metrics
- Quick action buttons
- Data tables for management

## Common Tasks

### Add a Student
1. Click "Students" in sidebar
2. Click "Add Student" button
3. Fill form with student details
4. Click "Save"

### Take Attendance
1. Click "Attendance" in sidebar
2. Select course and date
3. Mark students present/absent
4. Click "Save"

### Manage Courses
1. Click "Courses" in sidebar
2. View list of courses
3. Add new course or edit existing

## Troubleshooting

### App won't start
- Check Python 3.8+ installed: `python --version`
- Check virtual environment activated
- Check all dependencies: `pip list`

### Can't login
- Verify Supabase credentials in `.env`
- Check email is correct
- Try "Forgot Password" link
- Check internet connection

### Database errors
- Verify `.env` file has correct credentials
- Check schema.sql was executed
- Go to Supabase Dashboard → Logs to check for errors

### GUI looks weird
- Update Tkinter: `pip install --upgrade tkinter`
- Restart application
- Check monitor resolution is 1024x768+

## Next Steps

1. **Read full README.md** for complete features
2. **Check API_DOCUMENTATION.md** for developer reference
3. **Review DATABASE_SETUP.md** for database details
4. **Explore code structure** in project folders

## Support Resources

- 📚 [Supabase Docs](https://supabase.com/docs)
- 📚 [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- 🐛 Check `logs/app.log` for errors
- 💬 Enable DEBUG=True in `.env` for more info

## Tips & Tricks

1. **Multiple Accounts**: Create different test accounts
2. **Test Data**: Use Database SQL Editor to insert test data
3. **Check Logs**: Review `logs/app.log` if something breaks
4. **Supabase Backups**: Regular backups in Supabase settings
5. **Mobile**: Use Supabase CLI for command-line management

---

**Happy Learning! 🚀**
