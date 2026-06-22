"""
Form Dialogs for Data Entry
Provides reusable form dialogs for adding and editing records
"""
import tkinter as tk
from tkinter import messagebox
from config.settings import COLORS, FONTS
from widgets.custom_widgets import CustomButton, CustomEntry, CustomFrame, PasswordEntry


class FormDialog(tk.Toplevel):
    """Base class for form dialogs"""
    
    def __init__(self, parent, title='Form', fields=None, on_submit=None):
        """
        Initialize form dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            fields: List of field definitions
            on_submit: Callback when form is submitted
        """
        super().__init__(parent)
        self.title(title)
        self.geometry('500x600')
        self.resizable(False, False)
        self.configure(bg=COLORS['bg_light'])
        
        # Center window
        self.transient(parent)
        self.grab_set()
        
        self.fields = fields or []
        self.on_submit = on_submit
        self.result = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create form widgets"""
        # Main frame
        main_frame = CustomFrame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scroll frame for fields
        canvas = tk.Canvas(main_frame, bg=COLORS['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store entry widgets
        self.entry_widgets = {}
        
        # Create input fields
        for field in self.fields:
            self._create_field(scrollable_frame, field)
        
        # Buttons frame
        buttons_frame = tk.Frame(self, bg=COLORS['bg_light'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        submit_btn = CustomButton(
            buttons_frame,
            text='Save',
            command=self._on_submit,
            width=12,
            bg_color=COLORS['primary']
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = CustomButton(
            buttons_frame,
            text='Cancel',
            command=self.cancel,
            width=12,
            bg_color=COLORS['secondary']
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_field(self, parent, field):
        """
        Create a form field
        
        Args:
            parent: Parent widget
            field: Field definition dict
        """
        field_name = field.get('name')
        field_label = field.get('label', field_name)
        field_type = field.get('type', 'text')
        required = field.get('required', False)
        
        # Label
        label_text = field_label + (' *' if required else '')
        label = tk.Label(
            parent,
            text=label_text,
            font=FONTS['body'],
            fg=COLORS['text_dark'],
            bg=COLORS['bg_light']
        )
        label.pack(anchor='w', pady=(10, 5))
        
        # Input widget
        if field_type == 'textarea':
            widget = tk.Text(
                parent,
                height=4,
                width=40,
                font=FONTS['body'],
                bg='#FFFFFF',
                relief=tk.FLAT,
                bd=1
            )
        elif field_type == 'password':
            container = tk.Frame(parent, bg=COLORS['bg_light'])
            container.pack(anchor='w', pady=(0, 5), fill=tk.X)
            widget = PasswordEntry(container)
            widget.pack(fill=tk.X)
        else:  # Default text
            widget = CustomEntry(
                parent,
                placeholder=field.get('placeholder', ''),
                width=40
            )
        
        if field_type != 'password':
            widget.pack(anchor='w', pady=(0, 5), fill=tk.X)
        
        self.entry_widgets[field_name] = widget
    
    def get_values(self):
        """Get form values"""
        values = {}
        for field in self.fields:
            field_name = field.get('name')
            widget = self.entry_widgets[field_name]
            
            if isinstance(widget, tk.Text):
                values[field_name] = widget.get('1.0', tk.END).strip()
            else:
                values[field_name] = widget.get_value()
        
        return values
    
    def _on_submit(self):
        """Handle submit button click"""
        # Validate required fields
        for field in self.fields:
            if field.get('required', False):
                field_name = field.get('name')
                value = self.entry_widgets[field_name].get_value()
                if not value or value.strip() == '':
                    messagebox.showerror(
                        'Validation Error',
                        f"{field.get('label', field_name)} is required"
                    )
                    return
        
        self.result = self.get_values()
        
        if self.on_submit:
            self.on_submit(self.result)
        
        self.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.destroy()


class StudentFormDialog(FormDialog):
    """Student form dialog"""
    
    def __init__(self, parent, on_submit=None, initial_data=None):
        """
        Initialize student form
        
        Args:
            parent: Parent window
            on_submit: Callback when form is submitted
            initial_data: Pre-fill form with data
        """
        fields = [
            {'name': 'first_name', 'label': 'First Name', 'required': True},
            {'name': 'last_name', 'label': 'Last Name', 'required': True},
            {'name': 'email', 'label': 'Email Address', 'required': True},
            {'name': 'phone', 'label': 'Phone Number', 'required': False},
            {'name': 'student_id', 'label': 'Student ID', 'required': True},
            {'name': 'program', 'label': 'Program/Course', 'required': False},
            {'name': 'enrollment_date', 'label': 'Enrollment Date (YYYY-MM-DD)', 'required': False},
            {'name': 'address', 'label': 'Address', 'type': 'textarea', 'required': False},
        ]
        
        title = 'Edit Student' if initial_data else 'Add New Student'
        super().__init__(parent, title=title, fields=fields, on_submit=on_submit)
        
        # Pre-fill if editing
        if initial_data:
            for key, value in initial_data.items():
                if key in self.entry_widgets:
                    widget = self.entry_widgets[key]
                    if isinstance(widget, tk.Text):
                        widget.insert('1.0', str(value))
                    else:
                        widget.insert(0, str(value))


class AttendanceFormDialog(FormDialog):
    """Attendance form dialog"""
    
    def __init__(self, parent, on_submit=None, initial_data=None):
        """
        Initialize attendance form
        
        Args:
            parent: Parent window
            on_submit: Callback when form is submitted
            initial_data: Pre-fill form with data
        """
        fields = [
            {'name': 'student', 'label': 'Student Name', 'required': True},
            {'name': 'course', 'label': 'Course', 'required': True},
            {'name': 'date', 'label': 'Date (YYYY-MM-DD)', 'required': True},
            {'name': 'status', 'label': 'Status (Present/Absent/Late)', 'required': True},
            {'name': 'remarks', 'label': 'Remarks', 'type': 'textarea', 'required': False},
        ]
        
        title = 'Edit Attendance' if initial_data else 'Mark Attendance'
        super().__init__(parent, title=title, fields=fields, on_submit=on_submit)
        
        if initial_data:
            for key, value in initial_data.items():
                if key in self.entry_widgets:
                    widget = self.entry_widgets[key]
                    if isinstance(widget, tk.Text):
                        widget.insert('1.0', str(value))
                    else:
                        widget.insert(0, str(value))


class CourseFormDialog(FormDialog):
    """Course form dialog"""
    
    def __init__(self, parent, on_submit=None, initial_data=None):
        """
        Initialize course form
        
        Args:
            parent: Parent window
            on_submit: Callback when form is submitted
            initial_data: Pre-fill form with data
        """
        fields = [
            {'name': 'course_code', 'label': 'Course Code', 'required': True},
            {'name': 'course_name', 'label': 'Course Name', 'required': True},
            {'name': 'department', 'label': 'Department', 'required': True},
            {'name': 'lecturer', 'label': 'Lecturer', 'required': False},
            {'name': 'credits', 'label': 'Credits', 'required': False},
            {'name': 'description', 'label': 'Description', 'type': 'textarea', 'required': False},
        ]
        
        title = 'Edit Course' if initial_data else 'Add New Course'
        super().__init__(parent, title=title, fields=fields, on_submit=on_submit)
        
        if initial_data:
            for key, value in initial_data.items():
                if key in self.entry_widgets:
                    widget = self.entry_widgets[key]
                    if isinstance(widget, tk.Text):
                        widget.insert('1.0', str(value))
                    else:
                        widget.insert(0, str(value))


class LecturerFormDialog(FormDialog):
    """Lecturer form dialog"""
    
    def __init__(self, parent, on_submit=None, initial_data=None):
        """
        Initialize lecturer form
        
        Args:
            parent: Parent window
            on_submit: Callback when form is submitted
            initial_data: Pre-fill form with data
        """
        fields = [
            {'name': 'first_name', 'label': 'First Name', 'required': True},
            {'name': 'last_name', 'label': 'Last Name', 'required': True},
            {'name': 'email', 'label': 'Email Address', 'required': True},
            {'name': 'phone', 'label': 'Phone Number', 'required': False},
            {'name': 'department', 'label': 'Department', 'required': True},
            {'name': 'specialization', 'label': 'Specialization/Subject', 'required': False},
            {'name': 'qualifications', 'label': 'Qualifications', 'type': 'textarea', 'required': False},
        ]
        
        title = 'Edit Lecturer' if initial_data else 'Add New Lecturer'
        super().__init__(parent, title=title, fields=fields, on_submit=on_submit)
        
        if initial_data:
            for key, value in initial_data.items():
                if key in self.entry_widgets:
                    widget = self.entry_widgets[key]
                    if isinstance(widget, tk.Text):
                        widget.insert('1.0', str(value))
                    else:
                        widget.insert(0, str(value))
