"""
Dashboard Page
Main dashboard showing statistics and quick access
"""
import tkinter as tk
from tkinter import messagebox
import uuid
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomFrame, CustomLabel, CustomButton
from widgets.form_dialogs import (
    StudentFormDialog, CourseFormDialog, LecturerFormDialog, AttendanceFormDialog
)
from database.local_connection import get_db
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage(CustomFrame):
    """
    Dashboard page displaying system statistics and quick access
    """
    
    def __init__(self, parent, user_data=None, on_logout=None, on_nav_click=None):
        """
        Initialize dashboard page
        
        Args:
            parent: Parent widget
            user_data: Current user data
            on_logout: Callback for logout
            on_nav_click: Callback for navigation
        """
        super().__init__(parent)
        
        self.user_data = user_data or {}
        self.on_logout = on_logout
        self.on_nav_click = on_nav_click
        self.db = get_db()
        self.parent_widget = parent
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dashboard widgets"""
        # Header - adjusted hero section
        header_frame = tk.Frame(self, bg=COLORS['primary'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)  # Lock height
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.user_data.get('email', 'User')}",
            font=FONTS['heading'],
            fg=COLORS['text_light'],
            bg=COLORS['primary']
        )
        welcome_label.pack(pady=10)  # Reduced from 20
        
        # Main content area
        content_frame = CustomFrame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Statistics cards container
        stats_frame = tk.Frame(content_frame, bg=COLORS['bg_light'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stat cards
        stats = [
            {'title': 'Total Students', 'value': '0', 'color': COLORS['primary']},
            {'title': 'Active Courses', 'value': '0', 'color': COLORS['success']},
            {'title': 'Lecturers', 'value': '0', 'color': COLORS['info']},
            {'title': 'Attendance Rate', 'value': '0%', 'color': COLORS['warning']},
        ]
        
        for stat in stats:
            self._create_stat_card(stats_frame, stat)
        
        # Quick actions
        actions_label = tk.Label(
            content_frame,
            text='Quick Actions',
            font=FONTS['subheading'],
            fg=COLORS['text_dark'],
            bg=COLORS['bg_light']
        )
        actions_label.pack(anchor='w', pady=(15, 10))
        
        actions_frame = tk.Frame(content_frame, bg=COLORS['bg_light'])
        actions_frame.pack(fill=tk.X)
        
        # Actions with command callbacks
        actions = [
            {'text': 'Add Student', 'command': self._on_add_student},
            {'text': 'Mark Attendance', 'command': self._on_mark_attendance},
            {'text': 'Add Course', 'command': self._on_add_course},
            {'text': 'Add Lecturer', 'command': self._on_add_lecturer},
        ]
        
        for action in actions:
            btn = CustomButton(
                actions_frame,
                text=action['text'],
                command=action['command'],
                width=18
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def _create_stat_card(self, parent, stat):
        """
        Create a statistics card
        
        Args:
            parent: Parent widget
            stat: Dictionary with title, value, color
        """
        card = tk.Frame(parent, bg=stat['color'], padx=20, pady=15)
        card.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            card,
            text=stat['title'],
            font=FONTS['small'],
            fg=COLORS['text_light'],
            bg=stat['color']
        )
        title_label.pack()
        
        value_label = tk.Label(
            card,
            text=stat['value'],
            font=FONTS['heading'],
            fg=COLORS['text_light'],
            bg=stat['color']
        )
        value_label.pack()
    
    def _on_add_student(self):
        """Handle add student button click"""
        def on_submit(data):
            try:
                student_id = data.get('student_id')
                if not student_id:
                    student_id = str(uuid.uuid4())[:8]
                
                self.db.execute('''
                    INSERT INTO students 
                    (id, student_id, first_name, last_name, email, phone, program, enrollment_date, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    student_id,
                    data.get('first_name', ''),
                    data.get('last_name', ''),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('program', ''),
                    data.get('enrollment_date', ''),
                    data.get('address', '')
                ))
                messagebox.showinfo('Success', 'Student added successfully!')
            except Exception as e:
                logger.error(f"Error adding student: {str(e)}")
                messagebox.showerror('Error', f'Failed to add student: {str(e)}')
        
        StudentFormDialog(self.parent_widget, on_submit=on_submit)
    
    def _on_add_course(self):
        """Handle add course button click"""
        def on_submit(data):
            try:
                self.db.execute('''
                    INSERT INTO courses 
                    (id, course_code, course_name, department, lecturer, credits, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('course_code', ''),
                    data.get('course_name', ''),
                    data.get('department', ''),
                    data.get('lecturer', ''),
                    data.get('credits', ''),
                    data.get('description', '')
                ))
                messagebox.showinfo('Success', 'Course added successfully!')
            except Exception as e:
                logger.error(f"Error adding course: {str(e)}")
                messagebox.showerror('Error', f'Failed to add course: {str(e)}')
        
        CourseFormDialog(self.parent_widget, on_submit=on_submit)
    
    def _on_add_lecturer(self):
        """Handle add lecturer button click"""
        def on_submit(data):
            try:
                self.db.execute('''
                    INSERT INTO lecturers 
                    (id, first_name, last_name, email, phone, department, specialization, qualifications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('first_name', ''),
                    data.get('last_name', ''),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('department', ''),
                    data.get('specialization', ''),
                    data.get('qualifications', '')
                ))
                messagebox.showinfo('Success', 'Lecturer added successfully!')
            except Exception as e:
                logger.error(f"Error adding lecturer: {str(e)}")
                messagebox.showerror('Error', f'Failed to add lecturer: {str(e)}')
        
        LecturerFormDialog(self.parent_widget, on_submit=on_submit)
    
    def _on_mark_attendance(self):
        """Handle mark attendance button click"""
        def on_submit(data):
            try:
                self.db.execute('''
                    INSERT INTO attendance 
                    (id, student, course, date, status, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('student', ''),
                    data.get('course', ''),
                    data.get('date', ''),
                    data.get('status', ''),
                    data.get('remarks', '')
                ))
                messagebox.showinfo('Success', 'Attendance marked successfully!')
            except Exception as e:
                logger.error(f"Error marking attendance: {str(e)}")
                messagebox.showerror('Error', f'Failed to mark attendance: {str(e)}')
        
        AttendanceFormDialog(self.parent_widget, on_submit=on_submit)


class SidebarNavigation(tk.Frame):
    """
    Sidebar navigation menu
    """
    
    def __init__(self, parent, on_nav_click=None, on_logout=None):
        """
        Initialize sidebar navigation
        
        Args:
            parent: Parent widget
            on_nav_click: Callback when menu item is clicked
            on_logout: Callback for logout
        """
        super().__init__(parent, bg=COLORS['bg_dark'], width=250)
        self.pack(side=tk.LEFT, fill=tk.Y)
        
        self.on_nav_click = on_nav_click
        self.on_logout = on_logout
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create sidebar widgets"""
        # Logo area
        logo_frame = tk.Frame(self, bg=COLORS['primary'], height=80)
        logo_frame.pack(fill=tk.X)
        
        logo_label = tk.Label(
            logo_frame,
            text='SMS',
            font=FONTS['title'],
            fg=COLORS['text_light'],
            bg=COLORS['primary']
        )
        logo_label.pack(pady=20)
        
        # Menu items
        menu_items = [
            ('Dashboard', 'dashboard'),
            ('Students', 'students'),
            ('Attendance', 'attendance'),
            ('Courses', 'courses'),
            ('Lecturers', 'lecturers'),
            ('Profile', 'profile'),
            ('Settings', 'settings'),
        ]
        
        for item_name, item_id in menu_items:
            self._create_menu_item(item_name, item_id)
        
        # Logout button at bottom
        logout_btn = CustomButton(
            self,
            text='Logout',
            command=self.on_logout,
            bg_color=COLORS['danger'],
            width=20
        )
        logout_btn.pack(pady=20)
    
    def _create_menu_item(self, name, item_id):
        """
        Create a menu item button
        
        Args:
            name (str): Display name
            item_id (str): Menu item ID
        """
        btn = tk.Button(
            self,
            text=name,
            font=FONTS['body'],
            bg=COLORS['bg_dark'],
            fg=COLORS['text_light'],
            border=0,
            padx=20,
            pady=15,
            anchor='w',
            activebackground=COLORS['primary'],
            activeforeground=COLORS['text_light'],
            command=lambda: self._on_item_click(item_id)
        )
        btn.pack(fill=tk.X)
    
    def _on_item_click(self, item_id):
        """Handle menu item click"""
        if self.on_nav_click:
            self.on_nav_click(item_id)
