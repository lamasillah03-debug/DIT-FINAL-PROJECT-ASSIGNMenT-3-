# School Management System

A desktop School Management System built with **Python**, **Tkinter**, and a lightweight **JSON file** as the data store (no SQL/database server required). It supports three roles — **Admin**, **Teacher**, and **Student** — each with its own dashboard, and uses a custom dark theme with rounded cards and buttons instead of default Tkinter widgets.

## Features

- **Role-based login** (Admin / Teacher / Student) with a single shared login screen
- **Admin dashboard** — full CRUD for students and teachers, plus account creation for any role
- **Teacher dashboard** — view all students and record grades
- **Student dashboard** — view personal profile and grades (read-only)
- **Modern UI** — dark theme, rounded cards/buttons with hover states, responsive/resizable windows
- **JSON storage** — all data lives in a single human-readable `school.json` file
- **Mock data** — sample students, teachers, courses, and grades seeded automatically on first run

## Project Structure

```
school_project/
├── main.py               # Entry point - initializes data and launches the login screen
├── database.py            # JSON data layer (CRUD functions, no SQL)
├── mock_data.py            # Seeds sample data for demo purposes
├── theme.py                # Color palette, fonts, ttk style configuration
├── widgets.py               # Reusable styled widgets (rounded buttons, cards, inputs, tables)
├── login_window.py           # Login screen, routes users to the correct dashboard
├── admin_dashboard.py         # Admin panel (students, teachers, user accounts)
├── teacher_dashboard.py        # Teacher panel (student list, grade entry)
├── student_dashboard.py         # Student panel (profile, grades)
├── school.json                   # Auto-generated data file (created on first run)
├── LICENSE
└── README.md
```

## Requirements

- Python 3.8+
- Tkinter (included with most standard Python installations)

No external/pip packages are required — everything uses the Python standard library.

## Running the App

```bash
python main.py
```

On first launch, `school.json` is created automatically and pre-filled with sample students, teachers, courses, and grades.

## Demo Accounts

| Role    | Username  | Password     |
|---------|-----------|--------------|
| Admin   | admin     | admin123     |
| Teacher | teacher1  | teacher123   |
| Student | student1  | student123   |

## How Roles Work

- **Admin** creates students/teachers and issues login accounts. When creating a teacher or student account, the linked record ID (shown in the corresponding table) ties the login to that person's data.
- **Teacher** can view all students and submit grades for any student by ID.
- **Student** sees only their own profile and grades.

## Data Storage

Instead of SQL, all data is stored as plain JSON in `school.json`:

```json
{
  "users": [...],
  "students": [...],
  "teachers": [...],
  "courses": [...],
  "grades": [...]
}
```

`database.py` reads and rewrites this file for every operation — simple, transparent, and easy to inspect or back up by hand.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
