"""
Login Page - Simple Card-based Design
Clean and simple login form for user authentication
"""
import tkinter as tk
from tkinter import messagebox
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomButton, CustomEntry, CustomLabel, CustomFrame, PasswordEntry
from auth.auth_manager import get_auth_manager
from utils.validators import validate_email


class LoginPage(CustomFrame):
    """
    Simple login page with card-based form design
    Allows users to sign in with email and password
    """
    
    def __init__(self, parent, on_login_success=None, on_register_click=None):
        """
        Initialize login page
        
        Args:
            parent: Parent widget
            on_login_success: Callback on successful login
            on_register_click: Callback when register button is clicked
        """
        super().__init__(parent)
        
        self.on_login_success = on_login_success
        self.on_register_click = on_register_click
        self.auth_manager = get_auth_manager()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create login page widgets with card design"""
        # Create main container
        main_container = CustomFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create centered card frame
        card_frame = tk.Frame(
            main_container,
            bg='#FFFFFF',
            relief=tk.FLAT,
            bd=0
        )
        card_frame.pack(anchor='center', pady=50)
        
        # Title
        title_label = tk.Label(
            card_frame,
            text='Student Management System',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg='#FFFFFF'
        )
        title_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle = tk.Label(
            card_frame,
            text='Sign In to Your Account',
            font=FONTS['body'],
            fg='#666666',
            bg='#FFFFFF'
        )
        subtitle.pack(pady=(0, 30))
        
        # Email label and entry
        email_label = tk.Label(
            card_frame,
            text='Email Address',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        email_label.pack(anchor='w', padx=40, pady=(0, 5))
        
        self.email_entry = CustomEntry(
            card_frame,
            placeholder='your.email@example.com',
            width=35
        )
        self.email_entry.pack(padx=40, pady=(0, 15), fill=tk.X)
        
        # Password label and entry
        password_label = tk.Label(
            card_frame,
            text='Password',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        password_label.pack(anchor='w', padx=40, pady=(0, 5))
        
        password_container = tk.Frame(card_frame, bg='#FFFFFF')
        password_container.pack(padx=40, pady=(0, 20), fill=tk.X)
        
        self.password_entry = PasswordEntry(
            password_container,
            placeholder='Enter your password'
        )
        self.password_entry.pack(fill=tk.X)
        
        # Login button
        login_btn = CustomButton(
            card_frame,
            text='Sign In',
            command=self._on_login,
            width=25,
            bg_color=COLORS['primary'],
            fg_color='#FFFFFF'
        )
        login_btn.pack(pady=20)
        
        # Register link
        register_frame = tk.Frame(card_frame, bg='#FFFFFF')
        register_frame.pack(pady=(0, 30))
        
        register_text = tk.Label(
            register_frame,
            text="Don't have an account? ",
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        register_text.pack(side=tk.LEFT)
        
        register_link = tk.Label(
            register_frame,
            text='Sign Up',
            font=FONTS['body'],
            fg=COLORS['primary'],
            bg='#FFFFFF',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT)
        register_link.bind('<Button-1>', lambda e: self._on_register())
    
    def _on_login(self):
        """Handle login button click"""
        email = self.email_entry.get_value()
        password = self.password_entry.get_value()
        
        # Validation
        if not email or not password:
            messagebox.showerror('Validation Error', 'Please fill in all fields')
            return
        
        if not validate_email(email):
            messagebox.showerror('Validation Error', 'Invalid email format')
            return
        
        # Attempt login
        result = self.auth_manager.sign_in_with_email(email, password)
        
        if result['success']:
            # Navigate directly to dashboard without showing success popup
            if self.on_login_success:
                self.on_login_success(result['user'])
        else:
            messagebox.showerror('Login Error', result['message'])
    
    def _on_register(self):
        """Handle register link click"""
        if self.on_register_click:
            self.on_register_click()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
