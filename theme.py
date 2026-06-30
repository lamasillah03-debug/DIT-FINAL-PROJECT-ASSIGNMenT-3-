"""
Central place for colors, fonts, and ttk styling.
Import COLORS / FONTS anywhere you build UI, and call apply_style(root)
once per Tk root window before building widgets on it.
"""

from tkinter import ttk

COLORS = {
    "bg": "#1e1e2f",          # main window background
    "sidebar": "#27293d",     # sidebar / header background
    "card": "#2b2d42",        # card / panel background
    "input_bg": "#34364f",    # entry / combobox background
    "border": "#3f4163",      # subtle borders

    "primary": "#6c5ce7",     # main accent (buttons, highlights)
    "primary_hover": "#8478ef",
    "success": "#00b894",
    "success_hover": "#1fd1a8",
    "danger": "#ff5e5e",
    "danger_hover": "#ff7d7d",
    "muted": "#6c6f93",       # secondary / clear buttons

    "text": "#f5f6fa",        # main text on dark backgrounds
    "text_muted": "#a0a3c4",  # secondary text
    "text_dark": "#1e1e2f",   # text on light/accent backgrounds
}

FONT_FAMILY = "Segoe UI"

FONTS = {
    "title": (FONT_FAMILY, 20, "bold"),
    "subtitle": (FONT_FAMILY, 11),
    "heading": (FONT_FAMILY, 13, "bold"),
    "body": (FONT_FAMILY, 10),
    "small": (FONT_FAMILY, 9),
    "button": (FONT_FAMILY, 10, "bold"),
}


def apply_style(root):
    """Configure ttk widgets (Treeview, Notebook, Combobox, Scrollbar) to match the theme."""
    root.configure(bg=COLORS["bg"])

    style = ttk.Style(root)
    style.theme_use("clam")

    # ---- Treeview ----
    style.configure(
        "Treeview",
        background=COLORS["card"],
        fieldbackground=COLORS["card"],
        foreground=COLORS["text"],
        rowheight=28,
        borderwidth=0,
        font=FONTS["body"],
    )
    style.map(
        "Treeview",
        background=[("selected", COLORS["primary"])],
        foreground=[("selected", COLORS["text"])],
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["sidebar"],
        foreground=COLORS["text"],
        font=FONTS["heading"],
        borderwidth=0,
        relief="flat",
    )
    style.map("Treeview.Heading", background=[("active", COLORS["sidebar"])])

    # ---- Notebook (tabs) ----
    style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COLORS["sidebar"],
        foreground=COLORS["text_muted"],
        padding=(16, 8),
        font=FONTS["body"],
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["primary"])],
        foreground=[("selected", COLORS["text"])],
    )

    # ---- Combobox ----
    style.configure(
        "TCombobox",
        fieldbackground=COLORS["input_bg"],
        background=COLORS["input_bg"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["text"],
        borderwidth=0,
    )

    # ---- Scrollbar ----
    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["sidebar"],
        troughcolor=COLORS["bg"],
        borderwidth=0,
        arrowsize=12,
    )

    return style
