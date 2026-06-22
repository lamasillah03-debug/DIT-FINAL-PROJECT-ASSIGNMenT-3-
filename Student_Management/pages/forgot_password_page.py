"""
Forgot Password Page
Password reset request page
"""
import tkinter as tk
from tkinter import messagebox
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomButton, CustomEntry, CustomLabel, CustomFrame
from auth.auth_manager import get_auth_manager
from utils.validators import validate_email


class ForgotPasswordPage(CustomFrame):
    """
    Forgot password page
    Allows users to request password reset
    """
    
    def __init__(self, parent, on_reset_sent=None, on_back_click=None):
        """
        Initialize forgot password page
        
        Args:
            parent: Parent widget
            on_reset_sent: Callback when reset email is sent
            on_back_click: Callback when back button is clicked
        """
        super().__init__(parent)
        
        self.on_reset_sent = on_reset_sent
        self.on_back_click = on_back_click
        self.auth_manager = get_auth_manager()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create forgot password page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Reset Your Password',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=30)
        
        # Message
        message = tk.Label(
            self,
            text='Enter your email address and we\'ll send you a link to reset your password',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg=COLORS['bg_light'],
            justify=tk.CENTER,
            wraplength=400
        )
        message.pack(pady=(0, 30))
        
        # Email label
        email_label = CustomLabel(self, text='Email Address', font=FONTS['body'])
        email_label.pack(anchor='w', padx=50, pady=(20, 5))
        
        # Email entry
        self.email_entry = CustomEntry(
            self,
            placeholder='Enter your email',
            width=40
        )
        self.email_entry.pack(padx=50, pady=(0, 20), fill=tk.X)
        
        # Reset button
        reset_btn = CustomButton(
            self,
            text='Send Reset Link',
            command=self._on_reset,
            width=20
        )
        reset_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Label(
            self,
            text='Back to Login',
            font=FONTS['small'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light'],
            cursor='hand2'
        )
        back_btn.pack(pady=20)
        back_btn.bind('<Button-1>', lambda e: self._on_back())
    
    def _on_reset(self):
        """Handle reset button click"""
        email = self.email_entry.get_value()
        
        if not email:
            messagebox.showerror('Error', 'Please enter your email address')
            return
        
        if not validate_email(email):
            messagebox.showerror('Error', 'Invalid email format')
            return
        
        # Send reset email
        result = self.auth_manager.reset_password(email)
        
        if result['success']:
            messagebox.showinfo('Success', result['message'])
            if self.on_reset_sent:
                self.on_reset_sent(email)
        else:
            messagebox.showerror('Error', result['message'])
    
    def _on_back(self):
        """Handle back button click"""
        if self.on_back_click:
            self.on_back_click()
    
    def clear_fields(self):
        """Clear email field"""
        self.email_entry.delete(0, tk.END)
