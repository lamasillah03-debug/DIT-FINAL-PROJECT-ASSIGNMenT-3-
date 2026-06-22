"""
Main Application File
Entry point for the Student Management System
Handles window management, page navigation, and authentication
"""
import tkinter as tk
from tkinter import messagebox
import sys

from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, COLORS
)
from pages.splash_screen import SplashScreen
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.dashboard_page import DashboardPage, SidebarNavigation
from pages.content_pages import (
    StudentManagementPage, AttendancePage, CoursePage,
    LecturerPage, ProfilePage, SettingsPage
)
from auth.auth_manager import get_auth_manager
from utils.logger import get_logger

logger = get_logger(__name__)


class StudentManagementApp:
    """
    Main application class
    Manages window, pages, and navigation
    """
    
    def __init__(self, root):
        """
        Initialize the application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.configure(bg=COLORS['bg_light'])
        
        # Center window on screen
        self._center_window()
        
        # Initialize variables
        self.auth_manager = get_auth_manager()
        self.current_user = None
        self.current_page = None
        self.container = None
        
        # Pages storage
        self.pages = {}
        
        # Start application
        self._show_splash_screen()
    
    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIGHT // 2)
        
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')
    
    def _show_splash_screen(self):
        """Show splash screen on startup"""
        splash = SplashScreen(self.root)
        
        # Simulate loading
        messages = [
            'Initializing database...',
            'Loading configuration...',
            'Starting application...'
        ]
        
        for msg in messages:
            splash.update_status(msg)
            splash.after(500)
        
        # Check authentication status
        self.root.after(2000, lambda: self._initialize_app(splash))
    
    def _initialize_app(self, splash):
        """
        Initialize application after splash screen
        
        Args:
            splash: Splash screen window
        """
        try:
            splash.destroy()
            
            # Check if user is already authenticated
            if self.auth_manager.is_authenticated():
                user = self.auth_manager.get_current_user()
                self.current_user = user.get('user') if user.get('success') else None
                self._show_main_app()
            else:
                self._show_login_screen()
        
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            messagebox.showerror('Error', f'Failed to initialize application: {str(e)}')
            self.root.quit()
    
    def _show_login_screen(self):
        """Show login screen"""
        self._clear_container()
        
        login_page = LoginPage(
            self.container,
            on_login_success=self._on_login_success,
            on_register_click=self._show_registration_screen
        )
        login_page.pack(fill=tk.BOTH, expand=True)
        self.current_page = login_page
    
    def _show_registration_screen(self):
        """Show registration screen"""
        self._clear_container()
        
        reg_page = RegistrationPage(
            self.container,
            on_registration_success=self._on_registration_success,
            on_login_click=self._show_login_screen
        )
        reg_page.pack(fill=tk.BOTH, expand=True)
        self.current_page = reg_page
    
    def _show_main_app(self):
        """Show main application (dashboard and sidebar)"""
        self._clear_container()
        
        # Create main container with sidebar
        main_frame = tk.Frame(self.root, bg=COLORS['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        sidebar = SidebarNavigation(
            main_frame,
            on_nav_click=self._on_nav_click,
            on_logout=self._on_logout
        )
        
        # Create content area
        content_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Store pages
        self.pages = {
            'dashboard': DashboardPage(content_frame, self.current_user, self._on_logout, self._on_nav_click),
            'students': StudentManagementPage(content_frame),
            'attendance': AttendancePage(content_frame),
            'courses': CoursePage(content_frame),
            'lecturers': LecturerPage(content_frame),
            'profile': ProfilePage(content_frame, self.current_user),
            'settings': SettingsPage(content_frame),
        }
        
        # Show dashboard by default
        self._show_page('dashboard')
    
    def _show_page(self, page_id):
        """
        Show a specific page
        
        Args:
            page_id (str): Page identifier
        """
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()
        
        # Show selected page
        if page_id in self.pages:
            self.pages[page_id].pack(fill=tk.BOTH, expand=True)
            self.current_page = self.pages[page_id]
    
    def _on_nav_click(self, page_id):
        """
        Handle navigation menu click
        
        Args:
            page_id (str): Page to navigate to
        """
        self._show_page(page_id)
    
    def _on_login_success(self, user):
        """
        Handle successful login - Navigate to dashboard
        
        Args:
            user: User data
        """
        self.current_user = user
        self._show_main_app()
    
    def _on_registration_success(self, user):
        """
        Handle successful registration - Navigate to dashboard
        
        Args:
            user: User data
        """
        self.current_user = user
        self._show_main_app()
    
    def _on_logout(self):
        """Handle logout"""
        if messagebox.askyesno('Confirm', 'Click to logout properly?'):
            self.auth_manager.sign_out()
            self.current_user = None
            messagebox.showinfo('Success', 'Successfully logged out!')
            self._show_login_screen()
    
    def _clear_container(self):
        """Clear main container"""
        if self.container:
            self.container.destroy()
        
        self.container = tk.Frame(self.root, bg=COLORS['bg_light'])
        self.container.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """
    Main entry point for the application
    """
    try:
        # Create root window
        root = tk.Tk()
        
        # Create and run application
        app = StudentManagementApp(root)
        app.run()
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        messagebox.showerror('Fatal Error', f'An error occurred: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()
