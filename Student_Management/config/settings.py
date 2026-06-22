"""
Configuration settings for the Student Management System
Loads environment variables and application settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== Supabase Configuration ====================
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

# ==================== Application Configuration ====================
APP_NAME = os.getenv('APP_NAME', 'Student Management System')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ==================== GUI Configuration ====================
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# ==================== Color Scheme ====================
# Modern professional colors
COLORS = {
    'primary': '#2563EB',          # Blue
    'secondary': '#64748B',         # Slate
    'success': '#10B981',           # Green
    'danger': '#EF4444',            # Red
    'warning': '#F59E0B',           # Amber
    'info': '#3B82F6',              # Light Blue
    'bg_dark': '#1F2937',           # Dark Gray
    'bg_light': '#F9FAFB',          # Light Gray
    'text_dark': '#111827',         # Very Dark Gray
    'text_light': '#FFFFFF',        # White
    'border': '#E5E7EB',            # Border Gray
    'hover': '#1E40AF',             # Darker Blue
}

# ==================== Font Configuration ====================
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11, 'normal'),
    'small': ('Segoe UI', 9, 'normal'),
    'code': ('Courier New', 10, 'normal'),
}

# ==================== Table Configuration ====================
TABLE_HEADERS_BG = '#2563EB'
TABLE_HEADERS_FG = '#FFFFFF'
TABLE_ROW_HEIGHT = 25
TABLE_ALTERNATING_ROW_COLOR = '#F3F4F6'

# ==================== API Configuration ====================
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# ==================== Database Tables ====================
DB_TABLES = {
    'users': 'users',
    'students': 'students',
    'attendance': 'attendance',
    'courses': 'courses',
    'lecturers': 'lecturers',
    'enrollments': 'enrollments',
}

# ==================== Validation Rules ====================
VALIDATION = {
    'email_regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'password_min_length': 8,
    'phone_regex': r'^\d{10,15}$',
    'student_id_regex': r'^STU\d{6}$',
}
