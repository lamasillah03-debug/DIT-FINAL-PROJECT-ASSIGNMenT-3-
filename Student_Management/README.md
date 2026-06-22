# Student Management System

A complete, production-ready Student Management System built with Python and Tkinter featuring a modern GUI, Supabase backend, and Email OTP authentication.

## Features
- ✅ Password Reset Functionality
- ✅ Secure Session Management
- ✅ Row Level Security (RLS) on Database

### User Management
- ✅ Student Management (Add, Edit, Delete, Search)
- ✅ Lecturer Management
- ✅ User Profile Management
- ✅ Role-based Access Control

### Academic Features
- ✅ Course Management
- ✅ Attendance Tracking
- ✅ Student Enrollment
- ✅ Grade Management
.
### Dashboard & UI
- ✅ Professional Modern Dashboard
- ✅ Statistics Cards
- ✅ Sidebar Navigation
- ✅ Responsive Layout
- ✅ Loading Indicators
- ✅ Notification System
- ✅ Data Tables with Treeview

## Project Structure

```
Student_Management/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── config/
│   ├── __init__.py
│   └── settings.py        # Global settings and configuration
├── database/
│   ├── __init__.py
│   ├── schema.sql         # Database schema and RLS policies
│   └── connection.py      # Supabase connection manager
├── auth/
│   ├── __init__.py
│   └── auth_manager.py    # Authentication and OTP management
├── pages/
│   ├── __init__.py
│   ├── splash_screen.py   # Splash screen
│   ├── login_page.py      # Login page
│   ├── registration_page.py # Registration page
│   ├── otp_page.py        # OTP verification
│   ├── forgot_password_page.py # Password reset
│   ├── dashboard_page.py  # Main dashboard
│   └── content_pages.py   # Student, attendance, course, etc. pages
├── widgets/
│   ├── __init__.py
│   └── custom_widgets.py  # Custom Tkinter widgets
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Logging configuration
│   ├── validators.py      # Input validation
│   └── helpers.py         # Utility functions
├── assets/                # Images and icons (placeholder)
└── logs/                  # Application logs (auto-created)
```

## System Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux
- Internet connection (for Supabase connection)
- Supabase account with PostgreSQL database

## Installation

### 1. Clone or Download the Project
```bash
cd Student_Management
```

### 2. Create Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


#### b. Get API Keys
1. Go to Settings → API
2. Copy `Project URL` (SUPABASE_URL)
3. Copy `anon public` key (SUPABASE_KEY)
4. Copy `service_role` key (SUPABASE_SERVICE_ROLE_KEY)



### 5. Initialize Database

#### Option A: Using Supabase Console (Recommended for Beginners)
1. Go to Supabase Dashboard → SQL Editor
2. Click "New Query"
3. Copy the entire content of `database/schema.sql`
4. Paste into the SQL editor
5. Click "Run"




### 6. Run the Application
```bash
python main.py
```

## Usage

### Login
1. Click "Sign In" on the login page
2. Enter your registered email and password
3. Click "Sign In" button

### Register
1. Click "Sign Up" link on login page
2. Fill in all required fields
3. Click "Create Account"
4. Verify your email with the OTP sent to your email
5. Login with your credentials

### Main Dashboard
- View statistics and quick access buttons
- Navigate using the sidebar menu
- Manage students, courses, attendance, etc.

### Managing Students
1. Go to "Students" from sidebar
2. **Add Student**: Click "Add Student" button and fill form
3. **Edit Student**: Select student and click "Edit Student"
4. **Delete Student**: Select student and click "Delete Student"
5. **Search Student**: Use search box and click "Search"

## Configuration

### Color Scheme
Edit `config/settings.py` to customize colors:
```python
COLORS = {
    'primary': '#2563EB',        # Main blue color
    'secondary': '#64748B',      # Secondary color
    'success': '#10B981',        # Success green
    'danger': '#EF4444',         # Error red
    # ... more colors
}
```

### Fonts
Customize fonts in `config/settings.py`:
```python
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    # ... more fonts
}
```

### Application Settings
```python
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
APP_NAME = 'Student Management System'
APP_VERSION = '1.0.0'
DEBUG = True
```

## Database Schema

### Tables
1. **users** - User profiles and authentication
2. **students** - Student information and enrollment
3. **lecturers** - Lecturer/instructor details
4. **courses** - Course information
5. **enrollments** - Student course enrollments
6. **attendance** - Attendance records

### Security Features
- Row Level Security (RLS) enabled on all tables
- Policies enforce user-based data access
- Auto-updating timestamps
- Soft delete support (is_active field)

See `database/schema.sql` for complete schema details.

## Troubleshooting

### Issue: Connection Refused
**Solution**: Check if Supabase credentials in `.env` are correct

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Tkinter Not Found (Linux)
**Solution**: Install Tkinter package
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (usually pre-installed)
```

### Issue: OTP Not Received
**Solution**: 
- Check spam folder
- Verify email in Supabase Auth settings
- Check email provider allows Supabase emails

## Development

### Adding New Pages
1. Create new file in `pages/` folder
2. Extend `CustomFrame` class
3. Implement `_create_widgets()` method
4. Register in `StudentManagementApp.pages` dictionary

### Adding New Widgets
1. Create in `widgets/custom_widgets.py`
2. Extend Tkinter base classes
3. Apply custom styling with `config.settings.COLORS`

### Database Queries
```python
from database.connection import get_db

db = get_db()
client = db.get_connection()

# Query example
response = client.table('students').select('*').execute()
```

## API Documentation

### Authentication Manager
```python
from auth.auth_manager import get_auth_manager

auth = get_auth_manager()

# Sign up
auth.sign_up_with_email(email, password)

# Sign in
auth.sign_in_with_email(email, password)

# Send OTP
auth.send_otp(email)

# Verify OTP
auth.verify_otp(email, otp_token)

# Reset password
auth.reset_password(email)

# Sign out
auth.sign_out()
```

### Validators
```python
from utils.validators import *

validate_email(email)
validate_password(password)
validate_phone(phone)
validate_name(name)
validate_date(date_str)
validate_student_id(student_id)
```

## Logging

Application logs are stored in `logs/app.log`:
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Information message")
logger.error("Error message")
```

## Performance Tips

1. **Lazy Loading**: Load data on demand, not at startup
2. **Pagination**: Use pagination for large datasets
3. **Indexing**: Database tables have proper indexes for performance
4. **Caching**: Cache frequently accessed data

## Security Best Practices

1. ✅ Never commit `.env` file with real credentials
2. ✅ Use strong passwords (min 8 characters, mixed case, numbers)
3. ✅ Enable 2FA in Supabase dashboard
4. ✅ Regularly update dependencies
5. ✅ Use HTTPS for all external connections
6. ✅ Validate all user inputs
7. ✅ Implement proper error handling

## Contributing

To contribute:
1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
2. Review [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
3. Check application logs in `logs/app.log`

## Changelog

### Version 1.0.0
- Initial release
- Complete authentication system
- Student management features
- Dashboard with statistics
- Attendance tracking
- Course management
- Responsive modern UI

## Future Enhancements

- [ ] Reports generation (PDF, Excel)
- [ ] Mobile app version
- [ ] Advanced analytics
- [ ] Online exam system
- [ ] Grade calculation automation

---

**Made with ❤️ by Your Development Team**
