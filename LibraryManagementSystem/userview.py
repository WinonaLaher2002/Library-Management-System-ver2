import tkinter as tk
from tkinter import messagebox, ttk

from app_assets import apply_window_icon
from borrowBook import create_borrow_book_window as create_user_borrow_window
from returnBook import create_return_book_window as create_user_return_window
from supabase_db import add_book as add_book_record, delete_book as delete_book_record, get_books


class UserView(tk.Toplevel):
    def __init__(self, master=None, on_logout=None):
        super().__init__(master)
        self.on_logout = on_logout
        self.title("User Panel")
        self.configure(bg="#E3FEF7")
        self.geometry("1920x1080")
        apply_window_icon(self)
        self.protocol("WM_DELETE_WINDOW", self.logout)

        self._build_ui()

    def _build_ui(self):
        header_label = tk.Label(
            self,
            text="Library Management System",
            font=("Arial", 18, "bold"),
            bg="#E3FEF7",
            fg="#003C43",
        )
        header_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        labels = ["Book ID:", "Title:", "Author:", "ISBN:", "Quantity:"]
        self.entries = []
        for i, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text, bg="#E3FEF7", fg="#003C43")
            label.grid(row=i + 1, column=0, padx=10, pady=3, sticky="w")
            entry = tk.Entry(self)
            entry.grid(row=i + 1, column=1, padx=10, pady=3, sticky="ew")
            self.entries.append(entry)

        (
            self.book_id_entry,
            self.title_entry,
            self.author_entry,
            self.isbn_entry,
            self.quantity_entry,
        ) = self.entries

        buttons = [
            ("Add Book", self.add_book),
            ("Display Books", self.display_books),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("Logout", self.logout),
        ]

        for i, (button_text, command) in enumerate(buttons):
            button = tk.Button(self, text=button_text, command=command, fg="white", bg="#135D66")
            button.grid(row=i + 1, column=2, padx=10, pady=5, sticky="ew")

        search_label = tk.Label(self, text="Search:", bg="#E3FEF7", fg="#003C43")
        search_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        search_button = tk.Button(self, text="Search", command=self.search_books, fg="white", bg="#135D66")
        search_button.grid(row=8, column=2, padx=10, pady=5, sticky="ew")

        reset_button = tk.Button(self, text="Reset", command=self.reset_fields, fg="white", bg="#135D66")
        reset_button.grid(row=9, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        treeview_columns = ["Book ID", "Title", "Author", "ISBN", "Quantity", "Borrowed Time", "Return Time"]
        self.treeview = ttk.Treeview(self, columns=treeview_columns, show="headings", selectmode="browse")
        for col in treeview_columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        self.treeview.grid(row=10, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        for i in range(11):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

    def add_book(self):
        book_id = self.book_id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()

        if title and author and isbn and quantity:
            try:
                add_book_record(book_id, title, author, isbn, quantity)
                messagebox.showinfo("Success", "Book added successfully!", parent=self)
                self.display_books()
            except Exception as error:
                messagebox.showerror("Error", str(error), parent=self)
        else:
            messagebox.showerror("Error", "Please fill in all fields.", parent=self)

    def display_books(self):
        self.treeview.delete(*self.treeview.get_children())
        for book in get_books():
            borrowed_time = "Not Borrowed!" if not book["borrowed_time"] else book["borrowed_time"].strftime("%m/%d/%Y")
            return_time = book["return_time"].strftime("%m/%d/%Y") if book["return_time"] else "Not Returned!"
            self.treeview.insert(
                "",
                "end",
                values=(book["book_id"], book["title"], book["author"], book["isbn"], book["quantity"], borrowed_time, return_time),
            )

    def borrow_book(self):
        create_user_borrow_window(self)

    def return_book(self):
        create_user_return_window(self)

    def search_books(self):
        search_term = self.search_entry.get() or ""
        self.treeview.delete(*self.treeview.get_children())
        for book in get_books(search_term):
            borrowed_time = "Not Borrowed!" if not book["borrowed_time"] else book["borrowed_time"].strftime("%m/%d/%Y")
            return_time = book["return_time"].strftime("%m/%d/%Y") if book["return_time"] else "Not Returned!"
            self.treeview.insert(
                "",
                "end",
                values=(book["book_id"], book["title"], book["author"], book["isbn"], book["quantity"], borrowed_time, return_time),
            )

    def reset_fields(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def logout(self):
        self.destroy()
        if self.on_logout:
            self.on_logout()


def create_user_view(master=None, on_logout=None):
    return UserView(master=master, on_logout=on_logout)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    window = create_user_view(master=root, on_logout=root.destroy)
    window.wait_window()
