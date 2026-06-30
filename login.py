import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import COLORS, FONTS, apply_style
from widgets import Card, Button, LabeledEntry, Label
from admin_dashboard import AdminDashboard
from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System - Login")
        self.root.geometry("420x420")
        self.root.resizable(False, False)
        apply_style(root)

        # Center the login card on the window
        wrapper = tk.Frame(root, bg=COLORS["bg"])
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        Label(wrapper, "School Management System", kind="title", bg=COLORS["bg"]).pack(pady=(0, 4))
        Label(wrapper, "Sign in to continue", kind="subtitle", fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(
            pady=(0, 20)
        )

        card = Card(wrapper, padding=24)
        card.pack()
        inner = card.inner

        _, self.username_entry = LabeledEntry(inner, "Username", width=26)
        self.username_entry.master.pack(fill="x", pady=6)

        _, self.password_entry = LabeledEntry(inner, "Password", width=26, show="*")
        self.password_entry.master.pack(fill="x", pady=6)
        self.password_entry.bind("<Return>", lambda e: self.login())

        Button(inner, "Login", command=self.login, kind="primary", width=20).pack(pady=(16, 0))

        Label(
            wrapper,
            "Default admin -> admin / admin123",
            kind="small",
            fg=COLORS["text_muted"],
            bg=COLORS["bg"],
        ).pack(pady=(16, 0))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Enter both username and password.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, role, ref_id FROM users WHERE username=? AND password=?",
            (username, password),
        )
        result = cur.fetchone()
        conn.close()

        if not result:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        user_id, role, ref_id = result
        self.root.destroy()
        new_root = tk.Tk()

        if role == "admin":
            AdminDashboard(new_root)
        elif role == "teacher":
            TeacherDashboard(new_root, ref_id)
        elif role == "student":
            StudentDashboard(new_root, ref_id)

        new_root.mainloop()
