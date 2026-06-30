"""
JSON-based data layer for the School Management System.
All records live in a single school.json file on disk (no SQL involved).
Every public function here reads the whole file, mutates it, then writes
it back -- simple and fine for a small single-user desktop app.
"""

import json
import os

DB_FILE = "school.json"

DEFAULT_DATA = {
    "users": [],     # {id, username, password, role, ref_id}
    "students": [],  # {id, name, age, grade_level, contact}
    "teachers": [],  # {id, name, subject, contact}
    "courses": [],   # {id, name, teacher_id}
    "grades": [],    # {id, student_id, course_name, score}
}


# ---------------- core read/write ----------------
def _load():
    if not os.path.exists(DB_FILE):
        return json.loads(json.dumps(DEFAULT_DATA))
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key in DEFAULT_DATA:
        data.setdefault(key, [])
    return data


def _save(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _next_id(records):
    return max((r["id"] for r in records), default=0) + 1


def init_db():
    """Create school.json (if missing) and make sure a default admin exists."""
    data = _load()
    if not any(u["role"] == "admin" for u in data["users"]):
        data["users"].append(
            {
                "id": _next_id(data["users"]),
                "username": "admin",
                "password": "admin123",
                "role": "admin",
                "ref_id": None,
            }
        )
    _save(data)


# ---------------- Users ----------------
def authenticate(username, password):
    """Return the matching user dict, or None."""
    for u in _load()["users"]:
        if u["username"] == username and u["password"] == password:
            return u
    return None


def get_users():
    return _load()["users"]


def add_user(username, password, role, ref_id=None):
    data = _load()
    if any(u["username"] == username for u in data["users"]):
        raise ValueError("That username is already taken.")
    user = {
        "id": _next_id(data["users"]),
        "username": username,
        "password": password,
        "role": role,
        "ref_id": int(ref_id) if ref_id not in (None, "") else None,
    }
    data["users"].append(user)
    _save(data)
    return user


# ---------------- Students ----------------
def get_students():
    return _load()["students"]


def get_student(student_id):
    student_id = int(student_id)
    for s in _load()["students"]:
        if s["id"] == student_id:
            return s
    return None


def add_student(name, age, grade_level, contact):
    data = _load()
    student = {
        "id": _next_id(data["students"]),
        "name": name,
        "age": age,
        "grade_level": grade_level,
        "contact": contact,
    }
    data["students"].append(student)
    _save(data)
    return student


def update_student(student_id, name, age, grade_level, contact):
    data = _load()
    student_id = int(student_id)
    for s in data["students"]:
        if s["id"] == student_id:
            s.update({"name": name, "age": age, "grade_level": grade_level, "contact": contact})
            break
    _save(data)


def delete_student(student_id):
    data = _load()
    student_id = int(student_id)
    data["students"] = [s for s in data["students"] if s["id"] != student_id]
    _save(data)


# ---------------- Teachers ----------------
def get_teachers():
    return _load()["teachers"]


def get_teacher(teacher_id):
    teacher_id = int(teacher_id)
    for t in _load()["teachers"]:
        if t["id"] == teacher_id:
            return t
    return None


def add_teacher(name, subject, contact):
    data = _load()
    teacher = {"id": _next_id(data["teachers"]), "name": name, "subject": subject, "contact": contact}
    data["teachers"].append(teacher)
    _save(data)
    return teacher


def update_teacher(teacher_id, name, subject, contact):
    data = _load()
    teacher_id = int(teacher_id)
    for t in data["teachers"]:
        if t["id"] == teacher_id:
            t.update({"name": name, "subject": subject, "contact": contact})
            break
    _save(data)


def delete_teacher(teacher_id):
    data = _load()
    teacher_id = int(teacher_id)
    data["teachers"] = [t for t in data["teachers"] if t["id"] != teacher_id]
    _save(data)


# ---------------- Courses ----------------
def get_courses():
    return _load()["courses"]


def add_course(name, teacher_id=None):
    data = _load()
    course = {
        "id": _next_id(data["courses"]),
        "name": name,
        "teacher_id": int(teacher_id) if teacher_id not in (None, "") else None,
    }
    data["courses"].append(course)
    _save(data)
    return course


# ---------------- Grades ----------------
def get_grades_by_student(student_id):
    student_id = int(student_id)
    return [g for g in _load()["grades"] if g["student_id"] == student_id]


def add_grade(student_id, course_name, score):
    data = _load()
    grade = {
        "id": _next_id(data["grades"]),
        "student_id": int(student_id),
        "course_name": course_name,
        "score": float(score),
    }
    data["grades"].append(grade)
    _save(data)
    return grade
