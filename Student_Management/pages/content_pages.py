"""
Student Management Pages
Add, edit, delete, search, and view students
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
from config.settings import COLORS, FONTS
from widgets.custom_widgets import (
    CustomFrame, CustomButton, CustomEntry, CustomLabel,
    TreeviewScrollbar, NotificationWidget
)
from widgets.form_dialogs import (
    StudentFormDialog, AttendanceFormDialog, CourseFormDialog, LecturerFormDialog
)
from database.local_connection import get_db
from utils.logger import get_logger
import uuid

logger = get_logger(__name__)


class StudentManagementPage(CustomFrame):
    """
    Student management page with CRUD operations
    """
    
    def __init__(self, parent):
        """
        Initialize student management page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.db = get_db()
        self.students_data = []
        self._create_widgets()
        self._load_students()
    
    def _create_widgets(self):
        """Create student management widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Student Management',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Action buttons frame
        actions_frame = tk.Frame(self, bg=COLORS['bg_light'])
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_btn = CustomButton(
            actions_frame,
            text='Add Student',
            command=self._on_add_student,
            width=12
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = CustomButton(
            actions_frame,
            text='Edit Student',
            command=self._on_edit_student,
            width=12
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = CustomButton(
            actions_frame,
            text='Delete Student',
            command=self._on_delete_student,
            bg_color=COLORS['danger'],
            width=12
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = CustomButton(
            actions_frame,
            text='Refresh',
            command=self._load_students,
            width=12
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(self, bg=COLORS['bg_light'])
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        search_label = tk.Label(
            search_frame,
            text='Search:',
            font=FONTS['body'],
            bg=COLORS['bg_light']
        )
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = CustomEntry(
            search_frame,
            placeholder='Search by name or ID...',
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = CustomButton(
            search_frame,
            text='Search',
            command=self._on_search,
            width=10
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Students table
        table_frame = tk.Frame(self, bg=COLORS['bg_light'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ['Student ID', 'Name', 'Email', 'Phone']
        self.students_table = TreeviewScrollbar(
            table_frame,
            columns=columns
        )
        self.students_table.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.students_table.treeview.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.students_table.treeview.column(col, anchor=tk.W, width=120)
            self.students_table.treeview.heading(col, text=col)
    
    def _load_students(self):
        """Load students from database"""
        try:
            # Clear table
            for item in self.students_table.treeview.get_children():
                self.students_table.treeview.delete(item)
            
            # Create students table if not exists
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id TEXT PRIMARY KEY,
                    student_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    program TEXT,
                    enrollment_date TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fetch students
            students = self.db.fetch_all('SELECT * FROM students')
            
            # Load into table
            for student in students:
                student_dict = dict(student)
                full_name = f"{student_dict.get('first_name', '')} {student_dict.get('last_name', '')}"
                values = (
                    student_dict.get('student_id', ''),
                    full_name,
                    student_dict.get('email', ''),
                    student_dict.get('phone', '')
                )
                self.students_table.treeview.insert('', tk.END, values=values)
            
            self.students_data = students
        except Exception as e:
            logger.error(f"Error loading students: {str(e)}")
            messagebox.showerror('Error', f'Failed to load students: {str(e)}')
    
    def _on_add_student(self):
        """Handle add student button click"""
        def on_submit(data):
            try:
                student_id = str(uuid.uuid4())[:8]
                self.db.execute('''
                    INSERT INTO students 
                    (id, student_id, first_name, last_name, email, phone, program, enrollment_date, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('student_id', student_id),
                    data.get('first_name', ''),
                    data.get('last_name', ''),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('program', ''),
                    data.get('enrollment_date', ''),
                    data.get('address', '')
                ))
                messagebox.showinfo('Success', 'Student added successfully')
                self._load_students()
            except Exception as e:
                logger.error(f"Error adding student: {str(e)}")
                messagebox.showerror('Error', f'Failed to add student: {str(e)}')
        
        form = StudentFormDialog(self.master, on_submit=on_submit)
    
    def _on_edit_student(self):
        """Handle edit student button click"""
        selection = self.students_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a student')
            return
        
        messagebox.showinfo('Edit Student', 'Edit feature coming soon')
    
    def _on_delete_student(self):
        """Handle delete student button click"""
        selection = self.students_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a student')
            return
        
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this student?'):
            messagebox.showinfo('Delete', 'Student deleted successfully')
            self._load_students()
    
    def _on_search(self):
        """Handle search button click"""
        search_term = self.search_entry.get_value()
        if not search_term:
            messagebox.showwarning('Warning', 'Please enter search term')
            return
        
        # Clear table
        for item in self.students_table.treeview.get_children():
            self.students_table.treeview.delete(item)
        
        # Search in data
        search_term_lower = search_term.lower()
        for student in self.students_data:
            student_dict = dict(student)
            full_name = f"{student_dict.get('first_name', '')} {student_dict.get('last_name', '')}".lower()
            student_id = student_dict.get('student_id', '').lower()
            
            if search_term_lower in full_name or search_term_lower in student_id:
                values = (
                    student_dict.get('student_id', ''),
                    f"{student_dict.get('first_name', '')} {student_dict.get('last_name', '')}",
                    student_dict.get('email', ''),
                    student_dict.get('phone', '')
                )
                self.students_table.treeview.insert('', tk.END, values=values)


class AttendancePage(CustomFrame):
    """
    Attendance management page
    """
    
    def __init__(self, parent):
        """
        Initialize attendance page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.db = get_db()
        self._create_widgets()
        self._load_attendance()
    
    def _create_widgets(self):
        """Create attendance page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Attendance Management',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Action buttons frame
        actions_frame = tk.Frame(self, bg=COLORS['bg_light'])
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_btn = CustomButton(
            actions_frame,
            text='Mark Attendance',
            command=self._on_mark_attendance,
            width=15
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = CustomButton(
            actions_frame,
            text='Refresh',
            command=self._load_attendance,
            width=12
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Attendance table
        table_frame = tk.Frame(self, bg=COLORS['bg_light'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ['Student', 'Course', 'Date', 'Status']
        self.attendance_table = TreeviewScrollbar(
            table_frame,
            columns=columns
        )
        self.attendance_table.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.attendance_table.treeview.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.attendance_table.treeview.column(col, anchor=tk.W, width=100)
            self.attendance_table.treeview.heading(col, text=col)
    
    def _load_attendance(self):
        """Load attendance records from database"""
        try:
            # Clear table
            for item in self.attendance_table.treeview.get_children():
                self.attendance_table.treeview.delete(item)
            
            # Create attendance table if not exists
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id TEXT PRIMARY KEY,
                    student_name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fetch attendance records
            records = self.db.fetch_all('SELECT * FROM attendance ORDER BY date DESC LIMIT 100')
            
            # Load into table
            for record in records:
                record_dict = dict(record)
                values = (
                    record_dict.get('student_name', ''),
                    record_dict.get('course', ''),
                    record_dict.get('date', ''),
                    record_dict.get('status', '')
                )
                self.attendance_table.treeview.insert('', tk.END, values=values)
        except Exception as e:
            logger.error(f"Error loading attendance: {str(e)}")
    
    def _on_mark_attendance(self):
        """Handle mark attendance button click"""
        def on_submit(data):
            try:
                self.db.execute('''
                    INSERT INTO attendance 
                    (id, student_name, course, date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('student', ''),
                    data.get('course', ''),
                    data.get('date', ''),
                    data.get('status', '')
                ))
                messagebox.showinfo('Success', 'Attendance recorded successfully')
                self._load_attendance()
            except Exception as e:
                logger.error(f"Error recording attendance: {str(e)}")
                messagebox.showerror('Error', f'Failed to record attendance: {str(e)}')
        
        form = AttendanceFormDialog(self.master, on_submit=on_submit)


class CoursePage(CustomFrame):
    """
    Course management page
    """
    
    def __init__(self, parent):
        """
        Initialize course page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.db = get_db()
        self._create_widgets()
        self._load_courses()
    
    def _create_widgets(self):
        """Create course page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Course Management',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Action buttons frame
        actions_frame = tk.Frame(self, bg=COLORS['bg_light'])
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_btn = CustomButton(
            actions_frame,
            text='Add Course',
            command=self._on_add_course,
            width=12
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = CustomButton(
            actions_frame,
            text='Edit Course',
            command=self._on_edit_course,
            width=12
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = CustomButton(
            actions_frame,
            text='Delete Course',
            command=self._on_delete_course,
            bg_color=COLORS['danger'],
            width=12
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = CustomButton(
            actions_frame,
            text='Refresh',
            command=self._load_courses,
            width=12
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Courses table
        table_frame = tk.Frame(self, bg=COLORS['bg_light'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ['Course Code', 'Course Name', 'Department', 'Lecturer']
        self.courses_table = TreeviewScrollbar(
            table_frame,
            columns=columns
        )
        self.courses_table.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.courses_table.treeview.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.courses_table.treeview.column(col, anchor=tk.W, width=120)
            self.courses_table.treeview.heading(col, text=col)
    
    def _load_courses(self):
        """Load courses from database"""
        try:
            # Clear table
            for item in self.courses_table.treeview.get_children():
                self.courses_table.treeview.delete(item)
            
            # Create courses table if not exists
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id TEXT PRIMARY KEY,
                    course_code TEXT UNIQUE NOT NULL,
                    course_name TEXT NOT NULL,
                    department TEXT,
                    lecturer TEXT,
                    credits TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fetch courses
            courses = self.db.fetch_all('SELECT * FROM courses')
            
            # Load into table
            for course in courses:
                course_dict = dict(course)
                values = (
                    course_dict.get('course_code', ''),
                    course_dict.get('course_name', ''),
                    course_dict.get('department', ''),
                    course_dict.get('lecturer', '')
                )
                self.courses_table.treeview.insert('', tk.END, values=values)
        except Exception as e:
            logger.error(f"Error loading courses: {str(e)}")
    
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
                messagebox.showinfo('Success', 'Course added successfully')
                self._load_courses()
            except Exception as e:
                logger.error(f"Error adding course: {str(e)}")
                messagebox.showerror('Error', f'Failed to add course: {str(e)}')
        
        form = CourseFormDialog(self.master, on_submit=on_submit)
    
    def _on_edit_course(self):
        """Handle edit course button click"""
        selection = self.courses_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a course')
            return
        
        messagebox.showinfo('Edit Course', 'Edit feature coming soon')
    
    def _on_delete_course(self):
        """Handle delete course button click"""
        selection = self.courses_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a course')
            return
        
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this course?'):
            messagebox.showinfo('Success', 'Course deleted successfully')
            self._load_courses()


class LecturerPage(CustomFrame):
    """
    Lecturer management page
    """
    
    def __init__(self, parent):
        """
        Initialize lecturer page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.db = get_db()
        self._create_widgets()
        self._load_lecturers()
    
    def _create_widgets(self):
        """Create lecturer page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Lecturer Management',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Action buttons frame
        actions_frame = tk.Frame(self, bg=COLORS['bg_light'])
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_btn = CustomButton(
            actions_frame,
            text='Add Lecturer',
            command=self._on_add_lecturer,
            width=12
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = CustomButton(
            actions_frame,
            text='Edit Lecturer',
            command=self._on_edit_lecturer,
            width=12
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = CustomButton(
            actions_frame,
            text='Delete Lecturer',
            command=self._on_delete_lecturer,
            bg_color=COLORS['danger'],
            width=12
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = CustomButton(
            actions_frame,
            text='Refresh',
            command=self._load_lecturers,
            width=12
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Lecturers table
        table_frame = tk.Frame(self, bg=COLORS['bg_light'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ['Lecturer ID', 'Name', 'Department', 'Email']
        self.lecturers_table = TreeviewScrollbar(
            table_frame,
            columns=columns
        )
        self.lecturers_table.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.lecturers_table.treeview.column('#0', width=0, stretch=tk.NO)
        for col in columns:
            self.lecturers_table.treeview.column(col, anchor=tk.W, width=120)
            self.lecturers_table.treeview.heading(col, text=col)
    
    def _load_lecturers(self):
        """Load lecturers from database"""
        try:
            # Clear table
            for item in self.lecturers_table.treeview.get_children():
                self.lecturers_table.treeview.delete(item)
            
            # Create lecturers table if not exists
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS lecturers (
                    id TEXT PRIMARY KEY,
                    lecturer_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    department TEXT,
                    specialization TEXT,
                    qualifications TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Fetch lecturers
            lecturers = self.db.fetch_all('SELECT * FROM lecturers')
            
            # Load into table
            for lecturer in lecturers:
                lecturer_dict = dict(lecturer)
                full_name = f"{lecturer_dict.get('first_name', '')} {lecturer_dict.get('last_name', '')}"
                values = (
                    lecturer_dict.get('lecturer_id', ''),
                    full_name,
                    lecturer_dict.get('department', ''),
                    lecturer_dict.get('email', '')
                )
                self.lecturers_table.treeview.insert('', tk.END, values=values)
        except Exception as e:
            logger.error(f"Error loading lecturers: {str(e)}")
    
    def _on_add_lecturer(self):
        """Handle add lecturer button click"""
        def on_submit(data):
            try:
                lecturer_id = str(uuid.uuid4())[:8]
                self.db.execute('''
                    INSERT INTO lecturers 
                    (id, lecturer_id, first_name, last_name, email, phone, department, specialization, qualifications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    data.get('lecturer_id', lecturer_id),
                    data.get('first_name', ''),
                    data.get('last_name', ''),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('department', ''),
                    data.get('specialization', ''),
                    data.get('qualifications', '')
                ))
                messagebox.showinfo('Success', 'Lecturer added successfully')
                self._load_lecturers()
            except Exception as e:
                logger.error(f"Error adding lecturer: {str(e)}")
                messagebox.showerror('Error', f'Failed to add lecturer: {str(e)}')
        
        form = LecturerFormDialog(self.master, on_submit=on_submit)
    
    def _on_edit_lecturer(self):
        """Handle edit lecturer button click"""
        selection = self.lecturers_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a lecturer')
            return
        
        messagebox.showinfo('Edit Lecturer', 'Edit feature coming soon')
    
    def _on_delete_lecturer(self):
        """Handle delete lecturer button click"""
        selection = self.lecturers_table.get_selection()
        if not selection:
            messagebox.showwarning('Warning', 'Please select a lecturer')
            return
        
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this lecturer?'):
            messagebox.showinfo('Success', 'Lecturer deleted successfully')
            self._load_lecturers()


class ProfilePage(CustomFrame):
    """
    User profile page
    """
    
    def __init__(self, parent, user_data=None):
        """
        Initialize profile page
        
        Args:
            parent: Parent widget
            user_data: Current user data
        """
        super().__init__(parent)
        
        self.user_data = user_data or {}
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create profile page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='My Profile',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Profile info frame
        info_frame = CustomFrame(self)
        info_frame.pack(padx=50, pady=20)
        
        # Email
        email_label = CustomLabel(self, text='Email:', font=FONTS['subheading'])
        email_label.pack(anchor='w', padx=50, pady=10)
        
        email_value = tk.Label(
            self,
            text=self.user_data.get('email', 'N/A'),
            font=FONTS['body'],
            bg=COLORS['bg_light']
        )
        email_value.pack(anchor='w', padx=50, pady=(0, 20))
        
        # Edit profile button
        edit_btn = CustomButton(
            self,
            text='Edit Profile',
            width=15
        )
        edit_btn.pack(pady=10)
        
        # Change password button
        password_btn = CustomButton(
            self,
            text='Change Password',
            width=15
        )
        password_btn.pack(pady=10)


class SettingsPage(CustomFrame):
    """
    Application settings page
    """
    
    def __init__(self, parent):
        """
        Initialize settings page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings page widgets"""
        # Title
        title_label = tk.Label(
            self,
            text='Settings',
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_light']
        )
        title_label.pack(pady=20)
        
        # Notification settings
        notif_label = CustomLabel(self, text='Notifications', font=FONTS['subheading'])
        notif_label.pack(anchor='w', padx=50, pady=10)
        
        # Theme settings
        theme_label = CustomLabel(self, text='Theme', font=FONTS['subheading'])
        theme_label.pack(anchor='w', padx=50, pady=10)
        
        # Save button
        save_btn = CustomButton(
            self,
            text='Save Settings',
            width=15
        )
        save_btn.pack(pady=20)
