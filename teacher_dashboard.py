import tkinter as tk
from tkinter import messagebox
import database as db
from theme import COLORS, apply_style
from widgets import Button, Entry, Label, Treeview


class TeacherDashboard:
    def __init__(self, root, teacher_id):
        self.root = root
        self.teacher_id = teacher_id
        self.root.title("Teacher Dashboard")
        self.root.geometry("720x540")
        self.root.minsize(620, 460)
        self.root.resizable(True, True)
        apply_style(root)

        teacher = db.get_teacher(teacher_id)
        name = teacher["name"] if teacher else "Unknown"
        subject = teacher["subject"] if teacher else "Unknown"

        header = tk.Frame(root, bg=COLORS["sidebar"], pady=14)
        header.pack(fill="x")
        Label(header, f"Welcome, {name}", kind="title", bg=COLORS["sidebar"]).pack(anchor="w", padx=20)
        Label(header, f"Subject: {subject}", kind="subtitle", fg=COLORS["text_muted"], bg=COLORS["sidebar"]).pack(
            anchor="w", padx=20, pady=(0, 4)
        )

        body = tk.Frame(root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # ---- Grade entry form ----
        Label(body, "Record a Grade", kind="heading", bg=COLORS["bg"]).pack(anchor="w", pady=(0, 8))
        form = tk.Frame(body, bg=COLORS["bg"])
        form.pack(fill="x", pady=(0, 15))

        Label(form, "Student ID", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(row=0, column=0, padx=4, sticky="w")
        self.student_id_entry = Entry(form, width=8)
        self.student_id_entry.grid(row=1, column=0, padx=4)

        Label(form, "Course Name", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(row=0, column=1, padx=4, sticky="w")
        self.course_entry = Entry(form, width=16)
        self.course_entry.grid(row=1, column=1, padx=4)

        Label(form, "Score", kind="small", fg=COLORS["text_muted"], bg=COLORS["bg"]).grid(row=0, column=2, padx=4, sticky="w")
        self.score_entry = Entry(form, width=8)
        self.score_entry.grid(row=1, column=2, padx=4)

        Button(form, "Submit Grade", command=self.submit_grade, kind="success", width=140, height=38).grid(
            row=1, column=3, padx=12
        )

        # ---- Student list ----
        Label(body, "All Students", kind="heading", bg=COLORS["bg"]).pack(anchor="w", pady=(5, 8))
        cols = ("id", "name", "age", "grade_level", "contact")
        self.student_tree = Treeview(body, cols, height=10)

        self.load_students()

    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        for s in db.get_students():
            self.student_tree.insert(
                "", "end", values=(s["id"], s["name"], s["age"], s["grade_level"], s["contact"])
            )

    def submit_grade(self):
        student_id = self.student_id_entry.get().strip()
        course = self.course_entry.get().strip()
        score = self.score_entry.get().strip()

        if not student_id or not course or not score:
            messagebox.showwarning("Missing Info", "Fill in all fields.")
            return

        if not db.get_student(student_id):
            messagebox.showerror("Error", "No student with that ID.")
            return

        try:
            db.add_grade(student_id, course, score)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Score must be a number.")
            return

        messagebox.showinfo("Success", "Grade recorded.")
        self.student_id_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
