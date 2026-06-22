# Troubleshooting Quick Reference

## Common Issues & Solutions

### ❌ Python/Installation Issues

#### Python not found
**Error:** `'python' is not recognized as an internal or external command`

**Solutions:**
1. Check installation: `python --version`
2. Add Python to PATH (Windows):
   - Control Panel → Environment Variables
   - Add Python installation path to PATH
3. Reinstall Python from python.org
   - Check "Add Python to PATH" during installation
4. Use `python3` instead of `python` on macOS/Linux

---

#### ModuleNotFoundError: No module named 'tkinter'
**Error:** `ModuleNotFoundError: No module named 'tkinter'`

**Solutions:**

**Windows:**
- Run Python installer
- Click "Modify"
- Check "tcl/tk and IDLE"
- Complete installation

**macOS:**
```bash
brew install python-tk
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

---

#### ModuleNotFoundError: No module named 'supabase'
**Error:** `ModuleNotFoundError: No module named 'supabase'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

---

### ❌ Configuration Issues

#### .env file not found
**Error:** `KeyError: 'SUPABASE_URL'` or similar

**Solutions:**
1. Verify .env file exists in project root:
   ```bash
   # Windows (PowerShell)
   Test-Path .env
   # macOS/Linux
   test -f .env && echo "File exists"
   ```

2. Create .env file if missing:
   ```bash
   # Copy from template
   cp .env.example .env  # if template exists
   ```

3. Edit .env with text editor (Notepad, VSCode, etc.)


#### Invalid Supabase credentials
**Error:** `ConnectionError: Failed to connect to Supabase`

**Solutions:**
1. Verify credentials in .env are correct:
   ```bash
   # Get correct values from:
   # supabase.com/dashboard → Your Project → Settings → API
   ```

2. Check .env format:
   - No spaces around equals sign: `KEY=value` ✅
   - Not: `KEY = value` ❌

3. Test credentials:
   - Visit SUPABASE_URL in browser
   - Should show Supabase API endpoint
   - Verify SUPABASE_KEY starts with "eyJ"

4. Ensure project is active:
   - Go to Supabase dashboard
   - Verify project status is "Active" (green)
   - Not "Pausing" or "Paused"

---

### ❌ Database Issues

#### Database schema not created
**Error:** Table not found or connection errors

**Solutions:**
1. Verify schema.sql was executed:
   ```bash
   # In Supabase SQL Editor, run:
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

2. If no tables shown:
   - Open `database/schema.sql`
   - Copy entire content
   - Paste in Supabase SQL Editor
   - Click "Run"
   - Check for error messages

3. If SQL error:
   - Copy error message
   - Check schema.sql for syntax
   - Run sections one at a time
   - Contact Supabase support if persistent

---

#### RLS policies not enabled
**Error:** Data access denied, getting empty results

**Solutions:**
1. Check RLS policies created:
   ```sql
   SELECT tablename, policyname 
   FROM pg_policies 
   WHERE schemaname = 'public';
   ```

2. If no policies:
   - Re-run schema.sql
   - Ensure entire file executed

3. Verify RLS enabled:
   ```sql
   SELECT * 
   FROM pg_tables 
   WHERE tablename = 'students';
   ```
   - Check `rowsecurity` column is TRUE

---

### ❌ Application Launch Issues

#### Application won't start
**Error:** Blank window or immediate crash

**Solutions:**
1. Check virtual environment activated:
   - Should see `(venv)` in terminal
   - If not: run `source venv/bin/activate` or `venv\Scripts\activate`

2. Verify all dependencies:
   ```bash
   pip list | grep -E "supabase|python-dotenv|requests|Pillow"
   ```

3. Check for Python errors:
   ```bash
   python main.py
   # Look for error messages in terminal
   ```

4. Check application log:
   ```bash
   cat logs/app.log  # macOS/Linux
   type logs\app.log  # Windows
   ```

5. Enable debug mode in .env:
   ```env
   DEBUG=True
   ```
   - Run again to see detailed messages

6. Verify Tkinter works:
   ```bash
   python -m tkinter
   # Should show small window
   ```

---

#### Application window appears then closes
**Error:** Rapid window close after launch

**Solutions:**
1. Run from terminal to see errors:
   ```bash
   python main.py
   # Look for error messages before window closes
   ```

2. Check logs:
   ```bash
   cat logs/app.log
   ```

3. Enable DEBUG mode in .env

4. Verify Supabase connection:
   - Check internet connection
   - Verify SUPABASE_URL and SUPABASE_KEY are set
   - Test in Supabase dashboard

5. Check Python version:
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

---

### ❌ Authentication Issues

#### Cannot sign up (email already exists)
**Error:** `Error: Email already in use`

**Solutions:**
1. Try different email address
2. Recover existing account:
   - Click "Forgot Password"
   - Check email for reset link
   - Set new password
   - Login
3. Check Supabase Auth → Users for account list
4. Delete test accounts:
   - Go to Supabase → Auth → Users
   - Click three dots → Delete User

---

#### OTP not received
**Error:** No email or OTP expires before arrival

**Solutions:**
1. Check spam/junk folder
2. Wait 2-3 minutes (sometimes delayed)
3. Click "Resend Code" button
4. Verify email in signup form was correct
5. Check Supabase:
   - Dashboard → Auth → Email Templates
   - Verify templates are enabled
6. Test email sending:
   - In Supabase Auth, trigger test email
   - Check if received

---

#### Cannot login (wrong password)
**Error:** `Error: Invalid login credentials`

**Solutions:**
1. Verify email is correct
2. Check CAPS LOCK is off
3. Try "Forgot Password":
   - Enter email
   - Check email for reset link
   - Create new password
   - Try login again
4. Verify password contains:
   - Uppercase letter
   - Lowercase letter
   - Number
   - Min 8 characters

---

#### Session expired
**Error:** Logged out unexpectedly or session error

**Solutions:**
1. Login again
2. Check internet connection
3. Verify Supabase project is active
4. Check browser cookies (if web version)
5. Clear application cache:
   ```bash
   rm -rf logs/  # macOS/Linux
   rmdir /s logs  # Windows
   # Restart application
   ```

---

### ❌ UI/Display Issues

#### GUI looks distorted
**Error:** Widgets misaligned, text cut off

**Solutions:**
1. Check monitor resolution:
   - Minimum: 1024x768
   - Recommended: 1366x768+

2. Update Tkinter:
   ```bash
   pip install --upgrade pillow
   ```

3. Adjust window size in code:
   - Edit `config/settings.py`
   - Change `WINDOW_WIDTH` and `WINDOW_HEIGHT`
   - Restart app

4. Check font availability:
   - Application uses "Segoe UI"
   - Falls back to default if unavailable
   - Safe on Windows, macOS, Linux

---

#### Windows positioned off-screen
**Error:** Application window doesn't appear

**Solutions:**
1. Delete application preferences if saved
2. Edit main.py and change window geometry:
   ```python
   # In _center_window()
   # Change default width/height
   ```

3. Use default window position:
   - Don't maximize on startup
   - Let _center_window() position

---

### ❌ Data Issues

#### Data not saving
**Error:** Add/edit operations don't persist

**Solutions:**
1. Check database connection:
   - Verify SUPABASE_URL and SUPABASE_KEY
   - Check internet connection
   
2. Check RLS policies:
   - User might not have insert/update permissions
   - Verify user role in database

3. Check database schema:
   ```sql
   -- In Supabase SQL Editor
   SELECT * FROM students LIMIT 1;
   ```

4. Check logs for errors:
   ```bash
   cat logs/app.log
   ```

5. Verify user is authenticated:
   - Should see Profile page properly

---

#### Empty data tables
**Error:** Tables show no data even though records exist

**Solutions:**
1. Check RLS policies:
   - May be blocking SELECT
   - Verify current user permissions

2. Query database directly:
   ```sql
   SELECT COUNT(*) FROM students;
   SELECT * FROM students LIMIT 10;
   ```

3. Check user role:
   - Go to users table in Supabase
   - Verify current user's role
   - Ensure role has SELECT permission

4. Refresh data:
   - Logout and login again
   - Switch pages and back

---

### ❌ Performance Issues

#### Application runs slowly
**Error:** Slow response times, lag

**Solutions:**
1. Check internet connection speed
2. Reduce data in queries:
   - Add pagination
   - Use filters/search
   - Limit results

3. Check Supabase performance:
   - Go to Dashboard → Metrics
   - Check query performance
   - Monitor database load

4. Clear logs (may grow large):
   ```bash
   rm logs/app.log  # macOS/Linux
   del logs\app.log  # Windows
   ```

5. Close other applications to free RAM

6. Restart application:
   - Close window
   - Wait 5 seconds
   - Run again

---

#### Database queries are slow
**Error:** Data takes long time to load

**Solutions:**
1. Check database indexes:
   ```sql
   SELECT * FROM pg_indexes WHERE tablename = 'students';
   ```

2. Re-run schema.sql if missing indexes:
   - Contains CREATE INDEX statements
   - Improves query performance

3. Check query in Supabase:
   - Dashboard → SQL Editor
   - Test query manually
   - Look for "Execution Time"

4. Optimize queries:
   - Use WHERE clauses
   - Select specific columns
   - Use LIMIT for pagination

---

## 🔍 Debugging Steps

### Step 1: Check Logs
```bash
# Open logs/app.log
cat logs/app.log  # macOS/Linux
type logs\app.log  # Windows
# Look for ERROR or EXCEPTION entries
```

### Step 2: Enable Debug Mode
```env
# In .env file
DEBUG=True
```

### Step 3: Check Database
```sql
-- In Supabase SQL Editor
-- Run diagnostic queries
SELECT version();  -- Check PostgreSQL version
SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';  -- Count tables
```

### Step 4: Test Components
```bash
# Test Tkinter
python -m tkinter

# Test Supabase connection
python -c "from database.connection import get_db; db = get_db(); print('Connected')"

# Test validators
python -c "from utils.validators import validate_email; print(validate_email('test@test.com'))"
```

### Step 5: Check Internet
```bash
ping supabase.com
# Should show successful responses
```

---

## 📞 Getting More Help

### Documentation Files
- 📖 README.md - Main documentation
- 📖 SETUP_INSTRUCTIONS.md - Setup help
- 📖 API_DOCUMENTATION.md - API reference
- 📖 DATABASE_SETUP.md - Database help

### External Resources
- 🔗 Supabase: https://supabase.com/docs
- 🔗 Supabase Support: https://supabase.com/support
- 🔗 Python: https://docs.python.org/3/
- 🔗 Tkinter: https://docs.python.org/3/library/tkinter.html

### When Asking for Help
Include:
1. Error message (exact text)
2. Steps to reproduce
3. Your operating system
4. Python version: `python --version`
5. Check `logs/app.log` for details
6. Screenshot of issue if possible

---

## ✅ Quick Verification Checklist

Use this to verify everything is working:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file exists with credentials
- [ ] SUPABASE_URL is correct
- [ ] SUPABASE_KEY is correct
- [ ] Database schema created in Supabase
- [ ] Can create account
- [ ] OTP email received
- [ ] Can login successfully
- [ ] Dashboard displays
- [ ] Profile shows user email
- [ ] Can navigate between pages
- [ ] Logs are created in logs/ folder

---

**If you're still having issues:**
1. Re-read relevant documentation section
2. Check your .env file format
3. Verify Supabase project is active
4. Enable DEBUG=True for more details
5. Check logs/app.log for specific errors
6. Try running diagnostic steps above

**Most issues are related to .env configuration or Supabase connectivity!**
