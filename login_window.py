import tkinter as tk
from tkinter import messagebox
import database as db
from theme import COLORS, apply_style
from widgets import Card, Button, LabeledEntry, Label
from admin_dashboard import AdminDashboard
from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System - Login")
        self.root.geometry("480x520")
        self.root.minsize(380, 460)
        self.root.resizable(True, True)
        apply_style(root)

        # Full-window background that resizes with the root window
        self.background = tk.Frame(root, bg=COLORS["bg"])
        self.background.pack(fill="both", expand=True)

        # Wrapper centers itself using relx/rely, so it stays centered on any
        # window size -> this is what makes the login screen responsive.
        wrapper = tk.Frame(self.background, bg=COLORS["bg"])
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        Label(wrapper, "School Management System", kind="title", bg=COLORS["bg"]).pack(pady=(0, 4))
        Label(wrapper, "Sign in to continue", kind="subtitle", fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(
            pady=(0, 20)
        )

        card = Card(wrapper, padding=28)
        card.pack()
        inner = card.inner

        _, self.username_entry = LabeledEntry(inner, "Username", width=28)
        self.username_entry.master.pack(fill="x", pady=6)

        _, self.password_entry = LabeledEntry(inner, "Password", width=28, show="*")
        self.password_entry.master.pack(fill="x", pady=6)
        self.password_entry.bind("<Return>", lambda e: self.login())

        Button(inner, "Login", command=self.login, kind="primary", width=220, height=44).pack(pady=(18, 4))

        demo_box = tk.Frame(inner, bg=COLORS["input_bg"])
        demo_box.pack(fill="x", pady=(16, 0))
        Label(demo_box, "Demo accounts", kind="small", fg=COLORS["text_muted"], bg=COLORS["input_bg"]).pack(
            anchor="w", padx=10, pady=(8, 2)
        )
        for line in [
            "Admin     ->  admin / admin123",
            "Teacher  ->  teacher1 / teacher123",
            "Student  ->  student1 / student123",
        ]:
            Label(demo_box, line, kind="small", fg=COLORS["text_muted"], bg=COLORS["input_bg"]).pack(
                anchor="w", padx=10
            )
        tk.Frame(demo_box, bg=COLORS["input_bg"], height=8).pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Enter both username and password.")
            return

        user = db.authenticate(username, password)
        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        role, ref_id = user["role"], user["ref_id"]
        self.root.destroy()
        new_root = tk.Tk()
        new_root.minsize(700, 500)

        if role == "admin":
            AdminDashboard(new_root)
        elif role == "teacher":
            TeacherDashboard(new_root, ref_id)
        elif role == "student":
            StudentDashboard(new_root, ref_id)

        new_root.mainloop()
