"""
Modern, rounded widgets built on tk.Canvas (real rounded corners, not flat
tk.Button/tk.Frame rectangles) so the app doesn't look like default tkinter.
"""

import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS


def _round_rect(canvas, x1, y1, x2, y2, radius=16, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def _parent_bg(parent):
    try:
        return parent["bg"]
    except Exception:
        return COLORS["bg"]


class RoundedButton(tk.Canvas):
    """A real rounded-corner button with hover/press states. kind: primary | success | danger | muted"""

    PALETTE = {
        "primary": (COLORS["primary"], COLORS["primary_hover"]),
        "success": (COLORS["success"], COLORS["success_hover"]),
        "danger": (COLORS["danger"], COLORS["danger_hover"]),
        "muted": (COLORS["muted"], COLORS["text_muted"]),
    }

    def __init__(self, parent, text, command=None, kind="primary", width=150, height=42, radius=14):
        bg = _parent_bg(parent)
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, bd=0)
        self.command = command
        self.text = text
        self.w, self.h, self.radius = width, height, radius
        self.base_color, self.hover_color = self.PALETTE.get(kind, self.PALETTE["primary"])
        self.disabled = False

        self._draw(self.base_color)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.configure(cursor="hand2")

    def _draw(self, color):
        self.delete("all")
        _round_rect(self, 1, 1, self.w - 1, self.h - 1, self.radius, fill=color, outline=color)
        self.create_text(
            self.w / 2, self.h / 2, text=self.text, fill=COLORS["text"], font=FONTS["button"]
        )

    def _on_enter(self, event):
        if not self.disabled:
            self._draw(self.hover_color)

    def _on_leave(self, event):
        if not self.disabled:
            self._draw(self.base_color)

    def _on_click(self, event):
        if not self.disabled and self.command:
            self.command()

    def set_disabled(self, disabled=True):
        self.disabled = disabled
        self._draw(COLORS["border"] if disabled else self.base_color)


def Button(parent, text, command=None, kind="primary", width=150, height=42):
    return RoundedButton(parent, text, command=command, kind=kind, width=width, height=height)


class Card(tk.Frame):
    """A rounded-corner panel that sizes itself to fit its content (self.inner)."""

    def __init__(self, parent, padding=20, radius=18, bg=None):
        self.parent_bg = bg or _parent_bg(parent)
        super().__init__(parent, bg=self.parent_bg)
        self.radius = radius
        self.canvas = tk.Canvas(self, bg=self.parent_bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        self.inner = tk.Frame(self.canvas, bg=COLORS["card"], padx=padding, pady=padding)
        self.win_id = self.canvas.create_window(0, 0, window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._redraw)

    def _redraw(self, event=None):
        self.inner.update_idletasks()
        w = max(self.inner.winfo_reqwidth(), 10)
        h = max(self.inner.winfo_reqheight(), 10)
        self.canvas.config(width=w, height=h)
        self.canvas.delete("bg")
        _round_rect(
            self.canvas, 1, 1, w - 1, h - 1, self.radius,
            fill=COLORS["card"], outline=COLORS["border"], tags=("bg",),
        )
        self.canvas.tag_lower("bg")
        self.canvas.coords(self.win_id, 0, 0)


def Entry(parent, width=22, show=None):
    """A flat, dark-themed entry field with a soft focus highlight."""
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
    """Vertical stack: muted label on top, styled entry below. Returns (frame, entry)."""
    frame = tk.Frame(parent, bg=_parent_bg(parent))
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
        bg=bg or _parent_bg(parent),
    )


def Badge(parent, text, kind="primary"):
    """Small rounded pill, e.g. for role tags."""
    colors = {
        "primary": COLORS["primary"],
        "success": COLORS["success"],
        "danger": COLORS["danger"],
        "muted": COLORS["muted"],
    }
    color = colors.get(kind, COLORS["primary"])
    canvas = tk.Canvas(parent, height=26, width=10 + len(text) * 8, bg=_parent_bg(parent), highlightthickness=0)
    canvas.update_idletasks()
    w = 20 + len(text) * 7
    canvas.config(width=w)
    _round_rect(canvas, 1, 1, w - 1, 25, 13, fill=color, outline=color)
    canvas.create_text(w / 2, 13, text=text, fill=COLORS["text"], font=FONTS["small"])
    return canvas


def Treeview(parent, columns, headings=None, height=10):
    """A styled ttk.Treeview with a vertical scrollbar, expands to fill its parent.
    Column headers are centered; row data is left-aligned."""
    container = tk.Frame(parent, bg=COLORS["bg"])
    container.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", anchor="center")

    tree = ttk.Treeview(container, columns=columns, show="headings", height=height, style="Custom.Treeview")
    headings = headings or {c: c.replace("_", " ").capitalize() for c in columns}
    for c in columns:
        tree.heading(c, text=headings.get(c, c.capitalize()), anchor="center")
        tree.column(c, width=120, anchor="w", stretch=True)

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tree.container = container
    return tree


def Sidebar(parent, width=200):
    """A fixed-width colored sidebar frame, useful for nav/role headers."""
    frame = tk.Frame(parent, bg=COLORS["sidebar"], width=width)
    frame.pack_propagate(False)
    return frame