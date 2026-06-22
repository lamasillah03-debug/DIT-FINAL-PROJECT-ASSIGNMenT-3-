"""
Authentication Module
Handles user authentication with simplified flow
Uses local SQLite database for offline operation
"""
from database.local_connection import get_db
from utils.validators import validate_email
from utils.logger import get_logger
import uuid
import hashlib

logger = get_logger(__name__)


class AuthenticationManager:
    """
    Manages user authentication with simplified registration and login
    Saves user data to local SQLite database
    """
    
    def __init__(self):
        """Initialize authentication manager"""
        self.db = get_db()
        self.current_user = None
        self.current_user_email = None
    
    def _hash_password(self, password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _convert_row_to_dict(self, row):
        """Convert sqlite3.Row to dictionary"""
        if row is None:
            return None
        return dict(row) if hasattr(row, 'keys') else row
    
    def sign_up_with_email(self, email: str, password: str, first_name: str = '', 
                          last_name: str = '') -> dict:
        """
        Register new user and save directly to database
        
        Args:
            email (str): User email address
            password (str): User password
            first_name (str): User first name
            last_name (str): User last name
        
        Returns:
            dict: Response with success/error
        """
        try:
            # Validate email format
            if not validate_email(email):
                return {'success': False, 'message': 'Invalid email format'}
            
            # Validate password
            if len(password) < 6:
                return {
                    'success': False,
                    'message': 'Password must be at least 6 characters long'
                }
            
            # Check if email already exists
            try:
                existing_user = self.db.fetch_one(
                    'SELECT * FROM users WHERE email = ?',
                    (email,)
                )
                if existing_user:
                    return {'success': False, 'message': 'Email already registered'}
            except Exception as e:
                logger.warning(f"Could not check existing email: {str(e)}")
            
            # Create user ID
            user_id = str(uuid.uuid4())
            
            # Hash password
            hashed_password = self._hash_password(password)
            
            # Insert user into database
            user_data = {
                'id': user_id,
                'email': email,
                'password': hashed_password,
                'full_name': f"{first_name} {last_name}".strip(),
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': '',
                'avatar_url': '',
                'role': 'user',
                'department': '',
                'is_active': True
            }
            
            try:
                self.db.execute(
                    '''INSERT INTO users 
                       (id, email, password, full_name, first_name, last_name, 
                        phone_number, avatar_url, role, department, is_active)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (
                        user_id, email, hashed_password,
                        user_data['full_name'], first_name, last_name,
                        '', '', 'user', '', True
                    )
                )
            except Exception as e:
                logger.error(f"Database insert error: {str(e)}")
                return {'success': False, 'message': f'Registration failed: {str(e)}'}
            
            logger.info(f"User registered successfully: {email}")
            
            # Set current user
            self.current_user = user_data
            self.current_user_email = email
            
            return {
                'success': True,
                'message': 'Registration successful',
                'user': user_data
            }
        
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': str(e)}
    
    def sign_in_with_email(self, email: str, password: str) -> dict:
        """
        Sign in user with email and password
        
        Args:
            email (str): User email address
            password (str): User password
        
        Returns:
            dict: Response with user data
        """
        try:
            if not validate_email(email):
                return {'success': False, 'message': 'Invalid email format'}
            
            # Query user from database
            user_row = self.db.fetch_one(
                'SELECT * FROM users WHERE email = ?',
                (email,)
            )
            
            if not user_row:
                return {'success': False, 'message': 'Email or password incorrect'}
            
            user = self._convert_row_to_dict(user_row)
            
            # Verify password
            hashed_password = self._hash_password(password)
            if user['password'] != hashed_password:
                return {'success': False, 'message': 'Email or password incorrect'}
            
            # Set current user
            self.current_user = user
            self.current_user_email = email
            
            logger.info(f"User signed in successfully: {email}")
            
            return {
                'success': True,
                'message': 'Sign in successful',
                'user': user
            }
        
        except Exception as e:
            error_msg = f"Sign in error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': str(e)}
    
    def get_current_user(self) -> dict:
        """
        Get current authenticated user
        
        Returns:
            dict: Current user data or None if not authenticated
        """
        if self.current_user:
            return {'success': True, 'user': self.current_user}
        return {'success': False, 'message': 'No user logged in'}
    
    def sign_out(self) -> dict:
        """
        Sign out current user
        
        Returns:
            dict: Response indicating sign out status
        """
        try:
            self.current_user = None
            self.current_user_email = None
            logger.info("User signed out successfully")
            return {'success': True, 'message': 'Signed out successfully'}
        except Exception as e:
            error_msg = f"Sign out error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': str(e)}
    
    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        return self.current_user is not None
    
    def update_user_profile(self, user_id: str, **kwargs) -> dict:
        """
        Update user profile information
        
        Args:
            user_id (str): User ID to update
            **kwargs: Fields to update
        
        Returns:
            dict: Response with update status
        """
        try:
            # Build dynamic update query
            set_clause = ', '.join([f'{k} = ?' for k in kwargs.keys()])
            values = list(kwargs.values())
            values.append(user_id)
            
            query = f'UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            self.db.execute(query, values)
            
            if self.current_user and self.current_user['id'] == user_id:
                self.current_user.update(kwargs)
            
            logger.info(f"User profile updated: {user_id}")
            return {'success': True, 'message': 'Profile updated successfully'}
        
        except Exception as e:
            error_msg = f"Profile update error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': str(e)}
    
    def reset_password(self, email: str) -> dict:
        """
        Reset password for user
        
        Args:
            email (str): User email address
        
        Returns:
            dict: Response with password reset status
        """
        try:
            # Validate email format
            if not validate_email(email):
                return {'success': False, 'message': 'Invalid email format'}
            
            # Check if email exists
            user = self.db.fetch_one(
                'SELECT * FROM users WHERE email = ?',
                (email,)
            )
            if not user:
                return {'success': False, 'message': 'Email not found in our system'}
            
            logger.info(f"Password reset requested for: {email}")
            
            return {
                'success': True,
                'message': 'If this email exists, you will receive password reset instructions'
            }
        
        except Exception as e:
            error_msg = f"Password reset error: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': str(e)}


def get_auth_manager():
    """
    Factory function to get authentication manager instance
    
    Returns:
        AuthenticationManager: Authentication manager instance
    """
    return AuthenticationManager()
