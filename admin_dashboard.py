import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from theme import COLORS, FONTS, apply_style
from widgets import Button, Entry, Label, Treeview


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("820x560")
        self.root.minsize(700, 480)
        self.root.resizable(True, True)
        apply_style(root)

        header = tk.Frame(root, bg=COLORS["sidebar"], pady=14)
        header.pack(fill="x")
        Label(header, "Admin Dashboard", kind="title", bg=COLORS["sidebar"]).pack(side="left", padx=20)

        body = tk.Frame(root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=15, pady=15)

        notebook = ttk.Notebook(body)
        notebook.pack(fill="both", expand=True)

        self.students_tab = tk.Frame(notebook, bg=COLORS["bg"])
        self.teachers_tab = tk.Frame(notebook, bg=COLORS["bg"])
        self.users_tab = tk.Frame(notebook, bg=COLORS["bg"])

        notebook.add(self.students_tab, text="Students")
        notebook.add(self.teachers_tab, text="Teachers")
        notebook.add(self.users_tab, text="User Accounts")

        self.build_students_tab()
        self.build_teachers_tab()
        self.build_users_tab()

    # ---------------- STUDENTS ----------------
    def build_students_tab(self):
        frame = self.students_tab
        form = tk.Frame(frame, bg=COLORS["bg"], pady=12)
        form.pack(fill="x")

        labels = ["Name", "Age", "Grade Level", "Contact"]
        self.student_entries = {}
        for i, label in enumerate(labels):
            Label(form, label, kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(
                row=0, column=i, padx=8, sticky="w"
            )
            entry = Entry(form, width=14)
            entry.grid(row=1, column=i, padx=8)
            self.student_entries[label] = entry

        btns = tk.Frame(frame, bg=COLORS["bg"])
        btns.pack(pady=8)
        Button(btns, "Add", command=self.add_student, kind="success", width=110, height=38).grid(row=0, column=0, padx=4)
        Button(btns, "Update", command=self.update_student, kind="primary", width=110, height=38).grid(row=0, column=1, padx=4)
        Button(btns, "Delete", command=self.delete_student, kind="danger", width=110, height=38).grid(row=0, column=2, padx=4)
        Button(btns, "Clear", command=self.clear_student_form, kind="muted", width=110, height=38).grid(row=0, column=3, padx=4)

        cols = ("id", "name", "age", "grade_level", "contact")
        self.student_tree = Treeview(frame, cols, height=11)
        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)

        self.selected_student_id = None
        self.load_students()

    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for s in db.get_students():
            self.student_tree.insert(
                "", "end", values=(s["id"], s["name"], s["age"], s["grade_level"], s["contact"])
            )

    def add_student(self):
        vals = [e.get().strip() for e in self.student_entries.values()]
        if not vals[0]:
            messagebox.showwarning("Missing Info", "Name is required.")
            return
        db.add_student(*vals)
        self.load_students()
        self.clear_student_form()

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("No Selection", "Select a student first.")
            return
        vals = [e.get().strip() for e in self.student_entries.values()]
        db.update_student(self.selected_student_id, *vals)
        self.load_students()
        self.clear_student_form()

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("No Selection", "Select a student first.")
            return
        db.delete_student(self.selected_student_id)
        self.load_students()
        self.clear_student_form()

    def on_student_select(self, event):
        selected = self.student_tree.focus()
        if not selected:
            return
        values = self.student_tree.item(selected, "values")
        self.selected_student_id = values[0]
        keys = list(self.student_entries.keys())
        for i, key in enumerate(keys):
            self.student_entries[key].delete(0, tk.END)
            self.student_entries[key].insert(0, values[i + 1])

    def clear_student_form(self):
        for e in self.student_entries.values():
            e.delete(0, tk.END)
        self.selected_student_id = None

    # ---------------- TEACHERS ----------------
    def build_teachers_tab(self):
        frame = self.teachers_tab
        form = tk.Frame(frame, bg=COLORS["bg"], pady=12)
        form.pack(fill="x")

        labels = ["Name", "Subject", "Contact"]
        self.teacher_entries = {}
        for i, label in enumerate(labels):
            Label(form, label, kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(
                row=0, column=i, padx=8, sticky="w"
            )
            entry = Entry(form, width=16)
            entry.grid(row=1, column=i, padx=8)
            self.teacher_entries[label] = entry

        btns = tk.Frame(frame, bg=COLORS["bg"])
        btns.pack(pady=8)
        Button(btns, "Add", command=self.add_teacher, kind="success", width=110, height=38).grid(row=0, column=0, padx=4)
        Button(btns, "Update", command=self.update_teacher, kind="primary", width=110, height=38).grid(row=0, column=1, padx=4)
        Button(btns, "Delete", command=self.delete_teacher, kind="danger", width=110, height=38).grid(row=0, column=2, padx=4)
        Button(btns, "Clear", command=self.clear_teacher_form, kind="muted", width=110, height=38).grid(row=0, column=3, padx=4)

        cols = ("id", "name", "subject", "contact")
        self.teacher_tree = Treeview(frame, cols, height=11)
        self.teacher_tree.bind("<<TreeviewSelect>>", self.on_teacher_select)

        self.selected_teacher_id = None
        self.load_teachers()

    def load_teachers(self):
        for row in self.teacher_tree.get_children():
            self.teacher_tree.delete(row)
        for t in db.get_teachers():
            self.teacher_tree.insert("", "end", values=(t["id"], t["name"], t["subject"], t["contact"]))

    def add_teacher(self):
        vals = [e.get().strip() for e in self.teacher_entries.values()]
        if not vals[0]:
            messagebox.showwarning("Missing Info", "Name is required.")
            return
        db.add_teacher(*vals)
        self.load_teachers()
        self.clear_teacher_form()

    def update_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("No Selection", "Select a teacher first.")
            return
        vals = [e.get().strip() for e in self.teacher_entries.values()]
        db.update_teacher(self.selected_teacher_id, *vals)
        self.load_teachers()
        self.clear_teacher_form()

    def delete_teacher(self):
        if not self.selected_teacher_id:
            messagebox.showwarning("No Selection", "Select a teacher first.")
            return
        db.delete_teacher(self.selected_teacher_id)
        self.load_teachers()
        self.clear_teacher_form()

    def on_teacher_select(self, event):
        selected = self.teacher_tree.focus()
        if not selected:
            return
        values = self.teacher_tree.item(selected, "values")
        self.selected_teacher_id = values[0]
        keys = list(self.teacher_entries.keys())
        for i, key in enumerate(keys):
            self.teacher_entries[key].delete(0, tk.END)
            self.teacher_entries[key].insert(0, values[i + 1])

    def clear_teacher_form(self):
        for e in self.teacher_entries.values():
            e.delete(0, tk.END)
        self.selected_teacher_id = None

    # ---------------- USER ACCOUNTS ----------------
    def build_users_tab(self):
        frame = self.users_tab
        form = tk.Frame(frame, bg=COLORS["bg"], pady=16)
        form.pack()

        Label(form, "Username", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(
            row=0, column=0, padx=8, pady=4, sticky="e"
        )
        self.user_username = Entry(form, width=22)
        self.user_username.grid(row=0, column=1, padx=8, pady=4)

        Label(form, "Password", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(
            row=1, column=0, padx=8, pady=4, sticky="e"
        )
        self.user_password = Entry(form, width=22)
        self.user_password.grid(row=1, column=1, padx=8, pady=4)

        Label(form, "Role", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(
            row=2, column=0, padx=8, pady=4, sticky="e"
        )
        self.user_role = ttk.Combobox(form, values=["admin", "teacher", "student"], state="readonly", width=19)
        self.user_role.grid(row=2, column=1, padx=8, pady=4)

        Label(
            form, "Linked record ID (teacher/student id)", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]
        ).grid(row=3, column=0, padx=8, pady=4, sticky="e")
        self.user_ref_id = Entry(form, width=22)
        self.user_ref_id.grid(row=3, column=1, padx=8, pady=4)

        Button(form, "Create Account", command=self.create_user, kind="success", width=200, height=42).grid(
            row=4, column=0, columnspan=2, pady=14
        )

        cols = ("id", "username", "role", "ref_id")
        self.user_tree = Treeview(frame, cols, height=8)
        self.load_users()

    def load_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for u in db.get_users():
            self.user_tree.insert("", "end", values=(u["id"], u["username"], u["role"], u["ref_id"]))

    def create_user(self):
        username = self.user_username.get().strip()
        password = self.user_password.get().strip()
        role = self.user_role.get().strip()
        ref_id = self.user_ref_id.get().strip() or None

        if not username or not password or not role:
            messagebox.showwarning("Missing Info", "Username, password, and role are required.")
            return

        try:
            db.add_user(username, password, role, ref_id)
            messagebox.showinfo("Success", "Account created.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.load_users()
        self.user_username.delete(0, tk.END)
        self.user_password.delete(0, tk.END)
        self.user_role.set("")
        self.user_ref_id.delete(0, tk.END)
