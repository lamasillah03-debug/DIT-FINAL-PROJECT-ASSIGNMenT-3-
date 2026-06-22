"""
Local SQLite Database Connection
Handles connection to local SQLite database for offline use
"""
import sqlite3
import os
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class LocalDatabaseConnection:
    """
    Singleton class to manage local SQLite database connection
    No internet required - works completely offline
    """
    
    _instance = None
    _connection = None
    DB_PATH = os.path.join(os.path.dirname(__file__), 'student_management.db')
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(LocalDatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database connection"""
        if self._connection is None:
            self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to local SQLite database"""
        try:
            self._connection = sqlite3.connect(self.DB_PATH, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            logger.info(f"Connected to local SQLite database at {self.DB_PATH}")
            self._create_tables()
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create tables if they don't exist"""
        cursor = self._connection.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone_number TEXT,
                avatar_url TEXT,
                role TEXT DEFAULT 'user',
                department TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                student_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                program TEXT,
                enrollment_date TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create lecturers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecturers (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                department TEXT NOT NULL,
                specialization TEXT,
                qualifications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id TEXT PRIMARY KEY,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                department TEXT NOT NULL,
                lecturer TEXT,
                credits TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id TEXT PRIMARY KEY,
                student TEXT NOT NULL,
                course TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self._connection.commit()
        logger.info("Database tables created/verified")
    
    def get_connection(self):
        """Get the database connection"""
        if self._connection is None:
            self._initialize_connection()
        return self._connection
    
    def execute(self, query, params=None):
        """Execute a query"""
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            return cursor
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            raise
    
    def fetch_one(self, query, params=None):
        """Fetch one row"""
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            return None
    
    def fetch_all(self, query, params=None):
        """Fetch all rows"""
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Fetch error: {str(e)}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed")


def get_db():
    """
    Factory function to get database instance
    Returns: LocalDatabaseConnection instance
    """
    return LocalDatabaseConnection()
