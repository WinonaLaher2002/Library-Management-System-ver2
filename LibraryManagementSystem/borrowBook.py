import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from app_assets import apply_window_icon
from supabase_db import get_book_by_id, update_book


class UserBorrowBookWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Borrow Book")
        self.configure(bg="#E3FEF7")
        self.geometry("390x300")
        apply_window_icon(self)

        header_label = tk.Label(self, text="Borrow Book", font=("Arial", 18, "bold"), bg="#E3FEF7", fg="#003C43")
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        labels = ["Book ID", "Borrowed Date (MM/DD/YYYY)"]
        entries = []
        for i, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text + ":", bg="#E3FEF7", fg="#003C43")
            label.grid(row=i + 1, column=0, padx=10, pady=3, sticky="w")
            entry = tk.Entry(self)
            entry.grid(row=i + 1, column=1, padx=10, pady=3, sticky="ew")
            entries.append(entry)

        self.book_id_entry, self.borrowed_time_entry = entries

        buttons = [("Borrow Book", self.borrow_book), ("Back to User Panel", self.destroy)]
        for i, (button_text, command) in enumerate(buttons):
            button = tk.Button(self, text=button_text, command=command, fg="white", bg="#135D66")
            button.grid(row=i + len(labels) + 1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def borrow_book(self):
        book_id = self.book_id_entry.get()
        borrowed_time = self.borrowed_time_entry.get()

        if not (book_id and borrowed_time):
            messagebox.showerror("Error", "Please fill in all fields.", parent=self)
            return

        try:
            result = get_book_by_id(book_id)
            if not result:
                messagebox.showerror("Error", "Book ID not found.", parent=self)
                return

            quantity = result["quantity"]
            if quantity == 0:
                messagebox.showerror(
                    "Error",
                    "The book is already borrowed. Please return it before borrowing again.",
                    parent=self,
                )
                return

            borrowed_time_dt = datetime.strptime(borrowed_time, "%m/%d/%Y")
            update_book(book_id, {"quantity": quantity - 1, "borrowed_time": borrowed_time_dt.isoformat()})
            messagebox.showinfo("Success", "Book borrowed successfully!", parent=self)
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)


def create_borrow_book_window(master=None):
    return UserBorrowBookWindow(master=master)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    window = create_borrow_book_window(master=root)
    window.wait_window()
