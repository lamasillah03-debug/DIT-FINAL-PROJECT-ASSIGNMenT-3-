"""
OTP Verification Page
Email OTP verification for authentication
"""
import tkinter as tk
from tkinter import messagebox
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomButton, CustomEntry, CustomLabel, CustomFrame
from auth.auth_manager import get_auth_manager


class OTPVerificationPage(CustomFrame):
    """
    OTP verification page
    Verifies user email using one-time password
    """
    
    def __init__(self, parent, email='', on_verification_success=None,
                 on_resend_otp=None, on_back_click=None):
        """
        Initialize OTP verification page
        
        Args:
            parent: Parent widget
            email (str): User email address
            on_verification_success: Callback on successful verification
            on_resend_otp: Callback when resend OTP is clicked
            on_back_click: Callback when back button is clicked
        """
        super().__init__(parent)
        
        self.email = email
        self.on_verification_success = on_verification_success
        self.on_resend_otp = on_resend_otp
        self.on_back_click = on_back_click
        self.auth_manager = get_auth_manager()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create OTP verification page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Verify Your Email',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=30)
        
        # Message
        message = tk.Label(
            self,
            text=f'We sent a verification code to:\n{self.email}',
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg=COLORS['bg_light'],
            justify=tk.CENTER
        )
        message.pack(pady=(0, 30))
        
        # OTP label
        otp_label = CustomLabel(self, text='Enter Verification Code', font=FONTS['body'])
        otp_label.pack(anchor='w', padx=50, pady=(20, 5))
        
        # OTP entry
        self.otp_entry = CustomEntry(
            self,
            placeholder='000000',
            width=40
        )
        self.otp_entry.pack(padx=50, pady=(0, 20), fill=tk.X)
        
        # Verify button
        verify_btn = CustomButton(
            self,
            text='Verify Code',
            command=self._on_verify,
            width=20
        )
        verify_btn.pack(pady=10)
        
        # Resend and back buttons frame
        button_frame = tk.Frame(self, bg=COLORS['bg_light'])
        button_frame.pack(pady=20)
        
        resend_btn = tk.Label(
            button_frame,
            text='Resend Code',
            font=FONTS['small'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light'],
            cursor='hand2'
        )
        resend_btn.pack(side=tk.LEFT, padx=20)
        resend_btn.bind('<Button-1>', lambda e: self._on_resend())
        
        back_btn = tk.Label(
            button_frame,
            text='Back to Login',
            font=FONTS['small'],
            fg=COLORS['secondary'],
            bg=COLORS['bg_light'],
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=20)
        back_btn.bind('<Button-1>', lambda e: self._on_back())
    
    def _on_verify(self):
        """Handle verify button click"""
        otp = self.otp_entry.get_value()
        
        if not otp:
            messagebox.showerror('Error', 'Please enter the verification code')
            return
        
        # Verify OTP
        result = self.auth_manager.verify_otp(self.email, otp)
        
        if result['success']:
            messagebox.showinfo('Success', 'Email verified successfully')
            if self.on_verification_success:
                self.on_verification_success(result['user'])
        else:
            messagebox.showerror('Verification Error', result['message'])
    
    def _on_resend(self):
        """Handle resend OTP"""
        result = self.auth_manager.send_otp(self.email)
        if result['success']:
            messagebox.showinfo('Success', result['message'])
        else:
            messagebox.showerror('Error', result['message'])
    
    def _on_back(self):
        """Handle back button click"""
        if self.on_back_click:
            self.on_back_click()
    
    def set_email(self, email):
        """Set email address to verify"""
        self.email = email
    
    def clear_fields(self):
        """Clear OTP field"""
        self.otp_entry.delete(0, tk.END)
