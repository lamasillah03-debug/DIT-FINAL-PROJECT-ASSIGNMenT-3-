"""
Registration Page - Simple Card-based Design
Simple registration form for new users
"""
import tkinter as tk
from tkinter import messagebox
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomButton, CustomEntry, CustomLabel, CustomFrame, PasswordEntry
from auth.auth_manager import get_auth_manager
from utils.validators import validate_email, validate_name


class RegistrationPage(CustomFrame):
    """
    Simple registration page with card-based form design
    Allows users to create new account with email and password
    """
    
    def __init__(self, parent, on_registration_success=None, on_login_click=None):
        """
        Initialize registration page
        
        Args:
            parent: Parent widget
            on_registration_success: Callback on successful registration
            on_login_click: Callback when login link is clicked
        """
        super().__init__(parent)
        
        self.on_registration_success = on_registration_success
        self.on_login_click = on_login_click
        self.auth_manager = get_auth_manager()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create registration page widgets with card design"""
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
            text='Create Account',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg='#FFFFFF'
        )
        title_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle = tk.Label(
            card_frame,
            text='Join Our Student Management Platform',
            font=FONTS['body'],
            fg='#666666',
            bg='#FFFFFF'
        )
        subtitle.pack(pady=(0, 30))
        
        # Full name
        name_label = tk.Label(
            card_frame,
            text='Full Name',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        name_label.pack(anchor='w', padx=40, pady=(0, 5))
        
        self.name_entry = CustomEntry(
            card_frame,
            placeholder='Enter your full name',
            width=35
        )
        self.name_entry.pack(padx=40, pady=(0, 15), fill=tk.X)
        
        # Email
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
        
        # Password
        password_label = tk.Label(
            card_frame,
            text='Password',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        password_label.pack(anchor='w', padx=40, pady=(0, 5))
        
        password_container = tk.Frame(card_frame, bg='#FFFFFF')
        password_container.pack(padx=40, pady=(0, 15), fill=tk.X)
        
        self.password_entry = PasswordEntry(
            password_container,
            placeholder='At least 6 characters'
        )
        self.password_entry.pack(fill=tk.X)
        
        # Register button
        register_btn = CustomButton(
            card_frame,
            text='Create Account',
            command=self._on_register,
            width=25,
            bg_color=COLORS['primary'],
            fg_color='#FFFFFF'
        )
        register_btn.pack(pady=20)
        
        # Login link
        login_frame = tk.Frame(card_frame, bg='#FFFFFF')
        login_frame.pack(pady=(0, 30))
        
        login_text = tk.Label(
            login_frame,
            text='Already have an account? ',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg='#FFFFFF'
        )
        login_text.pack(side=tk.LEFT)
        
        login_link = tk.Label(
            login_frame,
            text='Sign In',
            font=FONTS['body'],
            fg=COLORS['primary'],
            bg='#FFFFFF',
            cursor='hand2'
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind('<Button-1>', lambda e: self._on_login())
    
    def _on_register(self):
        """Handle registration button click"""
        full_name = self.name_entry.get_value()
        email = self.email_entry.get_value()
        password = self.password_entry.get_value()
        
        # Validation
        if not all([full_name, email, password]):
            messagebox.showerror('Validation Error', 'Please fill in all fields')
            return
        
        if not validate_name(full_name):
            messagebox.showerror('Validation Error', 'Name must be at least 2 characters')
            return
        
        if not validate_email(email):
            messagebox.showerror('Validation Error', 'Invalid email format')
            return
        
        if len(password) < 6:
            messagebox.showerror('Validation Error', 'Password must be at least 6 characters')
            return
        
        # Extract first and last name from full name
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Attempt registration
        result = self.auth_manager.sign_up_with_email(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        if result['success']:
            # Navigate directly to dashboard without showing success popup
            if self.on_registration_success:
                self.on_registration_success(result['user'])
        else:
            messagebox.showerror('Registration Error', result['message'])
    
    def _on_login(self):
        """Handle login link click"""
        if self.on_login_click:
            self.on_login_click()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
