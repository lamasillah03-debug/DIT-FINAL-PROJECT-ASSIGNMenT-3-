import tkinter as tk
import database as db
from theme import COLORS, apply_style
from widgets import Label, Treeview, Card


class StudentDashboard:
    def __init__(self, root, student_id):
        self.root = root
        self.student_id = student_id
        self.root.title("Student Dashboard")
        self.root.geometry("600x500")
        self.root.minsize(500, 420)
        self.root.resizable(True, True)
        apply_style(root)

        student = db.get_student(student_id)
        if student:
            name, age, grade_level, contact = (
                student["name"], student["age"], student["grade_level"], student["contact"]
            )
        else:
            name, age, grade_level, contact = "Unknown", "-", "-", "-"

        header = tk.Frame(root, bg=COLORS["sidebar"], pady=14)
        header.pack(fill="x")
        Label(header, f"Welcome, {name}", kind="title", bg=COLORS["sidebar"]).pack(anchor="w", padx=20)

        body = tk.Frame(root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=15, pady=15)

        info_card = Card(body, padding=16)
        info_card.pack(fill="x", pady=(0, 15))
        info = info_card.inner
        info.grid_columnconfigure((0, 1, 2), weight=1)
        Label(info, f"Age\n{age}", kind="body", bg=COLORS["card"]).grid(row=0, column=0, padx=10)
        Label(info, f"Grade Level\n{grade_level}", kind="body", bg=COLORS["card"]).grid(row=0, column=1, padx=10)
        Label(info, f"Contact\n{contact}", kind="body", bg=COLORS["card"]).grid(row=0, column=2, padx=10)

        Label(body, "My Grades", kind="heading", bg=COLORS["bg"]).pack(anchor="w", pady=(0, 8))
        cols = ("course_name", "score")
        headings = {"course_name": "Course", "score": "Score"}
        self.grade_tree = Treeview(body, cols, headings=headings, height=10)

        self.load_grades()

    def load_grades(self):
        for g in db.get_grades_by_student(self.student_id):
            self.grade_tree.insert("", "end", values=(g["course_name"], g["score"]))
