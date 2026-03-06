from pathlib import Path
import sys
import tkinter as tk


def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base_path / relative_path


def apply_window_icon(window):
    icon_path = resource_path("asset/book.png")
    if not icon_path.exists():
        return

    icon_image = tk.PhotoImage(file=str(icon_path))
    window.icon_image = icon_image
    window.iconphoto(True, icon_image)
