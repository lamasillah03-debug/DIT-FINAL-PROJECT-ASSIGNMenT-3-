import tkinter as tk
from database import init_db
from mock_data import seed_mock_data
from login_window import LoginWindow

if __name__ == "__main__":
    init_db()
    seed_mock_data()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
