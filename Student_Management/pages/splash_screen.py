"""
Splash Screen Page
Displays loading screen on application startup
"""
import tkinter as tk
from tkinter import ttk
from config.settings import COLORS, FONTS, WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME, APP_VERSION
from widgets.custom_widgets import LoadingSpinner


class SplashScreen(tk.Toplevel):
    """
    Splash screen displayed during application startup
    Shows app logo, name, version, and loading animation
    """
    
    def __init__(self, parent):
        """
        Initialize splash screen
        
        Args:
            parent: Parent window (root)
        """
        super().__init__(parent)
        
        # Configure window
        self.configure(bg=COLORS['bg_dark'])
        self.attributes('-topmost', True)
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Calculate window position (center of screen)
        width, height = 500, 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create splash screen widgets"""
        # Main container
        main_frame = tk.Frame(
            self,
            bg=COLORS['primary'],
            width=500,
            height=400
        )
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App name
        name_label = tk.Label(
            main_frame,
            text=APP_NAME,
            font=FONTS['title'],
            fg=COLORS['text_light'],
            bg=COLORS['primary']
        )
        name_label.pack(pady=(80, 10))
        
        # App version
        version_label = tk.Label(
            main_frame,
            text=f'Version {APP_VERSION}',
            font=FONTS['body'],
            fg=COLORS['border'],
            bg=COLORS['primary']
        )
        version_label.pack()
        
        # Loading spinner
        spinner = LoadingSpinner(main_frame, bg=COLORS['primary'])
        spinner.pack(pady=40)
        spinner.start()
        
        # Status text
        self.status_label = tk.Label(
            main_frame,
            text='Initializing application...',
            font=FONTS['small'],
            fg=COLORS['border'],
            bg=COLORS['primary']
        )
        self.status_label.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=10)
        self.progress.start()
    
    def update_status(self, message):
        """
        Update status message
        
        Args:
            message (str): Status message to display
        """
        self.status_label.config(text=message)
        self.update()
