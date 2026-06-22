"""
Custom Tkinter widgets and components for professional UI
"""
import tkinter as tk
from tkinter import ttk
from config.settings import COLORS, FONTS


class CustomButton(tk.Button):
    """
    Custom button widget with modern styling
    """
    def __init__(self, parent, text='', command=None, bg_color=COLORS['primary'],
                 fg_color=COLORS['text_light'], width=15, **kwargs):
        """
        Initialize custom button
        
        Args:
            parent: Parent widget
            text (str): Button text
            command: Command to execute on click
            bg_color (str): Background color
            fg_color (str): Text color
            width (int): Button width
        """
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=FONTS['body'],
            width=width,
            relief=tk.FLAT,
            cursor='hand2',
            activebackground=COLORS['hover'],
            activeforeground=fg_color,
            **kwargs
        )
        
        # Bind hover effects
        self.bind('<Enter>', lambda e: self._on_enter())
        self.bind('<Leave>', lambda e: self._on_leave())
        self.original_bg = bg_color
        self.hover_bg = COLORS['hover']
    
    def _on_enter(self):
        """Handle mouse enter"""
        self.config(bg=self.hover_bg)
    
    def _on_leave(self):
        """Handle mouse leave"""
        self.config(bg=self.original_bg)


class CustomEntry(tk.Entry):
    """
    Custom entry widget with placeholder support
    """
    def __init__(self, parent, placeholder='', **kwargs):
        """
        Initialize custom entry
        
        Args:
            parent: Parent widget
            placeholder (str): Placeholder text
        """
        super().__init__(
            parent,
            font=FONTS['body'],
            relief=tk.FLAT,
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_text = placeholder
        self.default_fg = COLORS['text_dark']
        self.placeholder_fg = '#AAAAAA'
        
        # Bind focus events
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        
        # Show placeholder on init
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=self.placeholder_fg)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.get() == self.placeholder_text:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg)
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if self.get() == '':
            self.insert(0, self.placeholder_text)
            self.config(fg=self.placeholder_fg)
    
    def get_value(self):
        """Get entry value, excluding placeholder"""
        value = self.get()
        if value == self.placeholder_text:
            return ''
        return value


class PasswordEntry(tk.Frame):
    """
    Custom password entry with visibility toggle eye icon
    """
    def __init__(self, parent, placeholder='', **kwargs):
        """
        Initialize password entry with eye icon
        
        Args:
            parent: Parent widget
            placeholder (str): Placeholder text
        """
        super().__init__(parent, bg=COLORS['bg_light'], **kwargs)
        
        self.placeholder = placeholder
        self.is_visible = False
        
        # Create frame for entry and icon
        entry_frame = tk.Frame(self, bg=COLORS['bg_light'])
        entry_frame.pack(fill=tk.X, expand=True)
        
        # Create password entry
        self.entry = tk.Entry(
            entry_frame,
            font=FONTS['body'],
            relief=tk.FLAT,
            bg='#FFFFFF',
            fg=COLORS['text_dark'],
            show='•',
            border=1,
            width=35
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Bind focus events for placeholder
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
        # Show placeholder on init
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg='#AAAAAA')
        
        # Create eye button for visibility toggle
        self.eye_button = tk.Label(
            entry_frame,
            text='👁',
            font=('Arial', 14),
            fg=COLORS['primary'],
            bg=COLORS['bg_light'],
            cursor='hand2'
        )
        self.eye_button.pack(side=tk.LEFT, padx=5)
        self.eye_button.bind('<Button-1>', self._toggle_visibility)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=COLORS['text_dark'])
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        if self.entry.get() == '':
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='#AAAAAA')
    
    def _toggle_visibility(self, event):
        """Toggle password visibility"""
        self.is_visible = not self.is_visible
        
        if self.is_visible:
            self.entry.config(show='')
            self.eye_button.config(text='👁‍🗨', fg=COLORS['success'])
        else:
            self.entry.config(show='•')
            self.eye_button.config(text='👁', fg=COLORS['primary'])
    
    def get(self):
        """Get password value"""
        return self.entry.get()
    
    def get_value(self):
        """Get password value, excluding placeholder"""
        value = self.entry.get()
        if value == self.placeholder:
            return ''
        return value
    
    def delete(self, start, end):
        """Delete characters from entry"""
        self.entry.delete(start, end)
    
    def insert(self, index, string):
        """Insert string into entry"""
        self.entry.insert(index, string)


class CustomLabel(tk.Label):
    """
    Custom label widget with consistent styling
    """
    def __init__(self, parent, text='', font=FONTS['body'], 
                 fg=COLORS['text_dark'], **kwargs):
        """
        Initialize custom label
        
        Args:
            parent: Parent widget
            text (str): Label text
            font: Font tuple
            fg (str): Text color
        """
        super().__init__(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=COLORS['bg_light'],
            **kwargs
        )


class CustomFrame(tk.Frame):
    """
    Custom frame with consistent background
    """
    def __init__(self, parent, **kwargs):
        """
        Initialize custom frame
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent, bg=COLORS['bg_light'], **kwargs)


class CustomLabelFrame(ttk.LabelFrame):
    """
    Custom label frame with modern styling
    """
    def __init__(self, parent, text='', **kwargs):
        """
        Initialize custom label frame
        
        Args:
            parent: Parent widget
            text (str): Frame title
        """
        # Configure style for label frame
        style = ttk.Style()
        style.configure('TLabelframe', background=COLORS['bg_light'],
                       foreground=COLORS['text_dark'])
        style.configure('TLabelframe.Label', background=COLORS['bg_light'],
                       foreground=COLORS['text_dark'], font=FONTS['subheading'])
        
        super().__init__(parent, text=text, **kwargs)


class NotificationWidget(tk.Toplevel):
    """
    Notification/Toast widget for messages
    """
    def __init__(self, parent, message='', type='info', duration=3000):
        """
        Initialize notification widget
        
        Args:
            parent: Parent widget
            message (str): Notification message
            type (str): Type - 'success', 'error', 'warning', 'info'
            duration (int): Duration in milliseconds
        """
        super().__init__(parent)
        
        # Set window properties
        self.withdraw()
        self.attributes('-topmost', True)
        self.attributes('-transparentcolor', COLORS['bg_light'])
        
        # Determine colors based on type
        colors = {
            'success': {'bg': COLORS['success'], 'fg': COLORS['text_light']},
            'error': {'bg': COLORS['danger'], 'fg': COLORS['text_light']},
            'warning': {'bg': COLORS['warning'], 'fg': COLORS['text_dark']},
            'info': {'bg': COLORS['info'], 'fg': COLORS['text_light']},
        }
        
        notification_colors = colors.get(type, colors['info'])
        
        # Create notification frame
        frame = tk.Frame(
            self,
            bg=notification_colors['bg'],
            padx=20,
            pady=10
        )
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add message label
        label = tk.Label(
            frame,
            text=message,
            font=FONTS['body'],
            bg=notification_colors['bg'],
            fg=notification_colors['fg'],
            wraplength=400
        )
        label.pack()
        
        # Position at bottom right
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_x() + parent.winfo_width() - width - 20
        y = parent.winfo_y() + parent.winfo_height() - height - 20
        
        self.geometry(f'+{x}+{y}')
        self.deiconify()
        
        # Auto-close after duration
        self.after(duration, self.destroy)


class LoadingSpinner(tk.Frame):
    """
    Loading spinner animation
    """
    def __init__(self, parent, **kwargs):
        """
        Initialize loading spinner
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent, **kwargs)
        
        self.spinning = False
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_char = 0
        
        # Create label for spinner
        self.label = tk.Label(
            self,
            text=self.spinner_chars[0],
            font=('Arial', 16),
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        self.label.pack()
    
    def start(self):
        """Start spinning animation"""
        self.spinning = True
        self._animate()
    
    def stop(self):
        """Stop spinning animation"""
        self.spinning = False
    
    def _animate(self):
        """Animate spinner"""
        if self.spinning:
            self.label.config(text=self.spinner_chars[self.current_char])
            self.current_char = (self.current_char + 1) % len(self.spinner_chars)
            self.after(100, self._animate)


class TreeviewScrollbar(tk.Frame):
    """
    Treeview with integrated scrollbar
    """
    def __init__(self, parent, columns=None, **kwargs):
        """
        Initialize treeview with scrollbar
        
        Args:
            parent: Parent widget
            columns: List of column names
        """
        super().__init__(parent, bg=COLORS['bg_light'], **kwargs)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.treeview = ttk.Treeview(
            self,
            columns=columns if columns else [],
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        # Configure scrollbar
        scrollbar.config(command=self.treeview.yview)
        
        # Pack treeview
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure style
        style = ttk.Style()
        style.configure('Treeview', rowheight=25, font=FONTS['small'])
        style.configure('Treeview.Heading', font=FONTS['subheading'])
        style.map('Treeview', background=[('selected', COLORS['primary'])])
    
    def insert_row(self, values):
        """
        Insert a row into treeview
        
        Args:
            values: List of values for columns
        """
        return self.treeview.insert('', tk.END, values=values)
    
    def delete_row(self, item):
        """Delete a row from treeview"""
        self.treeview.delete(item)
    
    def get_selection(self):
        """Get selected row"""
        return self.treeview.selection()
    
    def clear(self):
        """Clear all rows"""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
