"""
Seeds school.json with sample data so the app is ready to demo immediately.
Only inserts data if the relevant lists are empty (safe to call every run).
"""

import database as db


def seed_mock_data():
    # ---- Teachers ----
    if not db.get_teachers():
        for name, subject, contact in [
            ("Mr. Suliman Kalakoh", "Data Communication", "suliman.k@school.edu"),
            ("Mrs. Aminata Conteh", "Mathematics", "aminata.c@school.edu"),
            ("Mr. James Bangura", "English Language", "james.b@school.edu"),
        ]:
            db.add_teacher(name, subject, contact)

    # ---- Students ----
    if not db.get_students():
        for name, age, grade_level, contact in [
            ("Fatmata Sesay", 19, "DIT1202F", "fatmata.s@school.edu"),
            ("Mohamed Kargbo", 20, "DIT1202F", "mohamed.k@school.edu"),
            ("Isata Turay", 18, "DIT1102A", "isata.t@school.edu"),
            ("Abdul Koroma", 21, "DIT1202F", "abdul.k@school.edu"),
            ("Mariama Bah", 19, "DIT1102A", "mariama.b@school.edu"),
        ]:
            db.add_student(name, age, grade_level, contact)

    # ---- Courses ----
    if not db.get_courses():
        teachers = db.get_teachers()
        teacher_ids = [t["id"] for t in teachers]
        if teacher_ids:
            course_defs = [
                ("COMP105 - Data Communication", teacher_ids[0]),
                ("MATH101 - Algebra", teacher_ids[1] if len(teacher_ids) > 1 else teacher_ids[0]),
                ("ENG102 - Composition", teacher_ids[2] if len(teacher_ids) > 2 else teacher_ids[0]),
            ]
            for name, teacher_id in course_defs:
                db.add_course(name, teacher_id)

    # ---- Grades ----
    students = db.get_students()
    if students and not any(db.get_grades_by_student(s["id"]) for s in students):
        sample_courses = ["COMP105 - Data Communication", "MATH101 - Algebra", "ENG102 - Composition"]
        sample_scores = [88, 76, 92, 65, 81, 74, 90, 83, 69, 95]
        i = 0
        for s in students:
            for course in sample_courses[:2]:
                db.add_grade(s["id"], course, sample_scores[i % len(sample_scores)])
                i += 1

    # ---- Demo login accounts (teacher1 / student1) ----
    users = db.get_users()
    usernames = {u["username"] for u in users}

    teachers = db.get_teachers()
    if "teacher1" not in usernames and teachers:
        db.add_user("teacher1", "teacher123", "teacher", teachers[0]["id"])

    students = db.get_students()
    if "student1" not in usernames and students:
        db.add_user("student1", "student123", "student", students[0]["id"])
