"""
Database Connection Module
Handles connection to Supabase PostgreSQL database
"""
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY, DEBUG
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Singleton class to manage database connection to Supabase
    Ensures only one connection instance is used throughout the application
    """
    
    _instance = None
    _client = None
    
    def __new__(cls):
        """
        Implement singleton pattern to ensure only one connection instance
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the database connection"""
        if self._client is None:
            self._initialize_connection()
    
    def _initialize_connection(self):
        """
        Initialize connection to Supabase
        Raises ValueError if credentials are not configured
        """
        if not SUPABASE_URL or not SUPABASE_KEY:
            error_msg = (
                "Supabase credentials not configured. "
                "Please set SUPABASE_URL and SUPABASE_KEY in .env file"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            self._client = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("Successfully connected to Supabase")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            raise
    
    @property
    def client(self):
        """Get the Supabase client instance"""
        if self._client is None:
            self._initialize_connection()
        return self._client
    
    def get_connection(self):
        """
        Get the database connection/client
        Returns: Supabase client instance
        """
        return self.client
    
    def close(self):
        """Close the database connection"""
        self._client = None
        logger.info("Database connection closed")


def get_db():
    """
    Factory function to get database instance
    Returns: DatabaseConnection instance
    """
    return DatabaseConnection()
