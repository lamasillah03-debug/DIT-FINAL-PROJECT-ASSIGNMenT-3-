"""
Reusable styled widgets built on top of theme.py.
Use these instead of raw tk.Button / tk.Entry / ttk.Treeview to keep
a consistent look across the whole app.
"""

import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS


def Button(parent, text, command=None, kind="primary", width=14):
    """A flat, hover-aware button. kind: primary | success | danger | muted"""
    palette = {
        "primary": (COLORS["primary"], COLORS["primary_hover"]),
        "success": (COLORS["success"], COLORS["success_hover"]),
        "danger": (COLORS["danger"], COLORS["danger_hover"]),
        "muted": (COLORS["muted"], COLORS["text_muted"]),
    }
    bg, hover_bg = palette.get(kind, palette["primary"])

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=COLORS["text"],
        activebackground=hover_bg,
        activeforeground=COLORS["text"],
        font=FONTS["button"],
        relief="flat",
        bd=0,
        width=width,
        cursor="hand2",
        padx=6,
        pady=8,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def Card(parent, padding=20):
    """A rounded-feel panel (flat frame with padding + border color) to group content."""
    outer = tk.Frame(parent, bg=COLORS["border"], padx=1, pady=1)
    inner = tk.Frame(outer, bg=COLORS["card"], padx=padding, pady=padding)
    inner.pack(fill="both", expand=True)
    outer.inner = inner
    return outer


def Entry(parent, width=22, show=None):
    """A flat, dark-themed entry field."""
    entry = tk.Entry(
        parent,
        width=width,
        show=show,
        bg=COLORS["input_bg"],
        fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat",
        font=FONTS["body"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["primary"],
    )
    return entry


def LabeledEntry(parent, label_text, width=22, show=None):
    """A vertical stack: muted label on top, styled entry below. Returns (frame, entry)."""
    frame = tk.Frame(parent, bg=parent["bg"] if "bg" in parent.keys() else COLORS["card"])
    tk.Label(
        frame, text=label_text, bg=frame["bg"], fg=COLORS["text_muted"], font=FONTS["small"]
    ).pack(anchor="w")
    entry = Entry(frame, width=width, show=show)
    entry.pack(fill="x", pady=(2, 0))
    frame.entry = entry
    return frame, entry


def Label(parent, text, kind="body", fg=None, bg=None):
    """kind: title | subtitle | heading | body | small"""
    return tk.Label(
        parent,
        text=text,
        font=FONTS.get(kind, FONTS["body"]),
        fg=fg or COLORS["text"],
        bg=bg or (parent["bg"] if "bg" in parent.keys() else COLORS["bg"]),
    )


def Treeview(parent, columns, headings=None, height=10):
    """A styled ttk.Treeview with a vertical scrollbar attached. Returns the Treeview widget."""
    container = tk.Frame(parent, bg=COLORS["bg"])
    container.pack(fill="both", expand=True)

    tree = ttk.Treeview(container, columns=columns, show="headings", height=height)
    headings = headings or {c: c.replace("_", " ").capitalize() for c in columns}
    for c in columns:
        tree.heading(c, text=headings.get(c, c.capitalize()))
        tree.column(c, width=120, anchor="w")

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tree.container = container
    return tree


def Sidebar(parent, width=180):
    """A fixed-width colored sidebar frame, useful for nav/role headers."""
    frame = tk.Frame(parent, bg=COLORS["sidebar"], width=width)
    frame.pack_propagate(False)
    return frame
